"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

from Maze import Maze
import numpy as np


class HMM:
    def __init__(self, maze, moves, sensor_input):
        self.maze = maze
        self.moves = moves  # sequence of moves the robot makes
        self.sensor_input = sensor_input  # sequence of sensor readings corresponding to colors observed

        # initial starting probabilities, mappings between maze indices and states
        self.start_state, self.state_indices, self.indices_states = self.initialize_start_state()

        self.color_mapping = {"g": 0, "r": 1, "y": 2, "b": 3}  # map from color to index (for obs probs)
        self.trans_matrix = self.build_transition_matrix()  # transition probabilities between states
        self.obs_matrix = self.build_observation_matrix()  # observation probabilities

        # lists to store probabilities computed during forward pass, backward pass, and smooothing
        self.forward_probs = []
        self.backward_probs = []
        self.smoothed_probs = []

    '''
    Sets up initial state distribution and creates two dictionaries for mapping between the 
    indices of the state and their corresponding coordinates in the maze
    '''
    def initialize_start_state(self):
        index = 0  # cell counter for assigning indices to states
        start_state = []  # stores initial probabilities
        indices_states = {}  # indices to coordinates
        state_indices = {}  # coordinates to indices

        # fills in mappings first
        for i in range(self.maze.width):
            for j in range(self.maze.height):
                # check if a maze cell is a floor
                if self.maze.is_floor(i, j):
                    indices_states[index] = (i, j)
                    state_indices[(i, j)] = index
                    start_state.append(None)  # placeholder for state's probability
                    index += 1

        # uniform probability distribution for initial state
        for i in range(len(start_state)):
            start_state[i] = 1/len(start_state)

        return start_state, state_indices, indices_states

    '''
    Builds transition matrix based on possible moves from each state in the maze
    '''
    def build_transition_matrix(self):
        size = len(self.start_state)  # size based on number of states
        matrix = np.zeros((size, size))  # initial square matrix of zeros

        # loop through each state to calculate transition probabilities
        for (x, y), idx in self.state_indices.items():
            neighbors = self.maze.get_neighbors(x, y)

            # equal probability to transition to each neighbor
            for nx, ny in neighbors:
                matrix[self.state_indices[(nx, ny)], idx] = 0.25

            # self-transition probability based on number of actual neighbors
            matrix[idx, idx] = 0.25 * (4 - len(neighbors))

        return matrix

    '''
    Builds observation matrix based on colors of squares and sensor model
    '''
    def build_observation_matrix(self):
        # initialize matrix with small probability of sensor error for all states and observations
        matrix = np.full((len(self.start_state), 4), 0.04)

        # loop through each state to set the high probability for the actual square color
        for (x, y), idx in self.state_indices.items():
            color_idx = self.color_mapping[self.maze.get_color(x, y)]
            matrix[idx, color_idx] = 0.88

        return matrix

    '''
    Filtering process updates belief state based on evidence and movements
    '''
    def filtering(self):
        # start with initial uniform distribution
        state = self.start_state.copy()
        self.forward_probs.append(state)

        # loop through each move and corresponding sensor reading
        for move, sensor in zip(self.moves, self.sensor_input):
            # observation vector for current sensor reading
            obs_vector = self.obs_matrix[:, self.color_mapping[sensor]]

            # update belief state by multiplying previous state by transition matrix and observation vector
            state = self.normalize(obs_vector * self.trans_matrix.T.dot(state))
            self.forward_probs.append(state)

    '''
    Smoothing combines forward and backward info to refine probability distributions
    '''
    def smoothing(self):
        self.backward_probs = [np.ones(len(self.start_state))]  # Initialize with uniform probabilities.

        # iterate in reverse to propagate information backward.
        for sensor in reversed(self.sensor_input):
            obs_vector = self.obs_matrix[:, self.color_mapping[sensor]]  # get observation probabilities.
            # compute backward probabilities
            back_prob = self.normalize(self.trans_matrix.dot(obs_vector * self.backward_probs[-1]))
            self.backward_probs.append(back_prob)

        self.backward_probs = self.backward_probs[::-1]  # reverse the list to match

        # combine forward and backward probabilities to get smoothed probabilities.
        for forward, backward in zip(self.forward_probs, self.backward_probs):
            normalized_probs = self.normalize(forward * backward)
            self.smoothed_probs.append(normalized_probs)

    '''
    Helper function to normalize probability distribution
    '''
    def normalize(self, vector):
        total = np.sum(vector)  # sum elements in vector

        # if total is greater than zero, divide each by total to normalize
        if total > 0:
            return vector / total
        else:
            return vector
    '''
    Viterbi algorithm to find the most probable sequence of hidden states
    '''
    def viterbi(self):
        num_states = len(self.start_state)
        T = len(self.moves)
        V = np.zeros((num_states, T + 1))
        path = np.zeros((num_states, T + 1), dtype=int)

        # initial state probabilities
        V[:, 0] = self.start_state

        # run Viterbi when T > 0
        for t in range(1, T + 1):
            # loop over the states
            for s in range(num_states):
                # observation probability at time t
                obs_prob = self.obs_matrix[s, self.color_mapping[self.sensor_input[t - 1]]]
                # multiply the transition probabilities by the probabilities from previous step
                trans_prob = V[:, t - 1] * self.trans_matrix[s, :] * obs_prob

                max_trans_prob = np.max(trans_prob)  # max prob for each state
                V[s, t] = max_trans_prob  # set the probability for reaching state s at time t
                path[s, t] = np.argmax(trans_prob)

        # backtrack to find the best path
        best_path = []

        # start with the state with the highest probability at the last timestep
        last_state = np.argmax(V[:, T])
        best_path.append(last_state)

        # follow the back track till the first timestep
        for t in range(T, 0, -1):
            last_state = path[last_state, t]
            best_path.append(last_state)

        # reverse the path to start from timestep 0
        best_path = best_path[::-1]

        # convert state indices to coordinates
        best_path_coordinates = [self.indices_states[state] for state in best_path]

        return best_path_coordinates

    def convert_to_matrix(self, probs):
        prob_matrix = np.zeros((self.maze.width, self.maze.height))
        for idx, prob in enumerate(probs):
            x, y = self.indices_states[idx]
            prob_matrix[x, y] = "{:.4f}".format(prob)
        return prob_matrix

    '''
    Prints results of the HMM operations
    '''
    def display_results(self, smooth=False):
        # compute Viterbi best path for perceived positions
        actual_path = []
        current_position = self.maze.get_robot_location()  # assuming this is where the robot starts
        actual_path.append(current_position)  # the actual path starts with the initial position

        # calculate the actual robot positions based on moves
        for move in self.moves:
            if move == 'N':
                current_position = (current_position[0], current_position[1] + 1)
            elif move == 'S':
                current_position = (current_position[0], current_position[1] - 1)
            elif move == 'E':
                current_position = (current_position[0] + 1, current_position[1])
            elif move == 'W':
                current_position = (current_position[0] - 1, current_position[1])
            actual_path.append(current_position)

        # iterate over forward probabilities to print filtering results
        for i, (probs, actual_pos) in enumerate(zip(self.forward_probs, actual_path)):
            print("----------------------")
            self.maze.update_robot_location(actual_pos)  # update the maze with the actual robot position
            print("\nMaze + Actual Robot (X) Location: ")
            print(self.maze)  # print the maze with the actual robot position

            # print filtering results
            print(f"TIME: {i} \nFiltering Results:")
            forward_matrix = self.convert_to_matrix(probs)
            print(forward_matrix)

            # print smoothing results if enabled
            if smooth:
                print("\nSmoothing Results:")
                smoothed_matrix = self.convert_to_matrix(self.smoothed_probs[i])
                print(smoothed_matrix)

if __name__ == "__main__":
    print("MAZE 1:")
    maze1 = Maze("maze1.maz")
    hmm1 = HMM(maze1, ['W', 'N', 'N', 'E', 'E'], ['g', 'b', 'y', 'g', 'r'])
    hmm1.filtering()
    hmm1.smoothing()
    hmm1.display_results(smooth=True)
    best_path = hmm1.viterbi()
    print(f"\nObserved Colors: {hmm1.sensor_input}")
    print(f"Viterbi Best Path for Maze 1: {best_path}")
    print("-------------\n")

    print("MAZE 2:")
    maze2 = Maze("maze2.maz")
    hmm2 = HMM(maze2, ['N', 'E', 'E', 'S', 'E'], ['b', 'r', 'g', 'b', 'r'])
    hmm2.filtering()
    hmm2.smoothing()
    hmm2.display_results(smooth=True)
    best_path2 = hmm2.viterbi()
    print(f"\nObserved Colors: {hmm2.sensor_input}")
    print(f"Viterbi Best Path for Maze 2: {best_path2}")
    print("-------------\n")

    print("MAZE 3:")
    maze3 = Maze("maze3.maz")
    hmm3 = HMM(maze3, ['E', 'S', 'N', 'N', 'W'], ['y', 'g', 'y', 'g', 'b'])
    hmm3.filtering()
    hmm3.smoothing()
    hmm3.display_results(smooth=True)
    best_path3 = hmm3.viterbi()
    print(f"\nObserved Colors: {hmm3.sensor_input}")
    print(f"Viterbi Best Path for Maze 3: {best_path3}")
