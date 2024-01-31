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
    rankindex, fileindex = coord
    fileindex = chr(ord('A') + fileindex)
    rankindex = 8 - int(rankindex)
    return str(fileindex) + str(rankindex)


class Board:
    def __init__(self, fen):
        self.grid = [['·' for _ in range(8)] for _ in range(8)]
        self.fen = fen  # fenstring used to initiate the board
        self.ranks = '8 7 6 5 4 3 2 1'.split()
        self.files = 'A B C D E F G H'
        self.dim = 8  # board dimension
        self.turn = 0  # turn no.
        self.board_pieces = []  # list of Piece objects on the board
        self.captured_pieces = []  # list of captured Piece objects

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
                    self.board_pieces.append(piece)
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
        """
        :return: 2 strings: moving team, opposite team
        """
        if self.turn % 2 == 0:
            return 'White', 'Black'
        return 'Black', 'White'

    def get_pieces_pos(self):
        """
        Creates a list of the current pieces' positions on the board
        :return: list of white pieces' positions, list of black pieces' positions
        """
        whites = []
        blacks = []
        for element in self.board_pieces:
            if element.team == 'w':
                whites.append(element.pos)
            else:
                blacks.append(element.pos)
        return whites, blacks

    def find_piece(self, pos):
        """
        Used for finding a piece given its current position on the board
        """
        for element in self.board_pieces:
            if element.pos == pos:
                return element
        Exception('Couldnt find the piece what')

    def evaluate_check(self):
        """
        Checks if there is a check given the current pieces' positions on the board.
        It appends 'w' or 'b' to the return value as any piece checks throughout the iteration loop
        :return: str list
        """
        w, b = self.get_pieces_pos()

        team_in_check = []
        for element in self.board_pieces:
            _, capturing_squares = element.get_all_moves(w, b)
            for square in capturing_squares:
                attacked_piece = self.find_piece(square)
                if str(type(attacked_piece)) == "<class 'pieces.King'>":
                    if element.team == 'w':
                        team_in_check.append('b')
                    else:
                        team_in_check.append('w')

        return team_in_check

    def get_user_move(self, currentpiece, moving_squares, capturing_squares):
        """
        Gets the input from user and checks if it is a viable piece movement
        :param currentpiece: Current piece that's going to move
        :param moving_squares: List of positions the piece can move to
        :param capturing_squares: List of poistions the piece can capture
        :return: 2-element list of the piece's position with respect to index notation
        """
        original_pos = currentpiece.pos
        team_letter = self.get_color_turn()[0].lower()[0]
        while True:
            inputpos = input()
            while len(inputpos) != 2 or inputpos[0] not in 'A B C D E F G H'.split() or \
                    inputpos[1] not in '1 2 3 4 5 6 7 8'.split():
                print('type it correctly bruh')
                inputpos = input()
            movepos = convert_coords(inputpos)
            if movepos not in moving_squares + capturing_squares:
                print('nahhh cant move it there :/')
                continue

            elif movepos in moving_squares:
                currentpiece.set_pos(movepos)
                if team_letter in self.evaluate_check():
                    print('cant do that, own team is in check')
                    currentpiece.set_pos(original_pos)
                    continue
                break
                
            # elif movepos in capturing_squares:
            else:
                captured_piece = self.find_piece(movepos)
                currentpiece.set_pos(movepos)
                self.board_pieces.remove(captured_piece)
                self.captured_pieces.append(captured_piece)
                if team_letter in self.evaluate_check():
                    print('cant do that, own team is in check')
                    self.board_pieces.append(captured_piece)
                    self.captured_pieces.remove(captured_piece)
                    currentpiece.set_pos(original_pos)
                    continue
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
                break
        return currentpiece, piecepos

    def new_turn(self):
        """
        The main function that handles what happens in a turn of chess
        (moving, capturing, checking, etc)
        """
        color_turn, opposite_color = self.get_color_turn()
        team_letter = color_turn.lower()[0]   # 'w' or 'b'
        enemy_letter = opposite_color.lower()[0]   # 'b' or 'w'

        print('[ {} move ]\n'.format(color_turn))
        self.print_board()
        print('[ Choose a piece by typing its position in the board (i.e. E2, F3, G4) ]\n')

        while True:
            currentpiece, piecepos = self.get_user_pos(team_letter)
            w, b = self.get_pieces_pos()
            moving_squares, capturing_squares = currentpiece.get_all_moves(w, b)

            if not moving_squares + capturing_squares:
                print('[ That piece has nowhere to go, choose another one ]\n')
                continue

            possible_move_exists = False
            original_pos = currentpiece.pos

            for move in moving_squares:
                currentpiece.set_pos(move)
                if team_letter not in self.evaluate_check():
                    possible_move_exists = True
                    break
                currentpiece.set_pos(original_pos)
            currentpiece.set_pos(original_pos)

            for move in capturing_squares:
                captured_piece = self.find_piece(move)
                currentpiece.set_pos(move)
                self.board_pieces.remove(captured_piece)
                self.captured_pieces.append(captured_piece)
                if team_letter not in self.evaluate_check():
                    possible_move_exists = True
                    self.board_pieces.append(captured_piece)
                    self.captured_pieces.remove(captured_piece)
                    currentpiece.set_pos(original_pos)
                    break
                self.board_pieces.append(captured_piece)
                self.captured_pieces.remove(captured_piece)
                currentpiece.set_pos(original_pos)

            if possible_move_exists:
                break
            else:
                print('[ This piece cant stop its own team check ]') if team_letter in self.evaluate_check()\
                    else print('[ This piece is pinned ]')

        os.system('pause')
        os.system('cls')
        print('[ {} move ]\n'.format(color_turn))
        print('[ Chosen piece position:', reconvert_coords(piecepos), ']\n')
        self.print_board()
        print('[ Now type its final position ]\n')
        finalpos = self.get_user_move(currentpiece, moving_squares, capturing_squares)

        temp = copy.deepcopy(self.grid[piecepos[0]][piecepos[1]])
        self.grid[piecepos[0]][piecepos[1]] = '·'
        self.grid[finalpos[0]][finalpos[1]] = temp
        currentpiece.set_first_move(False)

        if finalpos in capturing_squares:
            os.system('cls')
            print('[ {} move ]\n'.format(color_turn))
            print('[ {} capture at {} ]\n'.format(color_turn, reconvert_coords(finalpos)))
            self.print_board()

        if enemy_letter in self.evaluate_check():
            os.system('cls')
            print('[ {} move ]\n'.format(color_turn))
            capture_msg = 'capture, ' if finalpos in capturing_squares else ''
            print('[ {} team {}check ]\n'.format(color_turn, capture_msg))
            self.print_board()

        self.turn += 1
