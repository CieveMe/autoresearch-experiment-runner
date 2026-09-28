"""A two-layer tanh MLP in pure Python.

Purpose: prove the adapter is real and make matrix-aware optimizers researchable. The
per-parameter update rules are the same object as the logistic trainer's — each hidden
unit's weight row gets its own optimizer state, which is what "per-parameter adaptive"
actually means.
"""

from __future__ import annotations

import math
import random
from typing import Any, Dict, List, Tuple

from .. import optimizers as optimizers_module
from ..dataset import Point
from .base import FitResult


def sigmoid(value: float) -> float:
    value = max(-60.0, min(60.0, value))
    return 1.0 / (1.0 + math.exp(-value))


def _init_params(input_size: int, hidden_sizes: List[int], seed: int) -> Dict[str, Any]:
    """Deterministic Xavier-style initialisation from the config seed."""
    rng = random.Random(seed)
    sizes = [input_size, *hidden_sizes, 1]
    weights: List[List[List[float]]] = []
    biases: List[List[float]] = []
    for layer in range(len(sizes) - 1):
        fan_in, fan_out = sizes[layer], sizes[layer + 1]
        limit = math.sqrt(6.0 / (fan_in + fan_out))
        matrix = [[rng.uniform(-limit, limit) for _ in range(fan_in)] for _ in range(fan_out)]
        weights.append(matrix)
        biases.append([0.0] * fan_out)
    return {"weights": weights, "biases": biases}


def _forward(params: Dict[str, Any], features: List[float]) -> Tuple[List[List[float]], float]:
    """Return (activations per layer, output probability).

    Hidden layers use tanh; the output layer is linear and the sigmoid is applied to it
    once. That convention matters: with tanh on the output too, the gradient of the loss
    w.r.t. the last pre-activation is (p − y)·(1 − tanh²), and forgetting the second
    factor is a ~1% error that looks like a slightly wrong optimizer.
    """
    activations: List[List[float]] = [list(features)]
    current = list(features)
    last_layer = len(params["weights"]) - 1
    for layer, matrix in enumerate(params["weights"]):
        pre = [sum(w * x for w, x in zip(row, current)) + params["biases"][layer][unit]
               for unit, row in enumerate(matrix)]
        current = pre if layer == last_layer else [math.tanh(value) for value in pre]
        activations.append(current)
    return activations, sigmoid(current[0])


def loss(rows: List[Point], params: Dict[str, Any], weight_decay: float) -> float:
    total = 0.0
    for features, label in rows:
        _, probability = _forward(params, features)
        probability = max(1e-12, min(1.0 - 1e-12, probability))
        total -= label * math.log(probability) + (1 - label) * math.log(1 - probability)
    regularization = weight_decay * sum(
        w * w for matrix in params["weights"] for row in matrix for w in row
    ) / 2.0
    return total / len(rows) + regularization


def evaluate(rows: List[Point], params: Dict[str, Any], weight_decay: float) -> Dict[str, float]:
    correct = 0
    for features, label in rows:
        _, probability = _forward(params, features)
        correct += int((1 if probability >= 0.5 else 0) == label)
    return {"accuracy": correct / len(rows), "loss": loss(rows, params, weight_decay)}


def _alloc_states(optimizer: str, params: Dict[str, Any], config: Dict[str, Any]) -> List[Any]:
    """One state object per (weight row, unit bias) pair, plus the output unit."""
    states: List[Any] = []
    for matrix in params["weights"]:
        states.append([optimizers_module.initial_state(optimizer, len(row), config) for row in matrix])
    return states


def gradients(rows: List[Point], params: Dict[str, Any]) -> Dict[str, Any]:
    """Raw (unnormalised) gradients of the summed loss, for every weight and bias.

    Exposed so the training loop and the numerical-gradient test use exactly the same
    code path: a backprop error would otherwise look like "the method does not work".
    """
    grad_weights = [[[0.0] * len(row) for row in matrix] for matrix in params["weights"]]
    grad_biases = [[0.0] * len(bias) for bias in params["biases"]]
    # Standard backprop: delta at the output is (p - y) because sigmoid+BCE cancel;
    # hidden deltas are (W_next^T delta_next) * tanh'(z) = ... * (1 - a^2).
    for features, label in rows:
        activations, probability = _forward(params, features)
        deltas: List[List[float]] = [[0.0] * len(matrix) for matrix in params["weights"]]
        deltas[-1] = [probability - label]
        for layer in range(len(params["weights"]) - 2, -1, -1):
            next_matrix = params["weights"][layer + 1]
            next_delta = deltas[layer + 1]
            deltas[layer] = [
                sum(next_matrix[unit][self_index] * next_delta[unit] for unit in range(len(next_delta)))
                * (1.0 - activations[layer + 1][self_index] ** 2)
                for self_index in range(len(params["weights"][layer]))
            ]
        for layer, delta in enumerate(deltas):
            for unit in range(len(params["weights"][layer])):
                grad_biases[layer][unit] += delta[unit]
                for index, activation in enumerate(activations[layer]):
                    grad_weights[layer][unit][index] += delta[unit] * activation
    return {"weights": grad_weights, "biases": grad_biases}


def fit(rows: List[Point], config: Dict[str, Any]) -> FitResult:
    optimizer = str(config.get("optimizer", "sgd")).lower()
    weight_decay = float(config.get("weight_decay", 0.0))
    max_epochs = int(config.get("epochs", 200))
    tolerance = float(config.get("tolerance", 1e-9))
    hidden_sizes = [int(value) for value in config.get("hidden_sizes", [8])]
    input_size = len(rows[0][0])
    params = _init_params(input_size, hidden_sizes, int(config.get("init_seed", config.get("seed", 0))))
    states = _alloc_states(optimizer, params, config)
    previous_loss = float("inf")
    final_loss = previous_loss
    epochs_run = 0
    loss_curve: List[float] = []
    scale = 1.0 / len(rows)

    for epoch in range(1, max_epochs + 1):
        raw = gradients(rows, params)
        grad_weights, grad_biases = raw["weights"], raw["biases"]
        # Track the evaluation point alongside the training parameters: for schedule-free
        # rules the reported model is the averaged sequence x, not the point y where the
        # gradients are taken. For every other rule the two coincide, so nothing changes.
        eval_params: Dict[str, Any] = {
            "weights": [[[0.0] * len(row) for row in matrix] for matrix in params["weights"]],
            "biases": [[0.0] * len(bias) for bias in params["biases"]],
        }

        for layer, matrix in enumerate(params["weights"]):
            for unit, row in enumerate(matrix):
                unit_gradients = [
                    value * scale + weight_decay * row[index] for index, value in enumerate(grad_weights[layer][unit])
                ]
                updated_bias = optimizers_module.apply_update(
                    optimizer,
                    row,
                    params["biases"][layer][unit],
                    unit_gradients,
                    grad_biases[layer][unit] * scale,
                    states[layer][unit],
                    config,
                    epoch,
                )
                params["biases"][layer][unit] = updated_bias
                row_eval, bias_eval = optimizers_module.eval_params(
                    optimizer, row, updated_bias, states[layer][unit]
                )
                eval_params["weights"][layer][unit] = row_eval
                eval_params["biases"][layer][unit] = bias_eval
        final_loss = loss(rows, eval_params, weight_decay)
        loss_curve.append(final_loss)
        epochs_run = epoch
        if abs(previous_loss - final_loss) < tolerance:
            break
        previous_loss = final_loss
    eval_params = _eval_params(optimizer, params, states)
    return FitResult(params=eval_params, epochs_run=epochs_run, final_loss=final_loss, loss_curve=loss_curve)


def _eval_params(optimizer: str, params: Dict[str, Any], states: List[Any]) -> Dict[str, Any]:
    """Assemble the evaluation-point parameters from the per-unit optimizer states.

    For schedule-free rules this is the averaged sequence `x`; for every other rule it is the
    training parameters themselves, so nothing about the existing results changes.
    """
    eval_params: Dict[str, Any] = {"weights": [], "biases": []}
    for layer, matrix in enumerate(params["weights"]):
        eval_rows = []
        eval_biases = []
        for unit, row in enumerate(matrix):
            row_eval, bias_eval = optimizers_module.eval_params(
                optimizer, row, params["biases"][layer][unit], states[layer][unit]
            )
            eval_rows.append(row_eval)
            eval_biases.append(bias_eval)
        eval_params["weights"].append(eval_rows)
        eval_params["biases"].append(eval_biases)
    return eval_params


class MLPTrainer:
    name = "mlp"

    def fit(self, rows: List[Point], config: Dict[str, Any]) -> FitResult:
        return fit(rows, config)

    def evaluate(self, rows: List[Point], params: Any, config: Dict[str, Any]) -> Dict[str, float]:
        return evaluate(rows, params, float(config.get("weight_decay", 0.0)))
