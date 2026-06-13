"""Tests for src/maze_generator.py — MazeGenerator facade."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from maze_generator import MazeGenerator
from models.maze_config import MazeConfig
from models.maze import Maze
from exceptions import MazeError, InvalidEntryExitError, MazeSizeError


# ─────────────────────────────────────────────
# 1. Algorithm mapping
# ─────────────────────────────────────────────


class TestAlgorithmMapping:
    def test_algo_map_has_dfs(self):
        assert "dfs" in MazeGenerator.ALGO_MAP

    def test_algo_map_has_prim(self):
        assert "prim" in MazeGenerator.ALGO_MAP

    def test_algo_map_has_kruskal(self):
        assert "kruskal" in MazeGenerator.ALGO_MAP

    def test_algo_map_has_wilson(self):
        assert "wilson" in MazeGenerator.ALGO_MAP

    def test_algo_map_values_are_classes(self):
        for algo_class in MazeGenerator.ALGO_MAP.values():
            assert callable(algo_class)


# ─────────────────────────────────────────────
# 2. Maze creation
# ─────────────────────────────────────────────


class TestMazeCreation:
    def test_create_basic_maze(self):
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)
        assert isinstance(maze, Maze)
        assert maze.width == 5
        assert maze.height == 5

    def test_create_with_prim(self):
        config = MazeConfig(width=5, height=5, algo="prim", seed=42)
        maze = MazeGenerator.create(config)
        assert isinstance(maze, Maze)

    def test_create_with_kruskal(self):
        config = MazeConfig(width=5, height=5, algo="kruskal", seed=42)
        maze = MazeGenerator.create(config)
        assert isinstance(maze, Maze)

    def test_create_with_wilson(self):
        config = MazeConfig(width=5, height=5, algo="wilson", seed=42)
        maze = MazeGenerator.create(config)
        assert isinstance(maze, Maze)

    def test_create_stores_seed(self):
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)
        assert maze.seed == 42

    def test_create_stores_algorithm(self):
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        maze = MazeGenerator.create(config)
        assert maze.algorithm == "dfs"

    def test_create_with_random_seed(self):
        config = MazeConfig(width=5, height=5, algo="dfs")
        maze = MazeGenerator.create(config)
        assert maze.seed is not None


# ─────────────────────────────────────────────
# 3. Animated generation
# ─────────────────────────────────────────────


class TestAnimatedGeneration:
    def test_create_animated_yields_mazes(self):
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        steps = list(MazeGenerator.create_animated(config))
        assert len(steps) > 0
        assert all(isinstance(step, Maze) for step in steps)

    def test_create_animated_final_maze_valid(self):
        config = MazeConfig(width=5, height=5, algo="dfs", seed=42)
        steps = list(MazeGenerator.create_animated(config))
        final_maze = steps[-1]
        assert final_maze.seed == 42
        assert final_maze.algorithm == "dfs"


# ─────────────────────────────────────────────
# 4. Entry and exit validation
# ─────────────────────────────────────────────


class TestEntryExitValidation:
    def test_invalid_entry_exit_same_point(self):
        config = MazeConfig(
            width=5, height=5, algo="dfs", seed=42,
            entry_point=(0, 0), exit_point=(0, 0)
        )
        with pytest.raises(InvalidEntryExitError):
            MazeGenerator.create(config)

    def test_valid_different_entry_exit(self):
        config = MazeConfig(
            width=5, height=5, algo="dfs", seed=42,
            entry_point=(0, 0), exit_point=(4, 4)
        )
        maze = MazeGenerator.create(config)
        assert maze.entry != maze.exit


# ─────────────────────────────────────────────
# 5. Error handling
# ─────────────────────────────────────────────


class TestErrorHandling:
    def test_unsupported_algorithm_raises(self):
        config = MazeConfig(width=5, height=5, algo="invalid_algo", seed=42)
        with pytest.raises(MazeError):
            MazeGenerator.create(config)

    def test_blocked_entry_raises(self):
        from hooks.blocked_area import AddBlockedArea
        hook = AddBlockedArea(start=(0, 0), width=1, height=1)
        config = MazeConfig(
            width=5, height=5, algo="dfs", seed=42,
            entry_point=(0, 0), hooks=[hook]
        )
        with pytest.raises(InvalidEntryExitError):
            MazeGenerator.create(config)

    def test_blocked_exit_raises(self):
        from hooks.blocked_area import AddBlockedArea
        hook = AddBlockedArea(start=(4, 4), width=1, height=1)
        config = MazeConfig(
            width=5, height=5, algo="dfs", seed=42,
            exit_point=(4, 4), hooks=[hook]
        )
        with pytest.raises(InvalidEntryExitError):
            MazeGenerator.create(config)
