"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

import chess
import time
from math import inf


class AlphaBetaAI2():

    def __init__(self, depth):
        self.depth_limit = depth
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
        best_move_value = float('-inf')
        best_move = None

        # iterate through all legal moves for current board state
        for depth in range(1, self.depth_limit + 1):
            self.depth = depth
            for move in list(board.legal_moves):
                alpha = float('-inf')
                beta = float('inf')

                # apply legal move to the board
                board.push(move)
                # call value method to evaluate current board state
                move_value = self.value(board, self.depth - 1, alpha, beta,False)

                # if new move value > best found value -> update best move
                if move_value > best_move_value:
                    best_move_value = move_value
                    best_move = move

                # revert move to restore original board -> to conduct search on other moves
                board.pop()

        print(f"Alpha-Beta AI2 recommending move {best_move} with value {best_move_value}")
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
    def reorder_moves_advanced(self, board, depth):
        moves = list(board.legal_moves)
        if depth > 1:  # Use the transposition table for depths greater than 1 to avoid overhead at shallow depths
            moves.sort(key=lambda move: self.trans_table.get(board.fen(), 0), reverse=True)
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

        # if cutoff test passes, evaluate current board state
        if self.cutoff_test(board, depth):
            return self.evaluation(board)

        # if current player is maximizing, calls max_value helper function
        if is_maximizer:
            return self.max_value(board, depth, alpha, beta, is_maximizer)
        else:
            return self.min_value(board, depth, alpha, beta, is_maximizer)

    """
    Searches for the move with the highest value for the maximizing player.
    Returns the value of the best move found for the maximizing player.
    """
    def max_value(self, board, depth, alpha, beta, is_maximizer):
        val = float('-inf')
        for move in self.reorder_moves_advanced(board, depth):
            board.push(move)
            val = max(val, self.value(board, depth - 1, alpha, beta, not is_maximizer))
            self.trans_table[board.fen()] = val
            board.pop()
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
        for move in self.reorder_moves_advanced(board, depth):
            board.push(move)
            val = min(val, self.value(board, depth - 1, alpha, beta, not is_maximizer))
            self.trans_table[board.fen()] = val
            board.pop()
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





