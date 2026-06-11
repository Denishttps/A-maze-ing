from typing import Type
from interfaces import MazeAlgorithm

from hooks.break_perfect import BreakPerfect
from hooks.pattern_42 import Add42Pattern

from models.maze_config import MazeConfig
from config import settings


def make_maze_config(
    algo: str | Type[MazeAlgorithm] = None,
) -> MazeConfig:
    hooks = [Add42Pattern()]
    if settings.perfect:
        hooks.append(BreakPerfect(percent=0.1, seed=420))
    return MazeConfig(
        width=settings.width,
        height=settings.height,
        entry_point=(0, 0),
        exit_point=(settings.width - 1, settings.height - 1),
        hooks=hooks,
        algo=algo or "prim",
        seed=settings.seed
    )
