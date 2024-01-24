import pieces


symbols = {'p': '♙', 'P': '♟',
           'b': '♗', 'B': '♝',
           'r': '♖', 'R': '♜',
           'n': '♘', 'N': '♞',
           'q': '♕', 'Q': '♛',
           'k': '♔', 'K': '♚'}


def convert_coords(coord):
    """
    Simple function to convert chess coordinates into array indexing
    for instance, "H4" -> "[4, 7]".
    :return: list containing the converted coordinates
    """
    y, x = coord
    y = ord(y) - ord('A')
    x = 8 - int(x)
    return [x, y]


class Board:
    def __init__(self, fen):
        self.grid = [['·' for _ in range(8)] for _ in range(8)]
        self.fen = fen
        self.ranks = '8 7 6 5 4 3 2 1'.split()
        self.files = 'a b c d e f g h'
        self.dim = 8
        self.turn = 0
        self.pieces = []

    def read_fenstring(self):
        """
        Starting game FEN: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        r, n, b, q, k, p: black pieces (rook, knight, etc)
        R, N, B, Q, K, P: white pieces
        8: 8 empty tiles in the current rank (the whole rank in this case)
        'w': white's turn
        'KQkq': Castling availability
        '-': No En Passant possible
        '0': 0 moves since a pawn moved or a piece was captured
        '1': 1st full move (increases after each black's move)
        """

        positions = self.fen.split('/')

        others = positions[-1].split(' ')
        positions.remove(positions[-1])

        positions.append(others[0])
        others.remove(others[0])

        for rankinfo in positions:
            rankindex = positions.index(rankinfo)
            fileindex = 0
            for char in rankinfo:
                if char.isdigit():
                    num = int(char)
                    fileindex += num
                else:
                    self.grid[rankindex][fileindex] = symbols[char]
                    piece = pieces.get_piece(char, self, [rankindex, fileindex])
                    self.pieces.append(piece)
                fileindex += 1

    def print_board(self):
        for i in range(self.dim):
            print(self.ranks[i], end=' ')
            for j in range(self.dim):
                print(self.grid[i][j], end=' ')
            print()
        print(' ', self.files)
        print()

    def get_color_turn(self):
        if self.turn % 2 == 0:
            return 'White'
        return 'Black'

    def get_pieces_pos(self):
        """
        Creates a list of the current pieces' positions on the board
        :return: list of white pieces' positions, list of black pieces' positions
        """
        whites = []
        blacks = []
        for element in self.pieces:
            if element.team == 'w':
                whites.append(element.pos)
            else:
                blacks.append(element.pos)
        return whites, blacks

    def find_piece(self, pos):
        """
        Used for finding a piece given its current position on the board
        """
        for element in self.pieces:
            if element.pos == pos:
                return element
        Exception('Couldnt find the piece what')

    def new_turn(self):
        color_turn = self.get_color_turn()
        print('[ {} move ]\n'.format(color_turn))
        self.print_board()
        print('Choose a piece by typing its position in the board (i.e. E2, F3, G4)\n\n')

        whitespaces, blackspaces = self.get_pieces_pos()
        piecepos = input()
        while True:
            while len(piecepos) != 2 or piecepos[0] not in 'A B C D E F G H'.split() or\
                    piecepos[1] not in '1 2 3 4 5 6 7 8'.split():
                print('type it correctly bruh')
                piecepos = input()
            inputpos = convert_coords(piecepos)
            if (color_turn[0].lower() == 'w' and inputpos not in whitespaces) or\
                    (color_turn[0].lower() == 'b' and inputpos not in blackspaces):
                print('not an actual piece position :/')
                piecepos = input()
            else:
                currentpiece = self.find_piece(inputpos)
                print(currentpiece, 'chosen')
                break

        self.turn += 1
