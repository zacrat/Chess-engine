 # -*- coding: utf-8 -*-
import copy
import TreeGraph
import Pieces
import Sides

class ChessEngine:
    def __init__(self, depth, side, position ='RNBQKBNRPPPPPPPP################################pppppppprnbqkbnr'):
        self.position = position
        self.board = [[' 'for i in range(8)]for _ in range(8)] #Create board to be used 
        self.side = side
        #initialize sides
        self.white = Sides.WhiteSide()
        self.black = Sides.BlackSide()
        self.white.enemy = self.black
        self.black.enemy = self.white
        #initialize sides

        #Turn string input into 2d array board structure
        count = 0
        for y in range(8):
            for x in range(8):
                if position[count].isupper(): colour = self.black
                else: colour = self.white
                match position[count].lower():
                    case 'p': self.board[y][x] = Pieces.pawn(colour)
                    case 'r': self.board[y][x] = Pieces.rook(colour)
                    case 'n': self.board[y][x] = Pieces.knight(colour)
                    case 'b': self.board[y][x] = Pieces.bishop(colour)
                    case 'q': self.board[y][x] = Pieces.queen(colour)
                    case 'k': self.board[y][x] = Pieces.king(colour)
                    case '#': self.board[y][x] = ' '
                count += 1
        
        #Initialize depth engine
        self.Depth = Depth(depth, self.board, side)
    def print_board(self):
        for row in self.board:   
            print(*row)
    def run(self):
        #Starts searching at depth
        return self.Depth.start()
    def evaluate(self, pos =None):
        self.get_move_val() #Will asign each piece their possible moves, does not account for illegal moves.
        self.get_piece_worth() #Gets accumalitive piece worth and asign it to each side
        self.get_check() #Will get whether any side is in check
        self.white.set_eval() #Accumuatees each value to a total value to judge the position in terms of this side.
        self.black.set_eval() #^^^^^^^^^^
        #Changes side to simulate it being the other side's turn
        if self.side == self.white:return self.white.Eval, self.black.Eval
        else: return self.black.Eval, self.white.Eval
    def get_piece_worth(self): # Collects the cumulative worth of all pieces from each side
        for y in range(8):
            for x in range(8):
                CurPiece = self.board[y][x]
                if isinstance(CurPiece, Pieces.piece):
                    if CurPiece.colour == self.white:self.white.pieceVal+=CurPiece.val
                    else:self.black.pieceVal+=CurPiece.val
    def get_check(self):
        if self.black.kingPos in self.white.PosMoves:
            self.black.check = True
        if self.white.kingPos in self.black.PosMoves:
            self.white.check = True
    def get_move_val(self):
        for y in range(8):
            for x in range(8):
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
                        if isinstance(Curpiece.colour, Sides.WhiteSide):
                            self.white.kingPos = [y,x]
                            self.white.king = Curpiece
                        else:
                            self.black.kingPos = [y,x]
                            self.black.king = Curpiece
    def copy_board(self):
        return copy.deepcopy(self.board)
    def get_str_pos(self ,board = None):
        #Turns the 2d array strucuture back into the string format
        if board == None: board = self.board
        position = ""
        for y in range(8):
            for x in range(8):
                Curpiece = board[y][x]
                if Curpiece == ' ':
                    position += "#"
                    continue
                if Curpiece.colour == self.white:
                    if isinstance(Curpiece, Pieces.pawn): position +="p"
                    elif isinstance(Curpiece,Pieces.rook): position+="r"
                    elif isinstance(Curpiece,Pieces.knight): position+="n"
                    elif isinstance(Curpiece,Pieces.bishop): position+="b"
                    elif isinstance(Curpiece,Pieces.queen): position+="q"
                    elif isinstance(Curpiece,Pieces.king): position+="k"
                else:
                    if isinstance(Curpiece, Pieces.pawn): position +="P"
                    elif isinstance(Curpiece,Pieces.rook): position+="R"
                    elif isinstance(Curpiece,Pieces.knight): position+="N"
                    elif isinstance(Curpiece,Pieces.bishop): position+="B"
                    elif isinstance(Curpiece,Pieces.queen): position+="Q"
                    elif isinstance(Curpiece,Pieces.king): position+="K"
        return position
    def Update_pos(self,pos):
        #Used to change the engine's current positions
        self.board = pos
        self.Depth.tree.root = TreeGraph.TreeNode(pos)
    def cleanPos(self):
        #Removes illegal moves
        board = self.board
        self.evaluate(board) #Used to get the possible moves of current 
        posMate = True
        col = self.side
        for y in range(8):
            for x in range(8):
                CurPiece = board[y][x]
                if isinstance(CurPiece, Pieces.piece):
                    if CurPiece.colour == col:
                        newMoves = []
                        for move in CurPiece.posMove:
                            newY = move[0]
                            newX = move[1]
                            newBoard = self.copy_board() # Creates a copy of the board to modify without modifying original board
                            newBoard[y][x] = ' '
                            if isinstance(CurPiece, Pieces.pawn): newBoard[newY][newX] = Pieces.pawn(CurPiece.colour)
                            elif isinstance(CurPiece, Pieces.bishop): newBoard[newY][newX] = Pieces.bishop(CurPiece.colour)
                            elif isinstance(CurPiece, Pieces.knight): newBoard[newY][newX] = Pieces.knight(CurPiece.colour)
                            elif isinstance(CurPiece, Pieces.rook): newBoard[newY][newX] = Pieces.rook(CurPiece.colour)
                            elif isinstance(CurPiece, Pieces.queen): newBoard[newY][newX] = Pieces.queen(CurPiece.colour)
                            elif isinstance(CurPiece, Pieces.king): newBoard[newY][newX] = Pieces.king(CurPiece.colour)
                            self.evaluate(newBoard)
                            if not col.check:
                                posMate = False
                                newMoves.append(move)
                        CurPiece.posMove = newMoves
        if posMate:
            return True
## add maps to each Piece - done
## implement location of attacked/defended/possible positions in check methods - done
# Pieces.king not defending - fixed
# bishop not working for white side - fixed
# check for checks and checkmate - if in check that sides possible moves only become Pieces.king's possible moves, outside of enemy vision
# makes each side a class - rework premade - done
# Move onto depth - 15/09/2025 - 16:15
# add check vision - 11:45 19/09/2025 - 
# fix index error - done 02:11 20/09/2025
# add sequencing/multiple sequences to be checked - may require re-coding of some stuff
# ^ As of now it only runs a single line of moves that it deems to be best, doesn't look far ahead. true depth = 1
# Try tree graphing - 16:04 22/09/2025
# Need to find depth of singed node in tree
# ^ know when to stop searching - 00:26 24/09/2025 - done 18:57 24/09/2025
# ADD CHECK
# FIX CHECK - 00:07 09/10/2025
# Depth algorithm finshed - 13/10/2025
# Continuous evaluation started - 19/11/2025
class Depth(ChessEngine):
    def __init__(self, depth, board, side):
        self.depth = depth
        self.side = side
        self.white = Sides.WhiteSide()
        self.black = Sides.BlackSide()
        self.white.enemy = self.black
        self.black.enemy = self.white
        self.board = board
        self.turn = side
        self.tree = TreeGraph.Tree(TreeGraph.TreeNode(self.board))
    def copy_board(self, board):
        self.board = board
        return super().copy_board()
    def print_path(self):
        cur = self.tree.root
        while cur is not None:
            for row in cur.content:
                print(*row)
            print("_________________")
            print(cur.getLevel())
            cur = cur.next
    def start(self):
        self.DepthMap(self.tree.root.content, self.tree.root)
        self.find(self.tree.root)
        return self.tree.root.next.content
    def DepthMap(self,board,parent):
        self.evaluate(board) #Used to get the possible moves of current 
        if self.turn.check or self.turn.enemy.check:
            posMate = True
            if self.turn.check:col = self.turn
            else:col = self.turn.enemy
            for y in range(8):
                for x in range(8):
                    CurPiece = board[y][x]
                    if isinstance(CurPiece, Pieces.piece):
                        if CurPiece.colour == col:
                            newMoves = []
                            for move in CurPiece.posMove:
                                newY = move[0]
                                newX = move[1]
                                newBoard = self.copy_board(board) # Creates a copy of the board to modify without modifying original board
                                newBoard[y][x] = ' '
                                if isinstance(CurPiece, Pieces.pawn): newBoard[newY][newX] = Pieces.pawn(CurPiece.colour)
                                elif isinstance(CurPiece, Pieces.bishop): newBoard[newY][newX] = Pieces.bishop(CurPiece.colour)
                                elif isinstance(CurPiece, Pieces.knight): newBoard[newY][newX] = Pieces.knight(CurPiece.colour)
                                elif isinstance(CurPiece, Pieces.rook): newBoard[newY][newX] = Pieces.rook(CurPiece.colour)
                                elif isinstance(CurPiece, Pieces.queen): newBoard[newY][newX] = Pieces.queen(CurPiece.colour)
                                elif isinstance(CurPiece, Pieces.king): newBoard[newY][newX] = Pieces.king(CurPiece.colour)
                                self.evaluate(newBoard)
                                if not col.check:
                                    posMate = False
                                    newMoves.append(move)
                            CurPiece.posMove = newMoves
            if posMate:
                parent.checkmate = True
        try:
            if parent.getLevel() == self.depth: return
        except:pass
        for y in range(8):
            for x in range(8):
                CurPiece = board[y][x]
                if isinstance(CurPiece,Pieces.piece):
                    if CurPiece.colour == self.turn:
                        for move in CurPiece.posMove:
                            newBoard = self.copy_board(board)
                            newY = move[0]
                            newX = move[1]
                            newBoard[y][x] = ' '
                            if isinstance(CurPiece, Pieces.pawn): newBoard[newY][newX] = Pieces.pawn(CurPiece.colour)
                            elif isinstance(CurPiece,Pieces.rook): newBoard[newY][newX] = Pieces.rook(CurPiece.colour)
                            elif isinstance(CurPiece,Pieces.knight): newBoard[newY][newX] = Pieces.knight(CurPiece.colour)
                            elif isinstance(CurPiece,Pieces.bishop): newBoard[newY][newX] = Pieces.bishop(CurPiece.colour)
                            elif isinstance(CurPiece,Pieces.queen): newBoard[newY][newX] = Pieces.queen(CurPiece.colour)
                            elif isinstance(CurPiece,Pieces.king): newBoard[newY][newX] = Pieces.king(CurPiece.colour)
                            parent.addChild(newBoard)
        for child in parent.children:
            self.switch()
            self.DepthMap(child.content,child)
            self.switch()  
    def evaluate(self,board):
        self.board = board
        return super().evaluate()
    def switch(self):
        self.turn = self.turn.enemy
    def get_str_pos(self, board):
        self.board = board
        return super().get_str_pos()
    def find(self, cur): # Assume opposition will play best move
        depth = cur.getLevel()
        if cur.children:
            evals = []
            maxEval = -10000000000000
            minEval = 10000000000000
            for child in cur.children:
                evals.append(self.find(child))
                for i in range(len(evals)):
                    if depth % 2 == 0: # if the depth of the current position is even that means it is the original side's turn
                        if evals[i] > maxEval:
                            cur.next = child
                            maxEval = evals[i]
                        val = maxEval
                    else:
                        if evals[i] < minEval:
                            cur.next = child
                            minEval = evals[i]
                        val = minEval
            return val
        else:
            AllyVal, EnemyVal = self.evaluate(cur.content)
            if cur.checkmate:
                if depth % 2 == 0: EnemyVal+= 1000-depth
                else: AllyVal += 1000-depth
            return round((AllyVal/EnemyVal), 2)
                    
