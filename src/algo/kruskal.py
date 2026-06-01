from random import Random

from interfaces import MazeAlgorithm
from models.cell import Cell


class KruskalMazeGenerator(MazeAlgorithm):
    name = 'kruskal'

    def generate(self, seed: int | None = None) -> None:
        self._generate_kruskal(seed)
        self._reset_visited()

    def _generate_kruskal(self, seed: int | None = None) -> None:
        rng = Random(seed)

        parent = {}
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.get_cell(x, y)
                if not cell.blocked:
                    parent[cell] = cell

        def find(cell: Cell) -> Cell:
            if parent[cell] != cell:
                parent[cell] = find(parent[cell])
            return parent[cell]

        def union(a: Cell, b: Cell) -> None:
            parent[find(a)] = find(b)

        def connected(a: Cell, b: Cell) -> bool:
            return find(a) == find(b)

        walls = []
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.get_cell(x, y)
                if cell.blocked:
                    continue
                for dx, dy in self._DIRECTIONS:
                    neighbor = self.maze.get_cell(x + dx, y + dy)
                    if neighbor and not neighbor.blocked:
                        walls.append((cell, neighbor))

        rng.shuffle(walls)

        for cell, neighbor in walls:
            if not connected(cell, neighbor):
                cell.remove_walls_between(neighbor)
                union(cell, neighbor)
                cell.visited = True
                neighbor.visited = True
