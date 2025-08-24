from typing import Optional
from .position import Position
from .types import Move
from .evaluate import evaluate

INF = 10**9

def alphabeta(pos: Position, depth: int, alpha: int, beta: int) -> int:
    done, score = pos.is_terminal()
    if done:
        return score
    if depth == 0:
        return evaluate(pos)

    best = -INF
    moves = pos.generate_moves()
    if not moves:
        # No legal move for side to move; if it's Wolf, it's already terminal above,
        # but keep a fallback:
        return evaluate(pos)

    for m in moves:
        pos.make(m)
        val = -alphabeta(pos, depth - 1, -beta, -alpha)
        pos.unmake(m)
        if val > best:
            best = val
        if best > alpha:
            alpha = best
        if alpha >= beta:
            break
    return best

def find_best_move(pos: Position, depth: int) -> Optional[Move]:
    alpha, beta = -INF, INF
    best_val = -INF
    best_move: Optional[Move] = None
    for m in pos.generate_moves():
        pos.make(m)
        val = -alphabeta(pos, depth - 1, -beta, -alpha)
        pos.unmake(m)
        if val > best_val:
            best_val = val
            best_move = m
        if best_val > alpha:
            alpha = best_val
    return best_move
