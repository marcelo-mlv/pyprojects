class Piece:
    def __init__(self, team):
        self.team = team

    def get_team(self):
        if self.team == 'w':
            return 'White'
        elif self.team == 'b':
            return 'Black'
        else:
            Exception("Piece.get_team: TF is goin wrong lmao")

    def get_available_moves(self):
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


def get_piece(char, board):
    board.pieces.append(piecedict[char])


piecedict = {'p': Pawn('b'), 'P': Pawn('w'),
             'b': Bishop('b'), 'B': Bishop('w'),
             'r': Rook('b'), 'R': Rook('w'),
             'n': Knight('b'), 'N': Knight('w'),
             'q': Queen('b'), 'Q': Queen('w'),
             'k': King('b'), 'K': King('w')}
