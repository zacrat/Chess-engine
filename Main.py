import Game
import Engine
import cProfile

white = Engine.Sides.WhiteSide()
black = Engine.Sides.BlackSide()
white.enemy = black
black.enemy = white
def main():
    print("START")
    running = True
    Start = Game.Game(white, 2)
    while running:
        running = Start.play()
main()