# You write this:
from Maze import Maze
from SensorlessProblem import SensorlessProblem
from astar_search import astar_search

# Maze 1
test_maze1 = Maze("maze1.maz")
test_sensorless = SensorlessProblem(test_maze1)
result = astar_search(test_sensorless, test_sensorless.possible_heuristic)
print(result)
test_sensorless.animate_path(result.path)

# Maze 2
test_maze2 = Maze("maze1.maz")
test_sensorless = SensorlessProblem(test_maze2)
result = astar_search(test_sensorless, test_sensorless.possible_heuristic)
print(result)
test_sensorless.animate_path(result.path)

# Maze 3
test_maze3 = Maze("maze3.maz")
test_sensorless = SensorlessProblem(test_maze3)
result = astar_search(test_sensorless, test_sensorless.possible_heuristic)
print(result)
test_sensorless.animate_path(result.path)

# Maze 4
test_maze4 = Maze("maze4.maz")
test_sensorless = SensorlessProblem(test_maze4)
result = astar_search(test_sensorless, test_sensorless.possible_heuristic)
print(result)
test_sensorless.animate_path(result.path)

# Maze 5
test_maze8 = Maze("maze8.maz")
test_sensorless = SensorlessProblem(test_maze8)
result = astar_search(test_sensorless, test_sensorless.possible_heuristic)
print(result)
test_sensorless.animate_path(result.path)



