from interfaces import MazeRenderer
from models.cell import Cell

from config import settings


class AsciiMazeRenderer(MazeRenderer[str]):
    name = 'ascii'

    def __init__(self, maze):
        super().__init__(maze)
        self.wall = settings.wall
        self.cell = settings.cell
        self.renderer = [[1] * (maze.width * 2 + 1) for _ in range(maze.height * 2 + 1)]

        # Theory
        # [
        # [1, 1, 1],
        # [1, 1, 1],
        # [1, 1, 1],

    def render(self) -> str:
        return self._render_ascii()

    def _render_ascii(self) -> str:
        return '\n'.join(self._render_row(y) for y in range(self.maze.height * 2 + 1))

    def _render_cell(self, cell: Cell, wall: int) -> str:
        if cell.has_wall(wall):
            return self.wall
        return self.cell

    def _render_row(self, y: int) -> str:
        pass

    def _render_cell_row(self, y: int) -> str:
        for cell in self.maze.grid[y]:
            self.renderer[y].append(self._render_cell(cell, Cell.WEST))
            self.renderer[y + 1].append(self._render_cell(cell, Cell.SOUTH))
