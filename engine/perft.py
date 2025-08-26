from typing import List
from .position import Position

def perft(pos: Position, depth: int) -> int:
    """Count leaf nodes at a given depth (tests move generation correctness)."""
    if depth == 0:
        return 1
    nodes = 0
    moves = pos.generate_moves()
    for m in moves:
        pos.make(m)
        nodes += perft(pos, depth - 1)
        pos.unmake(m)
    return nodes

def divide(pos: Position, depth: int) -> List[tuple]:
    """
    Returns list of (move, count) for depth-1 below root.
    Helps spot which branch is wrong when counts don't match.
    """
    results = []
    for m in pos.generate_moves():
        pos.make(m)
        c = perft(pos, depth - 1)
        pos.unmake(m)
        results.append((m, c))
    return results
