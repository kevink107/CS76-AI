# Kevin King, 9/18/23

class SearchSolution:
    def __init__(self, problem, search_method, start_state):
        self.problem_name = str(problem)
        self.search_method = search_method
        self.start_state = start_state
        self.path = []
        self.nodes_visited = 0

    # Illustrates the states at each point of the solution path
    def state_to_string(self, state):
        chickens, foxes, boat = state
        if boat == 1:
            return (('C' * chickens) + ('F' * foxes) + ' |B~~| ' + ('C' * (self.start_state[0] - chickens)) +
                    ('F' * (self.start_state[1] - foxes)))
        else:
            return (('C' * chickens) + ('F' * foxes) + ' |~~B| ' + ('C' * (self.start_state[0] - chickens)) +
                    ('F' * (self.start_state[1] - foxes)))

    def __str__(self):
        string = "----\n"
        string += "{:s}\n"
        string += "attempted with search method {:s}\n"

        if len(self.path) > 0:

            string += "number of nodes visited: {:d}\n"
            string += "solution length: {:d}\n"
            string += "path: {:s}\n"

            for state in self.path:
                string += self.state_to_string(state) + "\n"

            string = string.format(self.problem_name, self.search_method,
                self.nodes_visited, len(self.path) - 1, str(self.path))
        else:
            string += "no solution found after visiting {:d} nodes\n"
            string = string.format(self.problem_name, self.search_method, self.nodes_visited)

        return string
