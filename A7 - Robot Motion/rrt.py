"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

from shapely.geometry import Point, Polygon, LineString
import numpy as np
import random
from sklearn.neighbors import NearestNeighbors
from planar_trajectory import *
from planar_display import *
import matplotlib.pyplot as plt
import random


class Node:
    def __init__(self, state, parent=None, path=None, move=None):
        self.state = state  # The current state (position and orientation) of the node
        self.parent = parent  # The parent node in the path
        self.path = path if path is not None else [state]  # The path taken to reach this node
        self.move = move if move is not None else []  # The move or action leading to this node


class RRT:
    def __init__(self, step_size, border, obstacles):
        self.step_size = step_size  # Step size for expansion in RRT
        self.boundary = [[0, border[0]], [0, border[1]]]  # Boundary of the search space
        self.borders = self.create_borders()  # Creating borders based on the boundary
        self.obstacles = [Polygon(obstacle) for obstacle in obstacles]  # Creating obstacles as polygons

    '''
    Generates border lines from the boundary coordinates
    '''
    def create_borders(self):

        point1 = [self.boundary[0][0], self.boundary[1][0]]
        point2 = [self.boundary[0][1], self.boundary[1][1]]
        dx, dy = point2[0] - point1[0], point2[1] - point1[1]
        return [
            LineString([point1, [point1[0] + dx, point1[1]]]),
            LineString([point1, [point1[0], point1[1] + dy]]),
            LineString([point2, [point2[0] - dx, point2[1]]]),
            LineString([point2, [point2[0], point2[1] - dy]])
        ]

    '''
    Expands a vertex in the direction of a random configuration
    '''
    def expand_vertex(self, nearest_node, random_config, vertex, goal):
        for i in range(6):
            child_config = self.child_config(nearest_node, i)
            if child_config != nearest_node.state and self.check_collision(child_config):
                new_node = Node(child_config, nearest_node, nearest_node.path + [child_config], nearest_node.move + [i])
                vertex.append(new_node)
                if self.goal_test(child_config, goal):
                    return new_node
        return None

    def run(self, init, goal, max_iterations):
        vertex = [Node(init)]  # Initial set of vertices (starting with the initial node)
        for _ in range(max_iterations):
            random_config = self.random_config()  # Generate a random configuration
            nearest_node = self.nearest_vertex(random_config, vertex)  # Find nearest vertex to this configuration
            new_node = self.expand_vertex(nearest_node, random_config, vertex, goal)  # Expand towards the random configuration
            if new_node:
                return new_node.path, new_node.move  # If goal is reached, return the path and moves
        return None, None  # If goal is not reached within max iterations, return None

    '''
    Calculates a child configuration given a node and a move index
    '''
    def child_config(self, node, move_index):
        traj = PlanarTrajectory(controls_rs, *node.state, [move_index], [self.step_size])
        return traj.config_at_t(self.step_size - 0.0001)  # Configuration at a specific time

    '''
    Tests if the current state is within a threshold distance of the goal
    '''
    def goal_test(self, state, goal, threshold=1.0):
        distance = np.linalg.norm(np.array(goal) - np.array(state))
        return distance <= threshold

    '''
    Generates a random configuration within the defined boundary
    '''
    def random_config(self):
        return (
            random.uniform(*self.boundary[0]),
            random.uniform(*self.boundary[1]),
            random.random() * 2 * np.pi  # Random orientation
        )

    '''
    Checks for collisions with obstacles and borders
    '''
    def check_collision(self, q):
        point = Point(q[0], q[1]).buffer(0.25)  # Creates a buffer around the point for collision checking
        # Checks if the point is disjoint from all obstacles and borders (i.e., not colliding)
        return all(obstacle.disjoint(point) for obstacle in self.obstacles) and \
               all(border.disjoint(point) for border in self.borders)

    '''
    Finds the nearest vertex in the tree to a given point
    '''
    def nearest_vertex(self, q, vertex):
        X = np.array([v.state for v in vertex])  # Array of vertex states
        nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(X)
        distances, indices = nbrs.kneighbors([q])
        return vertex[indices[0][0]]  # Returns the nearest vertex


def draw_result(start, moves, duration, obstacles):
    traj = PlanarTrajectory(controls_rs, *start, moves, duration)
    view = TrajectoryView(traj, obstacles)
    ax = plt.axes()
    view.draw(ax, sum(duration) - 0.01)
    plt.show()


def is_far_enough(point, others, min_distance):
    return all(np.linalg.norm(np.array(point) - np.array(other)) >= min_distance for other in others)


def generate_obstacles(num_obstacles, boundary_size, min_size=5, max_size=10, min_distance=15):
    obstacles = []
    obstacle_centers = []
    while len(obstacles) < num_obstacles:
        x1, y1 = random.randint(10, boundary_size[0] - max_size - 10), random.randint(10, boundary_size[1] - max_size - 10)
        x2, y2 = x1 + random.randint(min_size, max_size), y1 + random.randint(min_size, max_size)
        center = [(x1 + x2) / 2, (y1 + y2) / 2]

        if is_far_enough(center, obstacle_centers, min_distance):
            obstacles.append([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
            obstacle_centers.append(center)

    return obstacles


def generate_test_case(boundary_size, step_size, k, num_obstacles, min_start_goal_distance=20):
    obstacles = generate_obstacles(num_obstacles, boundary_size)
    start = (random.uniform(5, boundary_size[0] - 5), random.uniform(5, boundary_size[1] - 5), random.uniform(0, 2 * np.pi))

    goal = (random.uniform(5, boundary_size[0] - 5), random.uniform(5, boundary_size[1] - 5), random.uniform(0, 2 * np.pi))
    while not is_far_enough(goal[:2], [start[:2]], min_start_goal_distance):
        goal = (random.uniform(5, boundary_size[0] - 5), random.uniform(5, boundary_size[1] - 5), random.uniform(0, 2 * np.pi))

    rrt = RRT(step_size, boundary_size, obstacles)
    path, moves = rrt.run(start, goal, k)
    if path:
        draw_result(start, moves, [rrt.step_size] * len(moves), obstacles)
    else:
        print("No path found")


if __name__ == '__main__':
    # Setting up a new RRT instance with a modified obstacle layout and boundary
    rrt = RRT(1.5, [60, 60], [[[20, 40], [40, 40], [40, 20], [20, 20]], [[35, 55], [55, 55], [55, 35], [35, 35]]])
    start_position = (30, 55, 0)  # Starting position
    goal_position = (55, 5, np.pi / 2)  # Goal position

    # Running the RRT algorithm with the new configuration
    path, moves = rrt.run(start_position, goal_position, 4000)  # Adjusted number of iterations
    if path:
        draw_result(start_position, moves, [rrt.step_size] * len(moves),
                    [[[20, 40], [40, 40], [40, 20], [20, 20]], [[35, 55], [55, 55], [55, 35], [35, 35]]])
    else:
        print("No path found")

    # Uncomment the below code to generate random configurations and test cases
    # print("Test 1")
    # generate_test_case([50, 50], 2, 5000, 3)
    #
    # print("Test 2")
    # # Test Case 2
    # generate_test_case([60, 60], 1.5, 5000, 4)
    #
    # print("Test 3")
    # # Test Case 3
    # generate_test_case([40, 40], 2, 3000, 2)
