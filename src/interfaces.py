from abc import ABC, abstractmethod

from models.cell_models import Cell


class MazeAlgorithm(ABC):
    def __init__(
        self,
        maze: list[list[Cell]],
        width: int,
        height: int,
        entry: Cell,
    ):
        self.maze = maze
        self.width = width
        self.height = height
        self.entry = entry

    @abstractmethod
    def generate(
        self,
        seed: int = None
    ) -> list[list[Cell]]:
        """Generate a maze with the specified parameters."""
        raise NotImplementedError()
