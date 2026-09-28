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


HIDDEN_ACTIVATIONS = ("tanh", "relu", "gelu")
# Normalisation of the hidden pre-activations. `none` is the original arithmetic;
# the other two are modelling choices a suite can vary, and both are verifiable
# against finite differences exactly like the activations are.
HIDDEN_NORMS = ("none", "layernorm", "batchnorm")
# Weight-initialisation scaling. `xavier` is the original (Glorot) limit and stays the
# default so every existing pinned number is unaffected; `he` scales by fan-in only and
# `plain` is a fixed 0.05, which is what a hand-written trainer usually starts with.
INIT_SCHEMES = ("xavier", "he", "plain")

NORM_EPSILON = 1e-5


def _init_limit(scheme: str, fan_in: int, fan_out: int) -> float:
    if scheme == "xavier":
        return math.sqrt(6.0 / (fan_in + fan_out))
    if scheme == "he":
        return math.sqrt(6.0 / fan_in)
    if scheme == "plain":
        return 0.05
    raise ValueError(f"unsupported init_scheme: {scheme} (available: {', '.join(INIT_SCHEMES)})")


def _init_params(
    input_size: int, hidden_sizes: List[int], seed: int, scheme: str = "xavier"
) -> Dict[str, Any]:
    """Deterministic initialisation from the config seed, with a selectable scaling."""
    rng = random.Random(seed)
    sizes = [input_size, *hidden_sizes, 1]
    weights: List[List[List[float]]] = []
    biases: List[List[float]] = []
    for layer in range(len(sizes) - 1):
        fan_in, fan_out = sizes[layer], sizes[layer + 1]
        limit = _init_limit(scheme, fan_in, fan_out)
        matrix = [[rng.uniform(-limit, limit) for _ in range(fan_in)] for _ in range(fan_out)]
        weights.append(matrix)
        biases.append([0.0] * fan_out)
    return {"weights": weights, "biases": biases}


def _activate(name: str, value: float) -> float:
    if name == "tanh":
        return math.tanh(value)
    if name == "relu":
        return value if value > 0.0 else 0.0
    if name == "gelu":
        # Exact (erf) GELU rather than the tanh approximation, so the derivative below is exact too.
        return 0.5 * value * (1.0 + math.erf(value / math.sqrt(2.0)))
    raise ValueError(f"unsupported hidden activation: {name} (available: {', '.join(HIDDEN_ACTIVATIONS)})")


def _activation_derivative(name: str, pre: float, activated: float) -> float:
    if name == "tanh":
        return 1.0 - activated ** 2
    if name == "relu":
        return 1.0 if pre > 0.0 else 0.0
    if name == "gelu":
        cdf = 0.5 * (1.0 + math.erf(pre / math.sqrt(2.0)))
        density = math.exp(-0.5 * pre * pre) / math.sqrt(2.0 * math.pi)
        return cdf + pre * density
    raise ValueError(f"unsupported hidden activation: {name}")


def _forward_batch(
    rows: List[Point], params: Dict[str, Any], activation: str = "tanh", norm: str = "none"
) -> Dict[str, Any]:
    """Forward pass for a whole batch, keeping what the backward pass needs.

    The output layer is linear and the sigmoid is applied to it once. That convention
    matters: with tanh on the output too, the gradient of the loss w.r.t. the last
    pre-activation is (p − y)·(1 − tanh²), and forgetting the second factor is a ~1%
    error that looks like a slightly wrong optimizer.

    `norm` normalises the hidden pre-activations, and it is the only place where rows
    are not independent: `batchnorm` takes its statistics across the batch, `layernorm`
    across the units of one row. There are no running statistics, so the statistics are
    recomputed on whatever batch is passed in — an honest scope note, not an oversight.
    `none` reproduces the original arithmetic term for term.
    """
    if norm not in HIDDEN_NORMS:
        raise ValueError(f"unsupported hidden_norm: {norm} (available: {', '.join(HIDDEN_NORMS)})")
    count = len(rows)
    last_layer = len(params["weights"]) - 1
    activations: List[List[List[float]]] = [[list(features) for features, _ in rows]]
    pre_activations: List[List[List[float]]] = []
    normalised: List[List[List[float]]] = []
    statistics: List[Any] = []
    for layer, matrix in enumerate(params["weights"]):
        inputs = activations[layer]
        pre_rows = [
            [sum(w * x for w, x in zip(row, inputs[index])) + params["biases"][layer][unit]
             for unit, row in enumerate(matrix)]
            for index in range(count)
        ]
        if layer == last_layer or norm == "none":
            current = pre_rows
            statistics.append(None)
        elif norm == "batchnorm":
            width = len(matrix)
            means = [sum(pre_rows[index][unit] for index in range(count)) / count
                     for unit in range(width)]
            variances = [sum((pre_rows[index][unit] - means[unit]) ** 2 for index in range(count)) / count
                         for unit in range(width)]
            scales = [1.0 / math.sqrt(value + NORM_EPSILON) for value in variances]
            current = [[(pre_rows[index][unit] - means[unit]) * scales[unit] for unit in range(width)]
                       for index in range(count)]
            statistics.append((means, scales))
        else:  # layernorm: statistics across the units of one row
            width = len(matrix)
            means, scales, current = [], [], []
            for index in range(count):
                mean = sum(pre_rows[index]) / width
                variance = sum((value - mean) ** 2 for value in pre_rows[index]) / width
                scale = 1.0 / math.sqrt(variance + NORM_EPSILON)
                means.append(mean)
                scales.append(scale)
                current.append([(value - mean) * scale for value in pre_rows[index]])
            statistics.append((means, scales))
        pre_activations.append(pre_rows)
        normalised.append(current)
        activations.append(
            current if layer == last_layer
            else [[_activate(activation, value) for value in row] for row in current]
        )
    probabilities = [sigmoid(normalised[last_layer][index][0]) for index in range(count)]
    return {
        "activations": activations,
        "pre_activations": pre_activations,
        "normalised": normalised,
        "statistics": statistics,
        "probabilities": probabilities,
    }


def _forward(
    params: Dict[str, Any], features: List[float], activation: str = "tanh", norm: str = "none"
) -> Tuple[List[List[float]], List[List[float]], float]:
    """Single-row convenience wrapper: (activations, pre-activations, probability).

    For `batchnorm` a batch of one row has zero variance, so this wrapper is only
    meaningful for `none` and `layernorm`; the training path always goes through
    `_forward_batch`.
    """
    forward = _forward_batch([(list(features), 0)], params, activation, norm)
    return forward["activations"], forward["pre_activations"], forward["probabilities"][0]


def loss(
    rows: List[Point], params: Dict[str, Any], weight_decay: float,
    activation: str = "tanh", norm: str = "none",
) -> float:
    total = 0.0
    forward = _forward_batch(rows, params, activation, norm)
    for index, (_, label) in enumerate(rows):
        probability = forward["probabilities"][index]
        probability = max(1e-12, min(1.0 - 1e-12, probability))
        total -= label * math.log(probability) + (1 - label) * math.log(1 - probability)
    regularization = weight_decay * sum(
        w * w for matrix in params["weights"] for row in matrix for w in row
    ) / 2.0
    return total / len(rows) + regularization


def evaluate(
    rows: List[Point], params: Dict[str, Any], weight_decay: float,
    activation: str = "tanh", norm: str = "none",
) -> Dict[str, float]:
    correct = 0
    forward = _forward_batch(rows, params, activation, norm)
    for index, (_, label) in enumerate(rows):
        probability = forward["probabilities"][index]
        correct += int((1 if probability >= 0.5 else 0) == label)
    return {"accuracy": correct / len(rows), "loss": loss(rows, params, weight_decay, activation, norm)}


def _alloc_states(optimizer: str, params: Dict[str, Any], config: Dict[str, Any]) -> List[Any]:
    """One state object per (weight row, unit bias) pair, plus the output unit."""
    states: List[Any] = []
    for matrix in params["weights"]:
        states.append([optimizers_module.initial_state(optimizer, len(row), config) for row in matrix])
    return states


def _normalisation_backward(
    norm: str, dz_rows: List[List[float]], normalised: List[List[float]], statistics: Any, count: int
) -> List[List[float]]:
    """Turn dL/dz into dL/d(pre-activation) for one layer.

    Both normalisations have the same shape — subtract the mean of the gradient, subtract
    the component along the normalised value, rescale — and differ only in which axis the
    mean is taken over: the batch for batchnorm, the units of one row for layernorm. The
    finite-difference test covers every case, because 'the normalisation backward pass is
    slightly wrong' is indistinguishable from 'this optimizer does not work'.
    """
    if norm == "none" or statistics is None:
        return [list(row) for row in dz_rows]
    means, scales = statistics
    if norm == "batchnorm":
        width = len(dz_rows[0])
        totals = [sum(dz_rows[index][unit] for index in range(count)) for unit in range(width)]
        products = [
            sum(dz_rows[index][unit] * normalised[index][unit] for index in range(count))
            for unit in range(width)
        ]
        return [
            [
                (dz_rows[index][unit]
                 - totals[unit] / count
                 - normalised[index][unit] * products[unit] / count) * scales[unit]
                for unit in range(width)
            ]
            for index in range(count)
        ]
    # layernorm
    result: List[List[float]] = []
    for index in range(count):
        width = len(dz_rows[index])
        total = sum(dz_rows[index])
        product = sum(dz_rows[index][unit] * normalised[index][unit] for unit in range(width))
        result.append([
            (dz_rows[index][unit] - total / width - normalised[index][unit] * product / width)
            * scales[index]
            for unit in range(width)
        ])
    return result


def gradients(
    rows: List[Point], params: Dict[str, Any], activation: str = "tanh", norm: str = "none"
) -> Dict[str, Any]:
    """Raw (unnormalised) gradients of the summed loss, for every weight and bias.

    Exposed so the training loop and the numerical-gradient test use exactly the same
    code path: a backprop error would otherwise look like "the method does not work".

    The chain is propagated layer by layer over the whole batch rather than row by row,
    because normalisation is the one place where rows stop being independent. With
    `norm="none"` every quantity is the same one the row-at-a-time version produced, in
    the same order, so the existing pinned numbers do not move.
    """
    count = len(rows)
    last_layer = len(params["weights"]) - 1
    forward = _forward_batch(rows, params, activation, norm)
    grad_weights = [[[0.0] * len(row) for row in matrix] for matrix in params["weights"]]
    grad_biases = [[0.0] * len(bias) for bias in params["biases"]]
    # Standard backprop: delta at the output is (p - y) because sigmoid+BCE cancel;
    # hidden deltas are (W_next^T delta_next) * act'(z), and then through the
    # normalisation if there is one.
    deltas: List[Any] = [None] * len(params["weights"])
    deltas[last_layer] = [[forward["probabilities"][index] - label] for index, (_, label) in enumerate(rows)]
    for layer in range(last_layer - 1, -1, -1):
        next_matrix = params["weights"][layer + 1]
        next_delta = deltas[layer + 1]
        normalised_rows = forward["normalised"][layer]
        activated_rows = forward["activations"][layer + 1]
        dz_rows = [
            [
                sum(next_matrix[unit][self_index] * next_delta[index][unit]
                    for unit in range(len(next_delta[index])))
                * _activation_derivative(
                    activation, normalised_rows[index][self_index], activated_rows[index][self_index]
                )
                for self_index in range(len(params["weights"][layer]))
            ]
            for index in range(count)
        ]
        deltas[layer] = _normalisation_backward(
            norm, dz_rows, normalised_rows, forward["statistics"][layer], count
        )
    # Accumulate once per layer, with the rows still in their original order, so the
    # floating-point sums are the same ones the previous implementation produced.
    for layer, delta in enumerate(deltas):
        for unit in range(len(params["weights"][layer])):
            for index in range(count):
                grad_biases[layer][unit] += delta[index][unit]
            for index in range(count):
                layer_inputs = forward["activations"][layer][index]
                for position, layer_input in enumerate(layer_inputs):
                    grad_weights[layer][unit][position] += delta[index][unit] * layer_input
    return {"weights": grad_weights, "biases": grad_biases}


def fit(rows: List[Point], config: Dict[str, Any]) -> FitResult:
    optimizer = str(config.get("optimizer", "sgd")).lower()
    weight_decay = float(config.get("weight_decay", 0.0))
    max_epochs = int(config.get("epochs", 200))
    tolerance = float(config.get("tolerance", 1e-9))
    hidden_sizes = [int(value) for value in config.get("hidden_sizes", [8])]
    activation = str(config.get("hidden_activation", "tanh")).lower()
    norm = str(config.get("hidden_norm", "none")).lower()
    scheme = str(config.get("init_scheme", "xavier")).lower()
    input_size = len(rows[0][0])
    params = _init_params(
        input_size, hidden_sizes, int(config.get("init_seed", config.get("seed", 0))), scheme
    )
    states = _alloc_states(optimizer, params, config)
    previous_loss = float("inf")
    final_loss = previous_loss
    epochs_run = 0
    loss_curve: List[float] = []
    scale = 1.0 / len(rows)

    for epoch in range(1, max_epochs + 1):
        raw = gradients(rows, params, activation, norm)
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
        final_loss = loss(rows, eval_params, weight_decay, activation, norm)
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
        return evaluate(
            rows,
            params,
            float(config.get("weight_decay", 0.0)),
            str(config.get("hidden_activation", "tanh")).lower(),
            str(config.get("hidden_norm", "none")).lower(),
        )
