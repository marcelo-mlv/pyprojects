from pieces import Bishop, Pawn, Rook, Knight, King, Queen

symbols = {'p': '♙', 'P': '♟',
           'b': '♗', 'B': '♝',
           'r': '♖', 'R': '♜',
           'n': '♘', 'N': '♞',
           'q': '♕', 'Q': '♛',
           'k': '♔', 'K': '♚'}

unsymbols = {'♙': 'p', '♟': 'P',
             '♗': 'b', '♝': 'B',
             '♖': 'r', '♜': 'R',
             '♘': 'n', '♞': 'N',
             '♕': 'q', '♛': 'Q',
             '♔': 'k', '♚': 'K'}


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


def generate_new_piece(char, pos):
    """
    Generates a new piece on the board.
    It is called before the game starts according to the FEN string characters
    :param char: FEN string char
    :param pos: two element list of the new piece's coordinates
    :return: Piece object
    """
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
        Exception('pieces.generate_new_piece: bruh wat')
    newpiece.set_pos(pos)
    return newpiece


def check_out_of_bounds(pos):
    """
    Checks if a given position on the board is out of bounds
    :param pos: 2-element list
    :return: Boolean
    """
    rankindex, fileindex = pos
    possible_coords = [0, 1, 2, 3, 4, 5, 6, 7]
    if rankindex in possible_coords and fileindex in possible_coords:
        return False
    return True
