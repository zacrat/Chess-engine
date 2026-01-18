import Engine
import datetime
class Game():
    def __init__(self, turn, depth, pos = "RNBQKBNRPPPPPPPP################################pppppppprnbqkbnr"):
        self.white = Engine.Sides.WhiteSide()
        self.black = Engine.Sides.BlackSide()
        self.white.enemy = self.black
        self.black.enemy = self.white
        self.turn = turn
        now = datetime.datetime.now()
        self.date = now.strftime("%Y-%m-%d")
        self.time = now.strftime("%H-%M-%S")
        self.FileName = f"Chess game on {self.date} at {self.time}.txt"
        self.bot = Engine.ChessEngine(depth, turn, pos)
        self.GenBot = Engine.ChessEngine(1, turn.enemy, pos)
        self.curPos = self.bot.board
        open(self.FileName,'x')
        try:
            open("Data.txt",'a')
        except:
            open("Data.txt",'x')
        with open("Data.txt",'r') as file:
            self.lines = file.readlines()
            self.data = []
            for line in self.lines:
                self.data.append(line.split(":"))
    def write_move(self):
        with open(self.FileName, 'a') as file:
            file.write(f"{self.bot.get_str_pos(self.curPos)}:{self.bot.evaluate(self.curPos)[0]}\n")
            file.close()
    def checkmate(self):
        with open(self.FileName, 'a') as file:
            if self.white.check:
                file.write("Black Won by checkmate")
            elif self.black.check:
                file.write("White Won by checkmate")
            else:
                file.write("The game is a draw")
            file.close()
        if self.bot.side.check:
            lines = []
            with open(self.FileName,'r') as file:
                for line in file.readlines:
                    lines.append(line.split(":"))
            self.bot.REevaluate(lines)
        return False
    def play(self):
        self.write_move()
        LTN = ["a","b","c","d","e","f","g","h"]
        nums = [8,7,6,5,4,3,2,1]
        if self.bot.side == self.black:
            nums = nums.reverse()
            LTN = LTN.reverse()
        if self.turn == self.bot.side:
            try:
                for move in self.data:
                    if move[0] == self.bot.get_str_pos(self.curPos):
                        next_move = self.bot.str_to_board(move[1])
                        break
                raise Exception  
            except:    
                self.bot.evaluate(self.curPos)
                next_move = self.bot.run()
            if next_move == None:
                print("Game ended")
                self.checkmate()
                return False
            self.curPos = next_move        
        else:
            self.GenBot.evaluate(self.curPos)
            if self.GenBot.cleanPos():
                self.checkmate()
                return False
            move_valid = False
            piece_valid= False
            while not piece_valid:
                move_piece_pos = input("Enter position of the piece you wish to move: ") #Formatted A4, G7 etc
                x_coord_piece = LTN.index(move_piece_pos[0].lower())
                y_coord_piece = nums.index(int(move_piece_pos[1]))
                move_piece = self.bot.board[y_coord_piece][x_coord_piece]
                if not isinstance(move_piece, Engine.Pieces.piece):
                    continue
                print(move_piece)
                castle_move = []
                for move in move_piece.posMove:
                    if len(move) > 2:
                        print(f"{LTN[move[1][1]]}{nums[move[1][0]]}")
                        castle_move.append(move[1])
                    else:
                        print(f"{LTN[move[1]]}{nums[move[0]]}")# [What rook to move, Where to move the king, Where to move the rook]
                if move_piece.colour != self.bot.side: piece_valid = True
            while not move_valid:
                try:
                    move_to = input("Enter the position you would like to move: ")#Formatted A4, G7 etc
                    x_coord_move = LTN.index(move_to[0].lower())
                    y_coord_move = nums.index(int(move_to[1]))
                    trasnslated_move = [y_coord_move, x_coord_move]
                    if trasnslated_move in move_piece.posMove or castle_move:move_valid = True
                except: pass
            if trasnslated_move in castle_move:
                for move in move_piece.posMove:
                    if len(move) > 2:
                        if move[1] == trasnslated_move:
                            self.curPos[move[1][0]][move[1][1]] = move_piece
                            self.curPos[move[2][0]][move[2][1]] = self.curPos[move[0][0]][move[0][1]]
                            self.curPos[move[0][0]][move[0][1]] = ' '
                            break
            self.curPos[y_coord_piece][x_coord_piece] = ' '
            self.curPos[y_coord_move][x_coord_move] = move_piece
        self.bot.Update_pos(self.curPos)
        self.GenBot.Update_pos(self.curPos)
        row_no  = 0
        print(*LTN)
        for row in self.curPos:
            ref_row = row.copy()
            ref_row.append(nums[row_no])
            print(*ref_row)
            row_no +=1
        self.turn = self.turn.enemy
        return True