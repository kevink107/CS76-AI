"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

import random


class SAT:
    def __init__(self, cnf_filename):
        self.max_iterations = 100000
        self.variables = []
        self.cnf_filename = cnf_filename
        self.clauses, self.var_map = self.setup_problem()
        self.threshold = 0.7
        self.solution = None

    # creates a set of sets of clauses, with each variable converted to an integer
    def setup_problem(self):
        with open(self.cnf_filename, 'r') as f:
            clauses = set()
            var_map = {}
            count = 1

            for line in f:
                clause = set()
                variables = line.split()

                for var in variables:
                    negated = var[0] == '-'
                    if negated:
                        var = var[1:]

                    if var not in var_map:
                        var_map[var] = count
                        self.variables.append(count)
                        count += 1

                    value = -var_map[var] if negated else var_map[var]
                    clause.add(value)

                clauses.add(frozenset(clause))

        return clauses, var_map

    # boolean satisfiability problem algorithm #1
    def gsat(self):
        assignment = self.random_assignment()
        for _ in range(self.max_iterations):
            if self.is_consistent(assignment):
                self.solution = assignment
                return True

            if random.random() > self.threshold:
                random_index = random.randint(1, len(assignment) - 1)
                assignment[random_index] = 1 - assignment[random_index]
            else:
                best_index = self.choose_variable(self.variables, assignment)
                assignment[best_index] = 1 - assignment[best_index]

        return False

    # walksat
    def walksat(self):
        assignment = self.random_assignment()
        for _ in range(self.max_iterations):
            if self.is_consistent(assignment):
                self.solution = assignment
                return True

            if random.random() > self.threshold:
                random_index = random.randint(1, len(assignment) - 1)
                assignment[random_index] = 1 - assignment[random_index]
            else:
                vars = self.get_candidates(assignment)
                best_index = self.choose_variable(vars, assignment)
                assignment[best_index] = 1 - assignment[best_index]

        return False

    def get_candidates(self, assignment):
        unsatisfied_clauses = [clause for clause in self.clauses
                               if not self.is_clause_satisfied(assignment, clause)]
        # select one at random
        random_clause = random.choice(unsatisfied_clauses)

        # get all the variables from that clause
        return list(random_clause)

    def random_assignment(self):
        return ['empty'] + [random.randint(0, 1) for _ in self.var_map]

    def choose_variable(self, variables, assignment):
        best_score = float('-inf')
        best_var_list = []

        for var in variables:
            score = self.num_clauses_satisfied(var, assignment)
            if score > best_score:
                best_score = score
                best_var_list = [var]
            elif score == best_score:
                best_var_list.append(var)

        return random.choice(best_var_list)

    # calculates the number of clauses satisfied by flipping a given variable in the assignment
    def num_clauses_satisfied(self, var, assignment):
        assignment_copy = assignment.copy()
        assignment_copy[var] = 1 - assignment_copy[var]
        count = 0
        for clause in self.clauses:
            if self.is_clause_satisfied(assignment_copy, clause):
                count += 1
        return count

    # returns true if a clause is satisfied given some assignment, false otherwise
    def is_clause_satisfied(self, assignment, clause):
        for var in clause:
            val = assignment[var]
            if (var < 0 and val == 0) or (var > 0 and val == 1):
                return True
        return False

    # returns true if assignment satisfies all clauses
    def is_consistent(self, assignment):
        for clause in self.clauses:
            if not self.is_clause_satisfied(assignment, clause):
                return False
        return True

    # writes the solution to a .sol file
    def write_solution(self, filename):
        if self.solution is None:
            print("Error: No satisfying assignment to write.")
            return

        with open(filename, 'w') as sol_filename:
            for var in range(1, len(self.solution)):
                var_str = next(key for key, val in self.var_map.items() if val == var)
                prefix = '-' if not self.solution[var] else ''
                sol_filename.write(f'{prefix}{var_str}\n')

    def resolution(self):
        clauses = set(self.clauses)
        new = set()

        while True:
            for c1 in clauses:
                for c2 in clauses:
                    resolvents = self.resolve(c1, c2)
                    if frozenset() in resolvents:
                        return False  # unsatisfiable
                    new |= resolvents

            if new.issubset(clauses):
                return True  # satisfiable, or can't deduce more information

            clauses |= new

    def resolve(self, c1, c2):
        resolvents = set()
        for p in c1:
            if -p in c2:
                new_clause = (c1 - {p}) | (c2 - {-p})
                resolvents.add(frozenset(new_clause))
        return resolvents


if __name__ == "__main__":
    # Generate CNF file for 2x2 Sudoku upper left block constraint
    with open('sudoku.cnf', 'w') as f:
        cells = ['S11', 'S12', 'S21', 'S22']
        numbers = ['1', '2']

        # Each cell must contain at least one number
        for cell in cells:
            f.write(' '.join([cell + num for num in numbers]) + ' 0\n')

        # Each number must appear at least once
        for num in numbers:
            f.write(' '.join([cell + num for cell in cells]) + ' 0\n')

        # No cell can contain two numbers
        for cell in cells:
            for i in range(len(numbers)):
                for j in range(i + 1, len(numbers)):
                    f.write(f'-{cell}{numbers[i]} -{cell}{numbers[j]} 0\n')

    # Use SAT solver to prove something about the encoded Sudoku problem
    sat = SAT('sudoku.cnf')
    print(sat.resolution())
