import Engine
import datetime
import queue

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
        self.FileName = f"Past_games/Chess game on {self.date} at {self.time}.txt"
        self.bot = Engine.ChessEngine(depth, turn, pos)
        self.GenBot = Engine.ChessEngine(1, turn.enemy, pos)
        self.curPos = self.bot.board
        self.ongoing = True
        self.player_queue = queue.Queue()
        self.winner = None
        open(self.FileName,'x')
        try:
            open("App_data/Data.txt",'a')
        except:
            open("App_data/Data.txt",'x')
        with open("App_data/Data.txt",'r') as file:
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
                self.winner = self.black
            elif self.black.check:
                file.write("White Won by checkmate")
                self.winner = self.white
            else:
                file.write("The game is a draw")
                self.winner = None
            file.close()
        if self.bot.side.check:
            lines = []
            with open(self.FileName,'r') as file:
                for line in file.readlines():
                    lines.append(line.split(":"))
                file.close()
            with open("App_data/Recently_evaluated.txt") as file:
                file.write(self.FileName)
            self.bot.REevaluate(lines)
        self.ongoing = False
    def play(self):
        self.write_move()
        if self.turn == self.bot.side:
            try:
                with open("App_data/Data.txt",'r') as file:
                    data = file.readlines()
                    for line in data:
                        move = line.split(":")
                        for row in self.bot.str_to_board(move[0]):
                            print(*row)
                        if move[0] == self.bot.get_str_pos(self.curPos):
                            next_move = self.bot.str_to_board(move[1])
                            move_found = True
                            break
                if not move_found:
                    raise Exception  
            except:    
                self.bot.evaluate(self.curPos)
                next_move = self.bot.run()
            if next_move == None:
                print("Game ended")
                self.checkmate()
            self.curPos = next_move        
        else:
            self.GenBot.evaluate(self.curPos)
            if self.GenBot.cleanPos():
                self.checkmate()
            piece_valid= False
            while not piece_valid:
                player_move = self.player_queue.get()
                if len(player_move) > 2:
                    y_coord_piece, x_coord_piece = player_move[3]
                    rR, cR = player_move[0]
                    r, c = player_move[1]
                    rRM, cRM = player_move[2]
                    move_piece = self.curPos[y_coord_piece][x_coord_piece]
                    self.curPos[rRM][cRM] = self.curPos[rR][cR]
                    self.curPos[rR][cR] = ' '
                    y_coord_move = r
                    x_coord_move = c
                    piece_valid = True
                else:
                    from_pos, to_pos = player_move 
                    x_coord_piece = from_pos[1]
                    y_coord_piece = from_pos[0]
                    x_coord_move = to_pos[1]
                    y_coord_move = to_pos[0]
                    move_piece = self.curPos[y_coord_piece][x_coord_piece]
                    if isinstance(move_piece, Engine.Pieces.piece) and move_piece.colour == self.turn:
                        piece_valid = True
                        move_piece.posMove = []
                        move_piece.check(x_coord_piece, y_coord_piece, self.curPos)
                        possible_moves = move_piece.posMove
                        for move in possible_moves:
                            r, c = move
                            if r == y_coord_move and c == x_coord_move:
                                break
            self.curPos[y_coord_piece][x_coord_piece] = ' '
            self.curPos[y_coord_move][x_coord_move] = move_piece
        self.bot.Update_pos(self.curPos)
        self.GenBot.Update_pos(self.curPos)
        self.turn = self.turn.enemy
        return True