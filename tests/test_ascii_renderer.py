"""Tests for src/renderer/ascii.py — ASCII maze rendering."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from renderer.ascii import AsciiMazeRenderer
from models.maze import Maze
from algo.dfs import DFSMazeGenerator


# ─────────────────────────────────────────────
# 1. Construction
# ─────────────────────────────────────────────


class TestAsciiRendererConstruction:
    def test_renderer_name_attribute(self):
        maze = Maze(5, 5)
        renderer = AsciiMazeRenderer(maze)
        assert renderer.name == "ascii"

    def test_renderer_stores_maze(self):
        maze = Maze(5, 5)
        renderer = AsciiMazeRenderer(maze)
        assert renderer.maze is maze

    def test_renderer_default_path_none(self):
        maze = Maze(5, 5)
        renderer = AsciiMazeRenderer(maze)
        assert renderer.path is None

    def test_renderer_custom_path(self):
        maze = Maze(5, 5)
        path = [maze.grid[0][0], maze.grid[1][1]]
        renderer = AsciiMazeRenderer(maze, path=path)
        assert renderer.path == path

    def test_renderer_default_colors(self):
        maze = Maze(5, 5)
        renderer = AsciiMazeRenderer(maze)
        assert len(renderer.colors) == 6

    def test_renderer_custom_colors(self):
        maze = Maze(5, 5)
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        renderer = AsciiMazeRenderer(maze, colors=colors)
        assert len(renderer.colors) == 6


# ─────────────────────────────────────────────
# 2. Rendering
# ─────────────────────────────────────────────


class TestAsciiRendering:
    def test_render_returns_string(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        maze.open_entry_exit()

        renderer = AsciiMazeRenderer(maze)
        output = renderer.render()
        assert isinstance(output, str)
        assert len(output) > 0

    def test_render_contains_newlines(self):
        maze = Maze(5, 5)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)

        renderer = AsciiMazeRenderer(maze)
        output = renderer.render()
        assert "\n" in output

    def test_render_dimensions_match_maze(self):
        maze = Maze(3, 3)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)

        renderer = AsciiMazeRenderer(maze)
        output = renderer.render()
        lines = output.strip().split("\n")
        # Renderer creates grid of size (height*2+1) x (width*2+1)
        assert len(lines) == maze.height * 2 + 1

    def test_render_with_path(self):
        maze = Maze(3, 3)
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)
        maze.open_entry_exit()

        path = [maze.entry, maze.exit]
        renderer = AsciiMazeRenderer(maze, path=path)
        output = renderer.render()
        assert isinstance(output, str)
        assert len(output) > 0


# ─────────────────────────────────────────────
# 3. Color management
# ─────────────────────────────────────────────


class TestColorManagement:
    def test_set_colors_default(self):
        maze = Maze(5, 5)
        renderer = AsciiMazeRenderer(maze, colors=None)
        assert len(renderer.colors) == 6

    def test_set_colors_custom(self):
        maze = Maze(5, 5)
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        renderer = AsciiMazeRenderer(maze, colors=colors)
        assert len(renderer.colors) == 6
        assert renderer.colors[0] == (255, 0, 0)

    def test_set_colors_invalid_length_uses_default(self):
        maze = Maze(5, 5)
        colors = [(255, 0, 0), (0, 255, 0)]  # Only 2 colors
        renderer = AsciiMazeRenderer(maze, colors=colors)
        # Should use default colors
        assert len(renderer.colors) == 6


# ─────────────────────────────────────────────
# 4. Blocked cells rendering
# ─────────────────────────────────────────────


class TestBlockedCellsRendering:
    def test_render_with_blocked_cells(self):
        maze = Maze(5, 5)
        maze.grid[2][2].blocked = True
        gen = DFSMazeGenerator(maze)
        gen.generate(seed=42)

        renderer = AsciiMazeRenderer(maze)
        output = renderer.render()
        assert isinstance(output, str)
        assert len(output) > 0
