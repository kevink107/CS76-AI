# pip3 install python-chess


import chess
import random
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from AlphaBetaAI_TT import AlphaBetaAI_TT
from AlphaBetaAI2 import AlphaBetaAI2
from ChessGame import ChessGame
import time


import sys

random.seed(1)

overall_start = time.time()

player1 = AlphaBetaAI2(2)
# player1 = RandomAI()
# player1 = MinimaxAI(3)
# player1 = AlphaBetaAI_TT(2)
player2 = RandomAI()

game = ChessGame(player1, player2)

while not game.is_game_over():
    print(game)
    game.make_move()

overall_end = time.time()

print(f"Total Gametime: {overall_end - overall_start}")
# print(hash(str(game.board)))


# Function to test MinimaxAI vs. AlphaBetaAI
def test_ais(board):
    depth = 2  # You can change the depth as needed

    minimax_ai = MinimaxAI(depth)
    alphabeta_ai = AlphaBetaAI(depth)

    # Get the move and value from MinimaxAI
    minimax_move = minimax_ai.choose_move(board.copy())
    minimax_value = minimax_ai.evaluation(board.copy())

    # Get the move and value from AlphaBetaAI
    alphabeta_move = alphabeta_ai.choose_move(board.copy())
    alphabeta_value = alphabeta_ai.evaluation(board.copy())

    # Print the results
    print(f"Minimax move: {minimax_move}, value: {minimax_value}")
    print(f"AlphaBeta move: {alphabeta_move}, value: {alphabeta_value}")

    # Compare the moves and values
    assert minimax_move == alphabeta_move, "Moves are different!"
    assert minimax_value == alphabeta_value, "Values are different!"

    print("Both algorithms returned the same move and value. Test passed!")


# Test the AIs with a series of board states
# test_ais(chess.Board())
