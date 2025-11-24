import Game
import Engine

white = Engine.Sides.WhiteSide()
black = Engine.Sides.BlackSide()
white.enemy = black
black.enemy = white

running = True
Start = Game.Game(white, 2, "R##Q#R#K##PB##P#P###P#b##P#Pp#P#######q###p#p###pp###pppr###k##r")
while running:
    running = Start.play()

#unable to move bishop