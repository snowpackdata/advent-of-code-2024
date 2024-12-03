package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

func isSafe(row []int) bool {
	if len(row) < 2 {
		return true
	}

	firstDiff := row[1] - row[0]
	isDecreasing := firstDiff < 0

	if math.Abs(float64(firstDiff)) < 1 || math.Abs(float64(firstDiff)) > 3 {
		return false
	}

	for i := 1; i < len(row)-1; i++ {
		diff := row[i+1] - row[i]
		absDiff := math.Abs(float64(diff))

		if absDiff < 1 || absDiff > 3 {
			return false
		}

		if isDecreasing {
			if diff >= 0 {
				return false
			}
		} else {
			if diff <= 0 {
				return false
			}
		}
	}
	return true
}

func isSafe2(row []int) bool {
	for skipIndex := 0; skipIndex < len(row); skipIndex++ {
		newRow := make([]int, 0)
		for i := 0; i < len(row); i++ {
			if i != skipIndex {
				newRow = append(newRow, row[i])
			}
		}
		if isSafe(newRow) {
			return true
		}
	}
	return false
}

func main() {
	f, err := os.Open("day2/david/input.txt")
	// f, err := os.Open("day2/david/test.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	var grid [][]int

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := scanner.Text()
		strNums := strings.Fields(line)
		row := make([]int, 0)

		for _, strNum := range strNums {
			num, err := strconv.Atoi(strNum)
			if err != nil {
				log.Fatal(err)
			}
			row = append(row, num)
		}

		grid = append(grid, row)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	// Print test
	// fmt.Println("Printing each row:")
	// for i, row := range grid {
	// 	fmt.Printf("Row %d: %v\n", i, row)
	// }

	safeRows := 0
	for _, row := range grid {
		isSafe := isSafe(row)
		if isSafe {
			safeRows++
		}
	}

	safeRows2 := 0
	for _, row := range grid {
		isSafe2 := isSafe2(row)
		if isSafe2 {
			safeRows2++
		}
	}

	fmt.Println("Part 1:", safeRows)
	fmt.Println("Part 2:", safeRows2)
}
