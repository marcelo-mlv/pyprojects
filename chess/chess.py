symbols = {'p': '♙', 'P': '♟',
           'b': '♗', 'B': '♝',
           'r': '♖', 'R': '♜',
           'n': '♘', 'N': '♞',
           'q': '♕', 'Q': '♛',
           'k': '♔', 'K': '♚'}

class Board:
    def __init__(self, fen):
        self.board = [['·' for j in range(8)] for i in range(8)]
        self.fen = fen
        self.ranks = '8 7 6 5 4 3 2 1'.split()
        self.files = 'a b c d e f g h'

    def read_fenstring(self):
        positions = self.fen.split('/')
        
        others = positions[-1].split(' ')
        positions.remove(positions[-1])
        
        positions.append(others[0])
        others.remove(others[0])
        
        # print(self.fen)
        # print('POSITIONS:', positions)
        # print('OTHERS:', others)

        for rankinfo in positions:
            rankno = positions.index(rankinfo)
            fileindex = 0
            for char in rankinfo:
                if char.isdigit():
                    num = int(char)
                    fileindex += num
                else:
                    self.board[rankno][fileindex] = symbols[char]
                fileindex += 1

    def print_board(self):
        for i in range(8):
            print(self.ranks[i], end=' ')
            for j in range(8):
                print(self.board[i][j], end=' ')
            print()
        print(' ', self.files)
