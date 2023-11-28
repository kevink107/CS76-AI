"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

from SAT import SAT
from display import display_sudoku_solution
import time


def test_sudoku(cnf_filename, algorithm):
    print(f"Testing {algorithm} with {cnf_filename}")
    assignment = None
    sat = SAT(f"{cnf_filename}.cnf")

    start = time.time()
    if algorithm == "GSAT":
        assignment = sat.gsat()  # Adjust max_flips based on your need
    elif algorithm == "WalkSAT":
        assignment = sat.walksat()  # Adjust threshold and max_flips based on your need

    end = time.time()

    if assignment:
        print(f"Time elapsed: {end - start} seconds")
        sol_filename = f"{cnf_filename}.sol"
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
    else:
        print(f"No satisfying assignment found")


"""
TODO: 
- Make SAT class more time efficient 
- Extensions
"""

# Uncomment the following lines to test with different sudoku puzzles and algorithms
# test_sudoku("one_cell", "GSAT")
# test_sudoku("all_cells", "GSAT")
# test_sudoku("one_cell", "WalkSAT")
# test_sudoku("all_cells", "WalkSAT")
# test_sudoku("rows", "WalkSAT")
# test_sudoku("rows_and_cols", "WalkSAT")
test_sudoku("rules", "WalkSAT")
# test_sudoku("puzzle1", "WalkSAT")
# test_sudoku("puzzle2", "WalkSAT")
# test_sudoku("puzzle_bonus", "WalkSAT")
