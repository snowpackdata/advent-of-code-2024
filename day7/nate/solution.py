import os
import timeit
import copy

class Calibration:
    def __init__(self, text : str):
        conditions = text.split(":")
        self.target = int(conditions[0])
        self.inputs = [int(x) for x in conditions[1].strip("\n").split()]
        self.operands = ["+", "*"]
    def __repr__(self):
        return f"{self.target} : {self.inputs}"
    def __add__(self, other):
        if other.IsInstance(Calibration):
            return self.target + other.target
        return self.target + other
    def __radd__(self, other):
        try:
            if other.IsInstance(Calibration):
                return self.target + other.target
        except:
            return self.target + other
    def test_calibrations(self, calibration_list, operand : str) -> bool:
        deep_list = copy.deepcopy(calibration_list)
        # If the list is 0 then check value
        if len(calibration_list) == 1:
            return calibration_list[0] == self.target
        # If the current max value is already greater than the target we can return false as well
        if calibration_list[0] > self.target:
            return False
        if len(calibration_list) == 2:
            new_list = apply_operand(deep_list, operand)
            return self.test_calibrations(new_list, operand)
        # Split and check operands on both sides
        new_list = apply_operand(deep_list, operand)
        return self.test_calibrations(new_list, "+") or self.test_calibrations(new_list, "*")

    def test_calibrations_ternary(self, calibration_list, operand : str) -> bool:
        deep_list = copy.deepcopy(calibration_list)
        # If the list is 0 then check value
        if len(calibration_list) == 1:
            return calibration_list[0] == self.target
        # If the current max value is already greater than the target we can return false as well
        if calibration_list[0] > self.target:
            return False
        if len(calibration_list) == 2:
            new_list = apply_operand(deep_list, operand)
            return self.test_calibrations_ternary(new_list, operand)
        # Split and check operands on both sides
        new_list = apply_operand(deep_list, operand)
        return self.test_calibrations_ternary(new_list, "+") or self.test_calibrations_ternary(new_list, "*") or self.test_calibrations_ternary(new_list, "||")

def apply_operand(calibration_list : list[int], operand : str) -> list[int]:
    calibration_list.reverse()
    i = calibration_list.pop()
    j = calibration_list.pop()
    if operand == "+":
        out = i + j
        calibration_list.append(out)
        calibration_list.reverse()
        return calibration_list
    if operand == "*":
        out = i * j
        calibration_list.append(out)
        calibration_list.reverse()
        return calibration_list
    if operand == "||":
        out = str(i) + str(j)
        calibration_list.append(int(out))
        calibration_list.reverse()
        return calibration_list

def solve_part_one(calibrations : list[Calibration])-> int:
    solution = 0
    for c in calibrations:
        listcopy1 = copy.deepcopy(c.inputs)
        listcopy2 = copy.deepcopy(c.inputs)
        if c.test_calibrations(listcopy1, "+") or c.test_calibrations(listcopy2, "*"):
            solution += c.target
    return solution

def solve_part_two(calibrations: list[Calibration]) -> int:
    solution = 0
    for c in calibrations:
        listcopy1 = copy.deepcopy(c.inputs)
        listcopy2 = copy.deepcopy(c.inputs)
        if c.test_calibrations_ternary(listcopy1, "+") or c.test_calibrations_ternary(listcopy2, "*") or c.test_calibrations_ternary(listcopy2, "||"):
            solution += c.target
    return solution


def read_file(location: str):
    with open(location, 'r') as f:
        return f.readlines()

def parse_input(input : list[str]) -> list[Calibration]:
    calibrations = []
    for row in input:
        c = Calibration(row)
        calibrations.append(c)
    return calibrations


if __name__ == '__main__':
    print(os.getcwd())
    input = read_file('./nate/input.txt')
    calibrations = parse_input(input)
    # Solve Part One

    start_time = timeit.default_timer()
    solution_part_one = solve_part_one(calibrations)
    part_one_time = timeit.default_timer() - start_time
    # Solve Part Two
    start_time_two = timeit.default_timer()
    solution_part_two = solve_part_two(calibrations)
    part_two_time = timeit.default_timer() - start_time
    print(f"Solution to part 1: {solution_part_one} in {part_one_time*1000: .2f} ms")
    print(f"Solution to part 2: {solution_part_two} in {part_two_time*1000: .2f} ms")