from dataclasses import dataclass


@dataclass
class Symbol:
    id: str
    filename: str
    width: int
    height: int
    area: int