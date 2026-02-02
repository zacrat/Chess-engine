import Game
import Engine
import pygame
import sys
import threading
import UI
import PGN_importer
import os

white = Engine.Sides.WhiteSide()
black = Engine.Sides.BlackSide()
white.enemy = black
black.enemy = white

def game_loop(game):
    while game.ongoing:
        game.play()

def play_game():
    Start = Game.Game(white, 2)
    game_thread = threading.Thread(target=game_loop, args=(Start,), daemon=True)
    game_thread.start() 
    selected_square = None
    possible_moves = []
    while Start.ongoing:
        cur_pos = Start.curPos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = (mouse_x // SQUARE_SIZE)
                row = (mouse_y // SQUARE_SIZE)
                if [row, col] == selected_square:
                    selected_square = None
                elif [row, col] in possible_moves:
                    Start.player_queue.put((selected_square, [row, col]))
                    selected_square = None
                else:
                    selected_square = [row, col]
        for row in range(8):    
            for col in range(8):
                symbol = cur_pos[row][col].__str__()
                text = font.render(symbol, True, (0, 0, 0))  
                if [row, col] == selected_square:
                    color = (255, 0, 0)
                    board = Start.curPos
                    piece = board[row][col]
                    if isinstance(piece, Engine.Pieces.piece) :
                        piece.posMove = []
                        piece.check(col, row, board)
                        possible_moves = piece.posMove
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
        for move in possible_moves:
            if len(move) > 2:
                r, c = move[1]
            else:
                r, c = move
            pygame.draw.circle(
                screen,
                (0, 255, 0),
                (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2),
                SQUARE_SIZE // 4)
        pygame.display.flip()
        clock.tick(60)
def pgn_import():
    path = UI.choose_file()
    if path:
        PGN_importer.scan(path)

def open_data():
    path = "Data.txt"
    os.startfile(path)
pygame.init()
res = 720
pygame.display.set_caption("Chess Engine")
LIGHT = (240, 217, 181)
DARK  = (181, 136, 99)
font = pygame.font.SysFont("Segoe UI Symbol", 56)
screen = pygame.display.set_mode((res, res))
SQUARE_SIZE = res // 8
clock = pygame.time.Clock()  
# Buttons for menu UI
Start_button = UI.button(play_game, 100, 100, 200, 75, "Play Game")
Import_PGN_button = UI.button(pgn_import, 100, 200, 200, 75, "Import PGN")
Open_data_button = UI.button(open_data, 100, 300, 200, 75, "Open training data")
Exit_button = UI.button(sys.exit, 100, 400, 200, 75, "Exit")
def main():
    running = True
    buttons = [Start_button, Exit_button, Import_PGN_button, Open_data_button]
    while running == True:
        screen.fill((128, 128, 128))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(event):
                        button.function()
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

main()