import pieces
import copy
import os


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


def reconvert_coords(coord):
    """
    It does the opposite algorithm
    for instance, "[4, 7]" -> "H4".
    :return: list containing the converted coordinates
    """
    fileindex, rankindex = coord
    fileindex = chr(ord('A') + fileindex)
    rankindex = 8 - int(rankindex)
    return str(fileindex) + str(rankindex)


class Board:
    def __init__(self, fen):
        self.grid = [['·' for _ in range(8)] for _ in range(8)]
        self.fen = fen
        self.ranks = '8 7 6 5 4 3 2 1'.split()
        self.files = 'A B C D E F G H'
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
                    piece = pieces.generate_new_piece(char, [rankindex, fileindex])
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

    def get_user_move(self, moving_piece):
        """
        Gets the input from user and checks if it is a viable piece movement
        :param moving_piece: a pointer to the current moving piece
        :return: 2-element list of the piece position with respect to index notation
        """
        inputpos = input()
        w, b = self.get_pieces_pos()
        occupied_squares = w + b
        available_squares = moving_piece.get_available_moves(occupied_squares)
        while True:
            while len(inputpos) != 2 or inputpos[0] not in 'A B C D E F G H'.split() or \
                    inputpos[1] not in '1 2 3 4 5 6 7 8'.split():
                print('type it correctly bruh')
                inputpos = input()
            movepos = convert_coords(inputpos)
            if movepos not in available_squares:
                print('nahhh cant move it there :/')
                inputpos = input()
            else:
                break
        return movepos

    def get_user_pos(self, team):
        """
        Gets the input from user and checks if it is a viable position in the board
        :param team: 'w' or 'b', regarding the current turn
        :return: 2-element list of the piece position with respect to index notation
        """
        whitespaces, blackspaces = self.get_pieces_pos()
        inputpos = input()
        while True:
            while len(inputpos) != 2 or inputpos[0] not in 'A B C D E F G H'.split() or \
                    inputpos[1] not in '1 2 3 4 5 6 7 8'.split():
                print('type it correctly bruh')
                inputpos = input()
            piecepos = convert_coords(inputpos)
            if (team == 'w' and piecepos not in whitespaces) or \
                    (team == 'b' and piecepos not in blackspaces):
                print('not an actual piece position :/')
                inputpos = input()
            else:
                currentpiece = self.find_piece(piecepos)
                print(currentpiece, 'chosen')
                break
        return currentpiece, piecepos

    def new_turn(self):
        """
        The main function that handles what happens in a turn of chess
        (moving, capturing, checking, etc)
        """
        color_turn = self.get_color_turn()
        print('[ {} move ]\n'.format(color_turn))
        self.print_board()
        print('Choose a piece by typing its position in the board (i.e. E2, F3, G4)\n\n')

        currentpiece, piecepos = self.get_user_pos(color_turn.lower()[0])

        os.system('pause')
        os.system('cls')
        print('[ {} move ]\n'.format(color_turn))
        print('Chosen piece position:', reconvert_coords(piecepos))
        self.print_board()
        print('Now type its final position:')
        finalpos = self.get_user_move(currentpiece)

        currentpiece.setpos(finalpos)
        temp = copy.deepcopy(self.grid[piecepos[0]][piecepos[1]])
        self.grid[piecepos[0]][piecepos[1]] = '·'
        self.grid[finalpos[0]][finalpos[1]] = temp

        self.turn += 1
