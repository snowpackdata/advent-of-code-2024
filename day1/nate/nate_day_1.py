from collections import Counter

def read_file(location: str):
    with open(location, 'r') as f:
        return f.readlines()

def parse_content_to_output(readlines) -> ([int], [int]):
    listA = []
    listB = []
    for item in readlines:
        x, y = item.split()
        listA.append(int(x))
        listB.append(int(y))
    return listA, listB



def compare_lists(list_one: [int], list_two: [int]) -> int:
    assert len(list_one) == len(list_two), "lists must be the same length"
    list_one = sorted(list_one)
    list_two = sorted(list_two)
    distances = [abs(x-y) for x, y in zip(list_one, list_two)]
    total_distances =  sum(distances)
    return total_distances

def calculate_similarity_score(list_one: [int], list_two: [int]) -> int:
    # First create a corpus from list two
    list_two_corpus = Counter(list_two)
    total = 0
    for item in list_one:
        ct = list_two_corpus[item]
        if ct is None:
            multiplier = 0
        else:
            multiplier = ct
        total += (item * multiplier)
    return total

if __name__ == '__main__':
    filelines = read_file('./nate_input_1.1.txt')
    listA, listB = parse_content_to_output(filelines)
    output = compare_lists(listA, listB)
    print(f"Part 1: {output}")
    similarity_score = calculate_similarity_score(listA, listB)
    print(f"Part 2: {similarity_score}")


