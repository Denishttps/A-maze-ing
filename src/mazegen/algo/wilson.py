from random import Random
from typing import Generator

from ..interfaces import MazeAlgorithm
from ..models.cell import Cell

from ..models.maze import Maze


class WilsonMazeGenerator(MazeAlgorithm):
    name = 'wilson'

    def generate(self, seed: int | None = None) -> None:
        for _ in self._generate_wilson(seed):
            pass
        self._reset_visited()

    def generate_step(
        self,
        seed: int | None = None
    ) -> Generator[Maze, None, None]:
        """Generate a maze step-by-step using Wilson's algorithm."""
        yield from self._generate_wilson(seed)
        self._reset_visited()

    def _generate_wilson(
        self,
        seed: int | None = None
    ) -> Generator[Maze, None, None]:
        rng = Random(seed)

        all_cells = self.maze.get_unvisited()
        rng.choice(all_cells).visited = True

        for start in all_cells:
            if start.visited:
                continue

            next_step: dict[Cell, Cell] = {}
            cell = start

            while not cell.visited:
                neighbor = rng.choice(self._get_neighbors(cell))
                next_step[cell] = neighbor
                cell = neighbor

            cell = start
            while not cell.visited:
                nxt = next_step[cell]
                cell.remove_walls_between(nxt)
                cell.visited = True
                cell = nxt
            yield self.maze
