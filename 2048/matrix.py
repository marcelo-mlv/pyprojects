"""
For all functions here:
    mat: matrix argument
    n: matrix size
"""


def get_zeros(mat, n):
    zero_tiles = []
    for row in range(n):
        for tile in range(n):
            if mat[row][tile] == 0:
                zero_tiles.append([row, tile])
    return zero_tiles


def transpose(mat, n):
    for i in range(n):
        for j in range(i):
            tile = mat[i][j]
            trans_tile = mat[j][i]
            temp = tile
            mat[i][j] = trans_tile
            mat[j][i] = temp


def mirror(mat, n):
    for i in range(n):
        for j in range(int(n / 2)):
            tile = mat[i][j]
            mirror_tile = mat[i][n - 1 - j]
            temp = tile
            mat[i][j] = mirror_tile
            mat[i][n - 1 - j] = temp
