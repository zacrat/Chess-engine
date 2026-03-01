import Sides

# base class for all chess pieces, stores colour, value, movement list
class piece:
    def __init__(self, colour = None, val = 0, hasMoved = False): # intitalises the piece object with relevant values and properties.
        # colour: side instance; val: material value; hasMoved: tracks castling
        self.hasMoved = hasMoved
        self.val = val
        self.colour = colour
        self.posMove =[]
    def reset(self):
        self.posMove = []
    def check(self, x, y, board):
        raise NotImplementedError("Subclasses of 'piece' must implement check()")

class pawn(piece):
    def __init__(self, colour=None,hasMoved = False, val = 1):
        self.attackMove = [[1,-1],[-1,-1]]
        super().__init__(colour,hasMoved, val)
        self.mapWhite = [[0,0,0,0,0,0,0,0], 
                    [2,2,2,2,2,2,2,2],
                    [1,1.25,1.5,1.75,1.75,1.5,1.25,1], 
                    [0.75,1,1.25,1.5,1.5,1.25,1,0.75], 
                    [0.5,0.75,1,1.25,1.25,1,0.75,0.5], 
                    [0.25,0.5,0.75,1,1,0.75,0.5,0.25], 
                    [0,0.25,0.5,0.75,0.75,0.5,0.25,0],
                    [0,0,0,0,0,0,0,0]]
        self.mapBlack =  [[0,0,0,0,0,0,0,0], 
                    [0,0.25,0.5,0.75,0.75,0.5,0.25,0],
                    [0.25,0.5,0.75,1,1,0.75,0.5,0.25], 
                    [0.5,0.75,1,1.25,1.25,1,0.75,0.5], 
                    [0.75,1,1.25,1.5,1.5,1.25,1,0.75], 
                    [1,1.25,1.5,1.75,1.75,1.5,1.25,1], 
                    [2,2,2,2,2,2,2,2],
                    [0,0,0,0,0,0,0,0]]
        self.icon = "\u2659" if isinstance(colour, Sides.WhiteSide) else "\u265F"
    def __str__(self): return self.icon
    def check(self,x,y,board):
            AttackVal = 0
            DefenseVal = 0
            ToCheckWhiteY = [-1,-1]
            ToCheckX = [1,-1]
            ToCheckBlackY = [1,1]
            if isinstance(self.colour, Sides.WhiteSide):
                PosVal = self.mapWhite[y][x]
                ToCheckY = ToCheckWhiteY
                startLevel = 6
            else: 
                PosVal = self.mapBlack[y][x]
                ToCheckY = ToCheckBlackY
                startLevel = 1
            if 0<y+ToCheckY[0]<8 and not isinstance(board[y+ToCheckY[0]][x], piece):
                self.posMove.append([y+ToCheckY[0],x])
                if y == startLevel and not isinstance(board[y+2*(ToCheckY[0])][x], piece): 
                    self.posMove.append([y+2*(ToCheckY[0]),x]) # allows the pawn to move two squares forward on its first move, if both squares are unoccupied
            for i in range(2):
                # Checks for possible attacks
                if 0<y+ToCheckY[i]<8 and 0<x+ToCheckX[i]<8:
                    checking = board[y+ToCheckY[i]][x+ToCheckX[i]]
                    if isinstance(checking, piece): 
                        if checking.colour != self.colour:
                            AttackVal += checking.val
                            self.posMove.append([y+ToCheckY[i], x+ToCheckX[i]]) # allows the pawn to move diagonally to capture an enemy piece
                        else:
                            DefenseVal+= checking.val

                            
            return [AttackVal, PosVal, DefenseVal, self.posMove]
class rook(piece):
    def __init__(self, colour = None, hasMoved = False, val = 5,):
        super().__init__(colour,val,hasMoved)
        self.map = [[-0.25,0,0.25,0.5,0.5,0.25,0,-0.25], 
                    [0,0.25,0.5,0.75,0.75,0.5,0.25,0],
                    [0.25,0.75,1.25,1.75,1.75,1.25,0.75,0.25], 
                    [0.5,1,1.5,2,2,1.5,1,0.5], 
                    [0.5,1,1.5,2,2,1.5,1,0.5], 
                    [0.25,0.75,1.25,1.75,1.75,1.25,0.75,0.25], 
                    [0,0.25,0.5,0.75,0.75,0.5,0.25,0],
                    [-0.25,0,0.25,0.5,0.5,0.25,0,-0.25]]
        self.hasMoved = hasMoved
        self.icon = "\u2656" if isinstance(colour, Sides.WhiteSide) else "\u265C"
    def __str__(self): return self.icon
    def check(self,x,y,board):
        AttackVal = 0
        PosVal = self.map[y][x]
        DefenseVal = 0        
        limXpos = False
        limYpos = False
        limXNeg = False
        limYNeg = False
        for i in range(1,8): # positive values for x and y
            if not limXpos:
                try:
                    checking = board[y][x+i]
                    if (0<=x+i<=len(board[0])):
                        if isinstance(checking, piece): # Checks if square is occupied
                            if checking.colour != self.colour:# Checks if piece is an enemy piece
                                AttackVal += checking.val
                                self.posMove.append([y, x+i])
                            else:
                                DefenseVal+= checking.val
                            limXpos = True
                        else: self.posMove.append([y, x+i])
                except: limXpos = True
            if not limYpos:
                try:
                    if (0<=y+i<=len(board)):
                        checking = board[y+i][x]
                        if isinstance(checking, piece): # Checks if square is occupied
                            if checking.colour != self.colour: # Checks if piece is an enemy piece
                                AttackVal += checking.val
                                self.posMove.append([y+i, x])
                            else:
                                DefenseVal+= checking.val
                              
                            limYpos = True
                        else: self.posMove.append([y+i, x])
                except: limYpos = True
            if not limXNeg:    
                try:
                    if (0<=x-i<=len(board[0])):
                        checking = board[y][x-i]
                        if isinstance(checking, piece): # Checks if square is occupied
                            if checking.colour != self.colour: # Checks if piece is an enemy piece
                                AttackVal += checking.val
                                self.posMove.append([y, x-i])      
                            else:
                                DefenseVal+= checking.val
                                
                            limXNeg = True
                        else: self.posMove.append([y, x-i])
                except: limXNeg = True
            if not limYNeg:
                try:
                    if (0<=y-i<=len(board)):
                        checking = board[y-i][x]
                        if isinstance(checking, piece): # Checks if square is occupied
                            if checking.colour != self.colour: # Checks if piece is an enemy piece
                                AttackVal += checking.val
                                self.posMove.append([y-i, x])
                            else:
                                DefenseVal+= checking.val
                                
                            limYNeg = True
                        else: self.posMove.append([y-i, x])
                except: limYNeg = True
        return [AttackVal, PosVal, DefenseVal, self.posMove]
class knight(piece):
    def __init__(self, colour = None,hasMoved = False, val = 3,):
        super().__init__(colour,hasMoved, val)
        self.map = [[-0.75,-0.5,-0.25,0,0,-0.25,-0.5,-0.75], 
                    [-0.5, -0.25, 0,0.25,0.25,0,-0.25,-0.5],
                    [-0.25, 0, 0.25,0.5,0.5,0.25, 0, -0.25], 
                    [0, 0.25, 0.5, 0.75, 0.75, 0.5, 0.25,0], 
                    [0, 0.25, 0.5, 0.75, 0.75, 0.5, 0.25,0], 
                    [-0.25, 0, 0.25,0.5,0.5,0.25, 0, -0.25], 
                    [-0.5, -0.25, 0,0.25,0.25,0,-0.25,-0.5],
                    [-0.75,-0.5,-0.25,0,0,-0.25,-0.5,-0.75]]
        self.icon = "\u2658" if isinstance(colour, Sides.WhiteSide) else "\u265E"
    def __str__(self): return self.icon
    def check(self,x,y,board):
        AttackVal = 0
        PosVal = self.map[y][x]
        DefenseVal = 0
        ToCheckX = [2,2,-2,-2,1,1,-1,-1] # relative x and y coordinates of knight moves
        ToCheckY = [1,-1,1,-1,2,-2,-2,2] 
        # iterate through possible moves, checking for validity and whether they are attacking an enemy piece, defended by an ally piece, or an empty square
        for i in range(len(ToCheckX)):
            if not (0<=y+ToCheckY[i]<=len(board) and 0<=x+ToCheckX[i]<=len(board[0])):continue
            try:checking = board[y+ToCheckY[i]][x+ToCheckX[i]]
            except:continue
            if isinstance(checking, piece):
                if checking.colour != self.colour:
                    AttackVal += checking.val
                    self.posMove.append([y+ToCheckY[i], x+ToCheckX[i]])
                else:
                    DefenseVal += checking.val
            else:
                self.posMove.append([y+ToCheckY[i], x+ToCheckX[i]])
        return [AttackVal, PosVal, DefenseVal, self.posMove]
class bishop(piece):
    def __init__(self, colour = None,hasMoved=False, val = 3,):
        super().__init__(colour,hasMoved, val)
        self.map = [[-1, -0.5, 0, 0.5, 0.5, 0, -0.5, -1], 
                    [-0.5, -0.25, 0, 0.25, 0.25, 0, -0.25, -0.5],
                    [0, 0.25, 0.5, 0.75, 0.75, 0.5, 0.25, 0], 
                    [0.5, 0.75, 1, 2, 2, 1, 0.75, 0.5], 
                    [0.5, 0.75, 1, 2, 2, 1, 0.75, 0.5], 
                    [0, 0.25, 0.5, 0.75, 0.75, 0.5, 0.25, 0], 
                    [-0.5, -0.25 ,0, 0.25, 0.25, 0, -0.25, -0.5],
                    [-1, -0.5, 0, 0.5, 0.5, 0, -0.5, -1]]
        self.icon = "\u2657" if isinstance(colour, Sides.WhiteSide) else "\u265D"
    def __str__(self): return self.icon
    def check(self,x,y,board):
        AttackVal = 0
        PosVal = self.map[y][x]
        DefenseVal = 0        
        limXpos = False
        limYpos = False
        limXNeg = False
        limYNeg = False
        for i in range(1,8): # positive values for x and y
            if not limXpos:
                if (0<=y+i<=len(board) and 0<=x+i<=len(board[0])): 
                    try:
                        checking = board[y+i][x+i]
                        if isinstance(checking, piece): # Checks if square is occupied
                            if checking.colour != self.colour:
                                AttackVal += checking.val
                                self.posMove.append([y+i, x+i])
                            else:
                                DefenseVal += checking.val
                               
                            limXpos = True
                        else: self.posMove.append([y+i, x+i])
                    except Exception as e:
                        pass   
            if not limYpos:
                if (0<=y-i<=len(board) and 0<=x+i<=len(board[0])): 
                    try:
                        checking = board[y-i][x+i]
                        if isinstance(checking, piece):# Checks if square is occupied
                            if checking.colour != self.colour:
                                AttackVal += checking.val
                                self.posMove.append([y-i, x+i])
                            else:
                                DefenseVal+= checking.val
     
                            limYpos = True
                        else: self.posMove.append([y-i, x+i])
                    except Exception as e:
                        pass 
            if not limXNeg:
                if (0<=y-i<=len(board) and 0<=x-i<=len(board[0])):     
                    try:
                        checking = board[y-i][x-i]
                        if isinstance(checking, piece):# Checks if square is occupied
                            if checking.colour != self.colour:
                                AttackVal += checking.val
                                self.posMove.append([y-i, x-i])
                            else:
                                DefenseVal+= checking.val
    
                            limXNeg = True
                        else: self.posMove.append([y-i, x-i])
                    except Exception as e:
                        pass
            if not limYNeg:
                if (0<=y+i<=len(board) and 0<=x-i<=len(board[0])):
                    try:
                        checking = board[y+i][x-i]
                        if isinstance(checking, piece):# Checks if square is occupied
                            if checking.colour != self.colour:
                                AttackVal += checking.val
                                self.posMove.append([y+i, x-i])
                            else:
                                DefenseVal+= checking.val
                                
                            limYNeg = True
                        else: self.posMove.append([y+i, x-i])
                    except Exception as e:
                            pass  
        return [AttackVal, PosVal, DefenseVal, self.posMove]
class queen(piece):
    def __init__(self, colour = None,hasMoved=False, val = 9):
        super().__init__(colour,hasMoved, val)
        self.map = [[0,0.25,0.5,0.75,0.75,0.5,0.25,0],
                    [0.25,0.75,1.25,1.75,1.75,1.25,0.75,0.25],
                    [0.5,1,1.5,2,2,1.5,1,0.5], 
                    [0.75,1.25,1.75,2.25,2.25,1.75,1.25,0.75], 
                    [0.75,1.25,1.75,2.25,2.25,1.75,1.25,0.75], 
                    [0.5,1,1.5,2,2,1.5,1,0.5], 
                    [0.25,0.75,1.25,1.75,1.75,1.25,0.75,0.25],
                    [0,0.25,0.5,0.75,0.75,0.5,0.25,0]]
        self.icon = "\u2655" if isinstance(colour, Sides.WhiteSide) else "\u265B"
    def __str__(self): return self.icon
    def check(self,x,y,board):
        self.posMove = []
        # Utilises the movement of the rook and bishop combined, as the queen can move in straight lines and diagonals
        temp_rook = rook(self.colour)
        straightVal = temp_rook.check(x, y, board)
        temp_bishop = bishop(self.colour)
        DiagVal = temp_bishop.check(x, y, board)
        # combines the move lists and evaluations of the rook and bishop, to get the full move list and evaluation for the queen
        self.posMove = straightVal[3] + DiagVal[3]
        AttackVal = straightVal[0] + DiagVal[0]
        PosVal = straightVal[1]
        DefenseVal = straightVal[2] + DiagVal[2]
        return [AttackVal, PosVal, DefenseVal, self.posMove]
class king(piece):
    def __init__(self, colour = None, hasMoved = False, val = 10):
        super().__init__(colour,hasMoved, val)
        self.mapWhite = [[-2,-2,-2,-2,-2,-2,-2,-2], 
                    [-1.75,-1.75,-1.75,-1.75,-1.75,-1.75,-1.75,-1.75],
                    [-1.5,-1.5,-1.5,-1.5,-1.5,-1.5,-1.5,-1.5], 
                    [-1.25,-1.25,-1.25,-1.25,-1.25,-1.25,-1.25,-1.25], 
                    [-1,-1,-1,-1,-1,-1,-1,-1], 
                    [-0.75,-0.75,-0.75,-0.75,-0.75,-0.75,-0.75,-0.75,], 
                    [-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5],
                    [0,0,0,0,0,0,0,0]]
        self.mapBlack = [[0,0,0,0,0,0,0,0], 
                    [-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5],
                    [-0.75,-0.75,-0.75,-0.75,-0.75,-0.75,-0.75,-0.75], 
                    [-1,-1,-1,-1,-1,-1,-1,-1], 
                    [-1.25,-1.25,-1.25,-1.25,-1.25,-1.25,-1.25,-1.25], 
                    [-1.5,-1.5,-1.5,-1.5,-1.5,-1.5,-1.5,-1.5], 
                    [-1.75,-1.75,-1.75,-1.75,-1.75,-1.75,-1.75,-1.75],
                    [-2,-2,-2,-2,-2,-2,-2,-2]]
        self.hasMoved = hasMoved
        self.icon = "\u2654" if isinstance(colour, Sides.WhiteSide) else "\u265A"
    def __str__(self): return self.icon 
    def check(self,x,y,board):
        AttackVal = 0
        DefenseVal = 0
        CastlePositions =  []
        ToCheckX = [-1,0,1,1,1,0,-1,-1]
        ToCheckY = [-1,-1,-1,0,1,1,1,0]
        match isinstance(self.colour, Sides.WhiteSide):
            case True: PosVal = self.mapWhite[y][x]
            case False: PosVal = self.mapBlack[y][x]
        for i in range(len(ToCheckX)):
            try:checking = board[y+ToCheckY[i]][x+ToCheckX[i]]
            except:continue
            if (0<=y+ToCheckY[i]<=len(board) and 0<=x+ToCheckX[i]<=len(board[0])):
                if isinstance(checking, piece):
                    if checking.colour == self.colour:
                        DefenseVal += checking.val
                    else:
                        AttackVal += checking.val
                        self.posMove.append([y+ToCheckY[i], x+ToCheckX[i]])
                else:
                    self.posMove.append([y+ToCheckY[i], x+ToCheckX[i]])
        if self.hasMoved == False:
            # Castling possible
            rooksFound = 0 # Keeps track of whether we've found the king's rook, queen's rook, or both, to avoid unnecessary checks after finding both rooks or the relevant rook for the side we're on
            castle = False
            for cX in range(8):
                Curpiece = board[y][cX]
                if isinstance(Curpiece,rook) and Curpiece.colour == self.colour:
                    rooksFound += 1
                    if not Curpiece.hasMoved:
                        order = -1 if cX < x else 1 # Determines whether to check squares to the left or right of the king, depending on which rook we're looking at
                        for place in range(x+order, cX, order): 
                            if isinstance(board[y][place], empty):
                                castle = True
                            else:
                                castle = False
                                break
                        if castle:         
                            kingCastlePos = round((cX+x)/2) # Position the king moves to when castling, which is always halfway between the rook and king's starting positions
                            rookCastlePos = kingCastlePos+1 if cX < x else kingCastlePos-1 # Position the rook moves to when castling, which is always on the opposite side of the king from the rook's starting position
                            self.posMove.append([[y,cX], [y ,kingCastlePos], [y, rookCastlePos]])
                            CastlePositions.append([[y,cX], [y ,kingCastlePos], [y, rookCastlePos]])# [What rook to move, Where to move the king, Where to move the rook]
                if rooksFound == 2:
                    break
        return [AttackVal, PosVal, DefenseVal, self.posMove, CastlePositions]
class empty:
    # represents an empty square on the board, used to simplify move generation and board representation
    def __init__(self):
         self.val = 0
         self.colour = None
    def __str__(self): return " "