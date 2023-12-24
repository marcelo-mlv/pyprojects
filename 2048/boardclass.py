import random
import matrix as mt
import copy


def get_char(array):
    char = input()
    while char not in array:
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

    def print_board(self, grid):
        for row in range(self.size):
            print('[ ', end='')
            for col in range(self.size):
                if grid[row][col] == 0:
                    tile = ' '
                else:
                    tile = grid[row][col]
                print(tile, end=' ')
                if col != self.size-1:
                    print('-', end=' ')
            print(']')
        print()

    def generate_tile(self, tile_pos):
        """
        Odds of generating 2: 90%
        Odds of generating 4: 10%
        """
        num = [2]*9 + [4]
        rndnum = random.choice(num)

        # Place a random number on a random tile
        self.grid[tile_pos[0]][tile_pos[1]] = rndnum

    def start_board(self):
        print("[ New game ]\n")
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]

        empty_tiles = mt.get_zeros(self.grid, self.size)
        rndtile = random.choice(empty_tiles)
        self.generate_tile(rndtile)

    def merge(self, grid):
        for row in range(self.size):
            for col in range(self.size - 1):
                tile = grid[row][col]
                next_tile = grid[row][col + 1]
                if tile == next_tile:
                    grid[row][col] *= 2
                    grid[row][col+1] = 0

    def slide_left(self, grid):
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
                    tile = grid[row][col]
                    next_tile = grid[row][col + 1]
                    if tile == 0 and next_tile != 0:
                        changed = True
                        temp = tile
                        grid[row][col] = next_tile
                        grid[row][col + 1] = temp

    def move_left(self, grid):
        self.slide_left(grid)
        self.merge(grid)

    def move_tiles(self, grid, char):
        """
            Moving Logic: It's easier to program the moving logic to one side only, in this case, left,
            and use some matrix operations (transpose and mirror vertically) in order to move
            to other directions while using the same move-to-the-left code.

            For instance, to move to the right, you can mirror the grid matrix
            vertically, use the move-left code, and mirror it back!
        """
        if char == 'a':
            self.move_left(grid)
        if char == 'w':
            mt.transpose(grid, self.size)
            self.move_left(grid)
            mt.transpose(grid, self.size)
        if char == 'd':
            mt.mirror(grid, self.size)
            self.move_left(grid)
            mt.mirror(grid, self.size)
        if char == 's':
            mt.transpose(grid, self.size)
            mt.mirror(grid, self.size)
            self.move_left(grid)
            mt.mirror(grid, self.size)
            mt.transpose(grid, self.size)

    def test_moves(self):
        """
            When there are no tiles left (endgame), it's important to see if there are
            any moves available from the merging mechanic. If not, it's game over.

            Thus, this function will clone the current grid and move it in all 4 directions,
            checking if there is any direction that will keep the game going.

            returns the list of possible directions to move.
        """
        available_moves = []
        for direction in ['w', 'a', 's', 'd']:
            grid_clone = copy.deepcopy(self.grid)
            self.move_tiles(grid_clone, direction)
            if grid_clone != self.grid:
                available_moves.append(direction)
        return available_moves

    def new_turn(self):
        # Print the board
        self.print_board(self.grid)

        # Checking if there are empty tiles before a move
        empty_tiles = mt.get_zeros(self.grid, self.size)

        available_directions = self.test_moves()

        # If there are no empty tiles left AND there are no possible moves (game over)
        if not empty_tiles and not available_directions:
            return True

        # Move the tiles
        char = get_char(available_directions)
        self.move_tiles(self.grid, char)

        empty_tiles = mt.get_zeros(self.grid, self.size)
        rndtile = random.choice(empty_tiles)
        self.generate_tile(rndtile)

        return False
