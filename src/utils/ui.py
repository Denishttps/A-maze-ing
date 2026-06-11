from typing import Generator

from models.theme import Theme
import json


def build_ui(
    render_str: str,
    maze_seed: int,
    helper_str: str,
    algo: str,
    theme_name: str
) -> str:
    text = (
        f"{render_str}\n\n"
        f"A-maze-ing - A Maze Generator and Solver\n"
        f"Press buttons to interact with the maze:\n"
        f"Theme: {theme_name}\n"
        f"Algorithm: {algo}\n"
        f"Maze Seed: {maze_seed}\n"
        f"{helper_str}\n"
    )
    return text


def get_next_theme() -> Generator[Theme, None, None]:
    with open('themes.json', 'r') as f:
        themes_data = json.load(f)
    while True:
        for theme in themes_data:
            yield Theme(**theme)
