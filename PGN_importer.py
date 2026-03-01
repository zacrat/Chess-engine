import chess.pgn
import chess
from io import StringIO

def scan(path):
    # Scans a PGN file and prints the FEN string of each position in the mainline of the game
    vboard = chess.Board()
    pgn = open(path, 'r')
    pgn_lines = StringIO(pgn.read())
    game = chess.pgn.read_game(pgn_lines)
    for move in game.mainline_moves():
        vboard.push(move)
        print(FEN_to_STR(vboard.fen()))

def FEN_to_STR(fen):
    # Converts a FEN string to a custom string format where empty squares are represented by '#' and pieces are represented by their respective characters (uppercase for white and lowercase for black)
    str_form = ""
    for chr in fen:
        if chr == "/":
            continue
        elif chr == " ":
            break
        elif check_int(chr):
            for _ in range(int(chr)):
                str_form = f"{str_form}#"
        else:
            str_form = str_form + chr.lower() if chr.isupper() else str_form + chr.upper()
    return str_form

def check_int(chr):
    try:
        int(chr)
        return True
    except ValueError:
        return False