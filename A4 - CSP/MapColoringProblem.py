"""
Kevin King
Dartmouth COSC 76, Fall 2023
"""

from CSP import CSP


class Variable:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
        self.value = None

    def __str__(self):
        return self.name


class Constraint_MP:
    def __init__(self, var1, var2):
        self.variables = [var1, var2]

        # fill in constraints dictionary
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []

    def satisfied(self, assignment):
        if self.variables[0] not in assignment or self.variables[1] not in assignment:
            return True

        return assignment[self.variables[0]] != assignment[self.variables[1]]


class MapColoringProblem():
    def __init__(self, variables, domains, neighbors):
        self.variables = variables
        self.domains = domains
        self.constraints = {}

        # fill in constraints dictionary
        for variable in variables:
            self.constraints[variable] = []
            # if variable not in self.domains:
            #     raise LookupError("Every variable should have an assigned domain")
        self.neighbors = neighbors

    def add_constraint(self, constraint, variable):
        self.constraints[variable].append(constraint)

    def get_neighbors(self, variable):
        return self.neighbors[variable]


# TO-DO: Need to fix the testing file below
if __name__ == '__main__':

    # Variables initialization with their domains
    WA = Variable("Western Australia", ['red', 'green', 'blue'])
    NT = Variable("Northern Territory", ['red', 'green', 'blue'])
    SA = Variable("South Australia", ['red', 'green', 'blue'])
    Q = Variable("Queensland", ['red', 'green', 'blue'])
    NSW = Variable("New South Wales", ['red', 'green', 'blue'])
    V = Variable("Victoria", ['red', 'green', 'blue'])
    T = Variable("Tasmania", ['red', 'green', 'blue'])

    variables = [WA, NT, Q, SA, NSW, V, T]

    # Defining domains and neighbor relationships
    domains = {var.name: var.domain for var in variables}
    neighbors = {
        "Western Australia": ["Northern Territory", "South Australia"],
        "Northern Territory": ["Western Australia", "South Australia", "Queensland"],
        "South Australia": ["Western Australia", "Northern Territory", "Queensland", "New South Wales", "Victoria"],
        "Queensland": ["Northern Territory", "South Australia", "New South Wales"],
        "New South Wales": ["South Australia", "Queensland", "Victoria"],
        "Victoria": ["South Australia", "New South Wales"],
        "Tasmania": []
    }

    # Printing variables and domains for debugging
    # print(f"Variables: {[var.name for var in variables]}")
    # print(f"Domains: {list(domains.keys())}")

    # Creating the Map Coloring Problem instance and CSP algorithm instance
    MapCSP = MapColoringProblem(variables, domains, neighbors)
    csp = CSP(MapCSP, [var.name for var in MapCSP.variables], MapCSP.domains, None, 'lcv', False)

    # Adding constraints to the CSP based on the neighbor relationships
    for var in variables:
        for neighbor in neighbors[var.name]:
            csp.add_constraint(Constraint_MP(var.name, neighbor), var.name)

    # Calling the backtracking function to solve the CSP
    solution = csp.backtracking({})
    print(solution)

    # Printing the solution
    if solution:
        for variable, value in solution.items():
            print(f"{variable}: {value}")
    else:
        print("No solution found.")
