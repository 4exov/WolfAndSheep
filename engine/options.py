from dataclasses import dataclass
from .types import Side

@dataclass
class Options:
    board_size: int = 8
    # If True, Wolf starts on the top row and wants to reach the bottom row.
    wolf_at_top: bool = False
    side_to_move: Side = Side.WOLF
