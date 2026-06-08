from config import Settings
from exceptions import MazeSizeError

from interfaces import MazeHook
from models import Maze


class Add42Pattern(MazeHook):
    stage = "pre"

    MIN_WIDTH = 8
    MIN_HEIGHT = 7

    def __call__(self, maze: Maze) -> Maze:
        if maze.width < self.MIN_WIDTH or maze.height < self.MIN_HEIGHT:
            raise MazeSizeError(
                f"Maze must be at least {self.MIN_WIDTH}x{self.MIN_HEIGHT} "
                "to fit the 42 pattern."
            )
        ox = maze.width // 2 - 4
        oy = maze.height // 2 - 2
        maze.add_blocked_cells(Settings.pattern_42, offset=(ox, oy))
        return maze
