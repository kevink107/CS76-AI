"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

from AlphaBetaAI import AlphaBetaAI
from MinimaxAI import MinimaxAI


class IterativeDeepeningAI():

    def __init__(self, depth):
        self.depth_limit = depth

    def choose_move(self, board):
        best_move = None
        for depth in range(1, self.depth_limit):
            player = MinimaxAI(depth)
            best_move = player.choose_move(board)

            print(f"Iterative Deepening AI recommending move {best_move}")

        return best_move
