from collections import deque

from algo.dfs import DFSMazeGenerator
from algo.kruskal import KruskalMazeGenerator

from algo.prim import PrimMazeGenerator
from algo.wilson import WilsonMazeGenerator

from exceptions import (
    InvalidEntryExitError,
    MazeError,
    MazeSizeError
)
from models.maze import Maze
from typing import Type

from interfaces import MazeAlgorithm, MazeHook


class MazeGenerator:
    ALGO_MAP = {
        'dfs': DFSMazeGenerator,
        'prim': PrimMazeGenerator,
        'kruskal': KruskalMazeGenerator,
        'wilson': WilsonMazeGenerator,
    }

    @classmethod
    def create(
        cls,
        width: int,
        height: int,
        algo: str | Type[MazeAlgorithm] = "dfs",
        entry_point: tuple = (0, 0),
        exit_point: tuple | None = None,
        seed: int | None = None,
        hooks: list[MazeHook] | None = None
    ) -> Maze:
        maze = Maze(
            width=width,
            height=height,
            entry_point=entry_point,
            exit_point=exit_point or (width - 1, height - 1)
        )

        pre_hooks = [hook for hook in hooks or [] if hook.stage == "pre"]
        post_hooks = [hook for hook in hooks or [] if hook.stage == "post"]

        algo_class = algo
        if isinstance(algo, str):
            algo_class = cls.ALGO_MAP.get(algo or '')

        if algo_class is None:
            raise MazeError(f"Unsupported algorithm: {algo}")

        for hook in pre_hooks or []:
            maze = hook(maze)

        cls._validate(maze)

        algorithm = algo_class(maze=maze)
        algorithm.generate(seed=seed)

        maze.seed = seed
        maze.algorithm = algo_class.name

        for hook in post_hooks or []:
            maze = hook(maze)

        cls._valid_entry_exit(maze)

        return maze

    @staticmethod
    def _valid_entry_exit(maze: Maze) -> None:
        if not (maze.entry and maze.exit):
            raise InvalidEntryExitError(
                "Entry and exit points must be defined."
            )
        if maze.entry.blocked or maze.exit.blocked:
            raise InvalidEntryExitError(
                "Entry and exit points cannot be blocked."
            )
        if maze.entry == maze.exit:
            raise InvalidEntryExitError(
                "Entry and exit points cannot be the same."
            )

    @staticmethod
    def _is_connected(maze: Maze) -> bool:
        start = maze.entry
        if start.blocked:
            return False

        visited = set()
        queue = deque([start])
        visited.add((start.x, start.y))

        while queue:
            cell = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = maze.get_cell(cell.x + dx, cell.y + dy)
                if neighbor and not neighbor.blocked:
                    pos = (neighbor.x, neighbor.y)
                    if pos not in visited:
                        visited.add(pos)
                        queue.append(neighbor)

        total_free = sum(
            1 for row in maze.grid
            for cell in row
            if not cell.blocked
        )
        return len(visited) == total_free

    @classmethod
    def _validate(cls, maze: Maze) -> None:
        cls._valid_entry_exit(maze)
        if not cls._is_connected(maze):
            raise MazeSizeError("Blocked areas disconnect the maze.")
