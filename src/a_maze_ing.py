import sys
from pathlib import Path

from models.maze_config import MazeConfig
from maze_generator import MazeGenerator
from renderer.ascii import AsciiMazeRenderer
from solver.bfs import BFSMazeSolver
from config import settings


class MazeApp:
    def __init__(self, config_path: str):
        self.config = settings
        self.maze = None
        self.path = None
        self.show_path = False
        self.renderer = None
        self.colors = None
        self.generate_maze()

    def generate_maze(self):
        """Generate a new maze."""
        maze_config = MazeConfig(
            width=self.config.width,
            height=self.config.height,
            entry_point=self.config.entry,
            exit_point=self.config.exit,
            seed=self.config.seed,
            algo="dfs"
        )
        self.maze = MazeGenerator.create(maze_config)
        self.maze.open_entry_exit()
        self.path = None
        self.show_path = False
        print("✓ New maze generated!")

    def solve_maze(self):
        """Solve the maze and get the shortest path."""
        if not self.maze:
            print("✗ No maze generated yet.")
            return
        solver = BFSMazeSolver(self.maze)
        self.path = solver.solve()
        print(f"✓ Maze solved! Shortest path length: {len(self.path) if self.path else 0}")

    def toggle_path(self):
        """Toggle showing/hiding the path."""
        if not self.maze:
            print("✗ No maze generated yet.")
            return
        if not self.path:
            self.solve_maze()
        self.show_path = not self.show_path
        status = "shown" if self.show_path else "hidden"
        print(f"✓ Path is now {status}.")

    def set_custom_colors(self):
        """Set custom colors for the maze."""
        print("\nSet custom maze colors (RGB values 0-255):")
        try:
            wall_r = int(input("Wall color - Red (0-255): "))
            wall_g = int(input("Wall color - Green (0-255): "))
            wall_b = int(input("Wall color - Blue (0-255): "))

            cell_r = int(input("Cell color - Red (0-255): "))
            cell_g = int(input("Cell color - Green (0-255): "))
            cell_b = int(input("Cell color - Blue (0-255): "))

            path_r = int(input("Path color - Red (0-255): "))
            path_g = int(input("Path color - Green (0-255): "))
            path_b = int(input("Path color - Blue (0-255): "))

            entry_r = int(input("Entry color - Red (0-255): "))
            entry_g = int(input("Entry color - Green (0-255): "))
            entry_b = int(input("Entry color - Blue (0-255): "))

            self.colors = [
                (wall_r, wall_g, wall_b),
                (cell_r, cell_g, cell_b),
                (path_r, path_g, path_b),
                (entry_r, entry_g, entry_b),
            ]
            print("✓ Custom colors set!")
        except ValueError:
            print("✗ Invalid input. Using default colors.")
            self.colors = None

    def set_pattern_42_colors(self):
        """Set colors to display the '42' pattern."""
        print("\n🎓 Setting colors for the '42' pattern...")
        from hooks.pattern_42 import Add42Pattern
        from models.maze import Maze

        maze_config = MazeConfig(
            width=self.config.width,
            height=self.config.height,
            entry_point=self.config.entry,
            exit_point=self.config.exit,
            seed=self.config.seed,
            algo="dfs",
            hooks=[Add42Pattern("post")]
        )
        self.maze = MazeGenerator.create(maze_config)
        self.maze.open_entry_exit()
        self.path = None
        self.show_path = False

        self.colors = [
            (255, 200, 0),
            (255, 255, 255),
            (100, 200, 255),
            (0, 255, 0),
        ]
        print("✓ Maze with '42' pattern generated with custom colors!")

    def display_maze(self):
        """Display the maze with optional path."""
        if not self.maze:
            print("✗ No maze generated yet.")
            return

        path = self.path if self.show_path else None
        self.renderer = AsciiMazeRenderer(
            self.maze,
            path=path,
            colors=self.colors
        )
        self.renderer.display()

    def display_menu(self):
        """Display the interactive menu."""
        while True:
            print("\n" + "=" * 50)
            print("🎮 A-MAZE-ING INTERACTIVE MENU")
            print("=" * 50)
            print("1. Display maze")
            print("2. Generate new maze")
            print("3. Show/Hide shortest path")
            print("4. Set custom colors")
            print("5. Generate maze with '42' pattern")
            print("6. Exit")
            print("=" * 50)

            choice = input("Choose an option (1-6): ").strip()

            if choice == "1":
                self.display_maze()
            elif choice == "2":
                self.generate_maze()
                self.display_maze()
            elif choice == "3":
                self.toggle_path()
                self.display_maze()
            elif choice == "4":
                self.set_custom_colors()
                self.display_maze()
            elif choice == "5":
                self.set_pattern_42_colors()
                self.display_maze()
            elif choice == "6":
                print("\n👋 Thanks for playing A-MAZE-ING! Goodbye!")
                break
            else:
                print("✗ Invalid option. Please try again.")


def main() -> None:
    print("🎯 Welcome to A-MAZE-ING!")
    if len(sys.argv) != 2:
        print("Usage: python a_maze_ing.py config.txt")
        return

    config_path = sys.argv[1]
    if not Path(config_path).exists():
        print(f"✗ Config file not found: {config_path}")
        return

    app = MazeApp(config_path)
    app.display_maze()
    app.display_menu()


if __name__ == "__main__":
    main()

