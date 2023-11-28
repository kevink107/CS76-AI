"""
Modified by: Kevin King
Dartmouth COSC 76, Fall 2023
"""

from SAT import SAT


class MapColoringProblem:
    def __init__(self, variables, neighbors, domains):
        self.variables = variables
        self.neighbors = neighbors
        self.domains = domains

    def setup_problem(self, filename):
        with open(filename, "w") as f:
            # assign at least one color to each region
            for variable in self.variables:
                colors = ' '.join([f"{variable}_{domain}" for domain in self.domains])
                f.write(colors + "\n")  # appending 0 to indicate the end of a clause
            
            # ensure each region only has one color
            for variable in self.variables:
                for i, color1 in enumerate(self.domains):
                    for color2 in self.domains[i+1:]:
                        f.write(f"-{variable}_{color1} -{variable}_{color2} 0\n")
            
            # ensure neighbors do not have the same color
            for var1, var2 in self.neighbors:
                for color in self.domains:
                    f.write(f"-{var1}_{color} -{var2}_{color}\n")

    def display_solution(self, filename):
        with open(filename, "r") as file:
            print("Solution:")
            print("\n".join([line.strip() for line in file if line.strip() and line[0] != '-']))


if __name__ == "__main__":
    MCP_test = MapColoringProblem(["WA", "NT", "SA", "Q", "NSW", "V", "T"],
                                  [("WA", "NT"), ("WA", "SA"), ("SA", "NSW"), ("SA", "Q"), ("SA", "V"), ("NT", "Q"), ("NT", "SA"), ("Q", "NSW"), ("NSW", "V")],
                                  ["red", "green", "blue"])

    MCP_test.setup_problem("test_mcp.cnf")
    s = SAT("test_mcp.cnf")

    if s.walksat():
        s.write_solution("test_mcp.sol")
        MCP_test.display_solution("test_mcp.sol")
    else:
        print("No solution found.")


