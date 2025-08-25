from dataclasses import dataclass

@dataclass
class SearchConfig:
    max_depth: int = 4         # fallback depth if no time limit
    time_ms: int = 0           # 0 = no time control yet
    use_iterative_deepening: bool = True
    use_tt: bool = False
    # future toggles: aspiration, killer, history, etc.
