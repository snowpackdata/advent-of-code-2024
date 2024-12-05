import itertools
from typing import Self
from collections import defaultdict


class Ruleset:
    # A Ruleset is used to store the meaning of tokens and the results of their comparators
    # this means that by accessing the dictionary of values we can easily determine if the
    # given rule that has been requested is valid or invalid.
    def __init__(self, corpus : list[str]):
        self._ruleset = defaultdict(dict)
        for rule in corpus:
            token_i, token_j = rule.strip("\n").split("|")
            self.add_rule(token_i, token_j)
    def add_rule(self, a : str, b: str):
        self._ruleset[a][b] = True
        self._ruleset[b][a] = False
        return
    def compare(self, page_lesser : str, page_greater : str) -> bool:
        result = self._ruleset[page_lesser][page_greater]
        if result is not None:
            return result
        return True

class Page:
    # Initialize a Page and build the magic classes to allow
    # comparison operators against objects of the same type, and summation with integers.
    # This will allow us simple comparisons and enable us to use out of the box sorting.
    def __init__(self, ruleset : Ruleset, token: str):
        self._token = token
        # if I was using a better language all versions of the page could share a pointer to the same
        # ruleset that was created separately but we can't do that with python. Each gets their own
        self._ruleset = ruleset
    def __lt__(self, other: Self):
        return self._ruleset.compare(self._token, other._token)
    def __le__(self, other: Self):
        return self._ruleset.compare(self._token, other._token)
    def __eq__(self, other: Self):
        return self._token == other._token
    def __ne__(self, other: Self):
        return self._token != other._token
    def __gt__(self, other: Self):
        return not self._ruleset.compare(self._token, other._token)
    def __ge__(self, other: Self):
        return not self._ruleset.compare(self._token, other._token)
    def __repr__(self):
        return self._token
    def __add__(self, other):
        return int(self._token) + other
    def __radd__(self, other):
        return int(self._token) + other

def read_file(location: str):
    with open(location, 'r') as f:
        return f.readlines()

def parse_file_to_pages(readlines: list[str], ruleset: Ruleset) -> list[list[Page]]:
    pages = []
    for row in readlines:
        pages_row = [Page(ruleset, x) for x in row.strip("\n").split(',')]
        pages.append(pages_row)
    return pages

def row_is_valid(row : list[Page]) -> bool:
    for i, j in itertools.combinations(row, 2):
        if i > j:
            return False
    return True

def solution_part_one(pages: list[list[Page]]) -> int:
    solution = 0
    for row in pages:
        if row_is_valid(row):
            solution += row[int(len(row)/2)]
    return solution

def solution_part_two(pages: list[list[Page]]) -> int:
    solution = 0
    for row in pages:
        if not row_is_valid(row):
            # Sorting works out of the box because we've properly defined type rulesets
            sorted_row = sorted(row)
            solution += sorted_row[int(len(row) / 2)]
    return solution

if __name__ == '__main__':
    rules = read_file('./input_rules.txt')
    ruleset = Ruleset(rules)
    inputtext = read_file('./input_pages.txt')
    pages = parse_file_to_pages(inputtext, ruleset)
    solution_part_one =  solution_part_one(pages)
    solution_part_two = solution_part_two(pages)
    print(f"Solution to part 1: {solution_part_one}")
    print(f"Solution to part 2: {solution_part_two}")
