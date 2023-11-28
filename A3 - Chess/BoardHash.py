"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

class BoardHash:
    def __init__(self, board):
        self.board = board

    def __hash__(self):
        return hash(str(self.board))

    def __eq__(self, other):
        return str(self.board) == str(other.board)