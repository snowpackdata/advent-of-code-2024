import itertools
import math
import timeit
from dataclasses import dataclass
import sys
import resource

from collections import defaultdict


def read_file(location: str):
    with open(location, 'r') as f:
        return f.readlines()[0]

def solve_part_one(input_text) -> int:
    data = decompress(input_text)
    first_index = data.index(".")
    cold_storage = data[0:first_index]
    memory = data[first_index:]
    output = defrag(cold_storage, memory, 0)
    return checksum(output)

def solve_part_two(input_text) -> int:
    data, cache, max_id = decompress_for_partial_frag(input_text)
    output = partial_defrag(data, cache, max_id)
    testing = [i.frag() for i in output]
    return checksum(list(itertools.chain(*testing)))

@dataclass
class Block:
    file : bool
    id: int
    count: int
    def __str__(self):
        if not self.file:
            return "."*self.count
        return str(self.id)*self.count
    def frag(self):
        if not self.file:
            return ["."] * self.count
        return [str(self.id)]*self.count
    def __repr__(self):
        if not self.file:
            return "."*self.count
        return str(self.id)*self.count


def decompress(text : str) -> (list[str]):
    fraglist = []
    id_value = 0
    memory_cache = defaultdict(Block)
    for i, val in enumerate(text):
        if i%2 == 0:
            block = Block(True, id_value, int(val))
            fraglist.append(block)
            memory_cache[id_value] = block
            id_value+=1
        else:
            if val == '0':
                continue
            fraglist.append(Block(False, id_value, int(val)))
    return list(itertools.chain(*fraglist))

def decompress_for_partial_frag(text : str) -> (list[Block], dict, int):
    fraglist = []
    id_value = 0
    memory_cache = defaultdict(Block)
    for i, val in enumerate(text):
        if i%2 == 0:
            block = Block(True, id_value, int(val))
            fraglist.append(block)
            memory_cache[id_value] = block
            id_value+=1
        else:
            if val == '0':
                continue
            fraglist.append(Block(False, id_value, int(val)))
    return fraglist, memory_cache, id_value-1

def defrag(cold_storage : list[str], memory :list[str], free_memory:int) -> list[str]:
    try:
        first_blank_spot = memory.index('.')
        # split the memory on the frag, move the last item on blocks to memory, and defrag blocks
        cold_storage = [*cold_storage, *memory[0:first_blank_spot]]
        moved_block = memory.pop()
        memory = memory[first_blank_spot + 1:]
        memory = [moved_block] + memory
        return defrag(cold_storage, memory, free_memory + 1)
    except ValueError:
        free_memory_str = ["."]*free_memory
        return [*cold_storage,*memory,*free_memory_str]

def find_first_available_memory_index(blocks : list[Block], size :int, max_index) -> (int, list[Block]):
    for i, block in enumerate(blocks):
        if i >= max_index:
            return -1, []
        if not block.file and block.count >= size:
            if block.count > size:
                return i, [Block(False, 0, block.count-size)]
            return i, []
    return -1, []

def find_block_memory_index(blocks : list[Block], id):
    for i, block in enumerate(blocks):
        if block.id == id and block.file:
            return i

# Recursively combine memory together
def sweep_memory(memory: list[Block]) -> list[Block]:
    if not memory:
        return []

    combined_memory = []
    current_block = memory[0]

    for block in memory[1:]:
        if not current_block.file and not block.file:
            current_block.count += block.count
        else:
            combined_memory.append(current_block)
            current_block = block

    combined_memory.append(current_block)
    return combined_memory

def partial_defrag(memory : list[Block], memory_cache :dict, max_block):
    # get value of last memory slot
    while max_block > 0:
        block = memory_cache[max_block]
        block_location = find_block_memory_index(memory, block.id)
        memory_location, resultant_block = find_first_available_memory_index(memory, block.count, block_location)
        if memory_location > 0:
            fileblock = memory[block_location]
            memory[block_location] = Block(False, id=0, count=fileblock.count)
            left_memory = memory[0:memory_location]
            right_memory = memory[memory_location+1:]
            if len(resultant_block) > 0:
                memory = left_memory + [block] + resultant_block + right_memory
            else:
                memory = left_memory + [block] + right_memory
            memory = sweep_memory(memory)
        max_block -=1
    return sweep_memory(memory)


def checksum(defragged_storage: list[str]) -> int:
    total = 0
    for i, x in enumerate(defragged_storage):
        if x != ".":
            total += i*int(x)
    return total

if __name__ == '__main__':
    # LOL at needing to do this
    # sys.setrecursionlimit(99999)
    input_text  = read_file('input.txt')
    # Solve Part One
    # start_time_one = timeit.default_timer()
    # solution_part_one = solve_part_one(input_text)
    # part_one_time = timeit.default_timer() - start_time_one

    start_time_two = timeit.default_timer()
    solution_part_two = solve_part_two(input_text)
    part_two_time = timeit.default_timer() - start_time_two
    # print(f"Solution to part 1: {solution_part_one} in {part_one_time*1000: .2f} ms")
    print(f"Solution to part 1: {solution_part_two} in {part_two_time * 1000: .2f} ms")
