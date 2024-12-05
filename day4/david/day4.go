package main

import (
	"bufio"
	"fmt"
	"os"
)

type Grid struct {
	cells [][]rune
	rows  int
	cols  int
}

type Direction struct {
	rowDelta int
	colDelta int
}

func LoadGridFromFile(filename string) *Grid {
	file, _ := os.Open(filename)
	defer file.Close()

	var rows [][]rune
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := scanner.Text()
		rows = append(rows, []rune(line))
	}

	return &Grid{
		cells: rows,
		rows:  len(rows),
		cols:  len(rows[0]),
	}
}

func (g *Grid) FindPatternCounts() (int, int) {
	xmasDirections := []Direction{
		{0, 1}, {0, -1}, {1, 0}, {-1, 0}, // horizontal and vertical
		{1, 1}, {1, -1}, {-1, 1}, {-1, -1}, // diagonals
	}

	// diagonal MAS directions
	masDirections := []Direction{
		{1, 1}, {1, -1}, {-1, 1}, {-1, -1},
	}

	xmasCount := 0
	// I didnt know how else to store this info
	masMap := make(map[struct{ row, col int }]map[Direction]bool)

	for row := 0; row < g.rows; row++ {
		for col := 0; col < g.cols; col++ {
			// XMAS
			for _, dir := range xmasDirections {
				if g.checkWord(row, col, "XMAS", dir) {
					xmasCount++
				}
			}

			// diagonal MAS
			for _, dir := range masDirections {
				if g.checkWord(row, col, "MAS", dir) {
					aRow := row + dir.rowDelta
					aCol := col + dir.colDelta
					key := struct{ row, col int }{aRow, aCol}

					if masMap[key] == nil {
						masMap[key] = make(map[Direction]bool)
					}
					masMap[key][dir] = true
				}
			}
		}
	}

	// count crossing points
	crossCount := 0
	for _, directions := range masMap {
		if len(directions) > 1 {
			crossCount++
		}
	}

	return xmasCount, crossCount
}

func (g *Grid) checkWord(startRow, startCol int, target string, dir Direction) bool {
	if startRow < 0 || startCol < 0 ||
		startRow >= g.rows || startCol >= g.cols {
		return false
	}

	endRow := startRow + (len(target)-1)*dir.rowDelta
	endCol := startCol + (len(target)-1)*dir.colDelta

	if endRow < 0 || endCol < 0 ||
		endRow >= g.rows || endCol >= g.cols {
		return false
	}

	for i := 0; i < len(target); i++ {
		currentRow := startRow + i*dir.rowDelta
		currentCol := startCol + i*dir.colDelta
		if g.cells[currentRow][currentCol] != rune(target[i]) {
			return false
		}
	}

	return true
}

func main() {
	grid := LoadGridFromFile("day4/david/input.txt")
	// grid := LoadGridFromFile("day4/david/test.txt")

	xmasCount, crossCount := grid.FindPatternCounts()
	fmt.Printf("XMAS Counts: %d\n", xmasCount)
	fmt.Printf("X-MAS: %d\n", crossCount)
}
