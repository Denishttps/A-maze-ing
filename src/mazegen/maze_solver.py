from typing import Generator, Type
from .models.cell import Cell

from .models.maze import Maze
from .interfaces import BaseMazeSolver as MazeSolverBase

from .exceptions import MazeError
from .solver.bfs import BFSMazeSolver


class MazeSolver:
    SOLVER_MAP: dict[str, Type[MazeSolverBase]] = {
        'bfs': BFSMazeSolver,
    }

    @classmethod
    def solve(
        cls,
        maze: Maze,
        algo: str | Type[MazeSolverBase] = 'bfs'
    ) -> list[Cell] | None:
        for path in cls._build(maze, algo):
            pass
        return path or None

    @classmethod
    def solve_animated(
        cls,
        maze: Maze,
        algo: str | Type[MazeSolverBase] = 'bfs'
    ) -> Generator[list[Cell], None, None]:
        yield from cls._build(maze, algo, animated=True)

    @classmethod
    def _build(
        cls,
        maze: Maze,
        algo: str | Type[MazeSolverBase] = 'bfs',
        animated: bool = False
    ) -> Generator[tuple[list[Cell], bool] | list[Cell], None, None]:
        solver_class = algo
        if isinstance(algo, str):
            solver_class = cls.SOLVER_MAP.get(algo)

        if solver_class is None:
            raise MazeError(f"Unsupported solver: {algo}")

        solver = solver_class(maze)

        if animated:
            yield from solver.solve_step()
        else:
            yield solver.solve()
