from typing import Generator

from interfaces import MazeSolver
from models.cell import Cell

from collections import deque


class BFSMazeSolver(MazeSolver):
    name = "BFS"

    def solve(self) -> list[Cell] | None:
        """Solve the maze using the BFS algorithm."""
        for path in self._bfs():
            pass
        self.is_solved = False
        return path

    def solve_step(self) -> Generator[list[Cell] | None, None, None]:
        """Solve the maze step-by-step using the BFS algorithm."""
        yield from self._bfs()

    def _bfs(self) -> Generator[list[Cell] | None, None, None]:
        start = self.maze.entry
        end = self.maze.exit

        queue = deque([start])
        came_from: dict[Cell, Cell | None] = {start: None}

        while queue:
            cell = queue.popleft()

            if cell == end:
                self.is_solved = True
                path = self._reconstruct(came_from, end)
                for i in range(1, len(path) + 1):
                    yield path[:i]
                else:
                    yield path
                return

            for neighbor in self._get_passable_neighbors(cell):
                if neighbor in came_from:
                    continue
                came_from[neighbor] = cell
                queue.append(neighbor)
                yield list(came_from.keys())

        yield []

    def _reconstruct(
        self,
        came_from: dict[Cell, Cell | None],
        end: Cell
    ) -> list[Cell]:
        path = []

        cell = end
        while cell:
            path.append(cell)
            cell = came_from[cell]
        return path[::-1]

    def _get_passable_neighbors(self, cell: Cell) -> list[Cell]:
        passable = []

        for (dx, dy), wall in [
            ((0, -1), Cell.WEST),
            ((1, 0), Cell.SOUTH),
            ((0, 1), Cell.EAST),
            ((-1, 0), Cell.NORTH)
        ]:
            neighbor = self.maze.get_cell(cell.x + dx, cell.y + dy)
            if neighbor and not cell.has_wall(wall):
                passable.append(neighbor)
        return passable
