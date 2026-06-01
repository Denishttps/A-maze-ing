from typing import ClassVar


class Cell:
    TOP: ClassVar[int] = 0b1000
    RIGHT: ClassVar[int] = 0b0100
    BOTTOM: ClassVar[int] = 0b0010
    LEFT: ClassVar[int] = 0b0001

    def __init__(
        self,
        x: int,
        y: int,
        visited: bool = False,
        walls: int = 0b1111,
        blocked: bool = False
    ):
        self.x = x
        self.y = y
        self.visited = visited
        self.walls = walls
        self.blocked = blocked

    def remove_wall(
        self,
        direction: int
    ) -> None:
        self._validate_direction(value=direction)
        self.walls &= ~direction

    def has_wall(self, direction: int) -> bool:
        """Check if the cell has a wall in the specified direction."""
        self._validate_direction(value=direction)
        return (self.walls & direction) != 0

    def remove_walls_between(self, other: 'Cell') -> None:
        """Remove walls between this cell and another cell."""
        self._validate_cell_between(other)
        dx = other.x - self.x
        dy = other.y - self.y

        if dx == 1:
            self.remove_wall(Cell.RIGHT)
            other.remove_wall(Cell.LEFT)
        elif dx == -1:
            self.remove_wall(Cell.LEFT)
            other.remove_wall(Cell.RIGHT)
        elif dy == 1:
            self.remove_wall(Cell.BOTTOM)
            other.remove_wall(Cell.TOP)
        elif dy == -1:
            self.remove_wall(Cell.TOP)
            other.remove_wall(Cell.BOTTOM)

    def _validate_direction(
        self,
        value: int
    ) -> None:
        if value is not None and not (0 <= value <= 0b1111):
            raise ValueError(
                "Walls must be a 4-bit integer (0-15)."
            )

    def _validate_cell_between(self, other: 'Cell') -> None:
        dx = abs(other.x - self.x)
        dy = abs(other.y - self.y)
        if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
            return
        raise ValueError(
            "Cells must be adjacent to remove walls between them."
        )
