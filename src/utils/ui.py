from typing import Generator

from models.theme import Theme


def build_ui(
    render_str: str,
    maze_seed: int,
    helper_str: str,
    algo: str
) -> str:
    text = (
        f"{render_str}\n\n"
        f"A-maze-ing - A Maze Generator and Solver\n"
        f"Press buttons to interact with the maze:\n"
        f"Algorithm: {algo}\n"
        f"Maze Seed: {maze_seed}\n"
        f"{helper_str}\n"
    )
    return text


def get_next_theme() -> Generator[Theme, None, None]:
    colors = [
        Theme(),
        Theme(
            cell="#121212",
            wall="#00F0FF",
            blocked_cell="#1A1A2E",
            path="#FF007F"
        ),
        Theme(
            cell="#4A453A",
            wall="#2B261D",
            blocked_cell="#1C1913",
            path="#E6A15C"
        ),
        Theme(
            cell="#E8F5E9",
            wall="#2E7D32",
            blocked_cell="#1B5E20",
            path="#FFB300",
        ),
        Theme(
            cell="#0A2540",
            wall="#639FAB",
            blocked_cell="#001220",
            path="#FFFFFF",
        ),
        Theme(
            cell="#000000",
            wall="#2121DE",
            blocked_cell="#333333",
            path="#FFFF00",
        )
    ]
    while True:
        for color in colors:
            yield color
