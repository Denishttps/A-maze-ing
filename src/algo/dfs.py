from interfaces import MazeAlgorithm
from models.cell_models import Cell

from random import Random


class DFSMazeGenerator(MazeAlgorithm):
    def __init__(
        self,
        maze: list[list[Cell]],
        width: int,
        height: int,
        entry: Cell,
    ):
        super().__init__(maze, width, height, entry)
        self._DIRECTIONS = [
            (0, -1),  # Up
            (1, 0),   # Right
            (0, 1),   # Down
            (-1, 0)   # Left
        ]

    def generate(self, seed: int = None) -> list[list[Cell]]:
        """Generate a maze using the Depth-First Search algorithm."""
        self._generate_dfs(seed)
        self._reset_visited()
        return self.maze

    def _generate_dfs(self, seed: int = None) -> None:
        rng = Random(seed)
        stack = [self.entry]
        self.entry.visited = True

        while stack:
            current_cell = stack[-1]

            neighbors = self._get_unvisited_neighbors(current_cell)
            if neighbors:
                next_cell = rng.choice(neighbors)
                current_cell.remove_walls_between(next_cell)
                stack.append(next_cell)
                next_cell.visited = True
            else:
                stack.pop()

    def _get_unvisited_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors = []

        for dx, dy in self._DIRECTIONS:
            nx, ny = cell.x + dx, cell.y + dy

            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = self.maze[ny][nx]

                if not neighbor.visited and not neighbor.blocked:
                    neighbors.append(neighbor)

        return neighbors

    def _reset_visited(self) -> None:
        for row in self.maze:
            for cell in row:
                cell.visited = False
