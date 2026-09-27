from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

from .dataset import Point


def _sigmoid(value: float) -> float:
    value = max(-60.0, min(60.0, value))
    return 1.0 / (1.0 + math.exp(-value))


def _loss(rows: List[Point], weights: List[float], bias: float, weight_decay: float) -> float:
    total = 0.0
    for features, label in rows:
        probability = _sigmoid(sum(w * x for w, x in zip(weights, features)) + bias)
        probability = max(1e-12, min(1.0 - 1e-12, probability))
        total -= label * math.log(probability) + (1 - label) * math.log(1 - probability)
    regularization = weight_decay * sum(w * w for w in weights) / 2.0
    return total / len(rows) + regularization


SUPPORTED_OPTIMIZERS = ("sgd", "sgd_momentum", "adagrad", "rmsprop", "adam")


def train(rows: List[Point], config: Dict[str, float]) -> Tuple[List[float], float, int, float, List[float]]:
    """Train a logistic-regression head and return the full loss curve.

    Returns ``(weights, bias, epochs_run, final_loss, loss_curve)``. The curve is
    what makes a *convergence speed* claim checkable: final metrics alone cannot
    tell "reached the target in 12 epochs" from "reached it in 80".
    """
    optimizer = str(config.get("optimizer", "sgd")).lower()
    learning_rate = float(config.get("learning_rate", 0.15))
    weight_decay = float(config.get("weight_decay", 0.0))
    max_epochs = int(config.get("epochs", 80))
    tolerance = float(config.get("tolerance", 1e-7))
    weights = [0.0, 0.0]
    bias = 0.0
    # Adam / RMSProp / Adagrad state
    first_moment = [0.0, 0.0]
    second_moment = [0.0, 0.0]
    bias_first_moment = 0.0
    bias_second_moment = 0.0
    momentum = float(config.get("momentum", 0.9))
    decay = float(config.get("decay", 0.9))
    velocity = [0.0, 0.0]
    bias_velocity = 0.0
    squared_accumulator = [0.0, 0.0]
    bias_squared_accumulator = 0.0
    rms = [0.0, 0.0]
    bias_rms = 0.0
    bias_correction = bool(config.get("bias_correction", True))
    beta1 = float(config.get("beta1", 0.9))
    beta2 = float(config.get("beta2", 0.999))
    epsilon = float(config.get("epsilon", 1e-8))
    if optimizer not in SUPPORTED_OPTIMIZERS:
        raise ValueError(f"unsupported optimizer: {optimizer}")
    previous_loss = float("inf")
    final_loss = previous_loss
    epochs_run = 0
    loss_curve: List[float] = []

    for epoch in range(1, max_epochs + 1):
        gradients = [0.0, 0.0]
        bias_gradient = 0.0
        for features, label in rows:
            error = _sigmoid(sum(w * x for w, x in zip(weights, features)) + bias) - label
            for index, feature in enumerate(features):
                gradients[index] += error * feature
            bias_gradient += error
        scale = 1.0 / len(rows)
        gradients = [gradient * scale + weight_decay * weights[index] for index, gradient in enumerate(gradients)]
        bias_gradient *= scale
        if optimizer == "adam":
            step = epoch
            for index, gradient in enumerate(gradients):
                first_moment[index] = beta1 * first_moment[index] + (1.0 - beta1) * gradient
                second_moment[index] = beta2 * second_moment[index] + (1.0 - beta2) * gradient * gradient
                corrected_first = first_moment[index] / (1.0 - beta1**step) if bias_correction else first_moment[index]
                corrected_second = second_moment[index] / (1.0 - beta2**step) if bias_correction else second_moment[index]
                weights[index] -= learning_rate * corrected_first / (math.sqrt(corrected_second) + epsilon)
            bias_first_moment = beta1 * bias_first_moment + (1.0 - beta1) * bias_gradient
            bias_second_moment = beta2 * bias_second_moment + (1.0 - beta2) * bias_gradient * bias_gradient
            corrected_bias_first = bias_first_moment / (1.0 - beta1**step) if bias_correction else bias_first_moment
            corrected_bias_second = bias_second_moment / (1.0 - beta2**step) if bias_correction else bias_second_moment
            bias -= learning_rate * corrected_bias_first / (math.sqrt(corrected_bias_second) + epsilon)
        elif optimizer == "sgd_momentum":
            for index, gradient in enumerate(gradients):
                velocity[index] = momentum * velocity[index] + gradient
                weights[index] -= learning_rate * velocity[index]
            bias_velocity = momentum * bias_velocity + bias_gradient
            bias -= learning_rate * bias_velocity
        elif optimizer == "adagrad":
            for index, gradient in enumerate(gradients):
                squared_accumulator[index] += gradient * gradient
                weights[index] -= learning_rate * gradient / (math.sqrt(squared_accumulator[index]) + epsilon)
            bias_squared_accumulator += bias_gradient * bias_gradient
            bias -= learning_rate * bias_gradient / (math.sqrt(bias_squared_accumulator) + epsilon)
        elif optimizer == "rmsprop":
            for index, gradient in enumerate(gradients):
                rms[index] = decay * rms[index] + (1.0 - decay) * gradient * gradient
                weights[index] -= learning_rate * gradient / (math.sqrt(rms[index]) + epsilon)
            bias_rms = decay * bias_rms + (1.0 - decay) * bias_gradient * bias_gradient
            bias -= learning_rate * bias_gradient / (math.sqrt(bias_rms) + epsilon)
        else:
            for index, gradient in enumerate(gradients):
                weights[index] -= learning_rate * gradient
            bias -= learning_rate * bias_gradient
        final_loss = _loss(rows, weights, bias, weight_decay)
        loss_curve.append(final_loss)
        epochs_run = epoch
        if abs(previous_loss - final_loss) < tolerance:
            break
        previous_loss = final_loss
    return weights, bias, epochs_run, final_loss, loss_curve


def epochs_to_target(loss_curve: List[float], target_loss: float) -> Optional[int]:
    """First epoch (1-based) whose loss is at or below the target, else None."""
    for index, value in enumerate(loss_curve, start=1):
        if value <= target_loss:
            return index
    return None


def evaluate(rows: List[Point], weights: List[float], bias: float, weight_decay: float) -> Dict[str, float]:
    predictions = []
    for features, label in rows:
        probability = _sigmoid(sum(w * x for w, x in zip(weights, features)) + bias)
        predictions.append((1 if probability >= 0.5 else 0, label))
    accuracy = sum(prediction == label for prediction, label in predictions) / len(rows)
    return {"accuracy": accuracy, "loss": _loss(rows, weights, bias, weight_decay)}
