def read_file(location: str):
    with open(location, 'r') as f:
        return f.readlines()

def parse_content_to_output(readlines) -> [[int]]:
    output = []
    for item in readlines:
        values = list(map(int, item.split()))
        output.append(values)
    return output

def is_safe(input : [int]) -> bool:
    ascending = all([input[i] < input[i+1] for i in range(len(input)-1)])
    descending = all([input[i] > input[i+1] for i in range(len(input)-1)])
    step_size = all([abs(input[i] - input[i+1]) <4 for i in range(len(input)-1)])
    return (ascending or descending) and step_size

def solve_part_one(input_list : [[int]]) -> int:
     return sum(int(is_safe(x))for x in input_list)

def solve_part_two(input_list : [[int]]) -> int:
    # for each list get all sublists
    master_list = []
    counter = 0
    for subarray in input_list:
        counter += 1
        subsets = [subarray[:i] + subarray[i+1:] for i in range(len(subarray))]
        master_list.append(any(is_safe(i) for i in subsets))

    return sum(int(i) for i in master_list)


if __name__ == '__main__':
    filelines = read_file('./input.txt')
    listA = parse_content_to_output(filelines)
    solution_part_one = solve_part_one(listA)
    solution_part_two = solve_part_two(listA)
    print(f"Solution to part 1: {solution_part_one}")
    print(f"Solution to part 2: {solution_part_two}")
