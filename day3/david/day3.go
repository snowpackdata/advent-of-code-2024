package main

import (
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
)

func main() {
	content, err := os.ReadFile("day3/david/input.txt")
	// content, err := os.ReadFile("day3/david/test.txt")
	if err != nil {
		log.Fatal(err)
	}
	text := string(content)
	// fmt.Println(text)

	pattern := regexp.MustCompile(`mul\(([0-9]{1,3}),([0-9]{1,3})\)`)

	matches := pattern.FindAllStringSubmatch(text, -1)

	sum := 0
	for _, match := range matches {
		num1, err := strconv.Atoi(match[1])
		if err != nil {
			log.Fatal(err)
		}
		num2, err := strconv.Atoi(match[2])
		if err != nil {
			log.Fatal(err)
		}
		product := num1 * num2
		sum += product
	}
	fmt.Printf("Sum of all products: %d\n", sum)

	// this was the absolute worst to try to figure out so I just asked claude for the regex
	dodontPattern := regexp.MustCompile(`(mul\(([0-9]{1,3}),([0-9]{1,3})\)|do\(\)|don't\(\))`)
	matches2 := dodontPattern.FindAllStringSubmatch(text, -1)

	sum2 := 0
	enabled := true

	for _, match := range matches2 {
		operation := match[0]
		// do or do not
		if operation == "do()" {
			enabled = true
			continue
		}
		if operation == "don't()" {
			enabled = false
			continue
		}
		// if do
		if enabled {
			num1, err := strconv.Atoi(match[2])
			if err != nil {
				log.Fatal(err)
			}
			num2, err := strconv.Atoi(match[3])
			if err != nil {
				log.Fatal(err)
			}

			product := num1 * num2
			sum2 += product
		}
	}
	fmt.Printf("Sum of all enabled products: %d\n", sum2)
}
