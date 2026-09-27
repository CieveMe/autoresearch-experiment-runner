"""Shared trainer interface."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol

from ..dataset import Point


@dataclass
class FitResult:
    """What every trainer returns, plus the curve that makes speed measurable."""

    params: Any
    epochs_run: int
    final_loss: float
    loss_curve: List[float] = field(default_factory=list)


class Trainer(Protocol):
    name: str

    def fit(self, rows: List[Point], config: Dict[str, Any]) -> FitResult:
        ...

    def evaluate(self, rows: List[Point], params: Any, config: Dict[str, Any]) -> Dict[str, float]:
        ...
