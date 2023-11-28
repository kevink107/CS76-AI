

import chess
import random
import time
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from AlphaBetaAI_TT import AlphaBetaAI_TT
from ChessGame import ChessGame
from AlphaBetaAI2 import AlphaBetaAI2
from IterativeDeepeningAI import IterativeDeepeningAI


# Specify test depths
test_depths = [2, 3, 4]

winning_pos = chess.Board("8/5pk1/8/6Q1/8/8/8/7K w - - 0 1")
blocking_pos = chess.Board("r1b2rk1/pppp1ppp/2n5/2b1q3/3P4/2P5/PPP2PPP/R1BQKBNR w KQ - 0 1")


# Specify test positions
test_positions = [
    chess.Board("8/5pk1/8/6Q1/8/8/8/7K w - - 0 1"),  # Winning position
    chess.Board("r1b2rk1/pppp1ppp/2n5/2b1q3/3P1P2/8/PP4PP/R1BQKBNR w KQ - 0 1"),  # Blocking position
    # Add more positions as needed
]

# Iterate over each depth and position to test MinimaxAI and AlphaBetaAI
for depth in test_depths:
    print(f"Testing at depth {depth}:")

    for position in test_positions:
        print(f"\nInitial Position:\n{position}\n")

        # Test MinimaxAI
        minimax_ai = MinimaxAI(depth)
        minimax_start_time = time.time()
        minimax_move = minimax_ai.choose_move(position.copy())
        minimax_elapsed_time = time.time() - minimax_start_time
        minimax_value = minimax_ai.value(position.copy(), depth, True)
        minimax_nodes = minimax_ai.num_calls

        # Test AlphaBetaAI
        alphabeta_ai = AlphaBetaAI2(depth)
        alphabeta_start_time = time.time()
        alphabeta_move = alphabeta_ai.choose_move(position.copy())
        alphabeta_elapsed_time = time.time() - alphabeta_start_time
        alphabeta_value = alphabeta_ai.value(position.copy(), depth, float('-inf'), float('inf'), True)
        alphabeta_nodes = alphabeta_ai.num_calls

        # Print results
        print(
            f"MinimaxAI Move: {minimax_move}, Value: {minimax_value}, Time Elapsed: {minimax_elapsed_time}s")
        print(
            f"AlphaBetaAI Move: {alphabeta_move}, Value: {alphabeta_value}, Time Elapsed: {alphabeta_elapsed_time}s")

    print("--------------------")
