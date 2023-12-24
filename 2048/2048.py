import boardclass
import time
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


def play_game(board, status, endless):
    """
    0: Continue
    1: Loss
    2: Victory
    Endless mode: Keep on playing after victory

    This function calls new turns until its status variable equals 1 (referring to loss) or
    equals 2 (referring to victory, in case it isn't endless already), returning it afterwards.
    It is explained further in the boardclass file.
    """
    game_state = 0
    if endless:
        game_state = 2
    while status == game_state:
        status = board.new_turn(endless)
        if status == game_state:
            os.system("cls")
    return status


print("This is a project based on the game 2048.\n")
print("Use w, a, s, d to move the tiles accordingly.\n")
os.system('pause')

# It's a 4x4 grid by default
game = boardclass.Board(4, 2048)

while True:
    os.system("cls")
    print("Press w, a, s or d and then enter! Das it, probably\n\n")
    game.start_board()

    condition = play_game(game, 0, False)

    if condition == 2:

        print("[ WHAT?? You win? ]")
        time.sleep(2)
        print("[ You actually did it! I'm so proud of you :D ]")
        time.sleep(1)
        print("[ Would you like to continue? Y/N ]")

        ans = get_y_n()
        if ans in ['y', 'Y']:
            os.system('cls')
            print('[ Endless Mode ]\n')
            play_game(game, 2, True)
        else:
            break

    print("[ Game over :( ]\n")
    time.sleep(1)
    print("[ Play again? Y/N ]\n")
    x = get_y_n()
    if x in ['N', 'n']:
        break
