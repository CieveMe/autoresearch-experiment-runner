from __future__ import annotations

import random
from typing import List, Tuple

Point = Tuple[List[float], int]


def make_dataset(size: int, seed: int, noise: float = 0.18) -> List[Point]:
    """Create a deterministic two-feature binary classification task."""
    rng = random.Random(seed)
    rows: List[Point] = []
    for _ in range(size):
        x1 = rng.uniform(-1.0, 1.0)
        x2 = rng.uniform(-1.0, 1.0)
        margin = 1.35 * x1 - 0.85 * x2 + rng.gauss(0.0, noise)
        rows.append(([x1, x2], 1 if margin >= 0 else 0))
    return rows


def split_dataset(rows: List[Point], test_ratio: float) -> Tuple[List[Point], List[Point]]:
    cut = int(len(rows) * (1.0 - test_ratio))
    if cut <= 0 or cut >= len(rows):
        raise ValueError("test_ratio must leave non-empty train and test sets")
    return rows[:cut], rows[cut:]
