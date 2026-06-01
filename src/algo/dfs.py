from interfaces import MazeAlgorithm

from random import Random


class DFSMazeGenerator(MazeAlgorithm):
    name = "dfs"

    def generate(self, seed: int | None = None) -> None:
        """Generate a maze using the Depth-First Search algorithm."""
        self._generate_dfs(seed)
        self._reset_visited()

    def _generate_dfs(self, seed: int | None = None) -> None:
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
