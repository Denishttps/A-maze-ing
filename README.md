*This project has been created as part of the 42 curriculum by dbobrov, ymarmoud.*

# A-Maze-ing

> Create your own maze generator and display its result!

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Project Structure](#project-structure)
- [Instructions](#instructions)
- [Configuration File Format](#configuration-file-format)
- [Output File Format](#output-file-format)
- [Maze Generation Algorithms](#maze-generation-algorithms)
- [Reusable Module — mazegen](#reusable-module--mazegen)
- [Visual Representation](#visual-representation)
- [The "42" Pattern](#the-42-pattern)
- [Hooks System](#hooks-system)
- [Team & Project Management](#team--project-management)
- [Resources](#resources)

---

## Description

**A-Maze-ing** is a maze generator and solver written in Python 3.14+. The program reads a plain-text configuration file, generates a random maze — optionally *perfect* (exactly one path between any two cells) — and writes the result to a file using a hexadecimal wall encoding. It also provides an interactive ASCII visual representation directly in the terminal, rendered in colour via the [Rich](https://github.com/Textualize/rich) library.

The project is built around a modular, object-oriented architecture. The maze generation engine (`mazegen`) is fully decoupled from the application layer and can be installed as a standalone Python package in external projects.

## Features

- **Four generation algorithms** — DFS, Prim, Kruskal, Wilson
- **Perfect maze mode** — guaranteed single path between entry and exit
- **BFS shortest-path solver** — finds and displays the optimal route
- **Interactive ASCII terminal renderer** — colour themes, show/hide path, regenerate on-the-fly
- **Configurable** via a simple `KEY=VALUE` text file
- **Reproducible** mazes through an optional `SEED` parameter
- **Hook system** — pre- and post-generation transformations (blocked areas, "42" pattern, break-perfect)
- **Hexadecimal output file** with encoded wall data and path solution
- **Type-checked** with `mypy`, linted with `flake8`
- **Unit-tested** with `pytest`

## Project Structure

```
A-maze-ing/
├── Makefile                        # Build automation
├── README.md                       # This file
├── config.txt                      # Default configuration file
├── themes.json                     # Colour theme definitions
├── pyproject.toml                  # Project metadata and dependencies
├── a_maze_ing.py                   # CLI entry point
├── mazegen-1.0.0-py3-none-any.whl  # Pre-built reusable package
├── src/
│   ├── main.py                     # Application entry point
│   ├── config.py                   # Settings / configuration loader
│   ├── dispatcher.py               # CLI command dispatcher
│   ├── setup.py                    # Package build script for mazegen
│   ├── mazegen/                    # ← Reusable maze engine package
│   │   ├── __init__.py
│   │   ├── maze_generator.py       # MazeGenerator facade (public API)
│   │   ├── maze_solver.py          # MazeSolver facade (public API)
│   │   ├── interfaces.py           # Abstract base classes & protocols
│   │   ├── exceptions.py           # Custom exception classes
│   │   ├── algo/                   # Generation algorithms
│   │   │   ├── dfs.py
│   │   │   ├── prim.py
│   │   │   ├── kruskal.py
│   │   │   └── wilson.py
│   │   ├── hooks/                  # Pre/post-generation hooks
│   │   │   ├── pattern_42.py
│   │   │   ├── blocked_area.py
│   │   │   └── break_perfect.py
│   │   ├── models/                 # Internal data models
│   │   │   ├── cell.py
│   │   │   ├── maze.py
│   │   │   └── maze_config.py
│   │   └── solver/
│   │       └── bfs.py
│   ├── models/
│   │   └── theme.py                # Colour theme schema
│   ├── renderer/
│   │   └── ascii.py                # Terminal ASCII renderer
│   └── utils/
│       ├── file.py                 # File I/O helpers
│       ├── maze_config.py          # Config validation helpers
│       └── ui.py                   # Terminal UI helpers
└── tests/                          # Unit and integration tests
    ├── conftest.py
    └── test_*.py
```

---

## Instructions

### Requirements

- Python **3.14+**
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
make install
```

Runs `uv sync` and installs all dependencies defined in `pyproject.toml`:

| Dependency | Purpose |
|---|---|
| `pydantic` / `pydantic-settings` | Configuration validation |
| `rich` | Coloured terminal output |
| `readchar` | Single-keypress input |
| `flake8` | Code style linting |
| `mypy` | Static type checking |

### Running

```bash
make run
# equivalent to: uv run python3 a_maze_ing.py config.txt
```

You can pass a custom config file:

```bash
uv run python3 a_maze_ing.py my_config.txt
```

### Debugging

```bash
make debug
# equivalent to: uv run python3 -m pdb a_maze_ing.py config.txt
```

### Linting

```bash
make lint         # flake8 + mypy (standard flags)
make lint-strict  # flake8 + mypy --strict
```

### Testing

```bash
make test
# equivalent to: uv run pytest -v tests/
```

### Cleaning

```bash
make clean
```

Removes `__pycache__`, `.mypy_cache`, `.pytest_cache`, compiled Python files, and generated output files.

### Building the mazegen package

```bash
make build
# produces mazegen-1.0.0-py3-none-any.whl at the repository root
```

---

## Configuration File Format

The configuration file is a plain text file with one `KEY=VALUE` pair per line. Lines starting with `#` are treated as comments and ignored.

### Mandatory keys

| Key | Type | Description | Example |
|---|---|---|---|
| `WIDTH` | `int` | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | `int` | Maze height in cells | `HEIGHT=15` |
| `ENTRY` | `x,y` | Entry cell coordinates | `ENTRY=0,0` |
| `EXIT` | `x,y` | Exit cell coordinates | `EXIT=19,14` |
| `OUTPUT_FILE` | `string` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `bool` | Whether the maze is perfect | `PERFECT=true` |

### Optional keys

| Key | Type | Description | Example |
|---|---|---|---|
| `SEED` | `int` | Random seed for reproducibility | `SEED=42` |
| `THEMES_PATH` | `string` | Path to a custom themes JSON file | `THEMES_PATH=themes.json` |

### Default `config.txt`

```ini
WIDTH=20
HEIGHT=15
ENTRY=4,3
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=true
# SEED=42       Optional — omit for a random seed
# THEMES_PATH   Optional
```

---

## Output File Format

The maze is written to the output file using **one hexadecimal digit per cell**. Each digit encodes which walls of that cell are closed using a 4-bit bitmask:

| Bit | Direction |
|---|---|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

A closed wall sets the corresponding bit to `1`; an open wall sets it to `0`.

**Examples:**
- `3` (binary `0011`) → North and East walls closed
- `A` (binary `1010`) → East and West walls closed
- `F` (binary `1111`) → all four walls closed (fully isolated cell)

**File structure:**
1. One row of hex digits per line (no separators between cells).
2. An empty line.
3. Entry coordinates (`x,y`).
4. Exit coordinates (`x,y`).
5. Shortest path from entry to exit as a sequence of `N`, `E`, `S`, `W` letters.

All lines end with `\n`.

---

## Maze Generation Algorithms

The project supports four algorithms, all of which produce a spanning tree of the grid graph and therefore guarantee a connected maze. The algorithm is selected automatically (default: DFS) — future versions may expose it as a config key.

### Depth-First Search (DFS)

A recursive backtracker using an explicit stack. Starts from a cell, carves passages to unvisited neighbours, and backtracks when stuck. Produces mazes with long, winding corridors and relatively few dead ends.

### Prim's Algorithm

Grows the maze outward from a seed cell by maintaining a frontier list and picking a random frontier cell at each step. Produces mazes with more branching and shorter corridors than DFS.

### Kruskal's Algorithm

Randomly shuffles all internal walls and removes each one if it connects two previously disjoint sets (Union-Find). Produces evenly distributed, balanced mazes.

### Wilson's Algorithm

Uses loop-erased random walks to add paths to the growing maze. Produces an unbiased uniform spanning tree, resulting in statistically uniform mazes. Slower to generate on large grids.

### Why these algorithms?

| Algorithm | Corridor style | Complexity | Notable quality |
|---|---|---|---|
| DFS | Long, winding | O(n) | Fast, visually dramatic |
| Prim | Short, branching | O(n log n) | Many dead ends |
| Kruskal | Balanced | O(n log n) | Uniform distribution |
| Wilson | Uniform random | Variable | Statistically unbiased |

All four were chosen to showcase different graph-traversal strategies and to let users compare the visual and structural results of each approach. Supporting multiple algorithms also qualifies as a bonus feature per the project specification.

---

## Reusable Module — mazegen

The maze generation engine is packaged as a standalone pip-installable module located in `src/mazegen/`. It exposes two facades — `MazeGenerator` and `MazeSolver` — that cover the full generate-and-solve workflow.

The package is available as:
- `mazegen-1.0.0-py3-none-any.whl` (pre-built wheel at the repository root)
- Rebuildable at any time with `make build`

Install in a virtualenv:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### What is reusable

The entire `src/mazegen/` directory is the reusable component:

- `MazeGenerator` — generates mazes from a `MazeConfig`
- `MazeSolver` — solves a `Maze` and returns the path
- `MazeConfig` — dataclass for generation parameters
- `Maze` / `Cell` — core data models
- All algorithm classes (`DFSMazeGenerator`, `PrimMazeGenerator`, `KruskalMazeGenerator`, `WilsonMazeGenerator`)
- All hook classes (`Add42Pattern`, `AddBlockedArea`, `BreakPerfect`)
- Abstract interfaces (`MazeAlgorithm`, `BaseMazeSolver`, `MazeHook`)

The renderer, config loader, CLI dispatcher, and file utilities are **not** part of the reusable package — they belong to the application layer.

### Basic usage

```python
from mazegen import MazeGenerator, MazeSolver
from mazegen.models.maze_config import MazeConfig

# 1. Build a configuration
cfg = MazeConfig(
    width=20,
    height=15,
    algo="dfs",
    entry_point=(0, 0),
    exit_point=(19, 14),
    seed=42,
)

# 2. Generate the maze
maze = MazeGenerator.create(cfg)

# 3. Solve it
path = MazeSolver.solve(maze)  # list[Cell] from entry to exit

# 4. Print the path as directions
for i in range(len(path) - 1):
    dx = path[i + 1].x - path[i].x
    dy = path[i + 1].y - path[i].y
    if   dx ==  1: print("S", end="")
    elif dx == -1: print("N", end="")
    elif dy ==  1: print("E", end="")
    elif dy == -1: print("W", end="")
print()
```

### Custom parameters

| `MazeConfig` field | Type | Default | Description |
|---|---|---|---|
| `width` | `int` | — | Maze width in cells |
| `height` | `int` | — | Maze height in cells |
| `algo` | `str \| Type[MazeAlgorithm]` | `"dfs"` | Algorithm: `"dfs"`, `"prim"`, `"kruskal"`, `"wilson"` |
| `entry_point` | `tuple[int, int]` | `(0, 0)` | Entry cell |
| `exit_point` | `tuple[int, int] \| None` | bottom-right | Exit cell |
| `seed` | `int \| None` | `None` (random) | Reproducibility seed |
| `hooks` | `list[MazeHook] \| None` | `None` | Pre/post-generation hooks |

### Accessing the generated structure

```python
# Grid — 2D list[list[Cell]], indexed as grid[y][x]
for row in maze.grid:
    for cell in row:
        has_north = cell.has_wall(Cell.NORTH)
        print(f"({cell.x},{cell.y}) blocked={cell.blocked} walls={cell.walls:#06b}")

# Entry and exit
print(maze.entry)  # Cell (x, y)
print(maze.exit)

# Metadata set after generation
print(maze.seed)   # int — actual seed used
print(maze.algo)   # str — algorithm name
```

### Accessing a solution

```python
path = MazeSolver.solve(maze)  # list[Cell], ordered entry → exit

if path:
    print(f"Solution length: {len(path)} cells")
    for cell in path:
        print(cell)  # prints "(x, y)"
```

---

## Visual Representation

The program renders the maze in the terminal using the `AsciiMazeRenderer` (in `src/renderer/ascii.py`), powered by the [Rich](https://github.com/Textualize/rich) library for full RGB colour support.

The interactive menu (shown below the maze) provides the following actions:

| Action | Description |
|---|---|
| Re-generate | Generate and display a brand-new random maze |
| Show / Hide path | Toggle the BFS shortest-path overlay |
| Change colours | Cycle through available colour themes |
| Quit | Exit the program |

Themes are defined in `themes.json`. Each theme specifies RGB values for cell background, walls, blocked cells, path highlight, entry and exit markers.

---

## The "42" Pattern

Every generated maze contains a visible **"42"** shape formed by fully closed (blocked) cells. The pattern is injected before generation by the `Add42Pattern` pre-hook and is centred in the maze automatically.

The pattern occupies a 7-column × 5-row bounding box. If the maze is smaller than **8 × 7** cells, the pattern cannot fit; a `MazeSizeError` is raised and an error message is printed to the console.

---

## Hooks System

Hooks are callable objects that transform a `Maze` before (`stage="pre"`) or after (`stage="post"`) the generation algorithm runs. They implement the `MazeHook` protocol defined in `src/mazegen/interfaces.py`.

| Hook | Stage | Description |
|---|---|---|
| `Add42Pattern` | `pre` | Stamps the "42" blocked-cell pattern centred in the maze |
| `AddBlockedArea` | `pre` | Marks an arbitrary rectangular region as blocked |
| `BreakPerfect` | `post` | Randomly removes a fraction of walls, introducing loops |

**Example — combining hooks:**

```python
from mazegen.hooks.pattern_42 import Add42Pattern
from mazegen.hooks.break_perfect import BreakPerfect

cfg = MazeConfig(
    width=20, height=15,
    hooks=[Add42Pattern(), BreakPerfect(percent=0.05, seed=7)],
)
maze = MazeGenerator.create(cfg)
```

---

## Team & Project Management

### Team roles

| Member | Responsibilities |
|---|---|
| **dbobrov** | Architecture, algorithms (DFS, Prim, Kruskal, Wilson), BFS solver, hook system, output format, linting, testing, documentation |
| **ymarmoud** | ASCII renderer, colour theme system, interactive UI, integration, config loading, file utilities |

### Planning & evolution

The project was developed in six phases:

1. **Core models** — `Cell` and `Maze` data structures with 4-bit wall encoding.
2. **Generation** — DFS first, then Prim, Kruskal, and Wilson added as comparison/bonus.
3. **Solver & output** — BFS solver and hexadecimal file format with path export.
4. **Rendering** — ASCII renderer with Rich, colour theme support, interactive menu.
5. **Hooks & patterns** — Hook protocol, `Add42Pattern`, `AddBlockedArea`, `BreakPerfect`.
6. **Polish** — `mazegen` pip package, comprehensive tests, README files, lint passes.

Originally only DFS was planned. The hook system was added mid-project when the "42" pattern requirement and the break-perfect feature were identified as logically independent transformations that should not pollute core generation code.

### What worked well

- Decoupling the engine (`mazegen`) from the application layer made it easy to test generation in isolation and later package it independently.
- The hook protocol kept `MazeGenerator._build()` clean while allowing open-ended extensibility.
- Rich made terminal rendering straightforward with no need for external graphical libraries.

### What could be improved

- Add graphical (MLX / pygame) rendering as an alternative to ASCII.
- Animate generation step-by-step in the terminal (the `generate_step` generator already supports it internally).
- More comprehensive integration tests covering the full CLI pipeline.

### Tools used

- **Python 3.14** — main language
- **uv** — fast package and virtualenv manager
- **Pydantic** — configuration validation
- **Rich** — terminal rendering
- **flake8** / **mypy** — code quality
- **pytest** — unit testing
- **Git** — version control

---

## Resources

- [Maze Generation Algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Depth-First Search (Recursive Backtracker) — Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [Prim's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [Kruskal's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)
- [Wilson's Algorithm (Loop-Erased Random Walk) — Wikipedia](https://en.wikipedia.org/wiki/Loop-erased_random_walk)
- [Breadth-First Search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Think Labyrinth — Maze Algorithm Comparison](http://www.astrolog.org/labyrnth/algrithm.htm)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [uv Documentation](https://docs.astral.sh/uv/)

### AI usage