"""Tests for src/utils/algo.py — Algorithm utilities."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils.algo import break_perfect
from models.maze import Maze
from models.maze_config import MazeConfig
from maze_generator import MazeGenerator


# ─────────────────────────────────────────────
# 1. Breaking perfect mazes
# ─────────────────────────────────────────────


class TestBreakPerfect:
    def test_break_perfect_basic(self):
        config = MazeConfig(width=10, height=10, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)

        # Count initial walls
        initial_walls = sum(
            1 for row in maze.grid
            for cell in row
            if cell.walls > 0
        )

        break_perfect(maze, percent=0.2, seed=42)

        # Count walls after breaking
        final_walls = sum(
            1 for row in maze.grid
            for cell in row
            if cell.walls > 0
        )

        # Should have fewer or equal walls (might be same if no walls to break)
        assert final_walls <= initial_walls

    def test_break_perfect_different_percentages(self):
        maze1 = Maze(5, 5)
        maze2 = Maze(5, 5)

        from algo.dfs import DFSMazeGenerator
        gen = DFSMazeGenerator(maze1)
        gen.generate(seed=42)

        # Copy maze1 to maze2
        for y in range(5):
            for x in range(5):
                maze2.grid[y][x].walls = maze1.grid[y][x].walls

        break_perfect(maze1, percent=0.05, seed=42)
        break_perfect(maze2, percent=0.2, seed=42)

        walls1 = sum(1 for row in maze1.grid for cell in row if cell.walls > 0)
        walls2 = sum(1 for row in maze2.grid for cell in row if cell.walls > 0)

        # Higher percentage should result in more walls broken
        assert walls2 <= walls1

    def test_break_perfect_respects_blocked_cells(self):
        maze = Maze(5, 5)
        maze.grid[2][2].blocked = True

        from algo.dfs import DFSMazeGenerator
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)

        break_perfect(maze, percent=0.2, seed=42)

        # Blocked cell should remain blocked
        assert maze.grid[2][2].blocked is True

    def test_break_perfect_zero_percent(self):
        maze = Maze(5, 5)
        from algo.dfs import DFSMazeGenerator
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)

        initial_state = [
            [cell.walls for cell in row]
            for row in maze.grid
        ]

        break_perfect(maze, percent=0.0, seed=42)

        final_state = [
            [cell.walls for cell in row]
            for row in maze.grid
        ]

        # Should be unchanged
        assert initial_state == final_state

    def test_break_perfect_with_seed(self):
        maze1 = Maze(5, 5)
        maze2 = Maze(5, 5)

        from algo.dfs import DFSMazeGenerator
        gen = DFSMazeGenerator(maze1)
        gen.generate(seed=42)

        # Copy maze1 to maze2
        for y in range(5):
            for x in range(5):
                maze2.grid[y][x].walls = maze1.grid[y][x].walls

        break_perfect(maze1, percent=0.1, seed=100)
        break_perfect(maze2, percent=0.1, seed=100)

        walls1 = [cell.walls for row in maze1.grid for cell in row]
        walls2 = [cell.walls for row in maze2.grid for cell in row]

        # Same seed should produce same result
        assert walls1 == walls2
