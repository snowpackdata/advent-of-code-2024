from typing import Self, Any
import copy
import timeit
import numpy as np

class Direction:
    def __init__(self, direction : str):
        self.token = direction
        self.directions = {
            "^" : (-1, 0),
            ">" : (0, 1),
            "v" : (1, 0),
            "<" : (0, -1)
        }
    def vector(self) -> tuple[int, int]:
        return self.directions[self.token]
    def rotate(self):
        if self.token == "^":
            self.token = ">"
            return
        if self.token == ">":
            self.token = "v"
            return
        if self.token == "v":
            self.token = "<"
            return
        if self.token == "<":
            self.token = "^"
            return
        return
    def __repr__(self):
        return f"{self.token}"
class Actor:
    def __init__(self, initial_direction : str, initial_location : tuple[int, int]):
        self.initial_direction = Direction(initial_direction)
        self.initial_location = initial_location

        self.direction = Direction(initial_direction)
        self.location = initial_location
    def next_step(self) -> tuple[int, int]:
        return  tuple(map(sum, zip(self.location, self.direction.vector())))
    def walk(self):
        self.location = self.next_step()
    def turn(self):
        self.direction.rotate()
    def reset(self):
        self.direction = copy.deepcopy(self.initial_direction)
        self.location = copy.deepcopy(self.initial_location)
        return

class Cell:
    def __init__(self, location : tuple[int, int], cell_type : str, visited=0):
        if cell_type in ("<", ">", "^", "v"):
            self.cell_type = "."
            self.location = location
            self.visited = 1
            self.cycle = []
            return
        self.location = location
        self.cell_type = cell_type
        self.visited = visited
        self.cycle = []
        return
    def visit(self):
        self.visited = 1
        self.cell_type = "X"
    def is_obstruction(self, direction : Direction) -> bool:
        if self.cell_type in ("#", "O"):
            self.cycle.append(direction.token)
            return True
        return False
    def is_cycle(self, direction: Direction) -> bool:
        if direction.token in self.cycle:
            return True
        return False
    def __add__(self, other):
        if isinstance(other, Cell):
            return self.cycle + other.cycle
        return self.cycle + other
    def __radd__(self, other):
        if isinstance(other, Cell):
            return self.cycle + other.cycle
        return self.cycle + other
    def __repr__(self):
        return f"{self.cell_type}"
    def __str__(self):
        return self.cell_type

class Map:
    def __init__(self, size : tuple[int, int]):
        self.x, self.y = size
        self.map = np.full(size, Cell, dtype=Cell)
    def add_cell(self, cell: Cell):
        x, y = cell.location
        self.map[x][y] = cell
    def get_cell(self, loc : tuple[int, int]) -> Cell:
        return self.map.item(loc)
    def cell_exists(self, loc : tuple[int, int]) -> bool:
        x, y = loc
        if x < 0 or x >= self.x:
            return False
        if y < 0 or y >= self.y:
            return False
        return True
    def __repr__(self):
        return str(self.map)
    def __str__(self):
        return str(self.map)

class Solver:
    def __init__(self, cell_map : Map, actor : Actor):
        self.map = copy.deepcopy(cell_map)
        self.initial_map = copy.deepcopy(cell_map)
        self.solved_map = copy.deepcopy(cell_map)
        self.actor = actor
    def reset_map(self):
        self.map = copy.deepcopy(self.initial_map)
    def simulate(self) -> str:
        while True:
            if not self.next_step_valid():
                return "noncycle"
            if self.next_step_cycle():
                return "cycle"
            if self.next_step_obstructed():
                self.actor.turn()
                continue
            if not self.next_step_obstructed():
                self.actor.walk()
                self.map.get_cell(self.actor.location).visit()
                continue
    def next_step_valid(self) -> bool:
        return self.map.cell_exists(self.actor.next_step())
    def next_step_obstructed(self) -> bool:
        return self.map.get_cell(self.actor.next_step()).is_obstruction(self.actor.direction)
    def next_step_cycle(self) -> bool:
        return self.map.get_cell(self.actor.next_step()).is_cycle(self.actor.direction)
    def place_cycle_obstruction(self, loc: tuple[int,int]):
        self.map.get_cell(loc).cell_type = "O"
        return
    def simulate_with_obstruction(self, obs_location) -> int:
        self.reset_map()
        self.actor.reset()

        # Place the obstruction
        self.place_cycle_obstruction(obs_location)
        # Simulate and return result
        result = self.simulate()
        self.reset_map()
        self.actor.reset()
        if result == "cycle":
            return 1
        else:
            return 0
    def solve(self):
        result = self.simulate()
        self.solved_map = copy.deepcopy(self.map)
    def solve_part_two(self) -> int:
        solution = 0
        for i in range(self.map.x):
            for j in range(self.map.y):
                # Simulate by placing an obstruction on actual paths we visit
                if self.solved_map.get_cell((i,j)).cell_type == "X":
                    if self.actor.initial_location == (i, j):
                        continue
                    result = self.simulate_with_obstruction((i,j))
                    solution += result
        return solution

def read_file(location: str):
    with open(location, 'r') as f:
        return f.readlines()

def parse_file_to_solver(readlines: list[str]) -> Any:
    rows = len(readlines)
    cols = len(readlines[0].strip("\n"))
    cellMap = Map((rows,cols))
    for i, row in enumerate(readlines):
        for j, col in enumerate(row.strip("\n")):
            if col == "^":
                actor = Actor(col, (i, j))
            cellMap.add_cell(Cell((i, j), col))
    solver = Solver(cellMap, actor)
    return solver


def solution_part_one(solution: Solver):
    return solution.solve()

def solution_part_two(solution: Solver) -> int:
    return solution.solve_part_two()

if __name__ == '__main__':
    inputtext = read_file('./input.txt')
    solver = parse_file_to_solver(inputtext)
    # Solve Part One
    start_time = timeit.default_timer()
    solution_part_one(solver)
    part_one_time = timeit.default_timer() - start_time
    # Solve Part Two
    start_time_two = timeit.default_timer()
    solution_part_two = solution_part_two(solver)
    part_two_time = timeit.default_timer() - start_time_two
    # print(f"Solution to part 1: {solution_part_one} in {part_one_time*1000: .2f} ms")
    print(f"Solution to part 2: {solution_part_two} in {part_two_time*1000: .2f} ms")
