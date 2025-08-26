# engine/position.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
from .types import Piece, Side, Move

__all__ = ["Position", "from_options_start"]

WOLF_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

def _sheep_dirs(wolf_at_top: bool):
    # Sheep move toward the wolf's starting side
    di = -1 if wolf_at_top else 1
    return [(di, -1), (di, 1)]

@dataclass
class Position:
    board: List[List[int]]          # Piece values (Piece.* ints)
    side_to_move: Side
    wolf_at_top: bool               # True: wolf starts top (row 0), goal is bottom
    wolf_pos: Tuple[int, int]       # (i, j)
    size: int

    def in_bounds(self, i: int, j: int) -> bool:
        return 0 <= i < self.size and 0 <= j < self.size

    def is_black_square(self, i: int, j: int) -> bool:
        return ((i + j) % 2) == 0

    def generate_moves(self) -> List[Move]:
        moves: List[Move] = []
        if self.side_to_move == Side.WOLF:
            wi, wj = self.wolf_pos
            for di, dj in WOLF_DIRS:
                ti, tj = wi + di, wj + dj
                if self.in_bounds(ti, tj) and self.board[ti][tj] == Piece.EMPTY and self.is_black_square(ti, tj):
                    moves.append(Move(wi, wj, ti, tj))
        else:
            dirs = _sheep_dirs(self.wolf_at_top)
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == Piece.SHEEP:
                        for di, dj in dirs:
                            ti, tj = i + di, j + dj
                            if self.in_bounds(ti, tj) and self.board[ti][tj] == Piece.EMPTY and self.is_black_square(ti, tj):
                                moves.append(Move(i, j, ti, tj))
        return moves

    def generate_moves_from(self, i: int, j: int) -> List[Move]:
        if self.side_to_move == Side.WOLF and (i, j) == self.wolf_pos:
            return [m for m in self.generate_moves() if m.fi == i and m.fj == j]
        if self.side_to_move == Side.SHEEP and self.board[i][j] == Piece.SHEEP:
            return [m for m in self.generate_moves() if m.fi == i and m.fj == j]
        return []

    def make(self, m: Move) -> None:
        p = self.board[m.fi][m.fj]
        self.board[m.fi][m.fj] = Piece.EMPTY
        self.board[m.ti][m.tj] = p
        if p == Piece.WOLF:
            self.wolf_pos = (m.ti, m.tj)
        self.side_to_move = Side.WOLF if self.side_to_move == Side.SHEEP else Side.SHEEP

    def unmake(self, m: Move) -> None:
        self.side_to_move = Side.WOLF if self.side_to_move == Side.SHEEP else Side.SHEEP
        p = self.board[m.ti][m.tj]
        self.board[m.ti][m.tj] = Piece.EMPTY
        self.board[m.fi][m.fj] = p
        if p == Piece.WOLF:
            self.wolf_pos = (m.fi, m.fj)

    def is_terminal(self) -> Tuple[bool, int]:
        # Goal is the opposite edge from where the wolf started
        goal_row = (self.size - 1) if self.wolf_at_top else 0
        wi, wj = self.wolf_pos
        if wi == goal_row:
            return True, +10**9  # wolf win
        wolf_moves_exist = any(
            self.in_bounds(wi + di, wj + dj)
            and self.board[wi + di][wj + dj] == Piece.EMPTY
            and self.is_black_square(wi + di, wj + dj)
            for di, dj in WOLF_DIRS
        )
        if not wolf_moves_exist:
            return True, -10**9     # sheep win
        return False, 0

    # Place the wolf on any empty black square (does NOT change side_to_move)
    def can_place_wolf(self, i: int, j: int) -> bool:
        return self.in_bounds(i, j) and self.is_black_square(i, j) and self.board[i][j] == Piece.EMPTY

    def place_wolf(self, i: int, j: int) -> bool:
        if not self.can_place_wolf(i, j):
            return False
        wi, wj = self.wolf_pos
        self.board[wi][wj] = Piece.EMPTY
        self.board[i][j] = Piece.WOLF
        self.wolf_pos = (i, j)
        return True

    def can_place_wolf(self, i: int, j: int) -> bool:
        return self.in_bounds(i, j) and self.is_black_square(i, j) and self.board[i][j] == Piece.EMPTY

    def place_wolf(self, i: int, j: int) -> bool:
        if not self.can_place_wolf(i, j):
            return False
        wi, wj = self.wolf_pos
        self.board[wi][wj] = Piece.EMPTY
        self.board[i][j] = Piece.WOLF
        self.wolf_pos = (i, j)
        return True


# --- Factory: create a standard starting position ---
def from_options_start(size: int = 8, wolf_at_top: bool = False) -> "Position":
    """
    Standard start:
      - Wolf on first black square of its start row.
      - Sheep on black squares of the opposite row.
      - Side to move: Wolf.
    """
    board: List[List[int]] = [[Piece.EMPTY for _ in range(size)] for _ in range(size)]

    wolf_row = 0 if wolf_at_top else (size - 1)
    sheep_row = (size - 1) if wolf_at_top else 0

    # Wolf at first black square in its row
    wolf_col = 0 if ((wolf_row + 0) % 2) == 0 else 1
    board[wolf_row][wolf_col] = Piece.WOLF
    wolf_pos = (wolf_row, wolf_col)

    # Sheep on all black squares of the opposite row
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
