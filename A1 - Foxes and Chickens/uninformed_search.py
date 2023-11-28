# Kevin King, 9/18/23

from collections import deque
from SearchSolution import SearchSolution


class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
        # you write this part
        self.state = state
        self.parent = parent
        self.depth = 0


# ******* BREADTH-FIRST SEARCH ******* #
def bfs_search(search_problem):
    # Set up start and goal states from the search problem
    start_state = search_problem.start_state

    sol = SearchSolution(search_problem, "BFS", start_state)

    # Initialize FIFO queue with start state
    queue = deque()
    queue.append(SearchNode(start_state))
    visited = set()  # marks start state as visited

    # should be path length of 11 for (3,1,1) - shouldn't count the first node
    while queue:
        # Explore next state
        node = queue.popleft()

        # Check if reached goal state
        if search_problem.goal_test(node.state):
            sol.nodes_visited = len(visited)
            backchain(node, sol)
            return sol

        # Enqueue them if not visited
        for successor_state in search_problem.get_successors(node.state):
            if successor_state not in visited:
                visited.add(successor_state)
                successor_node = SearchNode(successor_state, node)
                queue.append(successor_node)

    # If queue is empty and no solution found
    sol.nodes_visited = len(visited)
    return sol


# Helper function: Builds path from goal state to start state
def backchain(node, sol):
    while node:
        sol.path.insert(0, node.state)
        node = node.parent


# ******* DEPTH-FIRST SEARCH ******* #
def dfs_search(search_problem, depth_limit=100, node=None, sol=None):
    # Base Case: if no node object given, create a new search from starting state
    if node is None:
        node = SearchNode(search_problem.start_state)
        sol = SearchSolution(search_problem, "DFS", search_problem.start_state)

    sol.nodes_visited += 1
    # Base Case: check if reached goal state
    if search_problem.goal_test(node.state):
        backchain(node, sol)
        return sol

    # Recursive Case
    for successor_state in search_problem.get_successors(node.state):
        if check_path(node, successor_state):
            successor_node = SearchNode(successor_state, node)
            successor_node.depth = node.depth + 1
            if successor_node.depth < depth_limit:
                new_sol = dfs_search(search_problem, depth_limit, successor_node, sol)
                if len(new_sol.path) > 0:
                    return new_sol

    return sol


# Helper function: Checks if path from current node to start state has a loop
def check_path(node, successor_state):
    while node.parent:
        if node.parent.state == successor_state:
            return False
        node = node.parent
    return True


# ******* ITERATIVE DEEPENING SEARCH *******
def ids_search(search_problem, depth_limit=100):
    # Initialize depth_limit to start from 0
    node = SearchNode(search_problem.start_state)
    solution = SearchSolution(search_problem, "IDS", search_problem.start_state)

    for depth in range(depth_limit + 1):
        result = dfs_search(search_problem, depth, node, solution)

        if len(result.path) > 0:
            return solution

    return solution


# def dfs_search(search_problem, depth_limit=100, node=None, sol=None):
#     # Base Case: If no node object given, create a new search from starting state
#     if node is None:
#         node = SearchNode(search_problem.start_state)
#         sol = SearchSolution(search_problem, "DFS")
#
#     # Base Case: Check if reached goal state
#     if search_problem.goal_test(node.state):
#         sol.nodes_visited += 1  # increment nodes visited by 1  # add to path
#         sol.path.append(node.state)
#         return sol
#
#     visited = set()
#
#     # FIX: DFS currently counting # nodes visited incorrectly
#
#     for successor_state in search_problem.get_successors(node.state):
#         # Check if successor state isn't on curr path
#         if successor_state not in sol.path and successor_state not in visited:
#             sol.path.append(node.state)  # add to path
#             visited.add(successor_state)
#             sol.nodes_visited += 1
#             # print(sol.nodes_visited)
#
#             # Recursive call to DFS for successor state
#             successor_node = SearchNode(successor_state, node)
#             new_sol = dfs_search(search_problem, depth_limit - 1, successor_node, sol)
#
#             # If solution is found, return it (base case will handle depth limit)
#             if new_sol is not None:
#                 return new_sol
#
#             # Remove current state from path (backtrack)
#             sol.path.pop()
#
#     return None
#
#
# def ids_search(search_problem, depth_limit=100):
#     # Initialize depth_limit to start from 0
#
#     for depth in range(depth_limit + 1):
#         # Perform DFS with given depth_limit
#         sol = dfs_search(search_problem, depth)
#
#         if sol is not None:
#             sol.search_method = "IDS"
#             return sol
#
#     return None
#
#     # If no solution found after trying all depths
#     sol = SearchSolution(search_problem, "IDS")
#     return None
