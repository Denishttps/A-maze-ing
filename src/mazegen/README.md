# mazegen

> Reusable maze generation and solving library for Python 3.10+

**mazegen** is the standalone engine extracted from the *A-Maze-ing* project.
It generates random mazes, solves them, and gives you full programmatic access to the resulting data structures.
The library is algorithm-agnostic and extensible via a hook system.

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [MazeConfig — parameters reference](#mazeconfig--parameters-reference)
- [MazeGenerator — generating mazes](#mazegenerator--generating-mazes)
- [MazeSolver — solving mazes](#mazesolver--solving-mazes)
- [Maze and Cell — data models](#maze-and-cell--data-models)
- [Algorithms](#algorithms)
- [Hooks](#hooks)
- [Exceptions](#exceptions)
- [Building from source](#building-from-source)

---

## Installation

Install the pre-built wheel directly from the repository root:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Or build and install from source inside a virtualenv (see [Building from source](#building-from-source)).

---

## Quick Start

```python
from mazegen import MazeGenerator, MazeSolver
from mazegen.models.maze_config import MazeConfig

# 1. Describe what you want
cfg = MazeConfig(
    width=20,
    height=15,
    algo="dfs",          # "dfs" | "prim" | "kruskal" | "wilson"
    entry_point=(0, 0),
    exit_point=(19, 14),
    seed=42,             # omit for a random seed
)

# 2. Generate
maze = MazeGenerator.create(cfg)

# 3. Solve
path = MazeSolver.solve(maze)  # list[Cell], entry → exit

# 4. Print the solution as compass directions
directions = []
for i in range(len(path) - 1):
    dx = path[i + 1].x - path[i].x
    dy = path[i + 1].y - path[i].y
    if   dx ==  1: directions.append("S")
    elif dx == -1: directions.append("N")
    elif dy ==  1: directions.append("E")
    elif dy == -1: directions.append("W")

print("Path:", "".join(directions))
# Example output: Path: SSEENWWS...
```

---

## MazeConfig — parameters reference

`MazeConfig` is a plain Python `dataclass` that holds all generation parameters.

```python
from mazegen.models.maze_config import MazeConfig
```

| Field | Type | Default | Description |
|---|---|---|---|
| `width` | `int` | — | Maze width in cells. Required. |
| `height` | `int` | — | Maze height in cells. Required. |
| `algo` | `str \| Type[MazeAlgorithm]` | `"dfs"` | Algorithm to use. Accepts a name string or a class. |
| `entry_point` | `tuple[int, int]` | `(0, 0)` | (x, y) coordinates of the entry cell. |
| `exit_point` | `tuple[int, int] \| None` | `(width-1, height-1)` | (x, y) coordinates of the exit cell. `None` = bottom-right corner. |
| `seed` | `int \| None` | `None` | Random seed. `None` picks a random seed automatically. The used seed is stored in `maze.seed` after generation. |
| `hooks` | `list[MazeHook] \| None` | `None` | Pre/post-generation hooks (see [Hooks](#hooks)). |

**Example — minimal config:**

```python
cfg = MazeConfig(width=10, height=10)
# Uses: algo="dfs", entry=(0,0), exit=(9,9), random seed, no hooks
```

**Example — fully specified:**

```python
from mazegen.hooks.pattern_42 import Add42Pattern
from mazegen.hooks.break_perfect import BreakPerfect

cfg = MazeConfig(
    width=30,
    height=20,
    algo="wilson",
    entry_point=(0, 0),
    exit_point=(29, 19),
    seed=1337,
    hooks=[Add42Pattern(), BreakPerfect(percent=0.08, seed=1337)],
)
```

---

## MazeGenerator — generating mazes

```python
from mazegen import MazeGenerator
```

### `MazeGenerator.create(config)` → `Maze`

Generates and returns a fully built maze.
This is the primary method for most use cases.

```python
maze = MazeGenerator.create(cfg)
```

### `MazeGenerator.create_animated(config)` → `Generator[Maze, None, None]`

Yields intermediate `Maze` states step-by-step as the algorithm carves passages.
Useful for visualising generation progress.

```python
for intermediate_maze in MazeGenerator.create_animated(cfg):
    # render `intermediate_maze` to show the generation in progress
    pass
```

---

## MazeSolver — solving mazes

```python
from mazegen import MazeSolver
```

### `MazeSolver.solve(maze, algo="bfs")` → `list[Cell]`

Returns the shortest path from `maze.entry` to `maze.exit` as an ordered list of `Cell` objects.
Returns an empty list if no path exists.

```python
path = MazeSolver.solve(maze)

if path:
    print(f"Found path with {len(path)} steps")
else:
    print("No path found")
```

### `MazeSolver.solve_animated(maze, algo="bfs")` → `Generator[tuple[list[Cell], bool], None, None]`

Yields `(partial_path, is_final)` tuples as the solver explores the maze.
`is_final=True` on the last yield, which contains the complete path.

```python
for partial_path, is_final in MazeSolver.solve_animated(maze):
    if is_final:
        print("Complete path found, length:", len(partial_path))
    else:
        print("Exploring...", len(partial_path), "cells visited")
```

---

## Maze and Cell — data models

### `Maze`

Returned by `MazeGenerator.create()`. Represents the full generated grid.

```python
from mazegen.models.maze import Maze
```

| Attribute | Type | Description |
|---|---|---|
| `width` | `int` | Maze width in cells |
| `height` | `int` | Maze height in cells |
| `grid` | `list[list[Cell]]` | 2-D grid, indexed as `grid[y][x]` |
| `entry` | `Cell` | Entry cell |
| `exit` | `Cell` | Exit cell |
| `seed` | `int \| None` | Actual seed used during generation |
| `algo` | `str \| None` | Name of the algorithm used |

**`Maze.get_cell(x, y)`** → `Cell | None`

Returns the cell at column `x`, row `y`, or `None` if out of bounds.

```python
cell = maze.get_cell(5, 3)
if cell:
    print(cell.walls)
```

### `Cell`

Represents a single cell in the grid.

```python
from mazegen.models.cell import Cell
```

| Attribute | Type | Description |
|---|---|---|
| `x` | `int` | Column index (0 = leftmost) |
| `y` | `int` | Row index (0 = topmost) |
| `walls` | `int` | 4-bit bitmask of closed walls |
| `visited` | `bool` | Internal state flag (used during generation) |
| `blocked` | `bool` | `True` if the cell is part of a blocked area |

**Wall constants (bitmask flags):**

| Constant | Bit | Hex |
|---|---|---|
| `Cell.NORTH` | 0 (LSB) | `0x1` |
| `Cell.EAST` | 1 | `0x2` |
| `Cell.SOUTH` | 2 | `0x4` |
| `Cell.WEST` | 3 | `0x8` |

**Useful methods:**

```python
cell = maze.get_cell(2, 2)

# Check for a wall
if cell.has_wall(Cell.NORTH):
    print("North wall is closed")

# Walls as a 4-bit integer (matches the hex output file format)
print(f"{cell.walls:X}")  # e.g. "F" for fully enclosed, "0" for open

# Check if blocked
if cell.blocked:
    print("This cell is part of the '42' pattern or a blocked area")
```

**Iterating the full grid:**

```python
for row in maze.grid:
    for cell in row:
        print(f"({cell.x},{cell.y}): walls={cell.walls:#06b} blocked={cell.blocked}")
```

**Converting the path to compass directions:**

```python
path = MazeSolver.solve(maze)

def path_to_directions(path: list) -> str:
    dirs = []
    for i in range(len(path) - 1):
        dx = path[i + 1].x - path[i].x
        dy = path[i + 1].y - path[i].y
        if   dx ==  1: dirs.append("S")
        elif dx == -1: dirs.append("N")
        elif dy ==  1: dirs.append("E")
        elif dy == -1: dirs.append("W")
    return "".join(dirs)

print(path_to_directions(path))
```

---

## Algorithms

Four algorithms are built in. Pass the name string to `MazeConfig(algo=...)`.

| Name string | Class | Corridor style | Notes |
|---|---|---|---|
| `"dfs"` | `DFSMazeGenerator` | Long, winding | Default. Fast, O(n). |
| `"prim"` | `PrimMazeGenerator` | Short, branching | More dead ends. |
| `"kruskal"` | `KruskalMazeGenerator` | Balanced | Union-Find approach. |
| `"wilson"` | `WilsonMazeGenerator` | Uniform random | Unbiased; slower on large grids. |

You can also pass a class directly:

```python
from mazegen.algo.prim import PrimMazeGenerator

cfg = MazeConfig(width=15, height=15, algo=PrimMazeGenerator)
maze = MazeGenerator.create(cfg)
```

**Writing a custom algorithm** — subclass `MazeAlgorithm` from `mazegen.interfaces`:

```python
from mazegen.interfaces import MazeAlgorithm
from mazegen.models.maze import Maze

class MyAlgo(MazeAlgorithm):
    name = "my_algo"

    def generate(self, seed: int) -> None:
        # carve passages in self.maze using seed for randomness
        ...

cfg = MazeConfig(width=10, height=10, algo=MyAlgo)
```

---

## Hooks

Hooks let you modify the maze before or after generation without touching the core algorithm.
They implement the `MazeHook` protocol: a callable that takes a `Maze` and returns a `Maze`.

```python
from mazegen.interfaces import MazeHook
```

### Built-in hooks

#### `Add42Pattern` — pre-generation

Stamps a "42" shape made of blocked cells, centred in the maze.
Raises `MazeSizeError` if the maze is smaller than 8 × 7.

```python
from mazegen.hooks.pattern_42 import Add42Pattern

cfg = MazeConfig(width=20, height=15, hooks=[Add42Pattern()])
```

#### `AddBlockedArea` — pre-generation

Marks a rectangular region as blocked.

```python
from mazegen.hooks.blocked_area import AddBlockedArea

# Block a 4×3 region starting at (2, 2)
hook = AddBlockedArea(start=(2, 2), width=4, height=3)

# Named positions: "center:center", "right:bottom", "left:top", etc.
hook = AddBlockedArea(start="center:center", width=4, height=3)

cfg = MazeConfig(width=20, height=15, hooks=[hook])
```

#### `BreakPerfect` — post-generation

Randomly removes a fraction of walls after generation, introducing multiple paths (loops).

```python
from mazegen.hooks.break_perfect import BreakPerfect

# Remove 10 % of remaining walls
hook = BreakPerfect(percent=0.10, seed=99)

cfg = MazeConfig(width=20, height=15, hooks=[hook])
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `percent` | `float` | `0.1` | Fraction of walls to remove (0.0–1.0) |
| `seed` | `int \| None` | `None` | Seed for the wall-selection shuffle |

### Writing a custom hook

```python
from mazegen.interfaces import MazeHook
from mazegen.models.maze import Maze

class MySpiralHook:
    stage = "pre"   # or "post"

    def __call__(self, maze: Maze) -> Maze:
        # modify maze.grid cells here
        return maze

cfg = MazeConfig(width=20, height=15, hooks=[MySpiralHook()])
```

---

## Exceptions

All exceptions inherit from `MazeError` in `mazegen.exceptions`.

```python
from mazegen.exceptions import MazeError, InvalidEntryExitError, MazeSizeError, MazeWallError
```

| Exception | Raised when |
|---|---|
| `MazeError` | Base class for all mazegen errors |
| `InvalidEntryExitError` | Entry/exit are identical, out of bounds, or land on a blocked cell |
| `MazeSizeError` | Maze is too small for a hook (e.g. `Add42Pattern` needs ≥ 8×7) or blocked areas disconnect the maze |
| `MazeWallError` | Invalid wall bitmask or non-adjacent cells passed to wall-removal methods |

**Handling errors gracefully:**

```python
from mazegen.exceptions import MazeError

try:
    maze = MazeGenerator.create(cfg)
except MazeError as e:
    print(f"Maze generation failed: {e}")
```

---

## Building from source

Requires the repository to be cloned and `uv` to be installed.

```bash
# Inside a virtualenv or with uv:
cd src/
python3 -m pip install build
python3 setup.py bdist_wheel --dist-dir ..
# → produces ../mazegen-1.0.0-py3-none-any.whl

# Or use the Makefile shortcut from the repo root:
make build
```

Then install the wheel:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```