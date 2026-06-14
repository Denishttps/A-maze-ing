import sys

sys.path.append('.')
sys.path.append('src')


def main() -> None:
    from main import dp
    dp.run(refresh_per_second=60)


if __name__ == "__main__":
    try:
        if sys.argv[2] == "file_only":
            from main import maze_config
            from mazegen.maze_generator import MazeGenerator
            from mazegen.maze_solver import MazeSolver
            from utils.file import save_maze_to_file
            from config import settings

            maze = MazeGenerator.create(maze_config)
            path = MazeSolver.solve(maze)
            save_maze_to_file(maze, path, settings.output_file)
            exit(0)
    except IndexError:
        pass
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
