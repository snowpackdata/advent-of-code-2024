package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {
	f, err := os.Open("day1/david/david_input1.txt")
	// f, err := os.Open("day1/david/david_test.txt")
	if err != nil {
		log.Fatal(err)
	}

	defer func(f *os.File) {
		err = f.Close()
		if err != nil {
			log.Fatal(err)
		}
	}(f)

	var column1 []int
	var column2 []int

	s := bufio.NewScanner(f)
	for s.Scan() {
		// Split the line by whitespace
		numbers := strings.Fields(s.Text())
		if len(numbers) == 2 {
			// Convert first number and append to column1
			num1, err := strconv.Atoi(numbers[0])
			if err != nil {
				log.Fatal(err)
			}
			column1 = append(column1, num1)

			// Convert second number and append to column2
			num2, err := strconv.Atoi(numbers[1])
			if err != nil {
				log.Fatal(err)
			}
			column2 = append(column2, num2)
		}
	}

	err = s.Err()
	if err != nil {
		log.Fatal(err)
	}

	// Sort both columns
	sort.Ints(column1)
	sort.Ints(column2)

	var differences []int
	for i := 0; i < len(column1); i++ {
		diff := int(math.Abs(float64(column1[i] - column2[i])))
		differences = append(differences, diff)
	}

	sum := 0
	for _, diff := range differences {
		sum += diff
	}

	// Create products list (number from column1 * frequency in column2)
	var products []int
	for _, num1 := range column1 {
		count := 0
		// Count occurrences in column2
		for _, num2 := range column2 {
			if num1 == num2 {
				count++
			}
		}
		product := num1 * count
		products = append(products, product)
	}

	pt2_sum := 0
	for _, diff := range products {
		pt2_sum += diff
	}

	// Print the sorted results
	// fmt.Println("Sorted Column 1:", column1)
	// fmt.Println("Sorted Column 2:", column2)
	// fmt.Println("Differences:    ", differences)
	fmt.Println("Part 1:", sum)
	fmt.Println("Part 2:", pt2_sum)
}
