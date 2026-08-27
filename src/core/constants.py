from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Constants:
    """
    Константы проекта.

    Attributes:
        BASE_DIR (Path): Базовый путь директории проекта.
        LOGS_DIR (Path): Путь до папки логов в директории проекта.
    """

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    LOGS_DIR: Path = BASE_DIR / "logs"
