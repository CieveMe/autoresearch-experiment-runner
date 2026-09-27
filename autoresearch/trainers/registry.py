"""Trainer lookup by config key."""

from __future__ import annotations

from typing import Dict

from .logistic import LogisticTrainer
from .mlp import MLPTrainer

TRAINERS: Dict[str, object] = {
    "logistic": LogisticTrainer(),
    "mlp": MLPTrainer(),
}


def get_trainer(name: str):
    key = (name or "logistic").lower()
    if key not in TRAINERS:
        raise ValueError(f"unsupported trainer: {key} (available: {', '.join(sorted(TRAINERS))})")
    return TRAINERS[key]
