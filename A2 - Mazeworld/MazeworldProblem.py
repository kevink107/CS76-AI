from Maze import Maze
from time import sleep


class MazeworldProblem:

    # Constructor: initializes Mazeworld problem with given maze + goal locations

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.goal_locations = goal_locations
        self.start_state = tuple([0]+maze.robotloc)
        self.total_robots = len(maze.robotloc) // 2

    # String representation of MazeworldProblem
    def __str__(self):
        string = "Mazeworld problem: "
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        # (Be careful, this does modify the maze!)

    # Input: current robot, followed by x,y coordinates
    # Output: current robot + 1, followed by x,y coordinates
    def get_successors(self, state):
        self.maze.robotloc = tuple(state[1:])

        successors = []

        # Consider not moving, moving east, moving west, moving north, and moving south
        for direction in range(5):
            successor = self.move_robot(state, direction)
            if successor != "Invalid move":
                successors.append(successor)

        return successors

    # Input: current state, direction to move
    # Output: successor with input direction, whether the successor node is valid (no collisions)
    def move_robot(self, state, direction):
        # direction: (0 = wait, 1 = east, 2 = west, 3 = north, 4 = south)
        movements = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
        dx, dy = movements[direction]

        # Cost is 0 for no move, otherwise 1
        if direction == 0:
            cost = 0
        else:
            cost = 1

        # Get coordinates of the robot we are moving
        curr_robot = state[0]
        x_idx = 2 * curr_robot + 1
        y_idx = x_idx + 1
        new_x = state[x_idx] + dx
        new_y = state[y_idx] + dy

        # Determine next robot to move
        next_robot = (curr_robot + 1) % self.total_robots if curr_robot < self.total_robots - 1 else 0

        if direction == 0 or self.is_valid_action(state, new_x, new_y):
            new_state = list(state)
            new_state[0] = next_robot
            new_state[x_idx] = new_x
            new_state[y_idx] = new_y
            return cost, tuple(new_state)

        return "Invalid move"  # Could not move the robot in that direction

    # Check if move is valid (new location is a floor and not occupied by another robot
    def is_valid_action(self, state, new_x, new_y):
        if self.maze.is_floor(new_x, new_y) and not self.maze.has_robot(new_x, new_y):
            return True
        return False

    # Check if robots have reached goal locations
    def goal_test(self, locations):
        return locations[1:] == self.goal_locations

    # Calculate Manhattan distance from robots' current locs to their goals
    def manhattan_heuristic(self, state):
        s = 0
        curr_state = state[1:]

        for i in range(0, len(curr_state)):
            s += abs(curr_state[i] - self.goal_locations[i])

        return s

    # Visualize path solution
    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)

            print(str(self.maze))


# A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    print(test_mp.get_successors((0, 1, 0, 1, 2, 2, 1)))
