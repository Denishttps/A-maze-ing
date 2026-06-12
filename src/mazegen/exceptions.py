

class MazeError(Exception):
    """Base class for maze-related exceptions."""
    pass


class InvalidEntryExitError(MazeError):
    """Raised when the entry or exit point is invalid."""
    pass


class MazeSizeError(MazeError):
    """Raised when the maze size is invalid."""
    pass


class MazeWallError(MazeError):
    """Raised when an invalid wall configuration is encountered."""
    pass
