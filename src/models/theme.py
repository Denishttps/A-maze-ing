from dataclasses import dataclass


@dataclass
class Theme:
    name: str = "Default"
    cell: tuple[int, int, int] | str = "#000000"
    wall: tuple[int, int, int] | str = "#2596BE"
    blocked_cell: tuple[int, int, int] | str = "#757575"
    path: tuple[int, int, int] | str = "#FFFF00"
    entry: tuple[int, int, int] | str = "#FF00FF"
    exit: tuple[int, int, int] | str = "#FF0000"
