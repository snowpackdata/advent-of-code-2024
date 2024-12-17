package main

import (
	"bufio"
	"fmt"
	"os"
)

type Point struct {
	row, col int
}

type Grid [][]int

func readInput(filename string) Grid {
	file, _ := os.Open(filename)
	defer file.Close()

	var grid Grid
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		row := make([]int, len(line))
		for i, ch := range line {
			row[i] = int(ch - '0')
		}
		grid = append(grid, row)
	}
	return grid
}

func calculateTrailheadScore(grid Grid, start Point) int {
	rows, cols := len(grid), len(grid[0])
	visited := make(map[Point]bool)
	reachableNines := make(map[Point]bool)

	var dfs func(current Point, currentHeight int)
	dfs = func(current Point, currentHeight int) {
		visited[current] = true

		if grid[current.row][current.col] == 9 {
			reachableNines[current] = true
			return
		}

		directions := []Point{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
		for _, dir := range directions {
			next := Point{current.row + dir.row, current.col + dir.col}
			if next.row >= 0 && next.row < rows && next.col >= 0 && next.col < cols {
				nextHeight := grid[next.row][next.col]
				if nextHeight == currentHeight+1 && !visited[next] {
					dfs(next, nextHeight)
				}
			}
		}
	}

	dfs(start, 0)
	return len(reachableNines)
}

func calculateTrailheadRating(grid Grid, start Point) int {
	rows, cols := len(grid), len(grid[0])
	memo := make(map[Point]int)

	var countPaths func(current Point, currentHeight int) int
	countPaths = func(current Point, currentHeight int) int {
		if val, exists := memo[current]; exists {
			return val
		}

		if grid[current.row][current.col] == 9 {
			memo[current] = 1
			return 1
		}

		paths := 0
		directions := []Point{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
		for _, dir := range directions {
			next := Point{current.row + dir.row, current.col + dir.col}
			if next.row >= 0 && next.row < rows && next.col >= 0 && next.col < cols {
				nextHeight := grid[next.row][next.col]
				if nextHeight == currentHeight+1 {
					paths += countPaths(next, nextHeight)
				}
			}
		}

		memo[current] = paths
		return paths
	}

	return countPaths(start, 0)
}

func main() {
	grid := readInput("day10/david/input.txt")
	totalScore := 0
	totalRating := 0
	rows, cols := len(grid), len(grid[0])

	for row := 0; row < rows; row++ {
		for col := 0; col < cols; col++ {
			if grid[row][col] == 0 {
				totalScore += calculateTrailheadScore(grid, Point{row, col})
				totalRating += calculateTrailheadRating(grid, Point{row, col})
			}
		}
	}
	fmt.Printf("Part 1 - Sum of trailhead scores: %d\n", totalScore)
	fmt.Printf("Part 2 - Sum of trailhead ratings: %d\n", totalRating)
}
