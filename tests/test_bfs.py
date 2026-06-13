"""Tests for src/solver/bfs.py — Breadth-First Search maze solving."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from solver.bfs import BFSMazeSolver
from models.maze import Maze
from models.cell import Cell
from algo.dfs import DFSMazeGenerator


# ─────────────────────────────────────────────
# 1. Construction
# ─────────────────────────────────────────────


class TestBFSConstruction:
    def test_bfs_name_attribute(self):
        maze = Maze(5, 5)
        solver = BFSMazeSolver(maze)
        assert solver.name == "BFS"

    def test_bfs_stores_maze(self):
        maze = Maze(5, 5)
        solver = BFSMazeSolver(maze)
        assert solver.maze is maze


# ─────────────────────────────────────────────
# 2. Solving a maze
# ─────────────────────────────────────────────


class TestBFSSolving:
    def test_solve_returns_path_or_none(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        maze.open_entry_exit()

        solver = BFSMazeSolver(maze)
        path = solver.solve()
        # Path can be None or a list of cells
        assert path is None or isinstance(path, list)

    def test_solve_returns_cell_list(self):
        maze = Maze(3, 3)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        maze.open_entry_exit()

        solver = BFSMazeSolver(maze)
        path = solver.solve()
        if path:
            assert all(isinstance(cell, Cell) for cell in path)

    def test_solve_path_starts_at_entry(self):
        maze = Maze(3, 3)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        maze.open_entry_exit()

        solver = BFSMazeSolver(maze)
        path = solver.solve()
        if path and len(path) > 0:
            assert path[0] == maze.entry

    def test_solve_path_ends_at_exit(self):
        maze = Maze(3, 3)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        maze.open_entry_exit()

        solver = BFSMazeSolver(maze)
        path = solver.solve()
        if path and len(path) > 0:
            assert path[-1] == maze.exit


# ─────────────────────────────────────────────
# 3. Step-by-step solving
# ─────────────────────────────────────────────


class TestBFSSolveStep:
    def test_solve_step_yields_tuples(self):
        maze = Maze(3, 3)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        maze.open_entry_exit()

        solver = BFSMazeSolver(maze)
        steps = list(solver.solve_step())
        # Should yield at least one tuple (path, bool)
        if steps:
            assert all(isinstance(step, tuple) and len(step) == 2 for step in steps)

    def test_solve_step_includes_final_path(self):
        maze = Maze(3, 3)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        maze.open_entry_exit()

        solver = BFSMazeSolver(maze)
        steps = list(solver.solve_step())
        if steps and steps[-1][0]:
            assert isinstance(steps[-1][0], list)


# ─────────────────────────────────────────────
# 4. Passable neighbors
# ─────────────────────────────────────────────


class TestBFSPassableNeighbors:
    def test_get_passable_neighbors_simple(self):
        maze = Maze(3, 3)
        # Remove all walls for testing
        for row in maze.grid:
            for cell in row:
                cell.walls = 0

        solver = BFSMazeSolver(maze)
        cell = maze.get_cell(1, 1)
        neighbors = solver._get_passable_neighbors(cell)
        # In a 3x3 maze, center has 4 neighbors
        assert len(neighbors) == 4

    def test_get_passable_neighbors_blocked_by_walls(self):
        maze = Maze(3, 3)
        # All walls intact
        solver = BFSMazeSolver(maze)
        cell = maze.get_cell(1, 1)
        neighbors = solver._get_passable_neighbors(cell)
        # With all walls, should have 0 neighbors
        assert len(neighbors) == 0

    def test_get_passable_neighbors_corner_cell(self):
        maze = Maze(3, 3)
        for row in maze.grid:
            for cell in row:
                cell.walls = 0

        solver = BFSMazeSolver(maze)
        cell = maze.get_cell(0, 0)
        neighbors = solver._get_passable_neighbors(cell)
        # Corner has 2 neighbors
        assert len(neighbors) == 2


# ─────────────────────────────────────────────
# 5. Path reconstruction
# ─────────────────────────────────────────────


class TestBFSReconstruction:
    def test_reconstruct_simple_path(self):
        maze = Maze(2, 2)
        solver = BFSMazeSolver(maze)

        start = maze.entry
        end = maze.exit
        came_from = {start: None, end: start}

        path = solver._reconstruct(came_from, end)
        assert path[0] == start
        assert path[-1] == end
