import time

from rich import print
from maze_generator import MazeGenerator

from config import settings

from models.cell import Cell

from models.maze import Maze
from renderer.ascii import AsciiMazeRenderer

from solver.bfs import BFSMazeSolver
from hooks import BreakPerfect, Add42Pattern

from models.maze_config import MazeConfig

from rich.live import Live

from maze_solver import MazeSolver


cfg = MazeConfig(
    width=25,
    height=15,
    entry_point=(0, 0),
    exit_point=(24, 14),
    hooks=[
        Add42Pattern(),
        BreakPerfect(percent=0.1, seed=420)
    ],
    algo="prim",
)

maze = MazeGenerator.create(config=cfg)

colors = [
    (200, 200, 200),  # cell
    (37, 150, 190),   # wall
    (200, 200, 200),  # blocked wall
    (255, 255, 0),    # path
    (255, 0, 255),    # explored
    (255, 0, 0),      # entry/exit
]


path = MazeSolver.solve(maze)
renderer = AsciiMazeRenderer(maze, path, colors)
renderer.display()
# exit(0)
with Live(refresh_per_second=5) as live:
    for maze in MazeGenerator.create_animated(config=cfg):
        renderer = AsciiMazeRenderer(maze, colors=colors)
        live.update(renderer.render())
        # time.sleep(0.1)

    for path, is_final in MazeSolver.solve_animated(maze):
        renderer.connect = is_final
        renderer.path = path
        live.update(renderer.render())
        # time.sleep(0.1)
