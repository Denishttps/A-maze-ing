from models.cell import Cell


class Maze:
    def __init__(
        self,
        width: int,
        height: int,
        entry_point: tuple = (0, 0),
        exit_point: tuple | None = None,
    ):
        self.width = width
        self.height = height
        self.grid = [
            [Cell(x=x, y=y) for x in range(self.width)]
            for y in range(self.height)
        ]
        self.entry = self.get_cell(*entry_point)
        self.exit = self.get_cell(*(exit_point or (width - 1, height - 1)))
        self.seed: int | None = None
        self.algorithm: str | None = None

    def get_cell(self, x: int, y: int) -> Cell | None:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def add_blocked_area(
        self,
        start: str | tuple[int, int],
        width: int,
        height: int,
        maze_resize: bool = False
    ) -> None:
        if maze_resize:
            self.width = self.width + width
            self.height = self.height + height
            self.grid = [
                [Cell(x=x, y=y) for x in range(self.width)]
                for y in range(self.height)
            ]
        start, end = self._get_coordinates(start, width, height)
        if end[0] > self.width or end[1] > self.height:
            raise ValueError(
                "Blocked area exceeds maze boundaries."
            )
        self._add_blocked_area(start, end)

    def _add_blocked_area(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> None:
        for y in range(start[1], end[1]):
            for x in range(start[0], end[0]):
                self.grid[y][x].blocked = True

    def _get_coordinates(
        self,
        start: str | tuple[int, int],
        width: int,
        height: int,
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        if isinstance(start, str):
            start = self._get_coordinates_by_str(start, width, height)
        end = (start[0] + width, start[1] + height)
        return start, end

    def _get_coordinates_by_str(
        self,
        start: str,
        width: int,
        height: int,
    ) -> tuple[int, int]:
        positions = {
            "x": {
                "center": self.width // 2 - width // 2 - width % 2,
                "right": self.width - width,
                "left": 0,
            },
            "y": {
                "center": self.height // 2 - height // 2 - height % 2,
                "bottom": self.height - height,
                "top": 0,
            }
        }
        x_str, y_str = start.split(":", 1)
        x = positions["x"].get(x_str)

        if x is None:
            try:
                x = int(x_str)
            except ValueError:
                raise ValueError(f"Invalid x position: {x_str}")

        y = positions["y"].get(y_str)
        if y is None:
            try:
                y = int(y_str)
            except ValueError:
                raise ValueError(f"Invalid y position: {y_str}")

        return x, y

def open_entry_exit(self) -> None:
    self._open_border_wall(self.entry)
    self._open_border_wall(self.exit)

def _open_border_wall(self, cell: Cell) -> None:
    if cell.y == 0:
        cell.remove_wall(Cell.TOP)
    elif cell.y == self.height - 1:
        cell.remove_wall(Cell.BOTTOM)
    elif cell.x == 0:
        cell.remove_wall(Cell.LEFT)
    elif cell.x == self.width - 1:
        cell.remove_wall(Cell.RIGHT)
    else:
        raise ValueError(
            f"Cell ({cell.x}, {cell.y}) is not on the border."
        )

    def get_unvisited(self) -> list[Cell]:
        return [
            cell
            for row in self.grid
            for cell in row
            if not cell.visited and not cell.blocked
        ]
