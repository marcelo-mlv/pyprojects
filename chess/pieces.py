class Piece:
    def __init__(self, team):
        self.team = team
        self.pos = []
        self.first_move = True

    def setpos(self, newpos):
        """
        Set a new value to the piece's position attribute
        :param newpos: 2-element list
        """
        self.pos = newpos

    def get_available_moves(self, occupied_pos):
        """
        For each piece type, there's a code that calculates
        all possible squares for the piece to move.
        :param occupied_pos: List of all positions occupied by all pieces
        :return: List of all possible piece positions after the move
        """
        pass

    def get_moves_in_direction(self, direction, occupied_pos, possible_moves):
        """
        Auxiliary function to get_available_moves method, used for Bishop, Rook and Queen.
        This method appends squares in a certain direction until it reaches the board limit or reaches another piece.
        For instance, it will search for all squares in the direction [1,0] when the piece is a rook or a queen,
        and [1,1] incase of a bishop.
        :param direction: 2-element list
        :param occupied_pos: list of 2-element lists
        :param possible_moves: list of 2-element lists
        """
        i, j = direction
        x, y = self.pos
        while [x + i, y + j] not in occupied_pos and not check_out_of_bounds([x + i, y + j]):
            possible_moves.append([x + i, y + j])
            i += direction[0]
            j += direction[1]


class King(Piece):
    def get_available_moves(self, occupied_pos):
        possible_moves = []
        x, y = self.pos
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                new_move = [x + i, y + j]
                if new_move not in occupied_pos and not check_out_of_bounds(new_move):
                    possible_moves.append(new_move)
        self.first_move = False
        return possible_moves


class Pawn(Piece):
    def get_available_moves(self, occupied_pos):
        possible_moves = []

        if self.team == 'w':
            direction = -1
        else:
            direction = 1
        rankindex, fileindex = self.pos

        pos1 = [rankindex + direction, fileindex]
        pos2 = [rankindex + 2*direction, fileindex]

        if pos1 not in occupied_pos:
            possible_moves.append(pos1)
            if pos2 not in occupied_pos and self.first_move:
                possible_moves.append(pos2)
        self.first_move = False
        return possible_moves


class Rook(Piece):
    def get_available_moves(self, occupied_pos):
        possible_moves = []
        for direction in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
            self.get_moves_in_direction(direction, occupied_pos, possible_moves)
        self.first_move = False
        return possible_moves


class Knight(Piece):
    def get_available_moves(self, occupied_pos):
        possible_moves = []
        x, y = self.pos

        for direction in [[1, 2], [-1, 2], [1, -2], [-1, -2]]:
            i, j = direction
            pos1 = [x + i, y + j]
            if pos1 not in occupied_pos and not check_out_of_bounds(pos1):
                possible_moves.append(pos1)
            pos2 = [x + j, y + i]
            if pos2 not in occupied_pos and not check_out_of_bounds(pos2):
                possible_moves.append(pos2)

        self.first_move = False
        return possible_moves


class Bishop(Piece):
    def get_available_moves(self, occupied_pos):
        possible_moves = []

        for direction in [[1, 1], [1, -1], [-1, 1], [-1, -1]]:
            self.get_moves_in_direction(direction, occupied_pos, possible_moves)

        self.first_move = False
        return possible_moves


class Queen(Piece):
    def get_available_moves(self, occupied_pos):
        possible_moves = []
        for direction in [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
            self.get_moves_in_direction(direction, occupied_pos, possible_moves)

        self.first_move = False
        return possible_moves


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
    newpiece.setpos(pos)
    return newpiece
