"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

import numpy as np
import time
import random
from sklearn.neighbors import NearestNeighbors
from math import sin, cos, radians
from shapely.geometry.polygon import LinearRing, Polygon, LineString
from arm import ArmVisualizer
from heapq import heappush, heappop


class AstarSolution:
    def __init__(self):
        self.path = []
        self.nodes_visited = 0
        self.cost = 0


class AstarNode:
    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        # init method
        self.parent = parent
        self.state = state
        self.heuristic = heuristic
        self.cost = transition_cost

    def priority(self):
        return self.heuristic + self.cost
    def __lt__(self, other):
        return self.priority() < other.priority()


class PRM:
    """
    Probabilistic Roadmap (PRM) for motion planning.
    Attributes:
        arm_lengths (list): Lengths of the segments of the robotic arm.
        obstacles (list): List of shapely Polygon objects representing obstacles.
    """
    def __init__(self, arm_lengths, obstacles):
        self.arm_lengths = arm_lengths
        self.obstacles = [self.create_polygon(obstacle) for obstacle in obstacles]

    '''
    Creates a polygon from corner points for an obstacle.
    '''
    def create_polygon(self, corners):
        bl, tr = corners
        br = (tr[0], bl[1])
        tl = (bl[0], tr[1])
        return Polygon([bl, br, tr, tl, bl])

    '''
    Converts an arm configuration to coordinates.
    '''
    def config_to_coords(self, config):
        coords = [(0, 0)]
        for arm_length, angle in zip(self.arm_lengths, config):
            end_x = coords[-1][0] + arm_length * cos(np.radians(angle))
            end_y = coords[-1][1] + arm_length * sin(np.radians(angle))
            coords.append((end_x, end_y))
        return coords

    '''
    Checks if the given arm configuration collides with any obstacles.
    '''
    def check_collisions(self, coords):
        arm = LinearRing(coords)
        return all(obstacle.disjoint(arm) for obstacle in self.obstacles)

    def is_on_plane(self, coords):
        return all(x >= 0 and y >= 0 for x, y in coords)

    ''' 
    Generates a random configuration for the arm
    '''
    def random_config(self):
        return tuple(random.uniform(0, 360) for _ in self.arm_lengths)

    '''
    Calculates the heuristic for A* (Euclidean distance between configurations).
    '''
    def heuristic(self, config1, config2):
        return np.linalg.norm(np.subtract(config1, config2))

    '''
    Finds the nearest neighbors of a given configuration.
    '''
    def nearest_neighbors(self, config, vertices, k):
        if len(vertices) < k:
            return vertices

        nbrs = NearestNeighbors(n_neighbors=min(k + 1, len(vertices)), algorithm='ball_tree').fit(vertices)
        distances, indices = nbrs.kneighbors([config])
        return [vertices[i] for i, distance in zip(indices[0], distances[0]) if distance > 0 and i < len(vertices)]

    '''
    Connects a configuration to its neighbors if within a certain threshold.
    '''
    def connect_configs(self, config, neighbors, edges, threshold=50):
        for neighbor in neighbors:
            if self.heuristic(config, neighbor) < threshold:
                edges.add((config, neighbor) if config < neighbor else (neighbor, config))

    '''
    Sets up the PRM with randomly sampled configurations and connections.
    '''
    def setup(self, n, k):
        vertices = []
        edges = set()
        while len(vertices) < n:
            config = self.random_config()
            coords = self.config_to_coords(config)
            if self.check_collisions(coords) and self.is_on_plane(coords):
                vertices.append(config)
                neighbors = self.nearest_neighbors(config, vertices[:-1], k)
                self.connect_configs(config, neighbors, edges)
        return vertices, list(edges)

    '''
    Checks if two configurations can be connected.
    '''
    def can_connect(self, config1, config2, threshold=50):
        return self.heuristic(config1, config2) < threshold

    '''
     Performs the query to find a path between two configurations using A* search.
     '''
    def query(self, init_config, final_config, k, vertices, edges):
        vertices.extend([init_config, final_config])
        edges.extend([(config, init_config) for config in self.nearest_neighbors(init_config, vertices, k) if self.can_connect(config, init_config)])
        edges.extend([(config, final_config) for config in self.nearest_neighbors(final_config, vertices, k) if self.can_connect(config, final_config)])

        return self.astar_search(init_config, final_config, edges).path

    '''
    Gets the successors for a given configuration from the PRM.
    '''
    def get_successors(self, config, edges):
        return [neighbor for edge in edges for neighbor in edge if config in edge and neighbor != config]

    '''
    Backchains from the goal node to the start node to find the path.
    '''
    def backchain(self,node):
        result = []
        current = node
        while current:
            result.append(current.state)
            current = current.parent

        result.reverse()
        return result

    def astar_search(self, init, final, edges):
        start_node = AstarNode(init, self.heuristic(init, final))
        pq = []
        heappush(pq, start_node)

        solution = AstarSolution()

        visited_cost = {}
        visited_cost[start_node.state] = 0

        while pq:
            solution.nodes_visited += 1
            curr_node = heappop(pq)
            curr_state = curr_node.state

            # skip processing if a cheaper path to this state has been found
            if curr_state in visited_cost and visited_cost[curr_state] < curr_node.cost:
                continue

            # check if the current state is the final state
            if curr_state == final:
                solution.path = self.backchain(curr_node)
                solution.cost = curr_node.cost
                return solution

            # explore the successors of the current state
            for successor in self.get_successors(curr_state, edges):
                new_cost = curr_node.cost + self.heuristic(curr_state, successor)
                # only consider this successor if it's either not been visited yet or we've found a cheaper path to it
                if successor not in visited_cost or new_cost < visited_cost[successor]:
                    visited_cost[successor] = new_cost
                    heappush(pq, AstarNode(successor, self.heuristic(successor, final), curr_node, new_cost))

        return solution  # if the loop ends without returning, no path was found


if __name__ == '__main__':
    obstacles = [((1, 4), (2, 5)), ((5, 1), (6, 2))]
    arm_lengths = [4, 4, 5, 5]

    prm_model = PRM(arm_lengths, obstacles)
    vertices, edges = prm_model.setup(n=10000, k=3)

    init_config = (45, 60, 45, 90)
    final_config = (10, 80, 15, 45)

    path = prm_model.query(init_config, final_config, 3, vertices, edges)

    if path:
        print("Path found:", path)
        visualizer = ArmVisualizer(20, 20, arm_lengths, obstacles, init_config)
        visualizer.simulate_path(path)
        visualizer.start_graphics()
    else:
        print("No path found")


