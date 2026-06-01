# algo/wilson.py
from random import Random
from interfaces import MazeAlgorithm
from models.cell import Cell


class WilsonMazeGenerator(MazeAlgorithm):
    name = 'wilson'

    def generate(self, seed: int | None = None) -> None:
        self._generate_wilson(seed)
        self._reset_visited()

    def _generate_wilson(self, seed: int | None = None) -> None:
        rng = Random(seed)

        unvisited = self.maze.get_unvisited()

        first = rng.choice(unvisited)
        first.visited = True
        unvisited.remove(first)

        while unvisited:
            cell = rng.choice(unvisited)
            path = [cell]
            path_set = {cell}

            while not cell.visited:
                neighbors = self._get_neighbors(cell)
                cell = rng.choice(neighbors)

                if cell in path_set:
                    loop_index = path.index(cell)
                    for c in path[loop_index + 1:]:
                        path_set.discard(c)
                    path = path[: loop_index + 1]
                else:
                    path.append(cell)
                    path_set.add(cell)

            for i in range(len(path) - 1):
                path[i].remove_walls_between(path[i + 1])
                path[i].visited = True
                if path[i] in unvisited:
                    unvisited.remove(path[i])

    def _get_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors = []
        for dx, dy in self._DIRECTIONS:
            neighbor = self.maze.get_cell(cell.x + dx, cell.y + dy)
            if neighbor and not neighbor.blocked:
                neighbors.append(neighbor)
        return neighbors
