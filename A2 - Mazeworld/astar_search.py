from SearchSolution import SearchSolution
from heapq import heappush, heappop


class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        # you write this part
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.cost = transition_cost

    def priority(self):
        # you write this part
        return self.heuristic + self.cost

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):
    # I'll get you started:
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pq = []
    heappush(pq, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    visited_cost[start_node.state] = 0

    # you write the rest:

    # iterating through the nodes in the priority queue until it's empty
    while len(pq) > 0:
        solution.nodes_visited += 1
        curr_node = heappop(pq)
        curr_state = curr_node.state

        # skip current node if cost != cost of visiting its state - avoids revisiting
        if visited_cost[curr_state] != curr_node.cost:
            continue

        # checks if current state meets goal criteria - if so, backchain to find solution path
        if search_problem.goal_test(curr_state):
            solution.path = backchain(curr_node)
            solution.cost = visited_cost[curr_state]
            return solution

        # iterate through successors to explore alternate paths
        for successor in search_problem.get_successors(curr_state):
            # create new node for each successor with associated cost and heuristic
            s_node = AstarNode(successor[1], heuristic_fn(successor[1]), curr_node, successor[0] + visited_cost[curr_state])
            s_state = s_node.state

            # add successor to priority queue if state hasn't been visited or if it represents lower cost path
            if s_state not in visited_cost or s_node.cost < visited_cost[s_state]:
                visited_cost[s_state] = s_node.cost
                heappush(pq, s_node)

    return solution

