"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

import random
from CSP import *


class SectionConstraint:
    def __init__(self, students, leaders):
        self.students = students
        self.leaders = leaders

    def satisfied(self, assignment):

        # ensure there's exactly one section leader in each section
        sections = {}
        for leader in self.leaders:
            if leader in assignment:
                if assignment[leader] in sections:
                    return False  # Another leader is already assigned to this section
                else:
                    sections[assignment[leader]] = []

        # ensure no student is in a section without a section leader
        for student in self.students:
            if student in assignment:
                if assignment[student] not in sections:
                    return False  # student is assigned to a section without a leader
                else:
                    sections[assignment[student]].append(student)

        # ensure each section has n/k - 1 <= students <= n/k + 1
        n = len(self.students)
        k = len(self.leaders)
        min_students = n // k - 1
        max_students = n // k + 1

        for section, students in sections.items():
            if not (min_students <= len(students) <= max_students):
                return False  # section has too few or too many students

        return True


class StudentSectionAssignment:

    def __init__(self, students, section_leaders, domains):
        self.students = students
        self.section_leaders = section_leaders
        self.domains = domains  # domains are available times
        self.constraints = []
        self.sections = {}  # to hold the assigned sections

    def get_neighbors(self, variable):
        # all students and section leaders are neighbors as they can potentially be in the same section
        return [v for v in self.students + self.section_leaders if v != variable]

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def assign_sections(self, csp_solution):
        for var, time in csp_solution.items():
            if time not in self.sections:
                self.sections[time] = {"section_leader": None, "students": []}

            if '*' in var:  # this is a section leader
                self.sections[time]["section_leader"] = var
            else:  # this is a student
                self.sections[time]["students"].append(var)


if __name__ == '__main__':
    if __name__ == '__main__':
        # List of students
        students = ['Student1', 'Student2', 'Student3', 'Student4', 'Student5']

        # List of section leaders
        section_leaders = ['*Leader1', '*Leader2']

        # Available times for sections
        times = ['Monday 4:00', 'Tuesday 5:00', 'Wednesday 6:00']

        # Assigning random available times to each student and section leader
        domains = {}
        for student in students:
            domains[student] = random.sample(times, random.randint(1, len(times)))

        for leader in section_leaders:
            domains[leader] = random.sample(times, random.randint(1, len(times)))

        # Print out the domains for visualization
        print("Domains (availabilities):")
        for person, available_times in domains.items():
            print(f"{person}: {', '.join(available_times)}")

        # Creating an instance of StudentSectionAssignment
        ssa = StudentSectionAssignment(students, section_leaders, domains)

        # Adding the SectionConstraint to StudentSectionAssignment
        section_constraint = SectionConstraint(students, section_leaders)
        ssa.add_constraint(section_constraint)

        # Creating an instance of CSP
        csp = CSP(ssa, students + section_leaders, domains, None, None, False)

        # Solving the CSP with backtracking
        solution = csp.backtracking({})

        if solution:
            print("\nSolution found:")
            for person, time in solution.items():
                print(f"{person} -> {time}")

            # Assigning students and section leaders to sections based on the solution
            ssa.assign_sections(solution)

            print("\nSections:")
            for time, info in ssa.sections.items():
                if info['section_leader'] is None:
                    print(f"Unassigned students based on availabilities: {info['students']}")
                else:
                    print(f"Time: {time}, Section Leader: {info['section_leader']}, Students: {', '.join(info['students'])}")

        else:
            print("No solution found.")





