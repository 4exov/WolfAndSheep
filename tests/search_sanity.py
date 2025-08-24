from engine.position import from_options_start
from engine.search import find_best_move, alphabeta
from engine.types import Side

def main():
    pos = from_options_start(size=8, wolf_at_top=False)
    print("Side:", "WOLF" if pos.side_to_move == Side.WOLF else "SHEEP")

    m = find_best_move(pos, depth=2)  # start small; we can raise later
    print("Best move @depth2:", None if m is None else (m.fi, m.fj, "->", m.ti, m.tj))

    if m:
        # Show the score after applying the best move (from Wolf's POV)
        pos.make(m)
        val = -alphabeta(pos, depth=1, alpha=-10**9, beta=10**9)
        pos.unmake(m)
        print("Score after best move (Wolf POV):", val)

if __name__ == "__main__":
    main()
