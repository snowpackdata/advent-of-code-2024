import re

def read_file(location: str):
    with open(location, 'r') as f:
        return f.read()

def parse_content_to_output(readlines) -> [[int]]:
    return readlines

def solve_part_one(input_text : str) -> int:
    regex = re.compile('mul\((\d+)\,(\d+)\)')
    rolling_sum = 0
    for item in regex.findall(input_text):
        s1, s2 = item
        rolling_sum += (int(s1) * int(s2))
    return rolling_sum

def solve_part_two(input_text : str) -> int:
    rolling_sum = 0
    multiplier = 1
    # Match all do() don't() and mul() matches and name them for easier usage
    regex = re.compile('(?P<do>do\(\))|(?P<dont>don\'t)|mul\((?P<mult>(\d+)\,(\d+))\)')
    # create a match iterator
    for match in regex.finditer(input_text):
        # if we match a "do" then flip the multiplier to active
        if match.group(1):
           multiplier = max(multiplier, 1)
        # if we match a "dont" then flip the multiplier to inactive
        if match.group(2):
            multiplier = 0
        # if we match a mul(x,y) then retrieve them and multiply by the multiplier
        if match.group(3):
            rolling_sum += int(match.group(4)) * int(match.group(5)) * multiplier
    return rolling_sum

if __name__ == '__main__':
    filelines = read_file('./input.txt')
    output = parse_content_to_output(filelines)
    solution_part_one = solve_part_one(output)
    solution_part_two = solve_part_two(output)
    print(f"Solution to part 1: {solution_part_one}")
    print(f"Solution to part 2: {solution_part_two}")
