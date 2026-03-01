 # -*- coding: utf-8 -*-
import copy
import itertools
import TreeGraph
import Pieces
import Sides
import time

# Core engine class managing board state, move generation, and evaluation
class ChessEngine:
    def __init__(self, depth, side, position ='RNBQKBNRPPPPPPPP################################pppppppprnbqkbnr'):
        # set initial position string and prepare board array
        self.position = position
        self.board = [[Pieces.empty() for _ in range(8)]for _ in range(8)] #Create board to be used 
        self.side = side
        #initialize sides
        self.white = Sides.WhiteSide()
        self.black = Sides.BlackSide()
        self.white.enemy = self.black
        self.black.enemy = self.white
        for count, (y, x) in enumerate(itertools.product(range(8), range(8))):
            colour = self.black if position[count].isupper() else self.white
            match position[count].lower():
                case 'p': self.board[y][x] = Pieces.pawn(colour)
                case 'r': self.board[y][x] = Pieces.rook(colour, False)
                case 'n': self.board[y][x] = Pieces.knight(colour)
                case 'b': self.board[y][x] = Pieces.bishop(colour)
                case 'q': self.board[y][x] = Pieces.queen(colour)
                case 'k': self.board[y][x] = Pieces.king(colour, False)
        #Initialize depth engine
        self.Depth = Depth_engine(depth, self.board, side)
    def str_to_board(self, position):
        # convert position string into 2D board array of piece objects
        board = [[Pieces.empty() for _ in range(8)]for _ in range(8)] #Create board to be used 
        for count, (y, x) in enumerate(itertools.product(range(8), range(8))):
            colour = self.black if position[count].isupper() else self.white
            match position[count].lower():
                case 'p': board[y][x] = Pieces.pawn(colour)
                case 'r': board[y][x] = Pieces.rook(colour, False)
                case 'n': board[y][x] = Pieces.knight(colour)
                case 'b': board[y][x] = Pieces.bishop(colour)
                case 'q': board[y][x] = Pieces.queen(colour)
                case 'k': board[y][x] = Pieces.king(colour, False)
        return board
    def run(self):
        # trigger depth search and return best move chain
        #Starts searching at depth
        return self.Depth.start()
    def evaluate(self, pos =None):
        # examine current board (or given pos) and compute evaluation metrics
        self.board = pos if pos != None else self.board
        self.white.reset()
        self.black.reset()
        self.get_move_val()
        self.get_piece_worth()
        self.get_check()
        self.white.set_eval()
        self.black.set_eval()
        # Returns the evaluation for the side to move, and whether either king is in check, which is used for move pruning in the search.
        if self.side == self.white:
            ally_eval, enemy_eval = self.white.Eval, self.black.Eval
        else: 
            ally_eval, enemy_eval = self.black.Eval, self.white.Eval
        return ally_eval, enemy_eval, self.white.check, self.black.check
    def REevaluate(self, lines):
        # re-evaluate a list of historical positions looking for the most unstable one
        ready = False
        prev_eval = 0
        prev_pos = ""
        max_diff = 0
        NO_LIST = []
        pos_to_evaluate = ""
        while not ready: 
            for pos in lines:
                # Assures that only relevant positions are evaluated.
                if self.side == self.white and lines.index(pos) %2 !=0:
                    continue
                if self.side == self.black and lines.index(pos) %2 ==0:
                    continue
                if len(pos) <2 or pos[0] in NO_LIST:
                    continue
                curr_eval = float(pos[1].replace("\n",""))

            # Find the position with the biggest negative change in evaluation for the side to move, as this is likely where the engine went wrong and would benefit most from learning.
                if curr_eval-prev_eval > max_diff:
                    max_diff = prev_eval - curr_eval
                    pos_to_evaluate = prev_pos
                    prev_pos = pos[0]
            self.Depth.depth = self.Depth.critical_depth
            self.Update_pos(self.str_to_board(pos_to_evaluate))
            new_pos = self.run()
            new_eval = self.evaluate(new_pos)[0]
            if new_eval >= prev_eval :
                # If the re-evaluation has a better or equal evaluation than the original evaluation, we can assume that the engine has learned from this position and will not make the same mistake again, so we can stop the learning process.
                ready = True
                break
            else:
                NO_LIST.append(prev_pos)
        with open("App_data/Data.txt",'a') as file:
            # Log the new evaluation for this position, so that it can be used for future learning or move selection.
            file.write(f"{pos_to_evaluate}:{self.get_str_pos(new_pos)}\n")
            file.close()
    def get_piece_worth(self): # Collects the cumulative worth of all pieces from each side
        # iterate over board and tally material values
        for y, x in itertools.product(range(8), range(8)):
            CurPiece = self.board[y][x]
            if isinstance(CurPiece, Pieces.piece):
                if CurPiece.colour == self.white:self.white.pieceVal+=CurPiece.val
                else:self.black.pieceVal+=CurPiece.val
    def get_check(self):
        # determine if either king is currently under attack by scanning move lists
        if self.black.kingPos in self.white.PosMoves:
            self.black.check = True
        if self.white.kingPos in self.black.PosMoves:
            self.white.check = True
    def get_move_val(self):
        # compute move/attack/defense values for every piece and build move lists
        for y, x in itertools.product(range(8), range(8)):
            Curpiece = self.board[y][x]
            if isinstance(Curpiece, Pieces.piece):
                Curpiece.reset()
                ValArray = Curpiece.check(x,y,self.board) # returns Attack, Pos, Defense, PosMoves in that order
                colour = Curpiece.colour
                colour.AttackVal += ValArray[0]
                colour.PosVal += ValArray[1]
                colour.DefenseVal += ValArray[2]
                colour.PosMoves += ValArray[3]  
                #Save king position for each side, makes it easier to see if either side is in check
                if isinstance(Curpiece, Pieces.king):
                    Curpiece.colour.kingPos = [y,x]
                    Curpiece.colour.king  = Curpiece
                    Curpiece.colour.CastlePositions = ValArray[4]
                        
    def copy_board(self, board = None):
        # produce a shallow copy of the board 2D list
        if board is None: board = self.board
        return [row[:] for row in board]
    def get_str_pos(self ,board = None):
        #Turns the 2d array structue back into the string format
        # useful for logging or storage
        if board is None: board = self.board
        position = ""
        for y, x in itertools.product(range(8), range(8)):
            Curpiece = board[y][x]
            if Curpiece.colour is self.white:
                if isinstance(Curpiece, Pieces.pawn): position +="p"
                elif isinstance(Curpiece,Pieces.rook): position+="r"
                elif isinstance(Curpiece,Pieces.knight): position+="n"
                elif isinstance(Curpiece,Pieces.bishop): position+="b"
                elif isinstance(Curpiece,Pieces.queen): position+="q"
                elif isinstance(Curpiece,Pieces.king): position+="k"
            elif isinstance(Curpiece, Pieces.pawn): position +="P"
            elif isinstance(Curpiece,Pieces.rook): position+="R"
            elif isinstance(Curpiece,Pieces.knight): position+="N"
            elif isinstance(Curpiece,Pieces.bishop): position+="B"
            elif isinstance(Curpiece,Pieces.queen): position+="Q"
            elif isinstance(Curpiece,Pieces.king): position+="K"
            else: position+="#"
        return position
    def Update_pos(self,pos):
        #Used to change the engine's current positions
        # also update search tree root
        self.board = pos
        self.Depth.tree.root = TreeGraph.TreeNode(pos)
    
    def cleanPos(self):
        #Removes illegal moves
        # filter out moves that would leave the moving side in check
        board = self.board
        self.evaluate(board) #Used to get the possible moves of current 
        posMate = True
        col = self.side
        for y, x in itertools.product(range(8), range(8)):
            CurPiece = board[y][x]
            if isinstance(CurPiece, Pieces.empty) or CurPiece.colour != col:
                continue
            newMoves = []
            for move in CurPiece.posMove:
                newBoard = self.copy_board() # Creates a copy of the board to modify without modifying original board
                newBoard[y][x] = Pieces.empty()
                if len(move) > 2: # [What rook to move, Where to move the king, Where to move the rook]
                    newBoard[move[2][0]][move[2][1]] = Pieces.rook(CurPiece.colour, True)
                    newBoard[move[1][0]][move[1][1]] = Pieces.king(CurPiece.colour, True)
                    newBoard[move[0][0]][move[0][1]] = Pieces.empty()
                else:
                    newY, newX = move
                    # Generates a new board with a move applied to it, so that we can evaluate whether this move would leave the king in check or not
                    if isinstance(CurPiece, Pieces.pawn):
                        newBoard[newY][newX] = Pieces.pawn(CurPiece.colour, CurPiece.hasMoved, CurPiece.val)
                    elif isinstance(CurPiece, Pieces.rook):
                        newBoard[newY][newX] = Pieces.rook(CurPiece.colour, CurPiece.hasMoved, CurPiece.val)
                    elif isinstance(CurPiece, Pieces.knight):
                        newBoard[newY][newX] = Pieces.knight(CurPiece.colour, CurPiece.hasMoved, CurPiece.val)
                    elif isinstance(CurPiece, Pieces.bishop):
                        newBoard[newY][newX] = Pieces.bishop(CurPiece.colour, CurPiece.hasMoved, CurPiece.val)
                    elif isinstance(CurPiece, Pieces.queen):
                        newBoard[newY][newX] = Pieces.queen(CurPiece.colour, CurPiece.hasMoved, CurPiece.val)
                    elif isinstance(CurPiece, Pieces.king):
                        newBoard[newY][newX] = Pieces.king(CurPiece.colour, CurPiece.hasMoved, CurPiece.val)
               
                a, b, white_check, black_check = self.evaluate(newBoard)
                if (col == self.white and not white_check) or (col == self.black and not black_check):
                    posMate = False
                    newMoves.append(move)
            CurPiece.posMove = newMoves

        if posMate:
            return True
# Search helper subclass extending ChessEngine with full depth exploration
class Depth_engine(ChessEngine):
    def __init__(self, depth, board, side):
        self.depth = depth
        self.critical_depth = depth + 1
        self.side = side
        self.white = Sides.WhiteSide()
        self.black = Sides.BlackSide()
        self.white.enemy = self.black
        self.black.enemy = self.white
        self.board = board
        self.turn = side
        self.board_count = 0
        self.boards_analysed = 0
        self.tree = TreeGraph.Tree(TreeGraph.TreeNode(self.board))
    def copy_board(self, board):
        self.board = board
        return super().copy_board()
    def start(self):
        # trigger depth search and return best move chain
        self.DepthMap(self.tree.root.content, self.tree.root)
        self.find(self.tree.root, float('-inf'), float('inf'))
        try:
            return self.tree.root.next.content
        except Exception:
            return None
    def DepthMap(self,board,parent):
        # recursively build search tree up to configured depth, evaluating boards
        self.board_count += 1
        self.evaluate(board) #Used to get the possible moves of current 
        # filter out moves that would leave the moving side in check, and check for checkmate
        if self.turn.check or self.turn.enemy.check:
            posMate = True
            if self.turn.check:col = self.turn
            else:col = self.turn.enemy
            for y in range(8):
                for x in range(8):
                    CurPiece = board[y][x]
                    if isinstance(CurPiece, Pieces.empty) or CurPiece.colour != col:
                        continue
                    newMoves = []
                    cur_colour = CurPiece.colour

                    for move in CurPiece.posMove:
                        newBoard = self.copy_board(board) # Creates a copy of the board to modify without modifying original board
                        newBoard[y][x] = Pieces.empty() 
                        is_castling = len(move) > 2
                        if is_castling: # [What rook to move, Where to move the king, Where to move the rook]
                            rook_from_y, rook_from_x = move[0]
                            king_to_y, king_to_x = move[1]
                            rook_to_y, rook_to_x = move[2]

                            newBoard[rook_to_y][rook_to_x] = Pieces.rook(cur_colour, True)
                            newBoard[king_to_y][king_to_x] = Pieces.king(cur_colour, True)
                            newBoard[rook_from_y][rook_from_x] = Pieces.empty()
                        else:
                            newY = move[0]
                            newX = move[1]
                            if isinstance(CurPiece, Pieces.pawn):
                                newBoard[newY][newX] = Pieces.pawn(cur_colour, CurPiece.hasMoved, CurPiece.val)
                            elif isinstance(CurPiece, Pieces.rook):
                                newBoard[newY][newX] = Pieces.rook(cur_colour, CurPiece.hasMoved, CurPiece.val)
                            elif isinstance(CurPiece, Pieces.knight):
                                newBoard[newY][newX] = Pieces.knight(cur_colour, CurPiece.hasMoved, CurPiece.val)
                            elif isinstance(CurPiece, Pieces.bishop):
                                newBoard[newY][newX] = Pieces.bishop(cur_colour, CurPiece.hasMoved, CurPiece.val)
                            elif isinstance(CurPiece, Pieces.queen):
                                newBoard[newY][newX] = Pieces.queen(cur_colour, CurPiece.hasMoved, CurPiece.val)
                            elif isinstance(CurPiece, Pieces.king):
                                newBoard[newY][newX] = Pieces.king(cur_colour, CurPiece.hasMoved, CurPiece.val)
                        _, _, white_check, black_check = self.evaluate(newBoard)
                        if (col == self.white and not white_check) or (col == self.black and not black_check):
                            posMate = False
                            newMoves.append(move)
                    CurPiece.posMove = newMoves
            if posMate:
                parent.checkmate = True       
        if parent.getLevel() == self.depth: return # stop recursion at configured depth     
        for y, x in itertools.product(range(8), range(8)):
            CurPiece = board[y][x]
            if isinstance(CurPiece, Pieces.piece) and CurPiece.colour == self.turn:
                for move in CurPiece.posMove:
                        newBoard = self.copy_board(board)       
                        newBoard[y][x] = Pieces.empty()
                        if len(move) > 2: # [What rook to move, Where to move the king, Where to move the rook]
                                newBoard[move[2][0]][move[2][1]] = Pieces.rook(CurPiece.colour, True)
                                newBoard[move[1][0]][move[1][1]] = Pieces.king(CurPiece.colour, True)
                                newBoard[move[0][0]][move[0][1]] = Pieces.empty()
                        else:
                            newY = move[0]
                            newX = move[1]
                            if isinstance(CurPiece, Pieces.pawn):
                                newBoard[newY][newX] = Pieces.pawn(CurPiece.colour, CurPiece.hasMoved, CurPiece.val)
                            elif isinstance(CurPiece, Pieces.rook):
                                newBoard[newY][newX] = Pieces.rook(CurPiece.colour, CurPiece.hasMoved, CurPiece.val)
                            elif isinstance(CurPiece, Pieces.knight):
                                newBoard[newY][newX] = Pieces.knight(CurPiece.colour, CurPiece.hasMoved, CurPiece.val)
                            elif isinstance(CurPiece, Pieces.bishop):
                                newBoard[newY][newX] = Pieces.bishop(CurPiece.colour, CurPiece.hasMoved, CurPiece.val)
                            elif isinstance(CurPiece, Pieces.queen):
                                newBoard[newY][newX] = Pieces.queen(CurPiece.colour, CurPiece.hasMoved, CurPiece.val)
                            elif isinstance(CurPiece, Pieces.king):
                                newBoard[newY][newX] = Pieces.king(CurPiece.colour, CurPiece.hasMoved, CurPiece.val)
               
                        parent.addChild(newBoard)
        for child in parent.children:
            # recursively build tree for this child node, alternating turn to simulate opposition response
            self.switch() 
            self.DepthMap(child.content,child)
            self.switch()  
    def evaluate(self,board):
        # override to evaluate given board for the side to move in search
        self.board = board

        # Reset side state
        self.white.reset()
        self.black.reset()

        # Recompute all move/position values on this board
        self.get_move_val()
        self.get_piece_worth()
        self.get_check()
        self.white.set_eval()
        self.black.set_eval()

        # In the search, 'ally' is always the side to move: self.turn
        if self.side == self.white:
            ally_eval, enemy_eval = self.white.Eval, self.black.Eval
        else:
            ally_eval, enemy_eval = self.black.Eval, self.white.Eval

        return ally_eval, enemy_eval, self.white.check, self.black.check
    def switch(self):
        # swap turn to opposition for alternating search layers
        self.turn = self.turn.enemy
    def get_str_pos(self, board):
        # proxy to parent implementation while updating internal board
        self.board = board
        return super().get_str_pos()
    def find(self, cur, alpha = float('-inf'), beta = float('inf')): # Assume opposition will play best move
        # alpha-beta minimax search over constructed tree
        self.boards_analysed += 1
        depth = cur.getLevel()
        if cur.children:
            # Determine whether we are maximizing or minimizing at this layer of the tree (maximizing for the engine's move, minimizing for the opposition's response)
            maximizing = depth % 2 == 0 
            best_child = None
            if maximizing:
                best_value = float('-inf')
                # recursively evaluate children, updating alpha and pruning branches where possible
                for child in cur.children:
                    value = self.find(child, alpha, beta)
                    if value > best_value:
                        best_value = value
                        best_child = child
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        break 
                cur.next = best_child
                return best_value
            else:
                best_value = float('inf')
                # recursively evaluate children, updating beta and pruning branches where possible
                for child in cur.children:
                    value = self.find(child, alpha, beta)
                    if value < best_value:
                        best_value = value
                        best_child = child
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        break  
                cur.next = best_child
                return best_value
        AllyVal, EnemyVal, white_check, black_check = self.evaluate(cur.content)
        if cur.checkmate:
            if depth % 2 == 0: 
                EnemyVal += 1000 - depth
            else: 
                AllyVal += 1000 - depth
        denom = max(EnemyVal, 1)          
        return round((AllyVal/denom), 2) # Return a ratio of ally to enemy evaluation, to keep the evaluation relative and avoid issues with large positive or negative values dominating the search. The depth component in checkmate evaluation encourages faster mates and discourages slower ones.