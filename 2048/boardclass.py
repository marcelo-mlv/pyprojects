import random
import matrix as mt


def get_char():
    char = input()
    while char not in ['w', 'a', 's', 'd']:
        print("[ Nahh, press another key ]\n")
        char = input()
    return char


class Board:

    def __init__(self, size):
        """
        size: grid size
        """
        self.size = size
        self.grid = []

    def print_board(self):
        for row in range(self.size):
            print('[ ', end='')
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    tile = ' '
                else:
                    tile = self.grid[row][col]
                print(tile, end=' ')
                if col != self.size-1:
                    print('-', end=' ')
            print(']')
        print()

    def start_board(self):
        print("[ New game ]\n")
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def merge(self):
        for row in range(self.size):
            for col in range(self.size - 1):
                tile = self.grid[row][col]
                next_tile = self.grid[row][col + 1]
                if tile == next_tile:
                    self.grid[row][col] *= 2
                    self.grid[row][col+1] = 0

    def slide_left(self):
        """
            Since we're interested on sliding all non-zero tiles to the left, this algorithm
            consists in swapping two adjacent tiles when the leftmost is zero and the other
            is different from zero, checking this condition from left to right, and going back
            to the start while there's still changes to be made. It's kinda like bubblesort, actually
        """
        for row in range(self.size):
            changed = True
            while changed:
                changed = False
                for col in range(self.size - 1):
                    tile = self.grid[row][col]
                    next_tile = self.grid[row][col + 1]
                    if tile == 0 and next_tile != 0:
                        changed = True
                        temp = tile
                        self.grid[row][col] = next_tile
                        self.grid[row][col + 1] = temp

    def move_left(self):
        self.slide_left()
        self.merge()

    def move_tiles(self, char):
        """
            Moving Logic: It's easier to program the moving logic to one side only, in this case, left,
            and use some matrix operations (transpose and mirror vertically) in order to move
            to other directions while using the same move-to-the-left code.

            For instance, to move to the right, you can mirror the grid matrix
            vertically, use the move-left code, and mirror it back!
        """
        if char == 'a':
            self.move_left()
        if char == 'w':
            self.grid = mt.transpose(self.grid, self.size)
            self.move_left()
            self.grid = mt.transpose(self.grid, self.size)
        if char == 'd':
            self.grid = mt.mirror(self.grid, self.size)
            self.move_left()
            self.grid = mt.mirror(self.grid, self.size)
        if char == 's':
            self.grid = mt.transpose(self.grid, self.size)
            self.grid = mt.mirror(self.grid, self.size)
            self.move_left()
            self.grid = mt.mirror(self.grid, self.size)
            self.grid = mt.transpose(self.grid, self.size)

    def new_turn(self):
        # Print the board
        self.print_board()

        # Checking if there are empty tiles before a move
        empty_tiles = mt.get_zeros(self.grid, self.size)

        # If there are no empty tiles left (game over)
        if not empty_tiles:
            return True

        # Move the tiles
        char = get_char()
        self.move_tiles(char)

        empty_tiles = mt.get_zeros(self.grid, self.size)
        rndtile = random.choice(empty_tiles)

        # Odds of generating 2: 90%
        # Odds of generating 4: 10%
        num = [2]*9 + [4]
        rndnum = random.choice(num)

        # Place a random number on a random tile
        self.grid[rndtile[0]][rndtile[1]] = rndnum

        return False
