"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

from SAT import SAT


class NQueensProblem:
    def __init__(self, size):
        self.size = size  # size of the chess board (NxN board)

    '''
    Sets up the N-Queens problem in conjunctive normal form (CNF) and writes the clauses to a file.
    '''
    def setup_problem(self, output_file):

        clauses = []  # list to store the clauses representing the N-Queens problem

        # ensure that each row and column contains at least one queen
        for x in range(self.size):
            row, col = [], []
            for y in range(self.size):
                row.append(f"{x}{y}")  # literal for queen in row position
                col.append(f"{y}{x}")  # literal for queen in column position
            clauses.append(" ".join(row))
            clauses.append(" ".join(col))

        # ensure that no two queens are in the same row or column
        for x in range(self.size):
            for y in range(self.size):
                for z in range(y + 1, self.size):
                    clauses.append(f"-{x}{y} -{x}{z}")  # no two queens in the same row
                    clauses.append(f"-{y}{x} -{z}{x}")  # no two queens in the same column

        # ensure that no two queens are on the same diagonal
        for x in range(self.size):
            for y in range(self.size):
                for z in range(1, self.size):
                    # check diagonals to the left.
                    if x + z < self.size and y - z >= 0:
                        clauses.append(f"-{x}{y} -{x+z}{y-z}")
                    # check diagonals to the right.
                    if x + z < self.size and y + z < self.size:
                        clauses.append(f"-{x}{y} -{x+z}{y+z}")

        # write all generated clauses to the output file
        with open(output_file, "w") as f:
            f.write("\n".join(clauses))

    '''
    Reads the solution file produced by the SAT solver and 
    displays the board with queens placed accordingly.
    '''
    def display_solution(self, solution_file):

        positions = set()  # set to store the positions of the queens

        # read the solution file and extract queen positions
        with open(solution_file, "r") as f:
            for line in f:
                if not line.startswith('-'):
                    positions.add((int(line[0]), int(line[1])))

        # display the board
        board = ""
        for y in reversed(range(self.size)):
            for x in range(self.size):
                board += "Q" if (x, y) in positions else "."  # place a 'Q' for a queen and '.' otherwise
            board += "\n"
        print(board)


if __name__ == "__main__":
    nqueens = NQueensProblem(8)  # create 8x8 N-Queens problem instance
    nqueens.setup_problem("nqueens_problem.cnf")  # generate the CNF representation of the problem

    # Use the SAT solver to find a solution.
    solver = SAT("nqueens_problem.cnf")
    if solver.walksat():  # if a solution is found using the WalkSAT algorithm
        solver.write_solution("nqueens_solution.sol")  # write the solution to a file
        nqueens.display_solution("nqueens_solution.sol")  # display the solution
