"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

from CSP import CSP


# Base Constraint class
class Constraint:
    def __init__(self, variables):
        self.variables = variables

    def satisfied(self, assignment):
        raise NotImplementedError


# Constraint class that checks if two components overlap each other
class NoOverlapConstraint(Constraint):
    def __init__(self, component1, component2, sizes):
        Constraint.__init__(self, [component1, component2])
        self.component1 = component1
        self.component2 = component2
        self.sizes = sizes

    # Check if the constraint is satisfied with the given assignment
    def satisfied(self, assignment):
        # if either component has not been assigned, the constraint is considered satisfied
        if self.component1 not in assignment or self.component2 not in assignment:
            return True

        # extract positions and sizes of both components
        x1, y1 = assignment[self.component1]
        x2, y2 = assignment[self.component2]
        width1, height1 = self.sizes[self.component1]
        width2, height2 = self.sizes[self.component2]

        # check for overlap and return False if they overlap, True otherwise
        return (x1 + width1 <= x2
                or x2 + width2 <= x1
                or y1 + height1 <= y2
                or y2 + height2 <= y1)


class CircuitBoardProblem(CSP):
    def __init__(self, width, height, components, sizes, **kwargs):
        self.width = width  # width of the circuit board
        self.height = height  # height of the circuit board
        self.components = components  # list of components to be placed
        self.sizes = sizes  # sizes of the components

        variables = components
        domains = self.get_domains()  # possible positions for each component

        super().__init__(self, variables, domains, **kwargs)

        # add NoOverlapConstraints for all pairs of components
        for i in range(len(components)):
            for j in range(i + 1, len(components)):
                self.add_constraint(NoOverlapConstraint(components[i], components[j], sizes), components[i])
                self.add_constraint(NoOverlapConstraint(components[i], components[j], sizes), components[j])

    # Generates possible positions for each component on the board considering its size
    def get_domains(self):
        domains = {}
        for component in self.components:
            width, height = self.sizes[component]
            # possible positions where the component can be placed without going out of the board's bounds
            domains[component] = [
                (x, y) for x in range(self.width - width + 1)
                for y in range(self.height - height + 1)
            ]
        return domains

    # Returns the neighbors of a given component (every other component in this case)
    def get_neighbors(self, component):
        return [comp for comp in self.variables if comp != component]

    # Prints the final assignment of components on the board in a grid representation
    def display_solution(self, assignment):
        grid = [['.' for _ in range(self.width)] for _ in range(self.height)]

        # fill in the grid with the assigned positions of components
        for component, position in assignment.items():
            x, y = position
            width, height = self.sizes[component]
            for i in range(x, x + width):
                for j in range(y, y + height):
                    grid[j][i] = component[0]  # use first character of the component name

        # print the grid, reversed to start from the top
        for row in grid[::-1]:
            print(''.join(row))


if __name__ == '__main__':

    components = ['a', 'b', 'c', 'e']
    sizes = {'a': (3, 2), 'b': (5, 2), 'c': (2, 3), 'e': (7, 1)}
    circuit_problem = CircuitBoardProblem(10, 3, components, sizes, var_heuristic='mrv', val_heuristic=None, inference=True)

    # Using backtracking to find a solution
    solution = circuit_problem.backtracking({})
    circuit_problem.display_solution(solution)
