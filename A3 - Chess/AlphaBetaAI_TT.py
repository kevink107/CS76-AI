"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

import chess
import time
from math import inf
from BoardHash import BoardHash
from ZobristHash import ZobristHash
from AlphaBetaAI import AlphaBetaAI

use_reorder_func = True
use_zobrist_hash = False

class AlphaBetaAI_TT():

    def __init__(self, depth):
        self.depth = depth  # max depth of search tree
        self.num_calls = 0  # tracks number of calls to minimax
        self.trans_table = {}
        self.piece_values = {
            "p": 1,
            "n": 3,
            "b": 3,
            "r": 5,
            "q": 9,
            "k": 1000
        }
        self.zobrist_hash = ZobristHash()

    """
    Chooses the best move using alpha-beta pruning algorithm
    Params:
    - board: current chess board state
    Returns: 
    - The best move determined by the AI
    """
    def choose_move(self, board):
        start = time.time()
        self.turn = board.turn  # current player's turn
        value = float('-inf')
        best_move = None

        # iterate through all legal moves for current board state
        for move in list(board.legal_moves):
            alpha = float('-inf')
            beta = float('inf')

            # apply legal move to the board
            board.push(move)
            # call value method to evaluate current board state
            move_value = self.value(board, self.depth - 1, alpha, beta,False)

            # if new move value > best found value -> update best move
            if move_value > value:
                value = move_value
                best_move = move

            # revert move to restore original board -> to conduct search on other moves
            board.pop()

        if use_zobrist_hash:
            print(f"AlphaBetaAI_TT (using Zobrist) recommending move {best_move} with value {value}")
        else:
            print(f"AlphaBetaAI_TT recommending move {best_move} with value {value}")

        print(f"\tNodes searched: {self.num_calls}")

        end = time.time()
        print(f"\tTime elapsed: {end - start}")

        self.num_calls = 0  # Reset the counter after each search

        return best_move

    """
    Reorders moves to give priority to capturing moves
    Params:
    - board: current state of the chess board.
    - moves: list of legal moves 
    Returns:
    - Reordered list of legal moves
    """
    def reorder_moves(self, board, moves):
        for move in moves:
            if board.is_capture(move):
                moves.insert(0, moves.pop(moves.index(move)))
        moves.reverse()
        return moves

    """
    Determines whether to call min_value or max_value based on current player
    Params:
    - board: current state of the chess board.
    - depth: current depth in the game tree.
    - is_maximizer: boolean indicating whether current player is maximizing or not.
    Returns:
    - The value of the best move found for the current board state.
    """
    def value(self, board, depth, alpha, beta, is_maximizer):
        self.num_calls += 1

        board_hash = None
        if use_zobrist_hash:
            board_hash = self.zobrist_hash.hash(board)
        else:
            board_hash = BoardHash(board)

        if board_hash in self.trans_table and depth in self.trans_table[board_hash]:
            return self.trans_table[board_hash][depth]

        # if cutoff test passes, evaluate current board state
        if self.cutoff_test(board, depth):
            return self.evaluation(board)

        # if current player is maximizing, calls max_value helper function
        if is_maximizer:
            val = self.max_value(board, depth, alpha, beta, is_maximizer)
        else:
            val = self.min_value(board, depth, alpha, beta, is_maximizer)

        if board_hash not in self.trans_table:
            self.trans_table[board_hash] = {}
        self.trans_table[board_hash][depth] = val

        return val

    """
    Searches for the move with the highest value for the maximizing player.
    Returns the value of the best move found for the maximizing player.
    """
    def max_value(self, board, depth, alpha, beta, is_maximizer):
        val = float('-inf')
        moves = list(board.legal_moves)

        if use_reorder_func:
            legal_moves = self.reorder_moves(board, moves)
        else:
            legal_moves = moves

        # iterate over all legal moves to find the one with the highest value
        for move in legal_moves:
            board.push(move)  # apply move to the board

            # recursive call to evaluate current move
            val = max(val, self.value(board, depth - 1, alpha, beta, not is_maximizer))
            board.pop()  # reverts move to restore original board state

            # performs beta cut-off if value is >= beta
            if val >= beta:
                return val
            alpha = max(alpha, val)

        return val

    """
    Searches for the move with the lowest value for the minimizing player.
    Returns the value of the best move found for the minimizing player.
    """
    def min_value(self, board, depth, alpha, beta, is_maximizer):
        val = float('inf')
        moves = list(board.legal_moves)

        if use_reorder_func:
            legal_moves = self.reorder_moves(board, moves)
        else:
            legal_moves = moves

        # iterate over all legal moves to find the one with the lowest value
        for move in legal_moves:
            board.push(move)  # apply move to the board
            val = min(val, self.value(board, depth - 1, alpha, beta, not is_maximizer))
            board.pop()  # revert move to restore original board state

            # performs alpha cut-off if value is <= alpha
            if val <= alpha:
                return val
            beta = min(beta, val)

        return val

    """
    Tests whether the search should be cut off - if max depth is reached or game is over
    Returns boolean indicating whether the search should be cut off
    """
    def cutoff_test(self, board, depth):
        return depth == 0 or board.is_game_over()

    """
    Evaluates and returns current board state
    """
    def evaluation(self, board):
        score = 0  # initializes score

        # if current state is checkmate
        if board.is_checkmate():
            if board.turn != self.turn:
                score += self.piece_values["k"]
            else:
                score -= self.piece_values["k"]

        else:
            pieces = board.piece_map()  # map of pieces on chessboard

            # iterate over pieces to calculate values
            for piece in pieces.values():
                value = self.piece_values[str(piece).lower()]
                if piece.color == self.turn:
                    score += value
                else:
                    score -= value
        return score


if __name__ == "__main__":
    test_depths = [2, 3, 4]  # Adjust these depths as needed

    winning_position = chess.Board("8/5pk1/8/6Q1/8/8/8/7K w - - 0 1")
    blocking_position = chess.Board("r1b2rk1/pppp1ppp/2n5/2b1q3/3P1P2/8/PP4PP/R1BQKBNR w KQ - 0 1")

    positions = {
        "WINNING POSITION": winning_position,
        "BLOCKING POSITION": blocking_position
        # Add more positions as needed with the format "POSITION NAME": board
    }

    for position_name, position in positions.items():
        print(position_name)
        print(position)
        print("\n----------------\na b c d e f g h\n")

        for depth in test_depths:
            print(f"Testing {position_name.lower()} at depth {depth}:")

            # Test AlphaBetaAI
            alphabeta_ai = AlphaBetaAI(depth)
            alphabeta_move = alphabeta_ai.choose_move(position.copy())
            alphabeta_nodes = alphabeta_ai.num_calls

            # Test AlphaBetaAI_TT
            alphabeta_tt_ai = AlphaBetaAI_TT(depth)
            alphabeta_tt_move = alphabeta_tt_ai.choose_move(position.copy())
            alphabeta_tt_nodes = alphabeta_tt_ai.num_calls

            position.push(alphabeta_move)  # Example with AlphaBetaAI; replace with AlphaBetaAI_TT as needed
            print(
                f"AlphaBetaAI Move: {alphabeta_move}, Evaluation: {alphabeta_ai.evaluation(position)}")
            position.pop()

            position.push(alphabeta_tt_move)  # Example with AlphaBetaAI_TT; replace with AlphaBetaAI as needed
            print(
                f"AlphaBetaAI_TT Move: {alphabeta_tt_move}, Evaluation: {alphabeta_tt_ai.evaluation(position)}")
            position.pop()

            # Demonstrate transposition table usage
            print(f"Transposition Table Entries: {len(alphabeta_tt_ai.trans_table)}")
            print("\n")

        print("--------------------")
