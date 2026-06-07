from config import settings
from interfaces import MazeHook

from models.cell import Cell
from utils.algo import break_perfect

from models.maze import Maze


class BreakPerfect(MazeHook):
    stage = "post"

    def __init__(self, percent: float = 0.1, seed: int | None = None):
        self.percent = percent
        self.seed = seed

    def __call__(self, maze: Maze) -> Maze:
        break_perfect(maze, percent=self.percent, seed=self.seed)
        return maze


class AddBlockedArea(MazeHook):
    stage = "pre"

    def __init__(
        self,
        start: str | tuple[int, int],
        width: int,
        height: int,
        maze_resize: bool = False
    ):
        self.start = start
        self.width = width
        self.height = height
        self.maze_resize = maze_resize

    def __call__(self, maze: Maze) -> Maze:
        self.add_blocked_area(maze)
        return maze

    def add_blocked_area(
        self,
        maze: Maze
    ) -> None:
        if self.maze_resize:
            maze.width = self.width + maze.width
            maze.height = self.height + maze.height
            maze.grid = [
                [Cell(x=x, y=y) for x in range(maze.width)]
                for y in range(maze.height)
            ]
        start, end = self._get_coordinates(maze)
        if end[0] > maze.width or end[1] > maze.height:
            raise ValueError(
                "Blocked area exceeds maze boundaries."
            )
        self._add_blocked_area(maze)

    def _add_blocked_area(self, maze: Maze) -> None:
        for y in range(self.start[1], self.start[1] + self.height):
            for x in range(self.start[0], self.start[0] + self.width):
                maze.grid[y][x].blocked = True

    def _get_coordinates(
        self,
        maze: Maze
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        if isinstance(self.start, str):
            start = self._get_coordinates_by_str(maze)
        else:
            start = self.start
        end = (start[0] + self.width, start[1] + self.height)
        return start, end

    def _get_coordinates_by_str(
        self,
        maze: Maze
    ) -> tuple[int, int]:
        height = maze.height
        width = maze.width
        positions = {
            "x": {
                "center": width // 2 - self.width // 2 - self.width % 2,
                "right": width - self.width,
                "left": 0,
            },
            "y": {
                "center": height // 2 - self.height // 2 - self.height % 2,
                "bottom": height - self.height,
                "top": 0,
            }
        }
        x_str, y_str = self.start.split(":", 1)
        x = positions["x"].get(x_str)
        y = positions["y"].get(y_str)
        if x is None:
            try:
                x = int(x_str)
            except ValueError:
                raise ValueError(f"Invalid x position: {x_str}")
        if y is None:
            try:
                y = int(y_str)
            except ValueError:
                raise ValueError(f"Invalid y position: {y_str}")
        return x, y


class Add42Pattern(MazeHook):
    stage = "pre"

    def __call__(self, maze: Maze) -> Maze:
        ox = maze.width // 2 - 3
        oy = maze.height // 2 - 2
        maze.add_blocked_cells(settings.pattern_42, offset=(ox, oy))
        return maze
