from rich import print
from maze_generator import MazeGenerator

from config import settings

from models.cell import Cell

from models.maze import Maze
from renderer.ascii import AsciiMazeRenderer

from solver.bfs import BFSMazeSolver
from hooks import BreakPerfect, Add42Pattern

from models.maze_config import MazeConfig


cfg = MazeConfig(
    width=20,
    height=10,
    entry_point=(19, 9),
    exit_point=(1, 1),
    hooks=[
        Add42Pattern(),
        BreakPerfect(percent=0.1, seed=420)
    ],
    algo="dfs"
)

maze = MazeGenerator.create(config=cfg)

colors = [
    (200, 200, 200),  # cell
    (37, 150, 190),   # wall
    (200, 200, 200),  # blocked wall
    (255, 255, 0),    # path
]

path = BFSMazeSolver(maze).solve()

renderer = AsciiMazeRenderer(maze, path=path, colors=colors)

renderer.render()
renderer.display()
