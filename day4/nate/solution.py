import itertools
"""Node
Defines any single location in the matrix of options -- it will allow us to trace the graph
and find neighbors to identify potential graph paths.
"""
import numpy as np


class Node:
    def __init__(self, value : str, index : tuple[int, int]):
        self.type = value
        self.index = index
        self.value = 0
        return
    def __repr__(self):
        return f"{self.type}: {self.index}"

class Solver:
    def __init__(self, rows : int, columns: int):
        self.rows = rows
        self.columns = columns
        self.matrix = np.full((rows, columns), dtype=Node, fill_value=None)
    def set_node(self, node: Node):
        self.matrix[node.index[0]][node.index[1]] = node
    def get_node(self, index: tuple[int, int]) -> Node:
        return self.matrix.item(index)
    def node_exists(self, index : tuple[int, int]) -> bool:
        x, y = index
        if (x < 0) or (x >= self.rows):
            return False
        if (y < 0) or (y >= self.columns):
            return False
        return True
    # def node_is_valid(self, node:Node, direction : tuple[int, int]) -> bool:
    #         return True
    def walk_to_next_node(self, current_node: Node, direction: tuple[int, int], depth: int) -> bool:
        if depth >3:
            return False
        next_location = (current_node.index[0] +direction[0], current_node.index[1]+direction[1])
        if not self.node_exists(next_location):
            return False
        next_node = self.get_node(next_location)
        if next_node.type == "S":
            return False
        if next_node.type == "X" and current_node.type == "M":
            next_node.value += 1
        if next_node.type == "M" and current_node.type == "A":
            self.walk_to_next_node(next_node, direction, depth+1)
        if next_node.type == "A" and current_node.type == "S":
            self.walk_to_next_node(next_node, direction, depth+1)
        return False

    def walk_to_next_node_secondary(self, current_node: Node, direction: tuple[int, int], depth:int) ->bool:
        if depth >2:
            return False
        next_location = (current_node.index[0] +direction[0], current_node.index[1]+direction[1])
        if not self.node_exists(next_location):
            return False
        next_node = self.get_node(next_location)
        if next_node.type == "S":
            return False
        if next_node.type == "X":
            return False
        if next_node.type == "M" and current_node.type == "A":
            current_node.value += 1
            return True
        if next_node.type == "A" and current_node.type == "S":
            self.walk_to_next_node_secondary(next_node, direction, depth+1)
        return False

    def solve(self):
        for index in list(itertools.product(range(self.rows), range(self.columns))):
            node = self.get_node(index)
            if node.type != "S":
                continue
            for direction in list(itertools.product(range(-1,2,1), range(-1,2,1))):
                if self.walk_to_next_node(node, direction, 0):
                    print("Found Solution")
        solution = 0
        for index in list(itertools.product(range(self.rows), range(self.columns))):
            solution += self.get_node(index).value
        return solution
    def solve_pt_2(self):
        for index in list(itertools.product(range(self.rows), range(self.columns))):
            node = self.get_node(index)
            if node.type != "S":
                continue
            for direction in list(itertools.product([-1, 1], [-1, 1])):
                if self.walk_to_next_node_secondary(node, direction, 0):
                    print("Found Solution")
        solution = 0
        for index in list(itertools.product(range(self.rows), range(self.columns))):
            if self.get_node(index).value == 2:
                solution +=1
        return solution


def read_file(location: str):
    with open(location, 'r') as f:
        return f.readlines()

def parse_content_to_output(readlines) -> Solver:
    # find the size
    solver = Solver(len(readlines), len(readlines[0].strip("\n")))
    for row_num, row in enumerate(readlines):
        for col_num, col in enumerate(list(row.strip("\n"))):
            node = Node(value=col, index=(row_num, col_num))
            solver.set_node(node)
    return solver


if __name__ == '__main__':
    filelines = read_file('./input.txt')
    solver = parse_content_to_output(filelines)
    solution_part_one = solver.solve()
    solution_part_two = solver.solve_pt_2()
    print(f"Solution to part 1: {solution_part_one}")
    print(f"Solution to part 2: {solution_part_two}")
