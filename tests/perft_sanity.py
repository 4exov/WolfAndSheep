from engine.position import from_options_start
from engine.perft import perft, divide
from engine.types import Side

def main():
    pos = from_options_start(size=8, wolf_at_top=False)
    print("Side:", "WOLF" if pos.side_to_move == Side.WOLF else "SHEEP")

    for d in (1, 2, 3):
        n = perft(pos, d)
        print(f"perft({d}) =", n)

    print("divide(2):")
    for m, c in divide(pos, 2):
        print(f"  {(m.fi, m.fj)} -> {(m.ti, m.tj)} : {c}")

if __name__ == "__main__":
    main()
