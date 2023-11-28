"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

import random


class ZobristHash:
    def __init__(self):
        self.zobrist_table = [[[random.randint(1, 2**64 - 1) for k in range(12)] for j in range(8)] for i in range(8)]

    def hash(self, board):

        h = 0  # initialize hash value to 0

        # iterate over each square on chess board
        for row in range(8):
            for col in range(8):
                piece = board.piece_at(row * 8 + col)

                # check if square is not empty
                if piece is not None:
                    # retrieve type and color of the piece
                    piece_type = piece.piece_type
                    color = piece.color

                    # calculate index based on piece type and color
                    if color:
                        index = piece_type - 1
                    else:
                        index = piece_type - 1 + 6

                    # XOR-ing hash value with corresponding value from Zobrist table
                    h ^= self.zobrist_table[row][col][index]

        return h

