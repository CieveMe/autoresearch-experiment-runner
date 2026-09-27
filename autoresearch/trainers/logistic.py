"""Logistic-regression head — the original trainer, moved without changing its arithmetic."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple

from .. import optimizers as optimizers_module
from ..dataset import Point
from .base import FitResult


def sigmoid(value: float) -> float:
    value = max(-60.0, min(60.0, value))
    return 1.0 / (1.0 + math.exp(-value))


def loss(rows: List[Point], weights: List[float], bias: float, weight_decay: float) -> float:
    total = 0.0
    for features, label in rows:
        probability = sigmoid(sum(w * x for w, x in zip(weights, features)) + bias)
        probability = max(1e-12, min(1.0 - 1e-12, probability))
        total -= label * math.log(probability) + (1 - label) * math.log(1 - probability)
    regularization = weight_decay * sum(w * w for w in weights) / 2.0
    return total / len(rows) + regularization


def fit(rows: List[Point], config: Dict[str, Any]) -> FitResult:
    optimizer = str(config.get("optimizer", "sgd")).lower()
    weight_decay = float(config.get("weight_decay", 0.0))
    decoupled_weight_decay = bool(config.get("decoupled_weight_decay", False))
    max_epochs = int(config.get("epochs", 80))
    tolerance = float(config.get("tolerance", 1e-7))
    weights = [0.0, 0.0]
    bias = 0.0
    state = optimizers_module.initial_state(optimizer, len(weights), config)
    previous_loss = float("inf")
    final_loss = previous_loss
    epochs_run = 0
    loss_curve: List[float] = []

    for epoch in range(1, max_epochs + 1):
        gradients = [0.0, 0.0]
        bias_gradient = 0.0
        for features, label in rows:
            error = sigmoid(sum(w * x for w, x in zip(weights, features)) + bias) - label
            for index, feature in enumerate(features):
                gradients[index] += error * feature
            bias_gradient += error
        scale = 1.0 / len(rows)
        if decoupled_weight_decay:
            gradients = [gradient * scale for gradient in gradients]
        else:
            gradients = [gradient * scale + weight_decay * weights[index] for index, gradient in enumerate(gradients)]
        bias_gradient *= scale
        bias = optimizers_module.apply_update(
            optimizer, weights, bias, gradients, bias_gradient, state, config, epoch
        )
        final_loss = loss(rows, weights, bias, weight_decay)
        loss_curve.append(final_loss)
        epochs_run = epoch
        if abs(previous_loss - final_loss) < tolerance:
            break
        previous_loss = final_loss
    return FitResult(params=(weights, bias), epochs_run=epochs_run, final_loss=final_loss, loss_curve=loss_curve)


def train(rows: List[Point], config: Dict[str, Any]) -> Tuple[List[float], float, int, float, List[float]]:
    """Backwards-compatible 5-tuple form (kept for the existing tests and callers)."""
    result = fit(rows, config)
    weights, bias = result.params
    return weights, bias, result.epochs_run, result.final_loss, result.loss_curve


def evaluate(rows: List[Point], weights: List[float], bias: float, weight_decay: float) -> Dict[str, float]:
    predictions = []
    for features, label in rows:
        probability = sigmoid(sum(w * x for w, x in zip(weights, features)) + bias)
        predictions.append((1 if probability >= 0.5 else 0, label))
    accuracy = sum(prediction == label for prediction, label in predictions) / len(rows)
    return {"accuracy": accuracy, "loss": loss(rows, weights, bias, weight_decay)}


class LogisticTrainer:
    name = "logistic"

    def fit(self, rows: List[Point], config: Dict[str, Any]) -> FitResult:
        return fit(rows, config)

    def evaluate(self, rows: List[Point], params: Any, config: Dict[str, Any]) -> Dict[str, float]:
        weights, bias = params
        return evaluate(rows, weights, bias, float(config.get("weight_decay", 0.0)))
