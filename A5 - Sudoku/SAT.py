"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

import random


class SAT:
    def __init__(self, cnf_filename):
        self.clauses = []  # list to store all the clauses from CNF file.
        self.value_to_index = {}  # maps variable names to their index.
        self.index_to_value = {}  # maps index to their variable names.
        self.assignment = []  # current truth assignment for the variables.
        self.max_iters = 100000  # maximum number of iterations for search algorithms.
        self.setup_problem(cnf_filename)  # set up SAT problem from CNF file.
        self.random_assignment()  # assign random boolean values to all variables.
        self.threshold = 0.7  # probability threshold for making decisions in search algorithms.

    '''
    Read CNF file and build the SAT problem
    '''
    def setup_problem(self, filename):
        with open(filename, "r") as file:
            count = 1
            for line in file:
                clause = []  # stores variables for each clause

                # iterate through literals in line/clause
                for s in line.split():
                    key = s[1:] if s[0] == "-" else s  # gets variable name

                    # if variable not already indexed, add to mappings and assignment list
                    if key not in self.value_to_index:
                        self.value_to_index[key] = count
                        self.index_to_value[count] = key
                        self.assignment.append(None)
                        count += 1

                    atom_index = self.value_to_index[key]
                    # append variable to clause (negative index if necessary)
                    clause.append(-atom_index if s[0] == "-" else atom_index)

                self.clauses.append(set(clause))
    '''
    Assign random boolean values to all variables
    '''
    def random_assignment(self):
        self.assignment = [random.choice([True, False]) for _ in self.assignment]

    '''
    Check if a specific clause is satisfied
    - Returns True if the provided clause is satisfied with the current assignment. 
    - Otherwise, returns False.
    '''
    def is_clause_satisfied(self, clause):
        for atom in clause:
            if atom > 0 and self.assignment[atom - 1]:
                return True
            elif atom < 0 and not self.assignment[-atom - 1]:
                return True
        return False

    '''
    Check if all clauses are satisfied with the current assignment
    -  Returns True if all are satisfied, otherwise returns False.
    '''
    def check_all_clauses(self):
        for clause in self.clauses:
            if not self.is_clause_satisfied(clause):  # Current clause is not satisfied
                return False
        return True  # All clauses were satisfied

    '''
    Counts how many clauses would be satisfied if the value at the given index is flipped
    '''
    def num_satisfied(self, index):

        count = 0
        # temporarily flip value at given index
        self.assignment[index] = not self.assignment[index]

        # count satisfied clauses
        for clause in self.clauses:
            if self.is_clause_satisfied(clause):
                count += 1

        # revert value at given index to its original state
        self.assignment[index] = not self.assignment[index]
        return count

    '''
    GSAT algorithm to find a satisfying assignment
    '''
    def gsat(self):
        for _ in range(self.max_iters):
            if self.check_all_clauses():
                return True

            # randomly decide whether to flip a random variable or the best one.
            if random.random() > self.threshold:
                rand_index = random.randint(0, len(self.assignment) - 1)
                self.assignment[rand_index] = not self.assignment[rand_index]
            else:
                # find the variable that, when flipped, satisfies the most clauses.
                satisfied_counts = [self.num_satisfied(i) for i in range(len(self.assignment))]
                max_count = max(satisfied_counts)
                highest_indices = [i for i, count in enumerate(satisfied_counts) if count == max_count]
                rand_index = random.choice(highest_indices)
                self.assignment[rand_index] = not self.assignment[rand_index]

        return False

    '''
    WalkSAT algorithm to find a satisfying assignment
    '''
    def walksat(self):
        for count in range(self.max_iters):
            if self.check_all_clauses():
                return True

            rand_index = random.randint(0, len(self.assignment) - 1)

            # randomly decide whether to flip a random variable or the best one in an unsatisfied clause.
            if random.random() > self.threshold:
                self.assignment[rand_index] = not self.assignment[rand_index]
            else:
                # get all unsatisfied clauses.
                unsat_clauses_indices = [
                    i for i, clause in enumerate(self.clauses)
                    if not self.is_clause_satisfied(clause)
                ]

                if not unsat_clauses_indices:
                    return True

                # select a random unsatisfied clause.
                rand_clause = self.clauses[random.choice(unsat_clauses_indices)]

                # for each variable in the clause, calculate the number of clauses that would be satisfied if it were flipped.
                candidates = [
                    (self.num_satisfied(abs(atom) - 1), abs(atom) - 1)
                    for atom in rand_clause
                ]

                # get the variable(s) that, when flipped, satisfies the most clauses.
                max_satisfied = max(candidates, key=lambda x: x[0])[0]
                best_indices = [
                    index for satisfied, index in candidates if satisfied == max_satisfied
                ]

                flip_var = random.choice(best_indices)
                self.assignment[flip_var] = not self.assignment[flip_var]

        return False

    '''
    Write the current assignment to a file
    '''
    def write_solution(self, filename):
        # generate the solution string based on the current assignment.
        solution = ''.join([f"{'-' if not self.assignment[i] else ''}{self.index_to_value[i + 1]}\n" for i in
                            range(len(self.assignment))])

        # write the solution string to the provided file.
        with open(filename, "w") as file:
            file.write(solution)


if __name__ == "__main__":
    pass
