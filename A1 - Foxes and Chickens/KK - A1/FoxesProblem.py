# Kevin King, 9/18/23

class FoxesProblem:
    def __init__(self, start_state):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.total_chickens = start_state[0]
        self.total_foxes = start_state[1]

    # Get successor states for the given state
    def get_successors(self, state):
        successors = []
        l_chickens, l_foxes, boat = state

        possible_actions = [(0, 1), (1, 0), (1, 1), (0, 2), (2, 0)]

        # Loop through each possible action
        for action in possible_actions:
            if boat == 1:
                new_l_chickens = l_chickens - action[0]
                new_l_foxes = l_foxes - action[1]
            else:
                new_l_chickens = l_chickens + action[0]
                new_l_foxes = l_foxes + action[1]

            if ((new_l_chickens > self.total_chickens or new_l_chickens < 0) or
                    (new_l_foxes > self.total_foxes or new_l_foxes < 0)):
                continue

            new_boat = 1 - boat

            new_state = (new_l_chickens, new_l_foxes, new_boat)
            # print(new_state)

            # Check if the move is valid
            if self.is_valid_action(new_l_chickens, new_l_foxes):
                new_state = (new_l_chickens, new_l_foxes, new_boat)
                successors.append(new_state)

        return successors

    def is_valid_action(self, l_chickens, l_foxes):
        r_chickens = self.total_chickens - l_chickens
        r_foxes = self.total_foxes - l_foxes

        if (l_foxes > l_chickens > 0) or (r_foxes > r_chickens > 0):
            return False

        return True

    def goal_test(self, state):
        return state == self.goal_state

    def __str__(self):
        string = "Foxes and chickens problem: " + str(self.start_state)
        return string


# Test code
if __name__ == "__main__":
    test_cp = FoxesProblem((3, 3, 1))
    print("Successors of (3, 3, 1): ", test_cp.get_successors((3, 3, 1)))
    print(test_cp)

    # print(FoxesProblem((3, 2, 0)))
    # print("Successors of (3, 2, 0): ", test_cp.get_successors((3, 2, 0)))
    # print(FoxesProblem((2, 2, 0)))
    # print("Successors of (2, 2, 0): ", test_cp.get_successors((2, 2, 0)))
    # print(FoxesProblem((3, 1, 0)))
    # print("Successors of (3, 1, 0): ", test_cp.get_successors((3, 1, 0)))
    # print(FoxesProblem((2, 3, 0)))
    # print("Successors of (3, 2, 0): ", test_cp.get_successors((2, 3, 0)))
    # print(FoxesProblem((1, 3, 0)))
    # print("Successors of (1, 3, 0): ", test_cp.get_successors((1, 3, 0)))

