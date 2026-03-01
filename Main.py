import Game
import Engine
import pygame
import sys
import threading
import UI
import PGN_importer
import itertools
import os
import tkinter as tk
from tkinter import messagebox

white = Engine.Sides.WhiteSide()
black = Engine.Sides.BlackSide()
white.enemy = black
black.enemy = white

def game_loop(game):
    # run the game engine loop until game ends
    while game.ongoing:
        game.play()

def play_game():
    screen.fill((25,51,0)) # Draws chess board background before game loop starts, to avoid white screen when loading the game
    # initialisation of all necessary variables for the game loop
    Start = Game.Game(white, 3)
    flipped = Start.bot.side == white
    if Start.bot.side == white:
        flipped = True
    # Creates game loop threas and starts it
    game_thread = threading.Thread(target=game_loop, args=(Start,), daemon=True)
    game_thread.start()

    #Variables for square seleciton from user input and possible moves for the selected piece
    selected_square = None
    possible_moves = []

    while Start.ongoing:
        cur_pos = Start.curPos #Keeps it updated with the game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Flip_button.is_clicked(event):
                    # Flag for signalling that when the board is next drawn, the pieces should be drawn flipped. Does not actually flip the board, just the coordinates of pieces and moves when drawn and when user clicks on them.
                    flipped = not flipped 
                if Home_button.is_clicked(event):
                    # Returns to main menu and terminates the game loop
                    game_thread.join()
                    return
                
                # Handles user mouse input
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Converts mouse coordinates to board coordinates, and accounts for flipped board
                col = (mouse_x // SQUARE_SIZE)
                row = (mouse_y // SQUARE_SIZE) 
                move_found = False

                #This loop checks if the user has clicked on a possible move for the currently selected piece
                for move in possible_moves:
                    from_pos = (7-selected_square[0], 7-selected_square[1]) if flipped else (selected_square[0], selected_square[1])
                    # For castling moves
                    if len(move) > 2:# [What rook to move, Where to move the king, Where to move the rook] 
                        board_move = [7-move[1][0],7-move[1][1]] if flipped else move
                        if board_move == [row, col]:                
                            # Queues the move for the game loop to process, and accounts for flipped board
                            Start.player_queue.put((move[0], move[1], move[2], from_pos))
                            selected_square = None
                            possible_moves = []
                            move_found = True
                            break
                    else:
                        board_move = [7-move[0],7-move[1]] if flipped else move
                        if board_move == [row,col]:
                            to_pos = (7-row,7-col) if flipped else (row,col)
                            # Queues the move for the game loop to process, and accounts for flipped board
                            Start.player_queue.put((from_pos, to_pos))
                            selected_square = None
                            possible_moves = []
                            move_found = True
                            break 
                if move_found:
                    break
                if [row, col] == selected_square:
                    # QOL, used to unselect a square by clocking on it again.
                    selected_square = None
                    possible_moves = []
                else:
                    # Simply to select a square
                    selected_square = [row, col]
                    possible_moves = []
        for row, col in itertools.product(range(8), range(8)):
            #Gets the text symbol for the piece on the current square, and accounts for flipped board
            symbol = (
                cur_pos[7 - row][7 - col].__str__()
                if flipped
                else cur_pos[row][col].__str__()
            )
            text = font.render(symbol, True, (0, 0, 0))
            if [row, col] == selected_square:
                # Draws a red square on the selected piece, and green circles on the possible moves for that piece
                color = (255, 0, 0)
                board = Start.curPos
                if flipped:piece = board[7-row][7-col]
                else: piece = board[row][col]
                if isinstance(piece, Engine.Pieces.piece) and piece.colour != Start.bot.side:
                    possible_moves = piece.posMove # Gets the possible moves for the selected piece, to be drawn as green circles on the board and to check if the user clicks on them
            else:
                # Draws the normal chess board pattern
                color = LIGHT if (row + col) % 2 == 0 else DARK
            # Draws the square and the piece on it
            pygame.draw.rect( screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            screen.blit(text,(col * SQUARE_SIZE + SQUARE_SIZE // 4,row * SQUARE_SIZE + SQUARE_SIZE // 8))

        for move in possible_moves:
            #Draws each possible move of selected piece with a green circle.
            r, c = move[1] if len(move) > 2 else move
            if flipped:
                r = 7-r
                c = 7-c
            pygame.draw.circle(screen,  (0, 255, 0),(c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2),SQUARE_SIZE // 4)
        
        # All info relevant to the game, to be drawn.
        info = [
            f"Bot depth : {str(Start.bot.Depth.depth)}",
            f"Date : {str(Start.date)}",
            f"Time : {str(Start.time)}",
            f"Turn : {str(Start.turn)}",
            f"Player side : {str(Start.GenBot.side)}",
            "Bot progress : "
            + str(Start.bot.Depth.boards_analysed)
            + " / "
            + str(Start.bot.Depth.board_count),
        ]
        # Draws the menu UI on the right side of the screen, and updates it with game info
        Flip_button.draw(screen)
        Home_button.draw(screen)
        INFO_BOX.draw(screen, info)

        #updates the display and ticks the clock for the next frame
        pygame.display.flip()
        clock.tick(60)
    end = True
    # Draws a box that symbolises the end of the game and whatever the result may be.
    end_menu = UI.TextBox(res_w//4,res_h//4,res_w//2,res_h//2,"", (64,67,81), font_console)
    Home_button_end = UI.button(None, (res_w//4)+20, (res_h//4)+180, (res_w//2) - 40, 120, "Return to the Main menu")
    if Start.winner != Start.bot.side:
        bot_activity = font_console.render("You have won,\nthe engine is learning...", True, (0, 0, 152))
    else:
        bot_activity = font_console.render("The engine has won", True, (152, 0, 0))
    while end:
        # Draws the end game menu and handles user input to return to the main menu, and also displays whether the player won or lost.
        end_menu.draw(screen, None)
        Home_button_end.draw(screen)
        screen.blit(bot_activity,((res_w//4)+20, (res_h//4)+50))
        #handle user input for end game menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Stops the user if the engine is still learning, to avoid them losing the data from the game they just played, and asks if they are sure they want to exit.
                root = tk.Tk()
                root.withdraw()
                res=messagebox.askquestion('Exit Application', 'The engine is currently analysing the game, do you wish to exit?')
                if res == 'yes':
                    sys.exit()
                root.destroy()
            if Home_button.is_clicked(event):
                #Stops the user if the engine is still learning.
                root = tk.Tk()
                root.withdraw()
                res=messagebox.askquestion('Exit Application', 'The engine is currently analysing the game, do you wish to exit?')
                if res == 'yes':
                    return
                root.destroy()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.display.flip()
        clock.tick(60)
def pgn_import():
    # let user choose a PGN file and scans all positions from it
    path = UI.choose_file()
    if path:
        PGN_importer.scan(path)

def open_data():
    # open the training data log in default text editor
    path = "App_data\Data.txt"
    os.startfile(path)
#colours
LIGHT = (240, 217, 181)
DARK  = (181, 136, 99)
BACKGROUND = (14,14,74)
#screen initialisation
pygame.init()
res_h = 720
res_w = 1280
pygame.display.set_caption("Chess Engine")
screen = pygame.display.set_mode((res_w, res_h))
SQUARE_SIZE = 720 // 8 # Size of each square on the chessboard. Rest of the screen for menu UI at 720px right.
clock = pygame.time.Clock()  
#fonts
font = pygame.font.SysFont("Segoe UI Symbol", 56)
font_console = pygame.font.SysFont("console", 34)
# Buttons for menu UI
Start_button = UI.button(play_game, 100, 120, 200, 75, "Play Game")
Import_PGN_button = UI.button(pgn_import, 100, 220, 200, 75, "Import PGN")
Open_data_button = UI.button(open_data, 100, 320, 200, 75, "Open training data")
Exit_button = UI.button(sys.exit, 100, 460, 200, 75, "Exit")
Flip_button = UI.button(None,740,330, 500, 50,"Flip board")
Home_button = UI.button(None,740,400, 500, 50,"Home")
#Menu UI
INFO_BOX = UI.TextBox(740,60,500,250,"Game details",(120,120,120),font_console)
Title = UI.TextBox(res_w//8, res_h//32, res_w//(8/6), 80, "", (255,255,255), font)

def main():
    # entry point for main menu loop
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
if __name__ == "__main__":
    main()