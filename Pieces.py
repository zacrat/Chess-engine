import Sides

class piece:
    def __init__(self, colour = None, val = 0, hasMoved = False): # intitalises the piece object with relevant values and properties.
        self.hasMoved = hasMoved
        self.val = val
        self.colour = colour
        self.posMove =[]
    def reset(self):
        self.__init__(self.colour,self.hasMoved, self.val)
    def check(self, x, y, board):
        self.check(x, y, board)

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
        if isinstance(colour, Sides.WhiteSide):self.icon = "\u2659"
        else: self.icon = "\u265F"
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
            if 0<y+ToCheckY[0]<8:
                if not isinstance(board[y+ToCheckY[0]][x], piece):
                    self.posMove.append([y+ToCheckY[0],x])
                    if y == startLevel and not isinstance(board[y+2*(ToCheckY[0])][x], piece):
                        self.posMove.append([y+2*(ToCheckY[0]),x])
            for i in range(2):
                if 0<y+ToCheckY[i]<8 and 0<x+ToCheckX[i]<8:
                    checking = board[y+ToCheckY[i]][x+ToCheckX[i]]
                    if isinstance(checking, piece):
                        if checking.colour != self.colour:
                            AttackVal += checking.val
                            self.posMove.append([y+ToCheckY[i], x+ToCheckX[i]])
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
        if isinstance(colour, Sides.WhiteSide):self.icon = "\u2656"
        else: self.icon = "\u265C"
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
                        if isinstance(checking, piece):
                            if checking.colour != self.colour:
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
                        if isinstance(checking, piece):
                            if checking.colour != self.colour:
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
                        if isinstance(checking, piece):
                            if checking.colour != self.colour:
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
                        if isinstance(checking, piece):
                            if checking.colour != self.colour:
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
        if isinstance(colour, Sides.WhiteSide):self.icon = "\u2658"
        else: self.icon = "\u265E"
    def __str__(self): return self.icon
    def check(self,x,y,board):
        AttackVal = 0
        PosVal = self.map[y][x]
        DefenseVal = 0
        ToCheckX = [2,2,-2,-2,1,1,-1,-1]
        ToCheckY = [1,-1,1,-1,2,-2,-2,2]
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
        if isinstance(colour, Sides.WhiteSide):self.icon = "\u2657"
        else: self.icon = "\u265D"
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
                        if isinstance(checking, piece):
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
                        if isinstance(checking, piece):
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
                        if isinstance(checking, piece):
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
                        if isinstance(checking, piece):
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
        if isinstance(colour, Sides.WhiteSide):self.icon = "\u2655"
        else: self.icon = "\u265B"
    def __str__(self): return self.icon
    def check(self,x,y,board):
        temp_rook = rook(self.colour)
        straightVal = temp_rook.check(x, y, board)
        temp_bishop = bishop(self.colour)
        DiagVal = temp_bishop.check(x, y, board)
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
        if isinstance(colour, Sides.WhiteSide):self.icon = "\u2654"
        else: self.icon = "\u265A"
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
                    if checking.colour != self.colour:
                        AttackVal += checking.val
                        self.posMove.append([y+ToCheckY[i], x+ToCheckX[i]])
                    else:
                        DefenseVal += checking.val
                else:
                    self.posMove.append([y+ToCheckY[i], x+ToCheckX[i]])
        if self.hasMoved == False:
            rooksFound = 0
            castle = False
            for cX in range(8):
                Curpiece = board[y][cX]
                if isinstance(Curpiece,rook) and Curpiece.colour == self.colour:
                    rooksFound += 1
                    if  not Curpiece.hasMoved:
                        if cX < x:order = -1
                        else: order = 1
                        for place in range(x+order, cX, order):
                            if board[y][place] == ' ':
                                castle = True
                            else:
                                castle = False
                                break
                        if castle:         
                            kingCastlePos = round((cX+x)/2)
                            if cX < x: rookCastlePos = kingCastlePos+1
                            else: rookCastlePos = kingCastlePos-1
                            self.posMove.append([[y,cX], [y ,kingCastlePos], [y, rookCastlePos]])
                            CastlePositions.append([[y,cX], [y ,kingCastlePos], [y, rookCastlePos]])# [What rook to move, Where to move the king, Where to move the rook]
                if rooksFound == 2:
                    break
        return [AttackVal, PosVal, DefenseVal, self.posMove, CastlePositions]
