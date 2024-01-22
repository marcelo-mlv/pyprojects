class Board:
    def __init__(self, fen):
        self.board = [['+' for j in range(8)] for i in range(8)]
        self.fen = fen
        self.files = '1 2 3 4 5 6 7 8'.split()
        self.ranks = 'a b c d e f g h'

    def read_fenstring(self):
        positions = self.fen.split('/')
        
        others = positions[-1].split(' ')
        positions.remove(positions[-1])
        
        positions.append(others[0])
        others.remove(others[0])
        
        # print(self.fen)
        # print('POSITIONS:', positions)
        # print('OTHERS:', others)

    def print_board(self):
        for i in range(8):
            print(self.files[i], end='')
            for j in range(8):
                print(' ', end=self.board[i][j])
            print()
        print(' ', self.ranks, end=' ')
