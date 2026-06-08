from rich import print
from maze_generator import MazeGenerator

from config import settings

from models.cell import Cell

from models.maze import Maze
from renderer.ascii import AsciiMazeRenderer

from solver.bfs import BFSMazeSolver
from hooks import BreakPerfect, Add42Pattern


width, height = 20, 10

maze = MazeGenerator.create(
    width=width,
    height=height,
    entry_point=(10, 9),
    exit_point=(19, 4),
    hooks=[
        BreakPerfect(percent=0.2, seed=42),
        Add42Pattern(),
    ],
    seed=420,
    algo="wilson",
)

colors = [
    (200, 200, 200),  # cell
    (37, 150, 190),   # wall
    (200, 200, 200),  # blocked wall
    (255, 255, 0),    # path
]

# maze.open_entry_exit()

path = BFSMazeSolver(maze).solve()

renderer = AsciiMazeRenderer(maze, path=path, colors=colors)

renderer.render()
renderer.display()
