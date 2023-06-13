from csv import DictReader
from typing import Generator
from pathlib import Path


def read_csv(path: str) -> Generator[dict[str, str], None, None]:
    with open(path) as f:
        reader = DictReader(f)
        rows = list(reader)
        return rows
