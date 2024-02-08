import copy
import os
import time

from utils import symbols, unsymbols, convert_coords, reconvert_coords, generate_new_piece


class Board:

    def __init__(self, fen):
        self.grid = [['·' for _ in range(8)] for _ in range(8)]
        self.fen = fen  # fenstring used to initiate the board
        self.ranks = '8 7 6 5 4 3 2 1'.split()
        self.files = 'A B C D E F G H'
        self.dim = 8  # board dimension
        self.turn = 0  # number of moves in total
        self.halfmoves = 0  # halfmove counter
        self.board_pieces = []  # list of Piece objects on the board
        self.en_passant_pos = '-'  # string that contains the position of the pawn that has just moved two squares

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
        '1': 1st full move (increases after each move from black)
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
                    piece = generate_new_piece(char, [rankindex, fileindex])
                    self.board_pieces.append(piece)
                    fileindex += 1

    def set_fenstring(self):
        fen = ''
        for rank in range(self.dim):
            empty_squares = 0
            for file in range(self.dim):
                symbol = self.grid[rank][file]
                if symbol == '·':
                    empty_squares += 1
                else:
                    if empty_squares != 0:
                        fen += str(empty_squares)
                        empty_squares = 0
                    fen += unsymbols[symbol]
            fen += str(empty_squares) if empty_squares != 0 else ''
            fen += '/' if rank != range(self.dim)[-1] else ' '

        fen += self.get_color_turn()[0].lower()[0] + ' '

        # Castle
        fen += 'KQkq '

        # En passant
        fen += str(self.en_passant_pos.lower()) + ' '

        # Halfmoves
        fen += str(self.halfmoves) + ' '

        # Fullmove formula
        fen += str((self.turn/2+1).__trunc__())

        print('FENSTRING:', fen, end='\n\n')

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
        :param pos: list with two ints
        :return: Piece object, if found.
        """
        for element in self.board_pieces:
            if element.pos == pos:
                return element
        return None

    def evaluate_team_movement(self):
        """
        Checks if there is any legal moves for the team that's not playing in the current turn.
        If there isn't, the game will obviously end, but depending on if the team's king is in check
        it could end either in a checkmate or a stalemate (draw).
        :return: boolean
        """
        _, enemy_color = self.get_color_turn()
        enemy_letter = enemy_color.lower()[0]
        w, b = self.get_pieces_pos()

        for piece in self.board_pieces:
            if piece.team == enemy_letter:
                moving_squares, capturing_squares = piece.get_all_moves(w, b)
                if self.evaluate_possible_move(piece, moving_squares, capturing_squares, enemy_letter):
                    return True
        return False

    def evaluate_check(self):
        """
        Checks if there is a check given the current pieces' positions on the board.
        It appends 'w' or 'b' to the return value as any piece checks throughout the iteration loop
        :return: str list
        """
        team_in_check = []
        w, b = self.get_pieces_pos()

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

    def evaluate_possible_move(self, currentpiece, moving_squares, capturing_squares, team_letter):
        """
        Given a piece and its possible moving/capturing positions, this method evaluates if at least one of its
        moves don't result in a check against its own team. If so, returns True. Otherwise, False, since all its
        moves are illegal.
        It is a pin if its team isn't in check. If not, it means the piece can't stop its own team's current check.
        :return: Boolean
        """
        original_pos = currentpiece.pos

        for move in moving_squares + capturing_squares:
            captured_piece = self.find_piece(move)
            currentpiece.set_pos(move)
            if captured_piece is not None:
                self.board_pieces.remove(captured_piece)

            if team_letter not in self.evaluate_check():
                currentpiece.set_pos(original_pos)
                if captured_piece is not None:
                    self.board_pieces.append(captured_piece)
                return True

            if captured_piece is not None:
                self.board_pieces.append(captured_piece)
            currentpiece.set_pos(original_pos)
        return False

    def evaluate_en_passant(self, currentpiece, en_passant_square):
        """
        Auxiliary function that appends an en passant to the move list if possible
        :param currentpiece: chosen piece that will move in the current turn
        :param en_passant_square: Empty list that may contain a pawn's position if conditions are met
        """
        if str(type(currentpiece)) == "<class 'pieces.Pawn'>":
            eprank, epfile = convert_coords(self.en_passant_pos)  # en passant capturable piece rank/file
            rank, file = currentpiece.pos  # chosen piece's rank/file
            if eprank == rank:
                if epfile == file + 1 or epfile == file - 1:
                    direction = -1 if self.get_color_turn()[0].lower()[0] == 'w' else 1
                    capturepos = [eprank + direction, epfile]
                    en_passant_square.append(capturepos)

    def get_user_move(self, currentpiece, moving_squares, capturing_squares):
        """
        Gets the input from user and checks if it is a legal piece movement,
        already changing its position in the process
        :param currentpiece: Current piece that's going to move
        :param moving_squares: List of positions the piece can move to
        :param capturing_squares: List of poistions the piece can capture
        :return: 2-element list of the piece's position with respect to index notation
        """
        original_pos = currentpiece.pos
        team_letter = self.get_color_turn()[0].lower()[0]
        en_passant_square = []

        if self.en_passant_pos != '-':
            self.evaluate_en_passant(currentpiece, en_passant_square)

        while True:
            inputpos = input()
            while len(inputpos) != 2 or inputpos[0] not in 'A B C D E F G H'.split() or \
                    inputpos[1] not in '1 2 3 4 5 6 7 8'.split():
                print('type it correctly bruh')
                inputpos = input()
            movepos = convert_coords(inputpos)
            if movepos not in moving_squares + capturing_squares + en_passant_square:
                print('nahhh cant move it there :/')
                continue

            elif movepos in moving_squares:
                currentpiece.set_pos(movepos)
                if team_letter in self.evaluate_check():
                    print('cant do that, own team is in check')
                    currentpiece.set_pos(original_pos)
                    continue
                break

            elif movepos in capturing_squares:
                captured_piece = self.find_piece(movepos)  # for en passant, this line is false
                currentpiece.set_pos(movepos)
                self.board_pieces.remove(captured_piece)
                if team_letter in self.evaluate_check():
                    print('cant do that, own team is in check')
                    self.board_pieces.append(captured_piece)
                    currentpiece.set_pos(original_pos)
                    continue
                break

            else:  # En passant
                eprank, epfile = convert_coords(self.en_passant_pos)
                captured_piece = self.find_piece([eprank, epfile])
                currentpiece.set_pos(movepos)
                self.board_pieces.remove(captured_piece)
                if team_letter in self.evaluate_check():
                    print('cant do that, own team is in check')
                    self.board_pieces.append(captured_piece)
                    currentpiece.set_pos(original_pos)
                    continue
                self.grid[eprank][epfile] = '·'
                break

        if str(type(currentpiece)) == "<class 'pieces.Pawn'>" and abs(movepos[0] - original_pos[0]) == 2:
            print(self.en_passant_pos, reconvert_coords(movepos))
            self.en_passant_pos = reconvert_coords(movepos)
        else:
            self.en_passant_pos = '-'

        currentpiece.set_first_move(False)
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
        The main function that the main file calls. It calls every other function, except the read_fenstring one.
        Also prints most of the output messages regarding what's happening in the turn (checking, capturing, moving)
        It also returns whether the game is over or not, that first case happening if there's a checkmate or a stalemate
        :return: Boolean
        """
        game_over = False
        color_turn, opposite_color = self.get_color_turn()
        team_letter = color_turn.lower()[0]   # 'w' or 'b'
        enemy_letter = opposite_color.lower()[0]   # 'b' or 'w'

        print('[ {} team move ]\n'.format(color_turn))
        self.print_board()
        print('[ Choose a piece by typing its position in the board (i.e. E2, F3, G4) ]\n')

        while True:
            currentpiece, piecepos = self.get_user_pos(team_letter)
            w, b = self.get_pieces_pos()
            moving_squares, capturing_squares = currentpiece.get_all_moves(w, b)

            if not moving_squares + capturing_squares:
                print('[ That piece has nowhere to go, choose another one ]\n')
                continue

            if self.evaluate_possible_move(currentpiece, moving_squares, capturing_squares, team_letter):
                break
            else:
                print('[ This piece cant stop its own team check ]') if team_letter in self.evaluate_check()\
                    else print('[ This piece is pinned ]')

        os.system('pause')
        os.system('cls')
        print('[ {} move ]\n'.format(color_turn))
        self.print_board()
        print('[ Chosen piece position:', reconvert_coords(piecepos), ']\n')
        print('[ Now type its final position ]\n')
        finalpos = self.get_user_move(currentpiece, moving_squares, capturing_squares)

        temp = copy.deepcopy(self.grid[piecepos[0]][piecepos[1]])
        self.grid[piecepos[0]][piecepos[1]] = '·'
        self.grid[finalpos[0]][finalpos[1]] = temp

        os.system('cls')
        if not self.evaluate_team_movement():
            if self.evaluate_check():
                print('[ CHECKMATE ]\n')
                time.sleep(1.2)
                print('[ {} wins! ]\n'.format(color_turn))
                self.print_board()
            else:
                print('[ STALEMATE ]\n')
                time.sleep(1.2)
                print("[ It's a Draw! ]\n".format(color_turn))
                self.print_board()
            game_over = True
        else:
            capture_msg = '[ {} team capture at {} ]\n\n'.format(color_turn, reconvert_coords(finalpos))
            check_msg = '[ {} team check ]\n\n'.format(color_turn)
            capture_check_msg = '[ {} team capture at {}, check ]\n\n'.format(color_turn, reconvert_coords(finalpos))

            msg = capture_check_msg if finalpos in capturing_squares and enemy_letter in self.evaluate_check() else \
                capture_msg if finalpos in capturing_squares else check_msg if enemy_letter in self.evaluate_check() \
                else '[ {} team move ]\n\n'.format(color_turn)
            print(msg, end='')
            self.print_board()

        if finalpos in capturing_squares or str(type(currentpiece)) == "<class 'pieces.Pawn'>":
            self.halfmoves = 0
        else:
            self.halfmoves += 1

        self.turn += 1
        os.system('pause')
        os.system('cls')
        self.set_fenstring()
        return game_over
