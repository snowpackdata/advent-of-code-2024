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

type Pos struct {
	row, col int
	dir      rune
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

func (g *Grid) Clone() *Grid {
	cells := make([][]rune, g.rows)
	for i := range cells {
		cells[i] = make([]rune, g.cols)
		copy(cells[i], g.cells[i])
	}
	return &Grid{cells, g.rows, g.cols}
}

func (g *Grid) findLoopPositions() (int, map[Pos]bool) {
	moves := map[rune][2]int{'>': {0, 1}, 'v': {1, 0}, '<': {0, -1}, '^': {-1, 0}}
	next := map[rune]rune{'>': 'v', 'v': '<', '<': '^', '^': '>'}

	// find start
	var start Pos
	for r, row := range g.cells {
		for c, ch := range row {
			if _, ok := moves[ch]; ok {
				start = Pos{r, c, ch}
				break
			}
		}
	}

	path := make(map[Pos]bool)
	visited := make(map[[2]int]bool)

	pos := start
	visited[[2]int{pos.row, pos.col}] = true
	path[pos] = true

	// record the original path
	for {
		move := moves[pos.dir]
		newRow, newCol := pos.row+move[0], pos.col+move[1]

		if newRow < 0 || newRow >= g.rows || newCol < 0 || newCol >= g.cols {
			break
		}

		if g.cells[newRow][newCol] == '#' {
			pos.dir = next[pos.dir]
			path[pos] = true
		} else {
			pos.row, pos.col = newRow, newCol
			path[pos] = true
			if !visited[[2]int{pos.row, pos.col}] {
				visited[[2]int{pos.row, pos.col}] = true
			}
		}
	}

	// put wall in positions in the original path
	loopCount := 0
	for posOnPath := range path {
		if posOnPath == start {
			continue
		}

		grid := g.Clone()
		if grid.cells[posOnPath.row][posOnPath.col] != '.' {
			continue
		}
		grid.cells[posOnPath.row][posOnPath.col] = '#'

		// check for loop
		pos := start
		seenStates := make(map[Pos]bool)
		seenStates[pos] = true

		foundLoop := false
		for steps := 0; steps < len(path)*2; steps++ {
			move := moves[pos.dir]
			newRow, newCol := pos.row+move[0], pos.col+move[1]

			if newRow < 0 || newRow >= g.rows || newCol < 0 || newCol >= g.cols {
				break
			}

			if grid.cells[newRow][newCol] == '#' {
				pos.dir = next[pos.dir]
				if seenStates[pos] {
					foundLoop = true
					break
				}
				seenStates[pos] = true
			} else {
				pos.row, pos.col = newRow, newCol
				if seenStates[pos] {
					foundLoop = true
					break
				}
				seenStates[pos] = true
			}
		}

		if foundLoop {
			loopCount++
		}
	}

	return loopCount, path
}

func (g *Grid) countVisited() int {
	moves := map[rune][2]int{'>': {0, 1}, 'v': {1, 0}, '<': {0, -1}, '^': {-1, 0}}
	next := map[rune]rune{'>': 'v', 'v': '<', '<': '^', '^': '>'}

	var pos Pos
	for r, row := range g.cells {
		for c, ch := range row {
			if _, ok := moves[ch]; ok {
				pos = Pos{r, c, ch}
				break
			}
		}
	}

	visited := make(map[[2]int]bool)
	visited[[2]int{pos.row, pos.col}] = true
	count := 1

	for {
		move := moves[pos.dir]
		newRow, newCol := pos.row+move[0], pos.col+move[1]

		if newRow < 0 || newRow >= g.rows || newCol < 0 || newCol >= g.cols {
			break
		}

		if g.cells[newRow][newCol] == '#' {
			pos.dir = next[pos.dir]
		} else {
			g.cells[pos.row][pos.col] = 'X'
			pos.row, pos.col = newRow, newCol
			if !visited[[2]int{pos.row, pos.col}] {
				count++
				visited[[2]int{pos.row, pos.col}] = true
			}
		}
	}

	return count
}

func main() {
	grid := LoadGridFromFile("day6/david/input.txt")
	fmt.Printf("Part 1: %d\n", grid.countVisited())

	grid = LoadGridFromFile("day6/david/input.txt")
	loopCount, _ := grid.findLoopPositions()
	fmt.Printf("Part 2: %d\n", loopCount)
}
