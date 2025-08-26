from engine.position import from_options_start
from engine.types import Side

def main():
    pos = from_options_start(size=8, wolf_at_top=False)
    print("Board size:", pos.size)
    print("Side to move:", "WOLF" if pos.side_to_move == Side.WOLF else "SHEEP")

    done, score = pos.is_terminal()
    print("Terminal?", done, "Score:", score)

    moves = pos.generate_moves()
    print("Initial legal moves count:", len(moves))
    for m in moves[:8]:
        print("  move:", (m.fi, m.fj), "->", (m.ti, m.tj))

    if moves:
        m0 = moves[0]
        old_wolf = pos.wolf_pos
        pos.make(m0)
        pos.unmake(m0)
        assert pos.wolf_pos == old_wolf, "unmake failed to restore wolf position"
        print("Make/unmake round-trip: OK")

if __name__ == "__main__":
    main()
