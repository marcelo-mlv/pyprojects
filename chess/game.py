import chess
import os

FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"

test = chess.Board(FEN)

test.read_fenstring()
test.print_board()
print('\n')
os.system('pause')
