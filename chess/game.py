import chess
import os

FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"

test = chess.Board(FEN)

test.print_board()
test.read_fenstring()
print('\n')
os.system('pause')
