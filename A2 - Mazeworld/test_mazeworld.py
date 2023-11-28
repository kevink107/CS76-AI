from MazeworldProblem import MazeworldProblem
from Maze import Maze

from uninformed_search import bfs_search
from astar_search import astar_search

import random


# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0


# build a new maze based on specified width/height
# wall_prob - probability of a wall at a specific tile
# returns the filename of the maze, number of robots, goal locations for the robots
def build_maze(width, height, wall_prob):
    filename = "maze" + str(width) + "x" + str(height) + ".maz"
    out_maze = open(filename, "w")
    available_positions = []

    for y in range(height):
        line = ""
        for x in range(width):
            if random.uniform(0, 1) <= wall_prob:
                line += "#"
            else:
                line += "."
                available_positions.append((x, y))
        out_maze.write(line + '\n')

    # shuffles the potential starting positions for the robots
    random.shuffle(available_positions)

    # starting number of robots
    num_robots = random.randint(1, 3)
    for i in range(num_robots):
        x, y = available_positions.pop()
        out_maze.write("\\robot " + str(x) + " " + str(y) + '\n')

    # randomized goal locations for robots
    goal_locations = []
    for i in range(num_robots):
        x, y = available_positions.pop()
        goal_locations.append(x)
        goal_locations.append(y)

    out_maze.close()
    print("created: " + filename)

    return filename, num_robots, tuple(goal_locations)


# Test problems
test_maze3 = Maze("maze3.maz")
test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

print(test_mp.get_successors(test_mp.start_state))

# this should explore a lot of nodes; it's just uniform-cost search
result = astar_search(test_mp, null_heuristic)
print(result)

# this should do a bit better:
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path(result.path)


# Your additional tests here:

# Maze 2
test_maze2 = Maze("maze1.maz")
test_m2 = MazeworldProblem(test_maze2, (2,2))
result2 = astar_search(test_m2, test_m2.manhattan_heuristic)
print(result2)
test_m2.animate_path(result2.path)

# Maze 1
test_maze1 = Maze("maze1.maz")
test_m1 = MazeworldProblem(test_maze1, (1,1, 3,1))
result1 = astar_search(test_m1, test_m1.manhattan_heuristic)
print(result1)
test_m1.animate_path(result1.path)

# Maze 4
test_maze4 = Maze("maze4.maz")
test_m4 = MazeworldProblem(test_maze4, (0,2, 1,2, 2,2))
result4 = astar_search(test_m4, test_m4.manhattan_heuristic)
print(result4)
test_m4.animate_path(result4.path)

# Unsolvable Test
test_maze5 = Maze("maze5.maz")
test_m5 = MazeworldProblem(test_maze5, (3,2, 7,3, 5,5))
result5 = astar_search(test_m5, test_m5.manhattan_heuristic)
print(result5)

# Using build_maze function to generate a random maze
random_maze, num_robots, goal_locations = build_maze(10, 10, 0.2)
print(goal_locations)
test_maze_builder = Maze(random_maze)
test_mb = MazeworldProblem(test_maze_builder, goal_locations)
result_random = astar_search(test_mb, test_mb.manhattan_heuristic)
print(result_random)
test_mb.animate_path(result_random.path)

# # 20x20 Maze Test
# test_maze20 = Maze("maze20x20.maz")
# test_20 = MazeworldProblem(test_maze20, (0,19, 5,19, 8,19))
# result20 = astar_search(test_20, test_20.manhattan_heuristic)
# print(result20)
# test_20.animate_path(result20.path)
#
# # 40x40 Maze Test
# test_maze40 = Maze("maze40x40.maz")
# test_40 = MazeworldProblem(test_maze40, (0,39, 36,39))
# result40 = astar_search(test_40, test_40.manhattan_heuristic)
# print(result40)
