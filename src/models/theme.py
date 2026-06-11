from dataclasses import dataclass


@dataclass
class Theme:
    cell: tuple[int, int, int] | str = "#CCCCCC"
    wall: tuple[int, int, int] | str = "#2596BE"
    blocked_cell: tuple[int, int, int] | str = "#CCCCCC"
    path: tuple[int, int, int] | str = "#FFFF00"
    entry: tuple[int, int, int] | str = "#FF00FF"
    exit: tuple[int, int, int] | str = "#FF0000"
