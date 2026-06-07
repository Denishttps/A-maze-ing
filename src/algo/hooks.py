from interfaces import MazeHook
from utils.algo import break_perfect
from models.maze import Maze


class BreakPerfect(MazeHook):
    def __init__(self, percent: float = 0.1, seed: int | None = None):
        self.percent = percent
        self.seed = seed

    def __call__(self, maze: Maze) -> Maze:
        break_perfect(maze, percent=self.percent, seed=self.seed)
        return maze


class AddBlockedArea(MazeHook):
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
        maze.add_blocked_area(
            start=self.start,
            width=self.width,
            height=self.height,
            maze_resize=self.maze_resize
        )
        return maze
