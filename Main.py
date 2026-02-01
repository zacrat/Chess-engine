import Game
import Engine
import cProfile
import pygame
import sys
import threading

white = Engine.Sides.WhiteSide()
black = Engine.Sides.BlackSide()
white.enemy = black
black.enemy = white
Start = Game.Game(white, 2)
def game_thread(game):
    while game.ongoing:
        game.play()
game_thread = threading.Thread(target=game_thread, args=(Start,), daemon=True)

def main():
    #do = input("what do you want to do? (play/profile): ")
    #match do.lower():
        #case "play": 
    pygame.init()
    res = 640
    pygame.display.set_caption("Chess Engine")
    LIGHT = (240, 217, 181)
    DARK  = (181, 136, 99)
    font = pygame.font.SysFont("Segoe UI Symbol", 56)
    screen = pygame.display.set_mode((res, res))
    SQUARE_SIZE = res // 8
    clock = pygame.time.Clock()  
    game_thread.start() 
    selected_square = None
    while Start.ongoing:
        
        cur_pos = Start.curPos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Start.ongoing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = (mouse_x // SQUARE_SIZE)
                row = (mouse_y // SQUARE_SIZE)
                selected_square = (row, col)
        for row in range(8):    
            for col in range(8):
                symbol = cur_pos[row][col].__str__()
                text = font.render(symbol, True, (0, 0, 0))  
                if (row, col) == selected_square:
                    color = (255, 0, 0)
                else:
                    color = LIGHT if (row + col) % 2 == 0 else DARK
                pygame.draw.rect(
                    screen,
                    color,
                    (col * SQUARE_SIZE, row * SQUARE_SIZE,
                    SQUARE_SIZE, SQUARE_SIZE)
                )
                screen.blit(
                    text,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 4,
                    row * SQUARE_SIZE + SQUARE_SIZE // 8)
                )
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()
        #case "profile":
        #    bot = Engine.ChessEngine(2, white)
        #    profile = input("Enter profile filename: ")
        #    board = bot.str_to_board(profile)
        #    for row in board:
        #        print(*row)

main()