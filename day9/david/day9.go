package main

import (
	"fmt"
	"os"
	"strconv"
)

func expandMap(diskMap string) []int {
	blocks := []int{}
	fileID := 0

	for i := 0; i < len(diskMap); i++ {
		length, _ := strconv.Atoi(string(diskMap[i]))

		if i%2 == 0 { // files
			for j := 0; j < length; j++ {
				blocks = append(blocks, fileID)
			}
			fileID++
		} else { // free space
			for j := 0; j < length; j++ {
				blocks = append(blocks, -1)
			}
		}
	}
	return blocks
}

// Part 1
func moveBlockByBlock(blocks []int) []int {
	result := make([]int, len(blocks))
	copy(result, blocks)

	for {
		// leftmost free space
		gapPos := -1
		for i, b := range result {
			if b == -1 {
				gapPos = i
				break
			}
		}
		if gapPos == -1 {
			break
		}

		// rightmost file block
		filePos := -1
		for i := len(result) - 1; i >= 0; i-- {
			if result[i] != -1 {
				filePos = i
				break
			}
		}
		if filePos < gapPos {
			break
		}

		result[gapPos] = result[filePos]
		result[filePos] = -1
	}
	return result
}

// Part 2
func moveWholeFiles(blocks []int) []int {
	result := make([]int, len(blocks))
	copy(result, blocks)

	// max file ID
	maxID := -1
	for _, b := range blocks {
		if b > maxID {
			maxID = b
		}
	}

	// files in decreasing order
	for fileID := maxID; fileID >= 0; fileID-- {
		// current file's location and size
		fileStart := -1
		fileSize := 0
		for i, b := range result {
			if b == fileID {
				if fileStart == -1 {
					fileStart = i
				}
				fileSize++
			}
		}
		if fileSize == 0 {
			continue
		}

		// leftmost valid gap before current position
		bestGapStart := -1
		currentGapStart := -1
		currentGapSize := 0

		for i := 0; i < fileStart; i++ {
			if result[i] == -1 {
				if currentGapStart == -1 {
					currentGapStart = i
				}
				currentGapSize++
				if currentGapSize >= fileSize {
					bestGapStart = currentGapStart
					break // Take the first valid gap
				}
			} else {
				currentGapStart = -1
				currentGapSize = 0
			}
		}

		// move the file
		if bestGapStart != -1 {
			for i := range result {
				if result[i] == fileID {
					result[i] = -1
				}
			}
			for i := 0; i < fileSize; i++ {
				result[bestGapStart+i] = fileID
			}
		}
	}
	return result
}

func calculateChecksum(blocks []int) int {
	checksum := 0
	for pos, fileID := range blocks {
		if fileID != -1 {
			checksum += pos * fileID
		}
	}
	return checksum
}

func main() {
	content, _ := os.ReadFile("day9/david/input.txt")
	diskMap := string(content)

	blocks := expandMap(diskMap)

	part1Blocks := moveBlockByBlock(blocks)
	checksum1 := calculateChecksum(part1Blocks)
	fmt.Printf("Part 1 Checksum: %d\n", checksum1)

	part2Blocks := moveWholeFiles(blocks)
	checksum2 := calculateChecksum(part2Blocks)
	fmt.Printf("Part 2 Checksum: %d\n", checksum2)
}
