# engine/options.py (engine layer)
from dataclasses import dataclass
from .types import Side

@dataclass
class EngineOptions:
    board_size: int = 8
    wolf_at_top: bool = False
    side_to_move: Side = Side.WOLF
