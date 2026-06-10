from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import ClassVar
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / "config.txt",
        env_file_encoding="utf-8",
    )

    pattern_42: ClassVar[list[tuple[int, int]]] = [
        (0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
        (4, 0), (5, 0), (6, 0), (6, 1), (6, 2), (5, 2), (4, 2), (4, 3), (4, 4),
        (5, 4), (6, 4),  # noqa: E501
    ]
    wall: ClassVar[str] = "\u2588\u2588"
    cell: ClassVar[str] = "  "
    path: ClassVar[str] = "\u2591\u2591"
    width: int
    height: int
    entry_raw: str = Field(alias="entry")
    exit_raw: str = Field(alias="exit")
    output_file: str
    perfect: bool
    seed: int | None = None

    @computed_field # type: ignore [prop-decorator]
    @property
    def entry(self) -> tuple[int, int]:
        x, y = self.entry_raw.split(',')
        return int(x), int(y)

    @computed_field # type: ignore [prop-decorator]
    @property
    def exit(self) -> tuple[int, int]:
        x, y = self.exit_raw.split(',')
        return int(x), int(y)


settings = Settings() # type: ignore[call-arg]
