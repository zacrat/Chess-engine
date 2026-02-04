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

def open_settings():
    pass

def play_game():
    Start = Game.Game(white, 2)
    LTN = ["a","b","c","d","e","f","g","h"]
    nums = [8,7,6,5,4,3,2,1]    
    if Start.bot.side == black:
        nums = nums.reverse()
        LTN = LTN.reverse()
    game_thread = threading.Thread(target=game_loop, args=(Start,), daemon=True)
    game_thread.start() 
    selected_square = None
    possible_moves = []
    prev_moves = []
    while Start.ongoing:
        cur_pos = Start.curPos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = (mouse_x // SQUARE_SIZE)
                row = (mouse_y // SQUARE_SIZE)
                move_found = False
                for move in possible_moves:
                    from_pos = (selected_square[0], selected_square[1])
                    if len(move) > 2:# [What rook to move, Where to move the king, Where to move the rook] 
                        if move[1] == [row, col]:                   
                            Start.player_queue.put((move[0], move[1], move[2], from_pos))
                            prev_moves.append((from_pos, move[1]))
                            selected_square = None
                            possible_moves = [] 
                            move_found = True
                            break
                    else:
                        if move == [row,col]:
                            to_pos = (row, col)
                            Start.player_queue.put((from_pos, to_pos))
                            prev_moves.append((from_pos, to_pos))
                            selected_square = None
                            possible_moves = []
                            move_found = True
                            break 
                if move_found:
                    break
                if [row, col] == selected_square:
                    selected_square = None
                    possible_moves = []
                else:
                    selected_square = [row, col]
                    possible_moves = []          
                
        for row in range(8):    
            for col in range(8):
                symbol = cur_pos[row][col].__str__()
                text = font.render(symbol, True, (0, 0, 0))  
                if [row, col] == selected_square:
                    color = (255, 0, 0)
                    board = Start.curPos
                    piece = board[row][col]
                    if isinstance(piece, Engine.Pieces.piece):
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
        Played_moves.draw(screen, None)
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
res_h = 720
res_w = 1280
pygame.display.set_caption("Chess Engine")
LIGHT = (240, 217, 181)
DARK  = (181, 136, 99)
BACKGROUND = (14,14,74)
font = pygame.font.SysFont("Segoe UI Symbol", 56)
font_console = pygame.font.SysFont("console", 34)
screen = pygame.display.set_mode((res_w, res_h))
SQUARE_SIZE = 720 // 8 # Size of each square on the chessboard. Rest of the screen for menu UI at 720px right.
clock = pygame.time.Clock()  
# Buttons for menu UI
Start_button = UI.button(play_game, 100, 120, 200, 75, "Play Game")
Import_PGN_button = UI.button(pgn_import, 100, 220, 200, 75, "Import PGN")
Open_data_button = UI.button(open_data, 100, 320, 200, 75, "Open training data")
Settings = UI.button(open_settings,100, 420, 200, 75, "Settings")
Exit_button = UI.button(sys.exit, 100, 420, 200, 75, "Exit")
#Menu UI
Played_moves = UI.TextBox(980,120,250,500,"Previous Moves",(120,120,120),font_console)
Title = UI.TextBox(res_w//8, res_h//32, res_w//(8/6), 80, "", (255,255,255), font)

def main():
    running = True
    buttons = [Start_button, Exit_button, Import_PGN_button, Open_data_button]
    while running == True:
        screen.fill(BACKGROUND)
        Title.draw(screen, "-----Welcome to my chess engine-----")
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