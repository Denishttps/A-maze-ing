from maze_generator import MazeGenerator
from models.cell_models import Cell

def display_maze(maze: list[list[Cell]]) -> None:
    """Print the maze using Unicode block characters.

    Cell values:
        0  passage      (space)
        1  wall         ██
        2  blocked area ▓▓
    """
    WALL    = "\u2588\u2588" 
    LABEL   = "\u2593\u2593"   # ▓▓  text pixel
    LABEL   = WALL
    PASS    = "  "             # passage
    ENTRY   = "\u25BA "        # ►  entrance
    EXIT    = " \u25C4"        # ◄  exit

    rows = len(maze)
    cols = len(maze[0])

    for r, row in enumerate(maze):
        line = []
        for c, cell in enumerate(row):
            if cell == 3:
                line.append(LABEL)
            elif cell == 2:
                line.append(BLOCKED)
            elif cell == 1:
                line.append(WALL)
            else:  # cell == 0
                if c == 0:
                    line.append(ENTRY)
                elif c == cols - 1:
                    line.append(EXIT)
                else:
                    line.append(PASS)
        print("".join(line))

if __name__ == "__main__":
    width, height = 20, 10
    entry_point = (0, 0)
    exit_point = (width - 1, height - 1)
    maze_gen = MazeGenerator(
        width=width,
        height=height,
        entry_point=entry_point,
        exit_point=exit_point,
        perfect=True
    )
    maze = maze_gen.generate_maze(seed=42, algo='dfs')