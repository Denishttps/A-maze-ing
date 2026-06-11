import sys
import os
from pathlib import Path

from solver.bfs import BFSMazeSolver
from hooks.pattern_42 import Add42Pattern
from models.maze_config import MazeConfig
from config import settings
from maze_generator import MazeGenerator
from renderer.ascii import AsciiMazeRenderer
import random  # for generating random colors


def clear_screen() -> None:
    """ Clears the terminal screen. Works on both Windows and Unix-like systems."""  # noqa: E501
    os.system('cls' if os.name == 'nt' else 'clear')


def main() -> None:
    print("🎯 Welcome to A-MAZE-ING!")
    if len(sys.argv) != 2:
        print("Usage: python a_maze_ing.py config.txt")
        return
    config_path = sys.argv[1]
    if not Path(config_path).exists():
        print(f"✗ Config file not found: {config_path}")
        return
    current_seed = settings.seed
    current_colors = [
        (200, 200, 0),  # 0:  paths colors
        (120, 50, 150),  # 1:  walls colors
        (70, 110, 150),  # 2:  blocked colors
        (255, 55, 100)  # 3:  solotion path color
    ]
    game_config = MazeConfig(
        height=settings.height,
        width=settings.width,
        entry_point=settings.entry,
        exit_point=settings.exit,
        seed=current_seed,
        hooks=[Add42Pattern()]  # start with 42 pattern by default
    )
    try:
        gen_maze = MazeGenerator.create(game_config)
        current_seed = gen_maze.seed
        renderer = AsciiMazeRenderer(gen_maze)
        renderer.display()
    except Exception as e:
        print(f"An error occurred during initialization: {e}")
        return
    show_42 = True  # 42 pattern is shown by default
    show_path = False  # check if the path is hidden by default
    # Main menu loop
    while True:
        print("="*30)
        print("Maze-Menu")
        print("-"*(len("maze-menu")))
        print("1-Re-generate a new maze and display it")
        print("42-Show/Hide 42 pattern in the maze")
        print("2-Show/Hide a valid shortest path")
        print("3-change the maze colours")
        print("4-change 42 color")
        print("0-exit")
        print("="*30)
        choice = input("Enter your choice (0-4) or 42: ").strip()
        if choice == "1":
            clear_screen()
            print("\n🔄 Re-generating a new maze...")
            try:
                game_config.seed = None  # reset seed to get a new maze
                show_42 = True  # reset 42 pattern to show by default
                show_path = False  # reset path visibility to hide by default
                game_config.hooks = [Add42Pattern()]  # noqa: E501 ensure 42 pattern is included
                gen_maze = MazeGenerator.create(game_config)
                current_seed = gen_maze.seed
                renderer = AsciiMazeRenderer(gen_maze, colors=current_colors)
                renderer.display()
            except Exception as e:
                print(f"An error occurred during maze generation: {e}")
        elif choice == "2":
            clear_screen()
            print("\n🛣️  Toggling Shortest Path...")
            show_path = not show_path
            try:
                if show_path:
                    solver = BFSMazeSolver(gen_maze)
                    renderer.path = solver.solve()
                else:
                    renderer.path = None
                renderer.display()
            except Exception as e:
                print(f"An error occurred while toggling path: {e}")
        elif choice == "3":
            clear_screen()
            print("\n🎨 Changing Wall Colors...")
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            current_colors[1] = (r, g, b)  # change wall color
            if show_path:
                solver = BFSMazeSolver(gen_maze)
                renderer.path = solver.solve()
            renderer.colors[1] = current_colors[1]
            renderer.display()
        elif choice == "4":
            clear_screen()
            print("\n💜 Changing 42 Theme Color...")
        elif choice == "42":
            clear_screen()
            print("\n🔍 Toggling 42 Pattern...")
            show_42 = not show_42
            game_config.seed = current_seed  # noqa: E501 keep the same seed to maintain maze structure
            if show_42:
                game_config.hooks = [Add42Pattern()]
            else:
                game_config.hooks = []  # remove hooks to hide 42 pattern
            try:
                gen_maze = MazeGenerator.create(game_config)
                renderer = AsciiMazeRenderer(gen_maze, colors=current_colors)
                renderer.display()
            except Exception as e:
                print(f"An error occurred while toggling 42 pattern: {e}")
        elif choice == "0":
            clear_screen()
            print("👋 Thank you for playing A-MAZE-ING! Goodbye!")
            break
        else:
            print("\n❌ Invalid choice! Please enter a number between 0 and 4.")


if __name__ == "__main__":
    main()
