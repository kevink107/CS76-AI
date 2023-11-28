from Maze import Maze
from time import sleep


class SensorlessProblem:

    # Constructor: initialize SensorlessProblem with given maze
    def __init__(self, maze):
        self.maze = maze
        locations = []  # list of possible locations of robot
        for i in range(maze.width):
            for j in range(maze.height):
                # adds coordinates of floor cells to locations list
                if maze.is_floor(i, j):
                    locations.append(i)
                    locations.append(j)
        # converts locations list to a tuple and assigns it as the starting state
        self.start_state = tuple(locations)

    # String representation of SensorlessProblem
    def __str__(self):
        string = "Blind robot problem: "
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    # Generates and returns successor of given state
    # Helper: move_robots
    def get_successors(self, state):
        successors = []
        for direction in range(4):
            successors.append(self.move_robots(state, direction))

        return successors

    # Helper function that moves robots in specified direction and returns resulting state
    def move_robots(self, state, direction):
        # Keep track of the nodes currently in the successor list
        coords = set()
        r_list = []

        # iterate through all robots' coordinates in current state
        for i in range(0, len(state), 2):
            movements = [(1, 0), (-1, 0), (0, -1), (0, 1)]  # possible movements
            dx, dy = movements[direction]  # selects movement for current direction
            x = state[i]
            y = state[i + 1]

            curr = (x + dx, y + dy)  # new coordinates after the move

            # Adds new states to the successor list if not already
            if curr not in coords:
                # Checks if new coordinates are a valid move
                if self.maze.is_floor(curr[0], curr[1]):
                    coords.add(curr)
                    r_list.append(curr[0])
                    r_list.append(curr[1])
                # Handles case where move isn't valid
                else:
                    coords.add((state[i], state[i + 1]))  # robot remains in current position
                    r_list.append(state[i])
                    r_list.append(state[i + 1])

        # Cost is always one because we are always moving one robot
        # Returns successor state with a cost of 1 for the move
        return 1, tuple(r_list)

    # Checks if given state meets the goal requirements
    def goal_test(self, state):
        return len(state) == 2

    # Possible heuristic function for the A* search algorithm
    def possible_heuristic(self, state):
        return len(state) // 2  # number of possible locations for the robot

    # Visualizes path solution
    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(1)

            print(str(self.maze))


# A bit of test code
if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)
