from algo.dfs import DFSMazeGenerator
from interfaces import MazeAlgorithm

from models.cell_models import Cell
from random import Random

from typing import Type


class MazeGenerator:
    ALGO_MAP = {
        'dfs': DFSMazeGenerator,
        # 'prim': PrimMazeGenerator,
        # 'kruskal': KruskalMazeGenerator,
        # 'wilson': WilsonMazeGenerator,
        # 'hunt_and_kill': HuntAndKillMazeGenerator,
    }

    def __init__(
        self,
        width: int,
        height: int,
        entry_point: tuple,
        exit_point: tuple,
        perfect: bool = False
    ):
        self.width = width
        self.height = height
        self.entry_point = entry_point
        self.exit_point = exit_point
        self.perfect = perfect
        self.maze: list[list[Cell]] = self._initialize_maze()

    def _initialize_maze(self) -> list[list[Cell]]:
        return [
            [Cell(x=x, y=y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def generate_maze(
        self,
        seed: int | None = None,
        algo: str | None = None,
        custom_algo: Type[MazeAlgorithm] | None = None,
    ) -> list[list[Cell]]:

        entry = self.maze[self.entry_point[1]][self.entry_point[0]]

        algo_class = None

        if custom_algo:
            algo_class = custom_algo
        elif algo:
            algo_class = self.ALGO_MAP.get(algo)

        if algo_class is None:
            raise ValueError(f"Unknown algorithm: {algo}")

        algorithm = algo_class(
            maze=self.maze,
            width=self.width,
            height=self.height,
            entry=entry,
        )

        algorithm.generate(seed=seed)

        if not self.perfect:
            self.break_perfect()

        return self.maze

    def break_perfect(self, percent: float = 0.1, seed: int = None) -> None:
        rng = Random(seed)
        walls = []

        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze[y][x]
                if x < self.width - 1:
                    neighbor = self.maze[y][x + 1]

                    if cell.walls & Cell.RIGHT:
                        walls.append(
                            (cell, neighbor)
                        )
                if y < self.height - 1:
                    neighbor = self.maze[y + 1][x]
                    if cell.walls & Cell.BOTTOM:
                        walls.append(
                            (cell, neighbor)
                        )
        rng.shuffle(walls)
        remove_count = int(len(walls) * percent)

        for cell, neighbor in walls[:remove_count]:
            cell.remove_walls_between(neighbor)

    def add_blocked_area(
        self,
        start: str | tuple[int, int],
        width: int,
        height: int,
    ) -> None:
        start, end = self._get_coordinates(start, width, height)
        self._add_blocked_area(start, end)

    def _add_blocked_area(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> None:
        """Randomly block a percentage of the maze cells."""
        for y in range(start[1], end[1]):
            for x in range(start[0], end[0]):
                self.maze[y][x].blocked = True

    def _get_coordinates(
        self,
        start: str | tuple[int, int],
        width: int,
        height: int,
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        if isinstance(start, str):
            start = self._get_coordinates_by_str(start, width, height)
        end = (start[0] + width, start[1] + height)
        return start, end

    def _get_coordinates_by_str(
        self,
        start: str,
        width: int,
        height: int,
    ) -> tuple[int, int]:
        positions = {
            "x": {
                "center": self.width // 2 - width // 2,
                "right": self.width - width,
                "left": 0,
            },
            "y": {
                "center": self.height // 2 - height // 2,
                "bottom": self.height - height,
                "top": 0,
            }
        }
        x_str, y_str = start.split(":", 1)
        x = positions["x"].get(x_str)
        if x is None:
            try:
                x = int(x_str)
            except ValueError:
                raise ValueError(f"Invalid x position: {x_str}")

        y = positions["y"].get(y_str)
        if y is None:
            try:
                y = int(y_str)
            except ValueError:
                raise ValueError(f"Invalid y position: {y_str}")
        return x, y
