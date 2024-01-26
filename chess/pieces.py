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
    def get_available_moves(self, occupied_pos):
        if self.team == 'w':
            direction = -1
        else:
            direction = 1
        rankindex, fileindex = self.pos

        move1 = [rankindex + direction, fileindex]
        move2 = [rankindex + 2*direction, fileindex]
        possible_moves = []

        if move1 not in occupied_pos:
            possible_moves.append(move1)
            if move2 not in occupied_pos and self.first_move:
                possible_moves.append(move2)
        self.first_move = False
        return possible_moves


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
