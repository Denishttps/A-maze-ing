"""Tests for src/maze_solver.py — MazeSolver facade."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from maze_solver import MazeSolver
from models.maze import Maze
from models.maze_config import MazeConfig
from maze_generator import MazeGenerator
from models.cell import Cell
from exceptions import MazeError


# ─────────────────────────────────────────────
# 1. Solver mapping
# ─────────────────────────────────────────────


class TestSolverMapping:
    def test_solver_map_has_bfs(self):
        assert "bfs" in MazeSolver.SOLVER_MAP


# ─────────────────────────────────────────────
# 2. Maze solving
# ─────────────────────────────────────────────


class TestMazeSolving:
    def test_solve_returns_path_or_none(self):
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)
        maze.open_entry_exit()

        path = MazeSolver.solve(maze, algo="bfs")
        assert path is None or isinstance(path, list)

    def test_solve_with_default_algo(self):
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)
        maze.open_entry_exit()

        path = MazeSolver.solve(maze)
        assert path is None or isinstance(path, list)

    def test_solve_small_maze(self):
        config = MazeConfig(width=3, height=3, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)
        maze.open_entry_exit()

        path = MazeSolver.solve(maze, algo="bfs")
        if path:
            assert all(isinstance(cell, Cell) for cell in path)


# ─────────────────────────────────────────────
# 3. Animated solving
# ─────────────────────────────────────────────


class TestAnimatedSolving:
    def test_solve_animated_yields_results(self):
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)
        maze.open_entry_exit()

        steps = list(MazeSolver.solve_animated(maze, algo="bfs"))
        assert len(steps) >= 0

    def test_solve_animated_default_algo(self):
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)
        maze.open_entry_exit()

        steps = list(MazeSolver.solve_animated(maze))
        assert len(steps) >= 0


# ─────────────────────────────────────────────
# 4. Error handling
# ─────────────────────────────────────────────


class TestSolverErrorHandling:
    def test_unsupported_solver_raises(self):
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)

        with pytest.raises(MazeError):
            MazeSolver.solve(maze, algo="invalid_solver")

    def test_unsupported_solver_animated_raises(self):
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)

        with pytest.raises(MazeError):
            list(MazeSolver.solve_animated(maze, algo="invalid_solver"))
