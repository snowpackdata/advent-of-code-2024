package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

type Grid struct {
	cells      [][]rune
	rows, cols int
}

type Point struct {
	row, col int
}

func (g *Grid) String() string {
	var result string
	for _, row := range g.cells {
		result += string(row) + "\n"
	}
	return result
}

func LoadGridFromFile(filename string) *Grid {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var rows [][]rune
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		rows = append(rows, []rune(scanner.Text()))
	}
	return &Grid{rows, len(rows), len(rows[0])}
}

func (g *Grid) GetCharacterLocations() map[rune][]Point {
	locations := make(map[rune][]Point)
	for row := 0; row < g.rows; row++ {
		for col := 0; col < g.cols; col++ {
			char := g.cells[row][col]
			if char != '.' {
				locations[char] = append(locations[char], Point{row, col})
			}
		}
	}
	return locations
}

func (g *Grid) CalculatePositions(charLocations map[rune][]Point, extendLine bool) []Point {
	hashPositions := make(map[Point]bool)

	for _, positions := range charLocations {
		if len(positions) < 2 {
			continue
		}

		for i := 0; i < len(positions); i++ {
			for j := i + 1; j < len(positions); j++ {
				pos1 := positions[i]
				pos2 := positions[j]

				rowDiff := pos2.row - pos1.row
				colDiff := pos2.col - pos1.col

				if extendLine {
					// Part 2: Line-based calculation
					gcd := gcd(abs(rowDiff), abs(colDiff))
					if gcd == 0 {
						gcd = 1
					}

					stepRow := rowDiff / gcd
					stepCol := colDiff / gcd

					// Forward direction
					row := pos1.row
					col := pos1.col
					for row >= 0 && row < g.rows && col >= 0 && col < g.cols {
						hashPositions[Point{row, col}] = true
						row += stepRow
						col += stepCol
					}

					// Backward direction
					row = pos1.row - stepRow
					col = pos1.col - stepCol
					for row >= 0 && row < g.rows && col >= 0 && col < g.cols {
						hashPositions[Point{row, col}] = true
						row -= stepRow
						col -= stepCol
					}
				} else {
					// Part 1: Original calculation
					hash1 := Point{
						row: pos1.row - rowDiff,
						col: pos1.col - colDiff,
					}
					hash2 := Point{
						row: pos2.row + rowDiff,
						col: pos2.col + colDiff,
					}

					if hash1.row >= 0 && hash1.row < g.rows && hash1.col >= 0 && hash1.col < g.cols {
						hashPositions[hash1] = true
					}
					if hash2.row >= 0 && hash2.row < g.rows && hash2.col >= 0 && hash2.col < g.cols {
						hashPositions[hash2] = true
					}
				}
			}
		}
	}

	result := make([]Point, 0, len(hashPositions))
	for pos := range hashPositions {
		result = append(result, pos)
	}
	return result
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func gcd(a, b int) int {
	a = abs(a)
	b = abs(b)
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func main() {
	grid := LoadGridFromFile("day8/david/input.txt")
	charLocations := grid.GetCharacterLocations()

	fmt.Printf("Part 1: %d", len(grid.CalculatePositions(charLocations, false)))
	fmt.Printf("\nPart 2: %d\n", len(grid.CalculatePositions(charLocations, true)))
}
