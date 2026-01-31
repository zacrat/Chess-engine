import Game
import Engine
import cProfile

white = Engine.Sides.WhiteSide()
black = Engine.Sides.BlackSide()
white.enemy = black
black.enemy = white
def main():
    do = input("what do you want to do? (play/profile): ")
    match do.lower():
        case "play":    
            running = True
            Start = Game.Game(white, 2)
            while running:
                running = Start.play()
        case "profile":
            bot = Engine.ChessEngine(2, white)
            profile = input("Enter profile filename: ")
            board = bot.str_to_board(profile)
            for row in board:
                print(*row)
main()