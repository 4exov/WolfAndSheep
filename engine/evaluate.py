# Python 3.8-safe
from typing import List, Optional, Tuple
from collections import deque
from .types import Piece
from .position import Position

INF = 10**9

def _count_wolf_moves(pos: Position) -> int:
    wi, wj = pos.wolf_pos
    cnt = 0
    for di, dj in [(-1,-1), (-1,1), (1,-1), (1,1)]:
        ti, tj = wi + di, wj + dj
        if pos.in_bounds(ti, tj) and pos.board[ti][tj] == Piece.EMPTY and pos.is_black_square(ti, tj):
            cnt += 1
    return cnt

def _count_sheep_moves(pos: Position) -> int:
    cnt = 0
    di = -1 if pos.wolf_at_top else 1
    for i in range(pos.size):
        for j in range(pos.size):
            if pos.board[i][j] == Piece.SHEEP:
                for dj in (-1, 1):
                    ti, tj = i + di, j + dj
                    if pos.in_bounds(ti, tj) and pos.board[ti][tj] == Piece.EMPTY and pos.is_black_square(ti, tj):
                        cnt += 1
    return cnt

def _bfs_min_steps_to_goal(pos: Position) -> Optional[int]:
    """Minimum diagonal steps for wolf to reach the goal row through empty black squares."""
    goal_row = (pos.size - 1) if pos.wolf_at_top else 0
    wi, wj = pos.wolf_pos
    if wi == goal_row:
        return 0

    visited = [[False]*pos.size for _ in range(pos.size)]
    q = deque()
    q.append((wi, wj, 0))
    visited[wi][wj] = True

    while q:
        i, j, d = q.popleft()
        for di, dj in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            ti, tj = i + di, j + dj
            if not pos.in_bounds(ti, tj):
                continue
            if visited[ti][tj]:
                continue
            if not pos.is_black_square(ti, tj):
                continue
            if pos.board[ti][tj] != Piece.EMPTY:
                continue
            if ti == goal_row:
                return d + 1
            visited[ti][tj] = True
            q.append((ti, tj, d + 1))
    return None  # unreachable under current blockers

def evaluate(pos: Position) -> int:
    """Static eval from the Wolf's perspective (higher is better for Wolf)."""
    done, score = pos.is_terminal()
    if done:
        return score

    # Distance component (like your get_heuristic_eval)
    steps = _bfs_min_steps_to_goal(pos)
    if steps is None:
        goal_term = -800  # wolf appears boxed in
    else:
        goal_term = 200 - steps * 20

    # Mobility
    wolf_moves = _count_wolf_moves(pos)
    sheep_moves = _count_sheep_moves(pos)
    mobility = 5 * (wolf_moves - (sheep_moves // 2))

    return goal_term + mobility
