import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Any
import timeit

import numpy as np


def read_file(location: str):
    with open(location, 'r') as f:
        return f.readlines()

@dataclass
class Coordinate:
    x : int
    y : int
    @property
    def loc(self):
        return self.x, self.y
    def dir(self, direction: tuple[int, int]):
        dx, dy = direction
        return self.x+dx, self.y+dy

class Cell:
    directions = [(0,1), (1,0), (0, -1), (-1, 0)]
    def __init__(self, coordinate: Coordinate, value : int):
        self.loc = coordinate
        self.value = value
        self.possible_paths = defaultdict(bool)
        self.is_dead_end = False
        for value in self.directions:
            self.possible_paths[value] = True
        self.routes = set()
    def __repr__(self):
        return f"{self.loc} : {self.value}"


def step_is_valid(current_cell : Cell, next_cell : Cell):
    if current_cell.value+1 == next_cell.value:
        return True
    return False


class Map:
    def __init__(self, height, width):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename="logging.log", encoding='utf-8', level=logging.DEBUG)
        self.height = height
        self.width = width
        self.map = np.full((width, height), dtype=Cell, fill_value=None)
        self.trailheads = defaultdict(int)
    def set_cell(self, cell: Cell):
        self.map[cell.loc.x][cell.loc.y] = cell
    def get_cell(self, index: tuple[int, int]) -> Cell:
        return self.map.item(index)
    def cell_exists(self, index: tuple[int, int]) -> bool:
        if index[0] >= self.width or index[0] < 0:
            return False
        if index[1] >= self.height or index[1] < 0:
            return False
        return True

    def walk_graph(self, start: Cell, c : Cell) -> int:
        self.logger.debug(f"At Cell {c}")
        if c.value == 9:
            start.routes.add(c.loc.loc)
            self.logger.debug(f"Found Peak {c}")
            return 1
        # Next we check the validity of each upcoming cell
        end_nodes = 0
        for direction in c.possible_paths.keys():
            # First check our cache and see if we've previously walked this path
            if not c.possible_paths[direction]:
                continue
            # If we haven't been on this path, find the index of the next cell
            next_index = add_tuples(c.loc.loc, direction)
            # If the cell doesn't exist update the cache and move on
            if not self.cell_exists(next_index):
                c.possible_paths[direction] = False
                continue
            next_cell = self.get_cell(next_index)
            # If step to the next cell is invalid update the cache and move on
            if not step_is_valid(c, next_cell):
                c.possible_paths[direction] = False
                continue
            # If the path is valid begin a new walk from the next cell
            end_nodes += self.walk_graph(start, next_cell)
        return end_nodes

def add_tuples(loc : tuple[int, int], direction : tuple[int,int]):
    x, y = loc
    dx, dy = direction
    return (x+dx, y+dy)

def parse_file_to_map(filerows : list[str]) -> Map:
    height = len(filerows)
    width = len(list(filerows[0].strip("\n")))
    cellmap = Map(height, width)
    for y, row in enumerate(filerows):
        for x, value in enumerate(list(row.strip("\n"))):
            if value == ".":
                cell = Cell(Coordinate(x, y), int(999))
            else:
                cell = Cell(Coordinate(x,y),int(value))
            cellmap.set_cell(cell)
            if value == "0":
                cellmap.trailheads[cell.loc.loc] = 0
    return cellmap

def solve_part_one(input: Any):
    cellmap = parse_file_to_map(input)
    total_routes = 0
    total_permutations = 0
    for trailhead in cellmap.trailheads:
        total_permutations += cellmap.walk_graph(cellmap.get_cell(trailhead), cellmap.get_cell(trailhead))
        total_routes += len(cellmap.get_cell(trailhead).routes)
    return total_routes

def solve_part_two(input: Any):
    cellmap = parse_file_to_map(input)
    total_routes = 0
    total_permutations = 0
    for trailhead in cellmap.trailheads:
        total_permutations += cellmap.walk_graph(cellmap.get_cell(trailhead), cellmap.get_cell(trailhead))
        total_routes += len(cellmap.get_cell(trailhead).routes)
    return total_permutations

if __name__ == '__main__':
    input_text  = read_file('input.txt')
    # Solve Part One
    start_time_one = timeit.default_timer()
    solution_part_one = solve_part_one(input_text)
    part_one_time = timeit.default_timer() - start_time_one

    start_time_two = timeit.default_timer()
    solution_part_two = solve_part_two(input_text)
    part_two_time = timeit.default_timer() - start_time_two
    print(f"Solution to part 1: {solution_part_one} in {part_one_time*1000: .2f} ms")
    print(f"Solution to part 1: {solution_part_two} in {part_two_time * 1000: .2f} ms")