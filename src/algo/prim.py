from typing import Generator
from interfaces import MazeAlgorithm
from exceptions import MazeError
from random import Random
from models.maze import Maze


class PrimMazeGenerator(MazeAlgorithm):
    name = 'prim'

    def generate(self, seed: int | None = None) -> None:
        for _ in self._generate_prim(seed):
            pass
        self._reset_visited()

    def generate_step(
        self,
        seed: int | None = None
    ) -> Generator[Maze, None, None]:
        """Generate a maze step-by-step using Prim's algorithm."""
        yield from self._generate_prim(seed)
        self._reset_visited()

    def _generate_prim(
        self,
        seed: int | None = None
    ) -> Generator[Maze, None, None]:
        rng = Random(seed)

        start = self.maze.get_cell(0, 0)
        if start is None:
            raise MazeError("Cannot generate maze: First cell (0,0) is missing or out of bounds.")  # noqa
        start.visited = True

        frontier = self._get_neighbors(start, visited=False)

        while frontier:
            cell = rng.choice(frontier)
            frontier.remove(cell)

            neighbors = self._get_neighbors(cell, visited=True)
            if neighbors:
                neighbor = rng.choice(neighbors)
                cell.remove_walls_between(neighbor)
                cell.visited = True
                frontier.extend(
                    c for c in self._get_neighbors(cell, visited=False)
                    if c not in frontier
                )
            yield self.maze
