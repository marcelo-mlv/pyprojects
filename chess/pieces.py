class Piece:
    def __init__(self, team):
        self.team = team  # string: 'w' or 'b'
        self.pos = []  # current position on the board
        self.moving_squares = []  # list of positions the piece can move to without capturing
        self.capturing_squares = []  # list of positions the piece can capture
        self.first_move = True

    def set_pos(self, newpos):
        """
        Set a new value to the piece's position attribute
        :param newpos: 2-element list
        """
        self.pos = newpos

    def get_all_moves(self, white_places, black_places):
        """
        For each piece type, there's a code that calculates
        all possible squares for the piece to move.
        :param black_places: List of all positions occupied by black pieces
        :param white_places: List of all positions occupied by white pieces
        :return: moving_squares, capturing_squares
        """
        pass

    def get_moves_in_direction(self, direction, occupied_places, enemy_team_places):
        """
        Auxiliary function to get_all_moves method, used for Bishop, Rook and Queen.
        This method appends squares in a certain direction until it reaches the board limit or reaches another piece.
        For instance, it will search for all squares in the direction [1,0] when the piece is a rook or a queen,
        and [1,1] incase of a bishop.
        :param direction: 2-element list
        :param occupied_places: List of all positions occupied by all pieces
        :param enemy_team_places: List of all positions occupied by the enemy pieces
        """
        i, j = direction
        x, y = self.pos
        if [x + i, y + j] in enemy_team_places:
            self.capturing_squares.append([x + i, y + j])
        while [x + i, y + j] not in occupied_places and not check_out_of_bounds([x + i, y + j]):
            self.moving_squares.append([x + i, y + j])
            i += direction[0]
            j += direction[1]
            if [x + i, y + j] in enemy_team_places:
                self.capturing_squares.append([x + i, y + j])

    def get_enemy_team_places(self, white_places, black_places):
        """
        Simple method to get all enemy pieces' positions
        :param white_places: List of all positions occupied by white pieces
        :param black_places: List of all positions occupied by black pieces
        :return: List of all positions occupied by enemy pieces
        """
        if self.team == 'w':
            return black_places
        return white_places


class King(Piece):
    def get_all_moves(self, white_places, black_places):
        occupied_places = white_places + black_places
        self.moving_squares = []
        self.capturing_squares = []
        enemy_team_places = self.get_enemy_team_places(white_places, black_places)
        x, y = self.pos
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                new_move = [x + i, y + j]
                if new_move not in occupied_places and not check_out_of_bounds(new_move):
                    self.moving_squares.append(new_move)
                if new_move in enemy_team_places:
                    self.capturing_squares.append(new_move)

        self.first_move = False
        return self.moving_squares, self.capturing_squares


class Pawn(Piece):
    def get_all_moves(self, white_places, black_places):
        occupied_places = white_places + black_places
        self.moving_squares = []
        self.capturing_squares = []
        enemy_team_places = self.get_enemy_team_places(white_places, black_places)

        if self.team == 'w':
            direction = -1
        else:
            direction = 1
        rankindex, fileindex = self.pos

        new_move1 = [rankindex + direction, fileindex]
        new_move2 = [rankindex + 2 * direction, fileindex]

        if new_move1 not in occupied_places:
            self.moving_squares.append(new_move1)
            if new_move2 not in occupied_places and self.first_move:
                self.moving_squares.append(new_move2)

        for i in [1, -1]:
            new_move = [rankindex + direction, fileindex + i]
            if new_move in enemy_team_places:
                self.capturing_squares.append(new_move)

        self.first_move = False
        return self.moving_squares, self.capturing_squares


class Rook(Piece):
    def get_all_moves(self, white_places, black_places):
        self.moving_squares = []
        self.capturing_squares = []
        occupied_places = white_places + black_places
        enemy_team_places = self.get_enemy_team_places(white_places, black_places)

        for direction in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
            self.get_moves_in_direction(direction, occupied_places, enemy_team_places)

        self.first_move = False
        return self.moving_squares, self.capturing_squares


class Knight(Piece):
    def get_all_moves(self, white_places, black_places):
        self.moving_squares = []
        self.capturing_squares = []
        occupied_places = white_places + black_places
        enemy_team_places = self.get_enemy_team_places(white_places, black_places)
        x, y = self.pos

        for direction in [[1, 2], [-1, 2], [1, -2], [-1, -2], [2, 1], [-2, 1], [2, -1], [-2, -1]]:
            i, j = direction
            new_move = [x + i, y + j]
            if new_move not in occupied_places and not check_out_of_bounds(new_move):
                self.moving_squares.append(new_move)
            if new_move in enemy_team_places:
                self.capturing_squares.append(new_move)

        self.first_move = False
        return self.moving_squares, self.capturing_squares


class Bishop(Piece):
    def get_all_moves(self, white_places, black_places):
        self.moving_squares = []
        self.capturing_squares = []
        occupied_places = white_places + black_places
        enemy_team_places = self.get_enemy_team_places(white_places, black_places)

        for direction in [[1, 1], [1, -1], [-1, 1], [-1, -1]]:
            self.get_moves_in_direction(direction, occupied_places, enemy_team_places)

        self.first_move = False
        return self.moving_squares, self.capturing_squares


class Queen(Piece):
    def get_all_moves(self, white_places, black_places):
        self.moving_squares = []
        self.capturing_squares = []
        enemy_team_places = self.get_enemy_team_places(white_places, black_places)

        occupied_places = white_places + black_places
        for direction in [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
            self.get_moves_in_direction(direction, occupied_places, enemy_team_places)

        self.first_move = False
        return self.moving_squares, self.capturing_squares


def check_out_of_bounds(pos):
    """
    Checks if a given position on the board is out of bounds
    :param pos: 2-element list
    :return: Boolean
    """
    rankindex, fileindex = pos
    possible_coords = [0, 1, 2, 3, 4, 5, 6, 7]
    if rankindex in possible_coords and fileindex in possible_coords:
        return False
    return True


def generate_new_piece(char, pos):
    """
    Generates a new piece on the board.
    It is called before the game starts according to the FEN string characters
    :param char: FEN string char
    :param pos: two element list of the new piece's coordinates
    :return: Piece object
    """
    newpiece = None
    if char == 'b':
        newpiece = Bishop('b')
    elif char == 'B':
        newpiece = Bishop('w')
    elif char == 'p':
        newpiece = Pawn('b')
    elif char == 'P':
        newpiece = Pawn('w')
    elif char == 'r':
        newpiece = Rook('b')
    elif char == 'R':
        newpiece = Rook('w')
    elif char == 'n':
        newpiece = Knight('b')
    elif char == 'N':
        newpiece = Knight('w')
    elif char == 'k':
        newpiece = King('b')
    elif char == 'K':
        newpiece = King('w')
    elif char == 'q':
        newpiece = Queen('b')
    elif char == 'Q':
        newpiece = Queen('w')
    else:
        Exception('pieces.generate_new_piece: bruh wat')
    newpiece.set_pos(pos)
    return newpiece
