from random import randint
from typing import Generator

from rich.live import Live

from dispatcher import Dispatcher
from models.theme import Theme

from models.maze import Maze
from utils.maze_config import make_maze_config

from utils.ui import build_ui, get_next_theme
from maze_solver import MazeSolver

from maze_generator import MazeGenerator
from renderer.ascii import AsciiMazeRenderer


dp = Dispatcher()
maze_config = make_maze_config()


@dp.startup
def startup(live: Live) -> None:
    maze = MazeGenerator.create(config=maze_config)
    dp.data['maze'] = maze
    theme = next(dp.data['theme_gen'])
    dp.data['theme'] = theme
    renderer = AsciiMazeRenderer(maze, colors=theme)
    live.update(build_ui(renderer.render(), maze_config.seed, dp.get_help(), maze.algo)) # noqa


@dp.shutdown
def shutdown() -> None:
    print("Bye!")


@dp.on('r', help="Regenerate the maze")
def regenerate_maze(live: Live, theme: Theme) -> None:
    maze_config.seed = randint(1, 100000000000000)
    maze = MazeGenerator.create(config=maze_config)
    dp.data['maze'] = maze
    renderer = AsciiMazeRenderer(maze, colors=theme, path=dp.data.get('path'))
    live.update(build_ui(renderer.render(), maze_config.seed, dp.get_help(), maze.algo)) # noqa


@dp.on('s', help="Swap colors")
def swap_colors(live: Live, maze: Maze, theme_gen: Generator) -> None:
    theme = next(theme_gen)
    dp.data['theme'] = theme
    renderer = AsciiMazeRenderer(maze, colors=theme, path=dp.data.get('path'))
    live.update(build_ui(renderer.render(), maze_config.seed, dp.get_help(), maze.algo)) # noqa


@dp.on('p', help="Show/hide the solution path")
def solve_maze(live: Live, maze: Maze, theme: Theme) -> None:
    if dp.data.get('path'):
        dp.data['path'] = None
    else:
        path = MazeSolver.solve(maze)
        dp.data['path'] = path
    renderer = AsciiMazeRenderer(maze, colors=theme, path=dp.data.get('path'))
    live.update(build_ui(renderer.render(), maze_config.seed, dp.get_help(), maze.algo)) # noqa


@dp.on('a', help="Animate the maze generation and solving")
def animate_maze_path(live: Live, theme: Theme) -> None:
    for maze in MazeGenerator.create_animated(config=maze_config):
        renderer = AsciiMazeRenderer(maze, colors=theme)
        live.update(build_ui(renderer.render(), maze_config.seed, dp.get_help(), maze.algo)) # noqa

    for path, is_final in MazeSolver.solve_animated(maze):
        renderer.connect = is_final
        renderer.path = path
        live.update(build_ui(renderer.render(), maze_config.seed, dp.get_help(), maze.algo)) # noqa
    dp.data['path'] = path


@dp.on("m", help="Animate the maze generation")
def animate_maze(live: Live, theme: Theme) -> None:
    for maze in MazeGenerator.create_animated(config=maze_config):
        renderer = AsciiMazeRenderer(maze, colors=theme)
        live.update(build_ui(renderer.render(), maze_config.seed, dp.get_help(), maze.algo)) # noqa


@dp.on("t", help="Animate the maze solving")
def animate_path(live: Live, maze: Maze, theme: Theme) -> None:
    renderer = AsciiMazeRenderer(maze, colors=theme)
    for path, is_final in MazeSolver.solve_animated(maze):
        renderer.connect = is_final
        renderer.path = path
        live.update(build_ui(renderer.render(), maze_config.seed, dp.get_help(), maze.algo)) # noqa
    dp.data['path'] = path


@dp.on('w', help="Swap algorithms")
def swap_algorithm(live: Live, maze: Maze, theme: Theme) -> None:
    algos = list(MazeGenerator.ALGO_MAP.keys())
    current_algo = maze_config.algo
    next_algo = algos[(algos.index(current_algo) + 1) % len(algos)]
    maze_config.algo = next_algo
    maze = MazeGenerator.create(config=maze_config)
    dp.data['maze'] = maze
    renderer = AsciiMazeRenderer(maze, colors=theme)
    live.update(build_ui(renderer.render(), maze_config.seed, dp.get_help(), maze.algo)) # noqa


@dp.on('q', help="Quit the application")
def quit_app() -> None:
    dp.stop()


def main():
    dp.data['theme_gen'] = get_next_theme()
    dp.run()


if __name__ == "__main__":
    main()
