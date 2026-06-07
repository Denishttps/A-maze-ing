from algo.dfs import DFSMazeGenerator
from algo.kruskal import KruskalMazeGenerator

from algo.prim import PrimMazeGenerator
from algo.wilson import WilsonMazeGenerator

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

        for hook in pre_hooks or []:
            maze = hook(maze)

        algo_class = algo
        if isinstance(algo, str):
            algo_class = cls.ALGO_MAP.get(algo or '')

        if algo_class is None:
            raise ValueError(f"Unsupported algorithm: {algo}")

        algorithm = algo_class(maze=maze)

        algorithm.generate(seed=seed)

        maze.seed = seed
        maze.algorithm = algo_class.name

        for hook in post_hooks or []:
            maze = hook(maze)

        return maze
