def sum_dirs(names: str) -> int:
    """Convert a string of direction names to a bitmask integer."""
    directions = {
        't': 0b1000,
        'r': 0b0100,
        'b': 0b0010,
        'l': 0b0001
    }
    return sum(
        directions[name] for name in names if name in directions
    )


def get_wall_value(names: str) -> int:
    """Convert a string of direction names to a bitmask integer."""
    sm = sum_dirs(names)
    if sm >= 0 and sm <= 0b1111:
        return sm
    raise ValueError("Invalid wall value. Must be a 4-bit integer (0-15).")


def validate_names(names: str) -> bool:
    """Validate that the provided names are valid direction characters."""
    valid_names = {'t', 'r', 'b', 'l'}
    for name in names:
        if name not in valid_names:
            return False
    return True


def get_wall_names(walls: int) -> str:
    """Convert a bitmask integer to a string of direction names."""
    directions = {
        0b1000: 't',
        0b0100: 'r',
        0b0010: 'b',
        0b0001: 'l'
    }
    return ''.join(
        name for bit, name in directions.items() if (walls & bit) != 0
    )
