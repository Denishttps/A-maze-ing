import random

# ---------------------------------------------------------------------------
# Pixel font  (3 wide × 5 tall, '#' = filled pixel)
# ---------------------------------------------------------------------------
_PIXEL_FONT: dict[str, list[str]] = {
    '0': ["###", "# #", "# #", "# #", "###"],
    '1': [" # ", " # ", " # ", " # ", " # "],
    '2': ["###", "  #", "###", "#  ", "###"],
    '3': ["###", "  #", "###", "  #", "###"],
    '4': ["# #", "# #", "###", "  #", "  #"],
    '5': ["###", "#  ", "###", "  #", "###"],
    '6': ["###", "#  ", "###", "# #", "###"],
    '7': ["###", "  #", "  #", "  #", "  #"],
    '8': ["###", "# #", "###", "# #", "###"],
    '9': ["###", "# #", "###", "  #", "###"],
}
_FONT_W, _FONT_H, _CHAR_GAP = 3, 5, 1


def _render_label(maze: list[list[int]], text: str, gx0: int, gy0: int, gx1: int, gy1: int) -> None:
    """Stamp pixel-art text (value 3) onto the blocked region of the maze."""
    area_w = gx1 - gx0 + 1
    area_h = gy1 - gy0 + 1
    total_pw = len(text) * _FONT_W + max(len(text) - 1, 0) * _CHAR_GAP
    pad_x = (area_w - total_pw) // 2
    pad_y = (area_h - _FONT_H) // 2
    if pad_x < 0 or pad_y < 0:
        return  # text doesn't fit
    for ci, ch in enumerate(text.upper()):
        glyph = _PIXEL_FONT.get(ch)
        if glyph is None:
            continue
        char_gx = gx0 + pad_x + ci * (_FONT_W + _CHAR_GAP)
        for py, row_str in enumerate(glyph):
            for px, pixel in enumerate(row_str):
                if pixel == '#':
                    gx = char_gx + px
                    gy = gy0 + pad_y + py
                    if gx0 <= gx <= gx1 and gy0 <= gy <= gy1:
                        maze[gy][gx] = 3


def generate_maze_dfs(
    width: int,
    height: int,
    seed: int = None,
    entry: tuple[int, int] = (0, 0),
    blocked: tuple[int, int] | None = None,
    label: str | None = None,
) -> list[list[int]]:
    """Generate a maze using Depth-First Search (recursive backtracker).

    Args:
        width, height: maze dimensions in cells.
        seed:          random seed for reproducibility.
        entry:         starting cell (cx, cy) for DFS.
        blocked:       (a, b) size of the always-walled central rectangle.

    Returns a grid where 0 = passage, 1 = wall, 2 = blocked obstacle.
    Grid size: (2*height+1) x (2*width+1).
    """
    rng = random.Random(seed)
    bw, bh = blocked if blocked is not None else (0, 0)

    # Total cell-space dimensions: maze area + blocked area.
    # The block sits in the center; the maze retains width×height free cells.
    total_w = width + bw
    total_h = height + bh
    rows = 2 * total_h + 1
    cols = 2 * total_w + 1
    maze = [[1] * cols for _ in range(rows)]

    # Mark the central blocked rectangle (value 2) before DFS so that
    # carve() never enters those cells.
    if blocked is not None:
        x0 = total_w // 2 - bw // 2
        y0 = total_h // 2 - bh // 2
        # Wipe both the cell nodes and the wall nodes inside the rectangle
        gx0 = 2 * x0
        gy0 = 2 * y0
        gx1 = 2 * (x0 + bw - 1) + 2  # one past the last wall column
        gy1 = 2 * (y0 + bh - 1) + 2
        for gy in range(gy0, gy1 + 1):
            for gx in range(gx0, gx1 + 1):
                if 0 <= gx < cols and 0 <= gy < rows:
                    maze[gy][gx] = 2

        if label:
            _render_label(maze, label, gx0, gy0, gx1, gy1)

    def carve(cx: int, cy: int):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        rng.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            gx, gy = 2 * nx + 1, 2 * ny + 1
            # Only visit unvisited, non-blocked cells (value == 1)
            if 0 <= nx < total_w and 0 <= ny < total_h and maze[gy][gx] == 1:
                maze[2 * cy + 1 + dy][2 * cx + 1 + dx] = 0
                maze[gy][gx] = 0
                carve(nx, ny)

    # Start DFS from the entry cell
    ex, ey = entry
    maze[2 * ey + 1][2 * ex + 1] = 0
    carve(ex, ey)

    # Entrance and exit
    maze[1][0] = 0                    # left entrance
    maze[rows - 2][cols - 1] = 0     # right exit

    return maze


def display_maze(maze: list[list[int]]) -> None:
    """Print the maze using Unicode block characters.

    Cell values:
        0  passage      (space)
        1  wall         ██
        2  blocked area ▓▓
    """
    WALL    = "\u2588\u2588"   # ██  wall
    BLOCKED = "\u2591\u2591"   # ░░  blocked background
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
    WIDTH, HEIGHT = 20, 10
    SEED = 4301
    maze = generate_maze_dfs(WIDTH, HEIGHT, seed=SEED, blocked=(5, 4), label="42")
    display_maze(maze)
