package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Equation struct {
	target int
	nums   []int
}

func loadEquations(filename string) []Equation {
	file, _ := os.Open(filename)
	defer file.Close()

	var equations []Equation
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		parts := strings.Split(scanner.Text(), ": ")
		target, _ := strconv.Atoi(parts[0])

		var nums []int
		for _, s := range strings.Fields(parts[1]) {
			n, _ := strconv.Atoi(s)
			nums = append(nums, n)
		}
		equations = append(equations, Equation{target, nums})
	}
	return equations
}

func evaluate(nums []int, ops []string) int {
	result := nums[0]
	for i := 0; i < len(ops); i++ {
		switch ops[i] {
		case "+":
			result += nums[i+1]
		case "*":
			result *= nums[i+1]
		case "||":
			resultStr := strconv.Itoa(result) + strconv.Itoa(nums[i+1])
			result, _ = strconv.Atoi(resultStr)
		}
	}
	return result
}

func tryPart1(eq Equation) bool {
	numOps := len(eq.nums) - 1
	for i := 0; i < (1 << numOps); i++ {
		ops := make([]string, numOps)
		for j := 0; j < numOps; j++ {
			if (i & (1 << j)) != 0 {
				ops[j] = "+"
			} else {
				ops[j] = "*"
			}
		}
		if evaluate(eq.nums, ops) == eq.target {
			return true
		}
	}
	return false
}

func pow(x, y int) int {
	result := 1
	for i := 0; i < y; i++ {
		result *= x
	}
	return result
}

func tryPart2(eq Equation) bool {
	numOps := len(eq.nums) - 1
	operators := []string{"+", "*", "||"}

	// Try all combinations: 3^numOps
	for i := 0; i < pow(3, numOps); i++ {
		ops := make([]string, numOps)
		temp := i
		for j := 0; j < numOps; j++ {
			ops[j] = operators[temp%3]
			temp /= 3
		}
		if evaluate(eq.nums, ops) == eq.target {
			return true
		}
	}
	return false
}

func main() {
	equations := loadEquations("day7/david/input.txt")

	sum1 := 0
	sum2 := 0
	for _, eq := range equations {
		if tryPart1(eq) {
			sum1 += eq.target
		}
		if tryPart2(eq) {
			sum2 += eq.target
		}
	}
	fmt.Printf("Part 1: %d\n", sum1)
	fmt.Printf("Part 2: %d\n", sum2)
}
