"""Learning-rate and coefficient schedules.

Default is ``constant``: ``schedule_factor`` then returns exactly ``1.0``, so routing
the existing optimizers through it cannot change a single bit of their arithmetic.
The AdEMAMix warmups follow the reference implementation (``apple/ml-ademamix``).
"""

from __future__ import annotations

import math
from typing import Any, Dict, Optional


def schedule_factor(step: int, config: Dict[str, Any]) -> float:
    """Multiplier applied to ``learning_rate`` for this step."""
    schedule = str(config.get("schedule", "constant")).lower()
    if schedule == "constant":
        return 1.0
    total = int(config.get("epochs", 1))
    if schedule == "cosine":
        return cosine_factor(step, total, float(config.get("min_lr_factor", 0.0)))
    if schedule == "warmup_cosine":
        warmup = int(config.get("warmup_steps", 0))
        if warmup and step <= warmup:
            return step / float(warmup)
        return cosine_factor(step - warmup, total - warmup, float(config.get("min_lr_factor", 0.0)))
    raise ValueError(f"unsupported schedule: {schedule}")


def cosine_factor(step: int, total_steps: int, min_lr_factor: float = 0.0) -> float:
    """Cosine decay from 1.0 at the first step to ``min_lr_factor`` at the last one."""
    if total_steps <= 1:
        return 1.0
    clamped = min(max(step, 1), total_steps)
    progress = (clamped - 1) / float(total_steps - 1)
    return min_lr_factor + (1.0 - min_lr_factor) * 0.5 * (1.0 + math.cos(math.pi * progress))


def linear_warmup(step: int, end: float, start: float = 0.0, warmup: Optional[int] = None) -> float:
    """Upstream ``linear_warmup_scheduler``: linear ramp, then the final value."""
    if not warmup:
        return end
    if step < warmup:
        ratio = step / float(warmup)
        return (1.0 - ratio) * start + ratio * end
    return end


def _half_life(beta: float, eps: float = 1e-8) -> float:
    return math.log(0.5) / math.log(beta + eps) - 1


def _half_life_inverse(value: float) -> float:
    return math.pow(0.5, 1 / (value + 1))


def linear_hl_warmup(step: int, end: float, start: float = 0.0, warmup: Optional[int] = None) -> float:
    """Upstream ``linear_hl_warmup_scheduler``: interpolate in half-life space."""
    if not warmup:
        return end
    if step < warmup:
        ratio = step / float(warmup)
        return _half_life_inverse((1.0 - ratio) * _half_life(start) + ratio * _half_life(end))
    return end


def alpha_schedule(step: int, alpha_final: float, alpha_warmup: Optional[int]) -> float:
    return linear_warmup(step, alpha_final, 0.0, alpha_warmup)


def beta3_schedule(step: int, beta3_final: float, beta3_warmup: Optional[int]) -> float:
    return linear_hl_warmup(step, beta3_final, 0.0, beta3_warmup)
