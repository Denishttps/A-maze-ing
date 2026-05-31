from pydantic import BaseModel
from typing import ClassVar

from utils.cell import validate_names, get_wall_value


class Cell(BaseModel):
    x: int
    y: int
    visited: bool = False
    walls: int = 0b1111  # top - 8, right - 4, bottom - 2, left - 1
    blocked: bool = False

    TOP: ClassVar[int] = 0b1000
    RIGHT: ClassVar[int] = 0b0100
    BOTTOM: ClassVar[int] = 0b0010
    LEFT: ClassVar[int] = 0b0001

    _directions: ClassVar[dict[str, int]] = {
        't': TOP,
        'r': RIGHT,
        'b': BOTTOM,
        'l': LEFT
    }

    def remove_wall(
        self,
        direction: int | None = None,
        names: str | None = None
    ) -> None:
        """Remove a wall from the cell in the specified direction."""
        self._validate_direction(value=direction, names=names)
        if direction is None and names is None:
            raise ValueError(
                "Without a direction value or name, no wall can be removed."
            )
        elif names is not None:
            direction = get_wall_value(names)
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
            self.remove_wall(names='r')
            other.remove_wall(names='l')
        elif dx == -1:
            self.remove_wall(names='l')
            other.remove_wall(names='r')
        elif dy == 1:
            self.remove_wall(names='b')
            other.remove_wall(names='t')
        elif dy == -1:
            self.remove_wall(names='t')
            other.remove_wall(names='b')

    def _validate_direction(
        self,
        value: int | None = None,
        names: str | None = None
    ) -> int:
        if value is not None and not (0 <= value <= 0b1111):
            raise ValueError(
                "Walls must be a 4-bit integer (0-15)."
            )
        if names is not None and not validate_names(names):
            raise ValueError(
                "Invalid wall name. Must be 't', 'r', 'b', or 'l'."
            )
        return value

    def _validate_cell_between(self, other: 'Cell') -> None:
        dx = abs(other.x - self.x)
        dy = abs(other.y - self.y)
        if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
            return
        raise ValueError(
            "Cells must be adjacent to remove walls between them."
        )
