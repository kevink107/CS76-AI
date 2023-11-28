"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

from CSP import CSP
from MapColoringProblem import *
from CircuitBoardProblem import *

'''
Map-Coloring Problem
'''

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


# Creating the Map Coloring Problem instance and CSP algorithm instance
MapCSP = MapColoringProblem(variables, domains, neighbors)

print("-----MAP COLORING PROBLEM-----")

# FIRST
print("\nNone, None, False")
csp = CSP(MapCSP, [var.name for var in MapCSP.variables], MapCSP.domains, None, None, False)

# Adding constraints to the CSP based on the neighbor relationships
for var in variables:
    for neighbor in neighbors[var.name]:
        csp.add_constraint(Constraint_MP(var.name, neighbor), var.name)

# Calling the backtracking function to solve the CSP
solution = csp.backtracking({})
print(solution)

# SECOND
print("\nMRV, None, False")
csp = CSP(MapCSP, [var.name for var in variables], domains, 'mrv', None, False)

# Adding constraints to the CSP based on the neighbor relationships
for var in variables:
    for neighbor in neighbors[var.name]:
        csp.add_constraint(Constraint_MP(var.name, neighbor), var.name)

# Calling the backtracking function to solve the CSP
solution = csp.backtracking({})
print(solution)

# THIRD
print("\nNone, LCV, False")
csp = CSP(MapCSP, [var.name for var in variables], domains, None, 'lcv', False)

# Adding constraints to the CSP based on the neighbor relationships
for var in variables:
    for neighbor in neighbors[var.name]:
        csp.add_constraint(Constraint_MP(var.name, neighbor), var.name)

# Calling the backtracking function to solve the CSP
solution = csp.backtracking({})
print(solution)

# FOURTH
print("\nMRV, LCV, False")
csp = CSP(MapCSP, [var.name for var in variables], domains, 'mrv', 'lcv', False)

# Adding constraints to the CSP based on the neighbor relationships
for var in variables:
    for neighbor in neighbors[var.name]:
        csp.add_constraint(Constraint_MP(var.name, neighbor), var.name)

# Calling the backtracking function to solve the CSP
solution = csp.backtracking({})
print(solution)

# FIFTH
print("\nNone, LCV, Inference")
csp = CSP(MapCSP, [var.name for var in variables], domains, None, 'lcv', True)

# Adding constraints to the CSP based on the neighbor relationships
for var in variables:
    for neighbor in neighbors[var.name]:
        csp.add_constraint(Constraint_MP(var.name, neighbor), var.name)

# Calling the backtracking function to solve the CSP
solution = csp.backtracking({})
print(solution)

# SIXTH
print("\nMRV, None, Inference")
csp = CSP(MapCSP, [var.name for var in variables], domains, 'mrv', None, True)

# Adding constraints to the CSP based on the neighbor relationships
for var in variables:
    for neighbor in neighbors[var.name]:
        csp.add_constraint(Constraint_MP(var.name, neighbor), var.name)

# Calling the backtracking function to solve the CSP
solution = csp.backtracking({})
print(solution)

# SEVENTH
print("\nDegree, None, Inference")
csp = CSP(MapCSP, [var.name for var in variables], domains, 'degree', None, True)

# Adding constraints to the CSP based on the neighbor relationships
for var in variables:
    for neighbor in neighbors[var.name]:
        csp.add_constraint(Constraint_MP(var.name, neighbor), var.name)

# Calling the backtracking function to solve the CSP
solution = csp.backtracking({})
print(solution)

print("\n")

# EIGHTH
print("\nDegree, LCV, Inference")
csp = CSP(MapCSP, [var.name for var in variables], domains, 'degree', 'lcv', True)

# Adding constraints to the CSP based on the neighbor relationships
for var in variables:
    for neighbor in neighbors[var.name]:
        csp.add_constraint(Constraint_MP(var.name, neighbor), var.name)

# Calling the backtracking function to solve the CSP
solution = csp.backtracking({})
print(solution)

print("\n")



'''
Circuit-Board Layout Problem
'''
print("\n-----CIRCUIT BOARD LAYOUT PROBLEM-----")
components = ['a', 'b', 'c', 'e']
sizes = {'a': (3, 2), 'b': (5, 2), 'c': (2, 3), 'e': (7, 1)}

print("\nNone, None, False")
circuit_problem = CircuitBoardProblem(10, 3, components, sizes, var_heuristic=None, val_heuristic=None, inference=None)
solution = circuit_problem.backtracking({})
circuit_problem.display_solution(solution)

print("\nNone, LCV, False")
circuit_problem = CircuitBoardProblem(10, 3, components, sizes, var_heuristic=None, val_heuristic='lcv', inference=False)
solution = circuit_problem.backtracking({})
circuit_problem.display_solution(solution)

print("\nMRV, None, False")
circuit_problem = CircuitBoardProblem(10, 3, components, sizes, var_heuristic='mrv', val_heuristic=None, inference=False)
solution = circuit_problem.backtracking({})
circuit_problem.display_solution(solution)

print("\nMRV, LCV, False")
circuit_problem = CircuitBoardProblem(10, 3, components, sizes, var_heuristic='mrv', val_heuristic='lcv', inference=False)
solution = circuit_problem.backtracking({})
circuit_problem.display_solution(solution)

print("\nMRV, LCV, Inference")
circuit_problem = CircuitBoardProblem(10, 3, components, sizes, var_heuristic='mrv', val_heuristic='lcv', inference=True)
solution = circuit_problem.backtracking({})
circuit_problem.display_solution(solution)

print("\nMRV, None, Inference")
circuit_problem = CircuitBoardProblem(10, 3, components, sizes, var_heuristic='mrv', val_heuristic=None, inference=True)
solution = circuit_problem.backtracking({})
circuit_problem.display_solution(solution)

print("\nNone, LCV, Inference")
circuit_problem = CircuitBoardProblem(10, 3, components, sizes, var_heuristic=None, val_heuristic='lcv', inference=True)
solution = circuit_problem.backtracking({})
circuit_problem.display_solution(solution)
