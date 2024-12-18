package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func readInput(filename string) []int64 {
	file, _ := os.Open(filename)
	defer file.Close()
	scanner := bufio.NewScanner(file)
	scanner.Scan()
	var nums []int64
	for _, s := range strings.Fields(scanner.Text()) {
		n, _ := strconv.ParseInt(s, 10, 64)
		nums = append(nums, n)
	}
	return nums
}

func transformStones(stones []int64) []int64 {
	var result []int64
	for _, stone := range stones {
		if stone == 0 {
			result = append(result, 1)
		} else {
			s := strconv.FormatInt(stone, 10)
			if len(s)%2 == 0 {
				half := len(s) / 2
				left, _ := strconv.ParseInt(s[:half], 10, 64)
				right, _ := strconv.ParseInt(s[half:], 10, 64)
				result = append(result, left, right)
			} else {
				result = append(result, stone*2024)
			}
		}
	}
	return result
}

func countStones(stone int64, depth int, maxDepth int, memo map[string]int) int {
	if depth == maxDepth {
		return 1
	}

	key := fmt.Sprintf("%d_%d", stone, depth)
	if count, exists := memo[key]; exists {
		return count
	}

	var count int
	if stone == 0 {
		count = countStones(1, depth+1, maxDepth, memo)
	} else {
		s := strconv.FormatInt(stone, 10)
		if len(s)%2 == 0 {
			half := len(s) / 2
			left, _ := strconv.ParseInt(s[:half], 10, 64)
			right, _ := strconv.ParseInt(s[half:], 10, 64)
			count = countStones(left, depth+1, maxDepth, memo) +
				countStones(right, depth+1, maxDepth, memo)
		} else {
			count = countStones(stone*2024, depth+1, maxDepth, memo)
		}
	}

	memo[key] = count
	return count
}

func main() {
	stones := readInput("day11/david/input.txt")

	// Part 1 - SLOW
	part1 := make([]int64, len(stones))
	copy(part1, stones)
	for i := 0; i < 25; i++ {
		part1 = transformStones(part1)
	}
	fmt.Println("Part 1:", len(part1))

	// Part 2 - FAST
	memo := make(map[string]int)
	count := 0
	for _, stone := range stones {
		count += countStones(stone, 0, 75, memo)
	}
	fmt.Println("Part 2:", count)
}
