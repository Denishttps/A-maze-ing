from typing import Generator
from interfaces import MazeAlgorithm

from random import Random
from models.maze import Maze


class DFSMazeGenerator(MazeAlgorithm):
    name = "dfs"

    def generate(self, seed: int | None = None) -> None:
        """Generate a maze using the Depth-First Search algorithm."""
        for _ in self._generate_dfs(seed):
            pass
        self._reset_visited()

    def generate_step(
        self,
        seed: int | None = None
    ) -> Generator[Maze, None, None]:
        """Generate a maze step-by-step using the Depth-First Search algorithm.""" # noqa
        yield from self._generate_dfs(seed)
        self._reset_visited()

    def _generate_dfs(
        self,
        seed: int | None = None
    ) -> Generator[Maze, None, None] | None:
        rng = Random(seed)
        stack = [self.maze.entry]
        self.maze.entry.visited = True

        while stack:
            current_cell = stack[-1]

            neighbors = self._get_neighbors(current_cell, visited=False)
            if neighbors:
                next_cell = rng.choice(neighbors)
                current_cell.remove_walls_between(next_cell)
                stack.append(next_cell)
                next_cell.visited = True
            else:
                stack.pop()
            yield self.maze
