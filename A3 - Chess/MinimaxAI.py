"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

import chess
import time


class MinimaxAI():

    def __init__(self, depth):
        self.depth = depth  # max depth of search tree
        self.num_calls = 0  # tracks number of calls to minimax
        self.piece_values = {
            "p": 1,
            "n": 3,
            "b": 3,
            "r": 5,
            "q": 9,
            "k": 1000
        }

    """
    Chooses the best move using minimax algorithm
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

        for move in list(board.legal_moves):
            board.push(move)
            move_value = self.value(board, self.depth - 1, False)
            if move_value > value:
                value = move_value
                best_move = move
            board.pop()

        print(f"Minimax AI recommending move {best_move} with value {value}")
        print(f"\tNodes searched: {self.num_calls}")
        end = time.time()
        print(f"\tTime elapsed: {end - start}")
        self.num_calls = 0  # Reset the counter after search

        return best_move

    """
    Determines whether to call min_value or max_value based on current player
    Params:
    - board: current state of the chess board.
    - depth: current depth in the game tree.
    - is_maximizer: boolean indicating whether current player is maximizing or not.
    Returns:
    - The value of the best move found for the current board state.
    """
    def value(self, board, depth, is_maximizer):
        self.num_calls += 1

        # if cutoff test passes, evaluate current board state
        if self.cutoff_test(board, depth):
            return self.evaluation(board)

        # if current player is maximizing, calls max_value helper function
        if is_maximizer:
            return self.max_value(board, depth, is_maximizer)
        else:
            return self.min_value(board, depth, is_maximizer)

    """
    Searches for the move with the highest value for the maximizing player.
    Returns the value of the best move found for the maximizing player.
    """
    def max_value(self, board, depth, is_maximizer):
        val = float('-inf')

        # iterate over all legal moves to find the one with the highest value
        for move in list(board.legal_moves):
            board.push(move)  # apply move to the board
            # recursive call to evaluate current move
            val = max(val, self.value(board, depth - 1, not is_maximizer))
            board.pop()  # reverts move to restore original board state
        return val

    """
    Searches for the move with the lowest value for the minimizing player.
    Returns the value of the best move found for the minimizing player.
    """
    def min_value(self, board, depth, is_maximizer):
        val = float('inf')

        # iterate over all legal moves to find the one with the lowest value
        for move in list(board.legal_moves):
            board.push(move)  # apply move to the board
            val = min(val, self.value(board, depth - 1, not is_maximizer))
            board.pop()  # revert move to restore original board state
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
    # Example board states
    winning_pos = chess.Board("8/5pk1/8/6Q1/8/8/8/7K w - - 0 1")
    blocking_pos = chess.Board("r1b2rk1/pppp1ppp/2n5/2b1q3/3P4/2P5/PPP2PPP/R1BQKBNR w KQ - 0 1")

    test_depths = [2, 3, 4]  # Depths to evaluate

    positions = {
        "WINNING POSITION": winning_pos,
        "BLOCKING POSITION": blocking_pos
    }

    for name, pos in positions.items():
        print(name)
        print(pos)
        print("\n----------------\na b c d e f g h\n")

        for depth in test_depths:
            print(f"Testing {name.lower()} at depth {depth}:")
            player = MinimaxAI(depth)
            best_move = player.choose_move(pos)
            pos.push(best_move)
            print(f"At depth {depth}, MinimaxAI recommends move: {best_move}, with score {player.evaluation(pos)}")
            pos.pop()
            print("\n")

