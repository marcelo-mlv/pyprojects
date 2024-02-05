import board
import os

FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

test = board.Board(FEN)
test.read_fenstring()

game_over = False
while not game_over:
    game_over = test.new_turn()

print('Game over, right?')
os.system('pause')
