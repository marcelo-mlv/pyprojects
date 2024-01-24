import pieces


symbols = {'p': '♙', 'P': '♟',
           'b': '♗', 'B': '♝',
           'r': '♖', 'R': '♜',
           'n': '♘', 'N': '♞',
           'q': '♕', 'Q': '♛',
           'k': '♔', 'K': '♚'}


class Board:
    def __init__(self, fen):
        self.board = [['·' for _ in range(8)] for _ in range(8)]
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

        # print(self.fen)
        # print('POSITIONS:', positions)
        # print('OTHERS:', others)

        for rankinfo in positions:
            rankindex = positions.index(rankinfo)
            fileindex = 0
            for char in rankinfo:
                if char.isdigit():
                    num = int(char)
                    fileindex += num
                else:
                    piece = pieces.get_piece(char, self)
                    self.board[rankindex][fileindex] = symbols[char]
                    self.pieces.append(piece)
                fileindex += 1

    def print_board(self):
        for i in range(self.dim):
            print(self.ranks[i], end=' ')
            for j in range(self.dim):
                print(self.board[i][j], end=' ')
            print()
        print(' ', self.files)
        print()

    def get_color_turn(self):
        if self.turn % 2 == 0:
            return 'White'
        return 'Black'

    def new_turn(self):
        color_turn = self.get_color_turn()
        print('[ {} move ]\n'.format(color_turn))
        self.print_board()
        self.turn += 1
