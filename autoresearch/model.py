"""Compatibility shim.

The implementation now lives in ``autoresearch/trainers/`` (the model) and
``autoresearch/optimizers.py`` (the update rules). This module keeps the original import
path working — ``from autoresearch.model import train, evaluate, epochs_to_target`` — so
existing scripts, tests and the negative controls in ``scripts/score_task.py`` keep
pointing at real code while the implementation moves out from under them.
"""

from __future__ import annotations

from .metrics import epochs_to_target
from .optimizers import SUPPORTED_OPTIMIZERS
from .trainers.logistic import evaluate, fit, loss as _loss, sigmoid as _sigmoid, train

__all__ = [
    "SUPPORTED_OPTIMIZERS",
    "epochs_to_target",
    "evaluate",
    "fit",
    "train",
    "_loss",
    "_sigmoid",
]
