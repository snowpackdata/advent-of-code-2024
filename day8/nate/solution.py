import math
import timeit
from dataclasses import dataclass
from collections import defaultdict
from typing import Any
from itertools import combinations, permutations


@dataclass
class Antenna:
    x : int
    y : int
    type : str
    def pos(self) -> tuple[int, int]:
        return self.x, self.y

@dataclass
class Line:
    slope : float
    intercept : float
    points: list[Antenna]
    def get_possible_locations(self, mapsize):
        locations = []
        max_x, max_y = mapsize
        # We will return locations at the line a +/-dx from our existing points
        assert self.points[0] != self.points[1]
        x1, y1 = self.points[0].pos()
        x2, y2 = self.points[1].pos()
        dx = abs(x1 - x2)
        high_x = max(x1, x2)
        low_x = min(x1, x2)
        while high_x <= max_x:
            y1 = self.slope* (high_x +dx) + self.intercept
            locations.append((high_x + dx, round(y1)))
            high_x += dx
        while low_x >= 0:
            y2 = self.slope* (low_x - dx) + self.intercept
            locations.append((low_x - dx, round(y2)))
            low_x -= dx
        return locations
def read_file(location: str):
    with open(location, 'r') as f:
        return f.readlines()

def parse_input(rowlist : list[str]) -> Any:
    # This puzzle is easier if we zero-index the map so that the first dot in the bottom left is at (1,1)
    height = len(rowlist)-1
    width = len(rowlist[0].strip('\n'))-1
    antennas = []
    for y, row in enumerate(rowlist):
        for x, val in enumerate(list(row.strip("\n"))):
            if val not in (".", "#"):
                antennas.append(Antenna(x, height-y, val))
    return antennas, (width, height)

def parse_antennae_to_lines(a: list[Antenna]) -> list[Line]:
    antennaedict = defaultdict(set)
    for i in a:
        antennaedict[str(i.type)].add(i.pos())
    lines = []
    for key in antennaedict.keys():
        for combo in combinations(antennaedict[key], 2):
            ant1, ant2 = combo
            A1 = Antenna(ant1[0], ant1[1], key)
            A2 = Antenna(ant2[0], ant2[1], key)
            lines.append(get_line_from_antenna(A1, A2))
    return lines

def get_line_from_antenna(antenna1 :Antenna, antenna2: Antenna) -> Line:
    x1, y1 = antenna1.pos()
    x2, y2 = antenna2.pos()
    if x1 == x2:
        raise ValueError("Need to support the vertical line case")
    if y1 == y2:
        raise ValueError("Need to support the horizontal line case")
    slope = (y2- y1)/(x2-x1)
    intercept = y1 - (slope * x1)
    return Line(slope, intercept, [antenna1, antenna2])

def position_is_valid(mapsize, point):
    max_x, max_y = mapsize
    x, y = point
    if x>max_x or x<0:
        return False
    if y>max_y or y<0:
        return False
    return True

def get_valid_locations(lines : list[Line], mapsize : tuple[int, int]) -> set[tuple[int, int]]:
    antenna_set = set()
    locations = set()
    for line in lines:
        for point in line.get_possible_locations(mapsize):
            antenna_set.add(line.points[0].pos())
            antenna_set.add(line.points[1].pos())
            if position_is_valid(mapsize, point):
                # round off the values and add them to the set
                x, y = point
                assert(abs(round(y)-y) < 0.0000001)
                locations.add((round(x), round(y)))
    return locations.union(antenna_set)

def solve_part_one(input_text) -> int:
    antennas, mapsize = parse_input(input_text)
    lines = parse_antennae_to_lines(antennas)
    locations = get_valid_locations(lines, mapsize)
    return len(locations)

def solve_part_two(input_text) -> int:
    antennas, mapsize = parse_input(input_text)
    lines = parse_antennae_to_lines(antennas)
    locations = get_valid_locations(lines, mapsize)
    return len(locations)

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
