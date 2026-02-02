import chess.pgn
import chess
from io import StringIO

def scan(path):
    vboard = chess.Board()
    pgn = open(path, 'r')
    pgn_lines = StringIO(pgn.read())
    game = chess.pgn.read_game(pgn_lines)
    for number, move in enumerate(game.mainline_moves()):
        vboard.push(move)
        print(FEN_to_STR(vboard.fen()))

def FEN_to_STR(fen):
    str_form = ""
    for chr in fen:
        if chr == "/":
            continue
        elif chr == " ":
            break
        elif check_int(chr):
            for num in range(int(chr)):
                str_form = str_form + "#"
        else:
            if chr.isupper():
                str_form = str_form + chr.lower()
            else:
                str_form = str_form + chr.upper()
    return str_form
def check_int(chr):
    try:
        int(chr)
        return True
    except ValueError:
        return False