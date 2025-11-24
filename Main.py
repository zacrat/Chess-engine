import Game
import Engine

white = Engine.Sides.WhiteSide()
black = Engine.Sides.BlackSide()
white.enemy = black
black.enemy = white

running = True
Start = Game.Game(white, 2)
while running:
    running = Start.play()
