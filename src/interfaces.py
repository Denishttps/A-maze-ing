from abc import ABC, abstractmethod
from typing import Protocol

from models.cell import Cell
from models.maze import Maze


class MazeAlgorithm(ABC):
    name: str
    _DIRECTIONS: list[tuple[int, int]] = [
        (0, -1),  # Up
        (1, 0),   # Right
        (0, 1),   # Down
        (-1, 0)   # Left
    ]

    def __init__(
        self,
        maze: Maze
    ):
        self.maze = maze

    @abstractmethod
    def generate(
        self,
        seed: int | None = None
    ) -> None:
        """Generate a maze with the specified parameters."""
        raise NotImplementedError()

    def _get_neighbors(
        self,
        cell: Cell,
        visited: bool | None = None
    ) -> list[Cell]:
        neighbors = []
        for dx, dy in self._DIRECTIONS:
            neighbor = self.maze.get_cell(cell.x + dx, cell.y + dy)
            if neighbor and not neighbor.blocked:
                if visited is None or neighbor.visited == visited:
                    neighbors.append(neighbor)
        return neighbors

    def _reset_visited(self) -> None:
        for row in self.maze.grid:
            for cell in row:
                cell.visited = False


class MazeHook(Protocol):
    def __call__(self, maze: Maze) -> Maze: ...
