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


def _render_maze(live: Live, maze: Maze, theme: Theme) -> AsciiMazeRenderer:
    path = dp.data.get('path') if dp.data.get('is_path_shown') else None
    renderer = AsciiMazeRenderer(maze, colors=theme, path=path)
    live.update(build_ui(
        renderer.render(),
        maze_config.seed,
        dp.get_help(),
        maze.algo,
        theme.name
    ))
    return renderer


def _refresh_path(maze: Maze) -> None:
    if dp.data.get('path'):
        dp.data['path'] = MazeSolver.solve(maze)
        dp.data['is_new_maze'] = False


@dp.startup
def startup(live: Live) -> None:
    maze = MazeGenerator.create(config=maze_config)
    theme = next(dp.data['theme_gen'])
    dp.data['maze'] = maze
    dp.data['theme'] = theme
    dp.data['is_new_maze'] = True
    _render_maze(live, maze, theme)


@dp.shutdown
def shutdown() -> None:
    print("Bye!")


@dp.on('r', help="Regenerate the maze")
def regenerate_maze(live: Live, theme: Theme) -> None:
    maze_config.seed = randint(1, 100000000000000)
    maze = MazeGenerator.create(config=maze_config)
    dp.data['is_new_maze'] = True
    dp.data['maze'] = maze
    _refresh_path(maze)
    _render_maze(live, maze, theme)


@dp.on('s', help="Swap colors")
def swap_colors(live: Live, maze: Maze, theme_gen: Generator) -> None:
    theme = next(theme_gen)
    dp.data['theme'] = theme
    _render_maze(live, maze, theme)


@dp.on('p', help="Show/hide the solution path")
def solve_maze(live: Live, maze: Maze, theme: Theme) -> None:
    if dp.data.get('is_path_shown'):
        dp.data['is_path_shown'] = False
    else:
        dp.data['is_path_shown'] = True
        if dp.data.get('is_new_maze'):
            dp.data['path'] = MazeSolver.solve(maze)
            dp.data['is_new_maze'] = False

    _render_maze(live, maze, theme)


@dp.on('a', help="Animate the maze generation and solving")
def animate_maze_path(live: Live, theme: Theme) -> None:
    dp.data['is_path_shown'] = False
    for maze in MazeGenerator.create_animated(config=maze_config):
        renderer = _render_maze(live, maze, theme)

    for path, is_final in MazeSolver.solve_animated(maze):
        renderer.connect = is_final
        renderer.path = path
        live.update(build_ui(
            renderer.render(),
            maze_config.seed,
            dp.get_help(),
            maze.algo,
            theme.name
        ))
    dp.data['path'] = path
    dp.data['is_path_shown'] = True
    dp.data['is_new_maze'] = False


@dp.on("m", help="Animate the maze generation")
def animate_maze(live: Live, theme: Theme) -> None:
    for maze in MazeGenerator.create_animated(config=maze_config):
        _render_maze(live, maze, theme)


@dp.on("t", help="Animate the maze solving")
def animate_path(live: Live, maze: Maze, theme: Theme) -> None:
    renderer = AsciiMazeRenderer(maze, colors=theme)
    for path, is_final in MazeSolver.solve_animated(maze):
        renderer.connect = is_final
        renderer.path = path
        live.update(build_ui(
            renderer.render(),
            maze_config.seed,
            dp.get_help(),
            maze.algo,
            theme.name
        ))
    dp.data['path'] = path
    dp.data['is_path_shown'] = True
    dp.data['is_new_maze'] = False


@dp.on('w', help="Swap algorithms")
def swap_algorithm(live: Live, maze: Maze, theme: Theme) -> None:
    algos = list(MazeGenerator.ALGO_MAP.keys())
    current_algo = maze_config.algo
    next_algo = algos[(algos.index(current_algo) + 1) % len(algos)]
    maze_config.algo = next_algo
    maze = MazeGenerator.create(config=maze_config)
    dp.data['maze'] = maze
    _refresh_path(maze)
    _render_maze(live, maze, theme)


@dp.on('q', help="Quit the application")
def quit_app() -> None:
    dp.stop()


if __name__ == "__main__":
    dp.data['theme_gen'] = get_next_theme()
    dp.run(30)
