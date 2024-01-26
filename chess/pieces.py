class Piece:
    def __init__(self, team):
        self.team = team
        self.pos = []
        self.first_move = True

    def setpos(self, newpos):
        self.pos = newpos

    def get_team(self):
        if self.team == 'w':
            return 'White'
        elif self.team == 'b':
            return 'Black'
        else:
            Exception("Piece.get_team: TF is goin on lmao")

    def get_available_moves(self, occupied_pos):
        pass


class King(Piece):
    pass


class Pawn(Piece):
    pass


class Rook(Piece):
    pass


class Knight(Piece):
    pass


class Bishop(Piece):
    pass


class Queen(Piece):
    pass


def generate_new_piece(char, board, pos):
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
        Exception('pieces.get_piece: bruh wat')
    newpiece.setpos(pos)
    board.pieces.append(newpiece)
    return newpiece
