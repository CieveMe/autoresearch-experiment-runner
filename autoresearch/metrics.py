"""Metric helpers that are not tied to a particular trainer."""

from __future__ import annotations

from typing import List, Optional


def epochs_to_target(loss_curve: List[float], target_loss: float) -> Optional[int]:
    """First epoch (1-based) whose loss is at or below the target, else None."""
    for index, value in enumerate(loss_curve, start=1):
        if value <= target_loss:
            return index
    return None
