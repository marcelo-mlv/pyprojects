import boardclass
import os


def get_y_n():
    """
    A simple function that receives an input and returns it
    """
    char = input()
    while char not in ['Y', 'N', 'y', 'n']:
        print("[ It's Y or N bro, come on ]\n")
        char = input()
    return char


print("This is a project based on the game 2048.\n")
print("Use w, a, s, d to move the tiles accordingly.\n")
os.system('pause')

# It's a 4x4 grid by default
game = boardclass.Board(4, 2048)

while True:
    os.system("cls")
    print("Press w, a, s or d and then enter! Das it, probably\n\n")
    game.start_board()
    lose = False
    while not lose:
        lose = game.new_turn()
        if not lose:
            os.system("cls")
    print("[ Game over :( ]\n")
    time.sleep(1)
    print("[ Play again? Y/N ]\n")
    x = get_y_n()
    if x in ['N', 'n']:
        break
