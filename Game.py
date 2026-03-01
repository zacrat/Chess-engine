import Engine
import datetime
import queue
class Game():
    def __init__(self, turn, depth, pos = "RNBQKBNRPPPPPPPP################################pppppppprnbqkbnr"):
        # Initializes both sides
        self.white = Engine.Sides.WhiteSide()
        self.black = Engine.Sides.BlackSide()
        self.white.enemy = self.black
        self.black.enemy = self.white

        self.turn = turn
        self.depth = depth

        # Game data initialization
        now = datetime.datetime.now()
        self.date = now.strftime("%Y-%m-%d")
        self.time = now.strftime("%H-%M-%S")
        self.FileName = f"Past_games/Chess game on {self.date} at {self.time}.txt"

        # Initializes the game chess engine and another engine for generating moves for the player
        self.bot = Engine.ChessEngine(depth, turn, pos)
        self.GenBot = Engine.ChessEngine(1, turn.enemy, pos)

        # Initializes the current position and a list to keep track of previous moves
        self.curPos = self.bot.board
        self.ongoing = True
        self.player_queue = queue.Queue()

        #for machine learning
        self.winner = None
        self.learning = False

        # Creates a new file to store the game data and reads existing data from a file if it exists
        open(self.FileName,'x')
        try:
            open("App_data/Data.txt",'a')
        except Exception:
            open("App_data/Data.txt",'x')
        with open("App_data/Data.txt",'r') as file:
            self.lines = file.readlines()
            self.data = [line.split(":") for line in self.lines]
    def check_for_mate(self):
        # Checks if the current position is a checkmate and updates the game state accordingly
        if self.GenBot.cleanPos():
                self.checkmate()
    def write_move(self):
        # Writes the current position and its evaluation to the game data file and adds the current position to the list of previous moves
        with open(self.FileName, 'a') as file:
            file.write(f"{self.bot.get_str_pos(self.curPos)}:{self.bot.evaluate(self.curPos)[0]}\n")
            file.close()
        self.prev_moves.append(self.bot.get_str_pos(self.curPos))
    def checkmate(self):
        # Writes the result of the game to the game data file and updates the winner of the game based on which side is in checkmate
        with open(self.FileName, 'a') as file:
            self.ongoing = False
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
            self.Machine_learning()
    
    def Machine_learning(self):
        # Re-evaluates the positions in the game data file and updates the evaluations based on the outcome of the game, then writes the updated evaluations back to the file
        lines = []
        with open(self.FileName,'r') as file:
            lines.extend(line.split(":") for line in file)
        with open("App_data/Recently_evaluated.txt", "a") as file:
            file.write(self.FileName+ "\n")
            file.close()
        self.learning = True
        self.bot.REevaluate(lines)
        self.learning = False
    def Search_for_position(self, pos):
        move_found = False
        with open("App_data/Data.txt",'r') as file:
                    # Reads game data and tries to find a move for the given position, if found, it returns the next position after that move, otherwise it raises an exception
                    data = file.readlines()
                    for line in data:
                        move = line.split(":")
                        if move[0] == pos:
                            next_move = self.bot.str_to_board(move[1])
                            move_found = True
                            break
        if not move_found:
            raise BaseException
        else:
            return next_move
    def bot_move(self):
        # Used to get the bot's next move manually.
        next_move = self.bot.run()
        self.bot.Depth.board_count = 0
        self.bot.Depth.boards_analysed = 0
        return next_move

    def player_move(self, move):
        # Processes the player's move, updates the current position accordingly.
        if len(move) > 2: 
            # Castling move
            y_coord_piece, x_coord_piece = move[3]
            rR, cR = move[0]
            r, c = move[1]
            rRM, cRM = move[2]
            move_piece = self.curPos[y_coord_piece][x_coord_piece]
            self.curPos[rRM][cRM] = self.curPos[rR][cR]
            self.curPos[rR][cR] = Engine.Pieces.empty()
            y_coord_move = r
            x_coord_move = c 
        else: 
            # Normal move
            from_pos, to_pos = move 
            x_coord_piece = from_pos[1]
            y_coord_piece = from_pos[0]
            x_coord_move = to_pos[1]
            y_coord_move = to_pos[0]
            move_piece = self.curPos[y_coord_piece][x_coord_piece]
            if isinstance(move_piece, Engine.Pieces.piece) and move_piece.colour == self.turn:
                move_piece.posMove = []
                move_piece.check(x_coord_piece, y_coord_piece, self.curPos)
                possible_moves = move_piece.posMove
                for move in possible_moves:
                    r, c = move
                    if r == y_coord_move and c == x_coord_move:
                        break
        # Update the current position with the player's move and update the bot's position accordingly
        self.curPos[y_coord_piece][x_coord_piece] = Engine.Pieces.empty()
        self.curPos[y_coord_move][x_coord_move] = move_piece
        self.GenBot.Update_pos(self.curPos)
        
    def play(self):
        # Checks for mate and writes the move to the game data file.
        self.check_for_mate()
        self.write_move()
        if self.turn == self.bot.side:
            # Tries to find next move from the training data, if unsuccessful it will use the traditional algorithm. 
            try:
                next_move = self.Search_for_position(self.bot.get_str_pos(self.curPos))
            except BaseException:
                next_move = self.bot_move()
            if next_move is None:
                self.checkmate()
            self.curPos = next_move
            self.bot.Update_pos(self.curPos)
        else: 
            # Waits for the player's move to be added to the queue and processes it.
            piece_valid= False
            while not piece_valid:
                player_move = self.player_queue.get()
                self.player_move(player_move)
                piece_valid = True
        self.turn = self.turn.enemy # Switch turns after each move
        return True # 