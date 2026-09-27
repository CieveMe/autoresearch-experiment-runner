"""Trainers: the replaceable part of the harness.

`logistic` is the original behaviour, moved without arithmetic changes. `mlp` is a
second trainer that exists to prove the adapter is real (same configuration, same
optimizer set, different model) and to make matrix-aware optimizer research possible.
"""

from .base import FitResult
from .registry import TRAINERS, get_trainer

__all__ = ["FitResult", "TRAINERS", "get_trainer"]
