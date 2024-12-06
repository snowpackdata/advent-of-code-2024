package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Pair struct {
	First, Second int
}

func parseFile(filename string) ([]Pair, [][]int) {
	file, _ := os.Open(filename)
	defer file.Close()
	scanner := bufio.NewScanner(file)
	pairs := make([]Pair, 0)
	sequences := make([][]int, 0)

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			break
		}
		var p Pair
		fmt.Sscanf(line, "%d|%d", &p.First, &p.Second)
		pairs = append(pairs, p)
	}

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}
		var seq []int
		for _, num := range strings.Split(line, ",") {
			var n int
			fmt.Sscanf(strings.TrimSpace(num), "%d", &n)
			seq = append(seq, n)
		}
		sequences = append(sequences, seq)
	}
	return pairs, sequences
}

func isValidSequence(seq []int, rules []Pair) bool {
	for _, rule := range rules {
		firstIdx, secondIdx := -1, -1
		for i, num := range seq {
			if num == rule.First {
				firstIdx = i
			}
			if num == rule.Second {
				secondIdx = i
			}
		}
		if firstIdx != -1 && secondIdx != -1 && firstIdx > secondIdx {
			return false
		}
	}
	return true
}

func fixSequence(seq []int, pairs []Pair) []int {
	result := make([]int, 0)
	nums := make(map[int]bool)
	for _, n := range seq {
		nums[n] = true
	}
	remaining := seq

	for len(result) < len(seq) {
	outer:
		for i, num := range remaining {
			for _, p := range pairs {
				if !nums[p.First] || !nums[p.Second] {
					continue
				}
				if num == p.Second {
					found := false
					for _, r := range result {
						if r == p.First {
							found = true
							break
						}
					}
					if !found {
						continue outer
					}
				}
			}
			result = append(result, num)
			remaining = append(remaining[:i], remaining[i+1:]...)
			break
		}
	}
	return result
}

func main() {
	pairs, sequences := parseFile("day5/david/input.txt")
	validSequences := make([][]int, 0)
	invalidSequences := make([][]int, 0)

	for _, seq := range sequences {
		if isValidSequence(seq, pairs) {
			validSequences = append(validSequences, seq)
		} else {
			invalidSequences = append(invalidSequences, seq)
		}
	}

	sum := 0
	for _, seq := range validSequences {
		sum += seq[len(seq)/2]
	}
	fmt.Printf("Part 1: %d\n", sum)

	sum2 := 0
	for _, seq := range invalidSequences {
		fixed := fixSequence(seq, pairs)
		sum2 += fixed[len(fixed)/2]
	}
	fmt.Printf("Part 2: %d\n", sum2)
}
