"""
Kevin King
Dartmouth COSC 76, Fall 2023
"""

from collections import deque
import time


class CSP:

    def __init__(self, problem, variables, domains, var_heuristic, val_heuristic, inference):
        self.problem = problem  # CSP problem -- MapColoring or CircuitBoard
        self.variables = variables
        self.domains = domains

        # holds constraints of each variable
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []

        # specifies use of heuristics and inference functions
        self.var_heuristic = var_heuristic
        self.val_heuristic = val_heuristic
        self.inference = inference

        self.nodes_visited = 0  # keep track of nodes visited / calls

    '''
    Adds constraints to variables
    '''
    def add_constraint(self, constraint, variable):
        self.constraints[variable].append(constraint)

    '''
    Checks if an assignment is consistent with constraints
    '''
    def consistent(self, variable, assignment):
        # checks if assignment satisfies all constraints
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    '''
    Selecting the next unassigned variable
    '''
    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

        print("No unassigned variables")
        return None

    '''
    Returns variable based on minimum remaining values in domain
    '''
    def mrv_heuristic(self, assignment):
        # list of unassigned variables
        unassigned = [v for v in self.variables if v not in assignment]
        if not unassigned:  # if all variables are assigned, no need to proceed
            return None

        min_variable = unassigned[0]
        min_count = float('inf')

        for variable in unassigned:
            # count the number of valid values remaining after considering the constraints
            count = 0
            for value in self.domains[variable]:
                # create a new assignment dictionary that includes the current value for the variable
                new_assignment = {**assignment, variable: value}
                if self.consistent(variable, new_assignment):
                    count += 1

            if count < min_count:
                min_count = count
                min_variable = variable

        return min_variable

    '''
    Returns values ordered based on least constrained value
    '''
    def lcv_heuristic(self, assignment, variable):
        lcv = {}
        for value in self.domains[variable]:
            constraints = 0  # Initialize the count of constraints for this value

            for neighbor in self.problem.get_neighbors(variable):
                # skip neighbors that are already assigned
                if neighbor in assignment:
                    continue
                # check if the value is in the neighbor's domain and count it as a constraint
                if value in self.domains[neighbor]:
                    constraints += 1

            lcv[value] = constraints  # storing the value and its constraints count in the lcv dictionary

        return sorted(lcv.keys(), key=lambda x: lcv[x])

    '''
    Returns variable with the most neighbors
    '''
    def degree_heuristic(self, assignment):
        # list of unassigned variables
        unassigned = [v for v in self.variables if v not in assignment]
        most_nbrs = unassigned[0]
        max = 0
        for variable in unassigned:
            count = 0
            for nbr in self.problem.get_neighbors(variable):
                if nbr in unassigned:
                    count += 1
            if count > max:
                max = count
                most_nbrs = variable

        return most_nbrs

    '''
    Inference method that revises domain of unassigned variables based on current assignment
    '''
    def mac3_inference(self, assignment, variable):
        # Create a queue to hold pairs of variables (xi, xj) to be checked for arc consistency.
        queue = deque([(xi, variable) for xi in self.variables if xi != variable])

        while queue:
            xi, xj = queue.popleft()

            # If revise returns True, meaning the domain of xi was reduced, then we have to check
            # all neighboring variables of xi again.
            if self.revise(xi, xj, assignment):
                # If the domain of xi is empty, this assignment is not arc-consistent.
                if len(self.domains[xi]) == 0:
                    return False

                # Add all neighbors of xi, except xj, back to the queue to recheck arc consistency.
                neighbors = [xk for xk in self.variables if xk != xj and (xk, xi) in queue]
                queue.extend([(xk, xi) for xk in neighbors])

        return True

    '''
    Revises the domain of xi to maintain arc consistency.
    '''
    def revise(self, xi, xj, assignment):

        revised = False
        for value_xi in self.domains[xi][:]:
            # Check if there exists a value in the domain of xj that satisfies the constraints
            # given that xi is assigned value_xi.
            if not any(self.consistent(xi, {xi: value_xi, xj: value_xj}) for value_xj in self.domains[xj]):
                self.domains[xi].remove(value_xi)
                revised = True

        return revised

    '''
    Backtracking search algorithm to solve the CSP
    '''
    def backtracking(self, assignment):
        self.nodes_visited += 1
        start = time.time()
        # if all variables are assigned, return assignment as solution
        if len(assignment) == len(self.variables):
            # print(f"Nodes visited: {self.nodes_visited}")
            return assignment

        # select next variable based on specified heuristic
        if self.var_heuristic == 'mrv':
            variable = self.mrv_heuristic(assignment)
        elif self.var_heuristic == 'degree':
            variable = self.degree_heuristic(assignment)
        else:
            variable = self.select_unassigned_variable(assignment)

        # If all variables are assigned, return failure
        if not variable:
            return None

        # ordering values of selected variable based on specified heuristic
        if self.val_heuristic == 'lcv':
            values = self.lcv_heuristic(assignment, variable)
        else:
            values = self.domains[variable]

        # assign values to variable and recursing
        for value in values:
            assignment[variable] = value
            # print(f"Assigning {value} to {variable}")

            # check if assignment is consistent
            if self.consistent(variable, assignment):
                # apply inference to revise domains of unassigned variables
                if self.inference:
                    inference_successful = self.mac3_inference(assignment, variable)
                    # if unsuccessful inference, backtrack
                    if not inference_successful:
                        # assignment.pop(variable)
                        continue  # Skip this value if the inference is not successful

                # Recursing to assign values to next variable
                result = self.backtracking(assignment)
                if result:
                    end = time.time()
                    # print(f"Time: {end - start}")
                    return result

            # backtracking if assignment is not consistent
            assignment.pop(variable)
