from src.interfaces import MazeHook
from src.models import Maze

from src.utils.algo import break_perfect


class BreakPerfect(MazeHook):
    stage = "post"

    def __init__(self, percent: float = 0.1, seed: int | None = None):
        self.percent = percent
        self.seed = seed

    def __call__(self, maze: Maze) -> Maze:
        break_perfect(maze, percent=self.percent, seed=self.seed)
        return maze
