from models.cell import Cell


def get_walls_between(cell1: Cell, cell2: Cell) -> int:
    """Get the walls between two adjacent cells."""
    dx = cell2.x - cell1.x
    dy = cell2.y - cell1.y

    if dx == 1:
        return cell1.SOUTH, cell2.NORTH
    elif dx == -1:
        return cell1.NORTH, cell2.SOUTH
    elif dy == 1:
        return cell1.EAST, cell2.WEST
    elif dy == -1:
        return cell1.WEST, cell2.EAST
