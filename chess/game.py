import board
import os

FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

test = board.Board(FEN)

test.read_fenstring()

for _ in range(3):
    test.new_turn()
    os.system('pause')
    os.system('cls')
