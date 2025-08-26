# --- Factory: create a standard starting position ---
from typing import List

from .position import Position
from .types import Piece, Side

def from_options_start(size: int = 8, wolf_at_top: bool = False) -> "Position":
    """
    Build the standard start:
      - Wolf on the first black square of its start row.
      - All sheep on black squares of the opposite row.
      - Side to move: Wolf.
    """
    board: List[List[int]] = [[Piece.EMPTY for _ in range(size)] for _ in range(size)]

    wolf_row = 0 if wolf_at_top else (size - 1)
    sheep_row = (size - 1) if wolf_at_top else 0

    # Place wolf at first black square in its row
    wolf_col = 0 if ((wolf_row + 0) % 2) == 0 else 1
    board[wolf_row][wolf_col] = Piece.WOLF
    wolf_pos = (wolf_row, wolf_col)

    # Place sheep on all black squares of the opposite row
    for j in range(0, size, 2):
        col = j if ((sheep_row + j) % 2) == 0 else j + 1
        if col < size:
            board[sheep_row][col] = Piece.SHEEP

    return Position(
        board=board,
        side_to_move=Side.WOLF,
        wolf_at_top=wolf_at_top,
        wolf_pos=wolf_pos,
        size=size
    )
