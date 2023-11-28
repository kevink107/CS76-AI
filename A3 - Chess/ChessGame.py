"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

import chess

from AlphaBetaAI import AlphaBetaAI

class ChessGame:
    def __init__(self, player1, player2):
        self.board = chess.Board()
        self.players = [player1, player2]

    def make_move(self):

        player = self.players[1 - int(self.board.turn)]
        move = player.choose_move(self.board)
        self.board.push(move)  # Make the move
        # print(f"\tPlayer's current score: {player.evaluation(self.board)}")

    def is_game_over(self):
        return self.board.is_game_over()

    def __str__(self):

        column_labels = "\n----------------\na b c d e f g h\n"
        board_str =  str(self.board) + column_labels

        # did you know python had a ternary conditional operator?
        move_str = "White to move" if self.board.turn else "Black to move"


        return board_str + "\n" + move_str + "\n"
