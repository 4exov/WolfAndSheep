from dataclasses import dataclass
from enum import IntEnum

class Piece(IntEnum):
    EMPTY = 0
    WOLF = 1
    SHEEP = 255

class Side(IntEnum):
    WOLF = 1
    SHEEP = -1

@dataclass(frozen=True)
class Move:
    fi: int
    fj: int
    ti: int
    tj: int
