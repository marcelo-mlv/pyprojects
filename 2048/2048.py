import boardclass
import os


print("This is a project based on the game 2048.\n")
print("Use w, a, s, d to move the tiles accordingly.\n")
os.system('pause')

# It's a 4x4 grid by default
game = boardclass.Board(4, 2048)

over = False
while not over:
    os.system("cls")
    print("Press w, a, s or d and then enter! Das it, probably\n\n")
    game.start_board()
    lose = False
    while not lose:
        lose = game.new_turn()
        if not lose:
            os.system("cls")
    print("[ Game over :( ]\n")
    print("[ Continue? Y/N ]\n")
    x = input()
    while x not in ['Y', 'N', 'y', 'n']:
        print("[ It's Y or N bro, come on ]\n")
        x = input()
    if x in ['N', 'n']:
        over = True
