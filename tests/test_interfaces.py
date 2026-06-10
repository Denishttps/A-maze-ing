"""Tests for src/interfaces.py — Abstract base classes and protocols."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from interfaces import MazeAlgorithm, MazeSolver, MazeRenderer, MazeHook
from models.maze import Maze
from models.cell import Cell


# ─────────────────────────────────────────────
# 1. MazeAlgorithm
# ─────────────────────────────────────────────


class TestMazeAlgorithmInterface:
    def test_has_name_attribute(self):
        from algo.dfs import DFSMazeGenerator
        maze = Maze(5, 5)
        algo = DFSMazeGenerator(maze)
        assert hasattr(algo, 'name')
        assert algo.name == "dfs"

    def test_has_directions(self):
        from algo.dfs import DFSMazeGenerator
        maze = Maze(5, 5)
        algo = DFSMazeGenerator(maze)
        assert hasattr(algo, '_DIRECTIONS')
        assert len(algo._DIRECTIONS) == 4

    def test_has_maze_attribute(self):
        from algo.dfs import DFSMazeGenerator
        maze = Maze(5, 5)
        algo = DFSMazeGenerator(maze)
        assert algo.maze is maze

    def test_generate_method_exists(self):
        from algo.dfs import DFSMazeGenerator
        maze = Maze(5, 5)
        algo = DFSMazeGenerator(maze)
        assert hasattr(algo, 'generate')
        assert callable(algo.generate)

    def test_generate_step_method_exists(self):
        from algo.dfs import DFSMazeGenerator
        maze = Maze(5, 5)
        algo = DFSMazeGenerator(maze)
        assert hasattr(algo, 'generate_step')
        assert callable(algo.generate_step)

    def test_get_neighbors_method(self):
        from algo.dfs import DFSMazeGenerator
        maze = Maze(5, 5)
        algo = DFSMazeGenerator(maze)
        cell = maze.grid[0][0]
        neighbors = algo._get_neighbors(cell, visited=False)
        assert isinstance(neighbors, list)


# ─────────────────────────────────────────────
# 2. MazeSolver
# ─────────────────────────────────────────────


class TestMazeSolverInterface:
    def test_has_name_attribute(self):
        from solver.bfs import BFSMazeSolver
        maze = Maze(5, 5)
        solver = BFSMazeSolver(maze)
        assert hasattr(solver, 'name')
        assert solver.name == "BFS"

    def test_has_directions(self):
        from solver.bfs import BFSMazeSolver
        maze = Maze(5, 5)
        solver = BFSMazeSolver(maze)
        assert hasattr(solver, '_DIRECTIONS')

    def test_has_maze_attribute(self):
        from solver.bfs import BFSMazeSolver
        maze = Maze(5, 5)
        solver = BFSMazeSolver(maze)
        assert solver.maze is maze

    def test_solve_method_exists(self):
        from solver.bfs import BFSMazeSolver
        maze = Maze(5, 5)
        solver = BFSMazeSolver(maze)
        assert hasattr(solver, 'solve')
        assert callable(solver.solve)

    def test_solve_step_method_exists(self):
        from solver.bfs import BFSMazeSolver
        maze = Maze(5, 5)
        solver = BFSMazeSolver(maze)
        assert hasattr(solver, 'solve_step')
        assert callable(solver.solve_step)


# ─────────────────────────────────────────────
# 3. MazeRenderer
# ─────────────────────────────────────────────


class TestMazeRendererInterface:
    def test_has_name_attribute(self):
        from renderer.ascii import AsciiMazeRenderer
        maze = Maze(5, 5)
        renderer = AsciiMazeRenderer(maze)
        assert hasattr(renderer, 'name')
        assert renderer.name == "ascii"

    def test_has_maze_attribute(self):
        from renderer.ascii import AsciiMazeRenderer
        maze = Maze(5, 5)
        renderer = AsciiMazeRenderer(maze)
        assert renderer.maze is maze

    def test_render_method_exists(self):
        from renderer.ascii import AsciiMazeRenderer
        maze = Maze(5, 5)
        renderer = AsciiMazeRenderer(maze)
        assert hasattr(renderer, 'render')
        assert callable(renderer.render)

    def test_display_method_exists(self):
        from renderer.ascii import AsciiMazeRenderer
        maze = Maze(5, 5)
        renderer = AsciiMazeRenderer(maze)
        assert hasattr(renderer, 'display')
        assert callable(renderer.display)


# ─────────────────────────────────────────────
# 4. MazeHook
# ─────────────────────────────────────────────


class TestMazeHookInterface:
    def test_hook_has_stage_attribute(self):
        from hooks.break_perfect import BreakPerfect
        hook = BreakPerfect()
        assert hasattr(hook, 'stage')

    def test_hook_stage_is_pre_or_post(self):
        from hooks.break_perfect import BreakPerfect
        hook = BreakPerfect()
        assert hook.stage in ["pre", "post"]

    def test_hook_is_callable(self):
        from hooks.break_perfect import BreakPerfect
        hook = BreakPerfect()
        assert callable(hook)

    def test_hook_accepts_maze_parameter(self):
        from hooks.break_perfect import BreakPerfect
        maze = Maze(5, 5)
        hook = BreakPerfect()
        result = hook(maze)
        assert isinstance(result, Maze)
