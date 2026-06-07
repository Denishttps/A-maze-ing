from random import Random

from models.maze import Maze
from models.cell import Cell


def break_perfect(
    maze: Maze,
    percent: float,
    seed: int | None = None
) -> None:
    rng = Random(seed)
    walls = []

    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]

            if cell.blocked:
                continue

            if x < maze.width - 1:
                neighbor = maze.grid[y][x + 1]

                if cell.walls & Cell.SOUTH and not neighbor.blocked:
                    walls.append((cell, neighbor))

            if y < maze.height - 1:
                neighbor = maze.grid[y + 1][x]

                if cell.walls & Cell.EAST and not neighbor.blocked:
                    walls.append((cell, neighbor))

    rng.shuffle(walls)
    remove_count = int(len(walls) * percent)

    for cell, neighbor in walls[:remove_count]:
        cell.remove_walls_between(neighbor)
