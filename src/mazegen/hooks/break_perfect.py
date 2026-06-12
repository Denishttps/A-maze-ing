from random import Random
from ..interfaces import MazeHook

from ..models.cell import Cell
from ..models.maze import Maze


class BreakPerfect(MazeHook):
    stage = "post"

    def __init__(self, percent: float = 0.1, seed: int | None = None):
        self.percent = percent
        self.seed = seed

    def __call__(self, maze: Maze) -> Maze:
        self._break_perfect(maze)
        return maze

    def _break_perfect(
        self,
        maze: Maze
    ) -> None:
        rng = Random(self.seed)
        walls: list[tuple[Cell, Cell]] = []

        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.grid[y][x]

                if cell.blocked:
                    continue

                if x < maze.width - 1:
                    neighbor = maze.grid[y][x + 1]

                    if cell.walls & Cell.SOUTH and not neighbor.blocked:
                        walls.append((cell, neighbor))

                if y < maze.height - 1:
                    neighbor = maze.grid[y + 1][x]

                    if cell.walls & Cell.EAST and not neighbor.blocked:
                        walls.append((cell, neighbor))

        rng.shuffle(walls)
        remove_count = int(len(walls) * self.percent)

        for cell, neighbor in walls[:remove_count]:
            cell.remove_walls_between(neighbor)
