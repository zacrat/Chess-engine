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
def STR_to_FEN(string):
    fen_form = ""
    count=0
    curr_streak = 0
    for chr in string:
        if count == 8:
            if curr_streak>0:
                fen_form = fen_form + str(curr_streak)
                curr_streak = 0
            fen_form = fen_form + "/"
            count = 0 
        if chr == "#":
            curr_streak += 1
        elif chr != "#":
            if curr_streak > 0:
                fen_form = fen_form + str(curr_streak)
                curr_streak = 0
            if chr.isupper():
                fen_form = fen_form + chr.lower()
            else:
                fen_form = fen_form + chr.upper()
        count+=1
    return fen_form

def check_int(chr):
    try:
        int(chr)
        return True
    except ValueError:
        return False