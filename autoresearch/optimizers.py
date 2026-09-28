"""Update rules, kept in one place.

Every rule is written against a plain list of parameters, so the same implementation
serves the logistic trainer and the MLP trainer. The arithmetic of the rules that
existed before this module was extracted is deliberately unchanged, expression for
expression: the pinned expectations in ``expected/`` are the regression test for that.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List

from . import schedules

SUPPORTED_OPTIMIZERS = (
    "sgd",
    "sgd_momentum",
    "adagrad",
    "rmsprop",
    "adam",
    "adamw",
    "ademamix",
    "schedule_free_adamw",
    "schedule_free_sgd",
)

# Rules that keep two sequences and are evaluated at the averaged one. Everything that
# reads the model's parameters has to go through `eval_params` for these, or the reported
# loss would be measured at the training point while the parameter update lives elsewhere.
SCHEDULE_FREE_OPTIMIZERS = ("schedule_free_adamw", "schedule_free_sgd")


def initial_state(optimizer: str, size: int, config: Dict[str, Any]) -> Dict[str, Any]:
    """Allocate every buffer a rule might need (sized to the parameter vector)."""
    return {
        "first_moment": [0.0] * size,
        "second_moment": [0.0] * size,
        "bias_first_moment": 0.0,
        "bias_second_moment": 0.0,
        "velocity": [0.0] * size,
        "bias_velocity": 0.0,
        "squared_accumulator": [0.0] * size,
        "bias_squared_accumulator": 0.0,
        "rms": [0.0] * size,
        "bias_rms": 0.0,
        "exp_avg_fast": [0.0] * size,
        "exp_avg_slow": [0.0] * size,
        "exp_avg_sq": [0.0] * size,
        "bias_exp_avg_fast": 0.0,
        "bias_exp_avg_slow": 0.0,
        "bias_exp_avg_sq": 0.0,
    }


def apply_update(
    optimizer: str,
    weights: List[float],
    bias: float,
    gradients: List[float],
    bias_gradient: float,
    state: Dict[str, Any],
    config: Dict[str, Any],
    epoch: int,
) -> float:
    """Apply one step in place on ``weights`` and return the updated bias."""
    if optimizer not in SUPPORTED_OPTIMIZERS:
        raise ValueError(f"unsupported optimizer: {optimizer}")
    learning_rate = float(config.get("learning_rate", 0.15)) * schedules.schedule_factor(epoch, config)
    epsilon = float(config.get("epsilon", 1e-8))

    if optimizer in {"adam", "adamw"}:
        beta1 = float(config.get("beta1", 0.9))
        beta2 = float(config.get("beta2", 0.999))
        bias_correction = bool(config.get("bias_correction", True))
        # AdamW differs from Adam only in how weight decay is applied: decoupled from
        # the adaptive step instead of added to the gradient. The `adam` path performs
        # exactly the operations it did before this variant existed.
        decoupled = optimizer == "adamw"
        weight_decay = float(config.get("weight_decay", 0.0))
        first_moment = state["first_moment"]
        second_moment = state["second_moment"]
        step = epoch
        for index, gradient in enumerate(gradients):
            first_moment[index] = beta1 * first_moment[index] + (1.0 - beta1) * gradient
            second_moment[index] = beta2 * second_moment[index] + (1.0 - beta2) * gradient * gradient
            corrected_first = first_moment[index] / (1.0 - beta1**step) if bias_correction else first_moment[index]
            corrected_second = second_moment[index] / (1.0 - beta2**step) if bias_correction else second_moment[index]
            weights[index] -= learning_rate * corrected_first / (math.sqrt(corrected_second) + epsilon)
            if decoupled:
                weights[index] -= learning_rate * weight_decay * weights[index]
        state["bias_first_moment"] = beta1 * state["bias_first_moment"] + (1.0 - beta1) * bias_gradient
        state["bias_second_moment"] = beta2 * state["bias_second_moment"] + (1.0 - beta2) * bias_gradient * bias_gradient
        corrected_bias_first = (
            state["bias_first_moment"] / (1.0 - beta1**step) if bias_correction else state["bias_first_moment"]
        )
        corrected_bias_second = (
            state["bias_second_moment"] / (1.0 - beta2**step) if bias_correction else state["bias_second_moment"]
        )
        bias -= learning_rate * corrected_bias_first / (math.sqrt(corrected_bias_second) + epsilon)
        if decoupled:
            bias -= learning_rate * weight_decay * bias
        return bias

    if optimizer == "sgd_momentum":
        momentum = float(config.get("momentum", 0.9))
        velocity = state["velocity"]
        for index, gradient in enumerate(gradients):
            velocity[index] = momentum * velocity[index] + gradient
            weights[index] -= learning_rate * velocity[index]
        state["bias_velocity"] = momentum * state["bias_velocity"] + bias_gradient
        return bias - learning_rate * state["bias_velocity"]

    if optimizer == "adagrad":
        squared_accumulator = state["squared_accumulator"]
        for index, gradient in enumerate(gradients):
            squared_accumulator[index] += gradient * gradient
            weights[index] -= learning_rate * gradient / (math.sqrt(squared_accumulator[index]) + epsilon)
        state["bias_squared_accumulator"] += bias_gradient * bias_gradient
        return bias - learning_rate * bias_gradient / (math.sqrt(state["bias_squared_accumulator"]) + epsilon)

    if optimizer == "rmsprop":
        decay = float(config.get("decay", 0.9))
        rms = state["rms"]
        for index, gradient in enumerate(gradients):
            rms[index] = decay * rms[index] + (1.0 - decay) * gradient * gradient
            weights[index] -= learning_rate * gradient / (math.sqrt(rms[index]) + epsilon)
        state["bias_rms"] = decay * state["bias_rms"] + (1.0 - decay) * bias_gradient * bias_gradient
        return bias - learning_rate * bias_gradient / (math.sqrt(state["bias_rms"]) + epsilon)

    if optimizer == "ademamix":
        # AdEMAMix (Apple, arXiv:2409.03137): a fast EMA, a slow EMA mixed in with a
        # growing coefficient alpha, and bias-corrected second moments. Decoupled
        # weight decay, as in the reference implementation.
        beta1 = float(config.get("beta1", 0.9))
        beta2 = float(config.get("beta2", 0.999))
        beta3 = float(config.get("beta3", 0.9999))
        alpha_final = float(config.get("alpha", 2.0))
        weight_decay = float(config.get("weight_decay", 0.0))
        alpha = schedules.alpha_schedule(epoch, alpha_final, config.get("alpha_warmup"))
        beta3_step = schedules.beta3_schedule(epoch, beta3, config.get("beta3_warmup"))
        exp_avg_fast = state["exp_avg_fast"]
        exp_avg_slow = state["exp_avg_slow"]
        exp_avg_sq = state["exp_avg_sq"]
        step = epoch
        for index, gradient in enumerate(gradients):
            if beta1 > 0.0:
                exp_avg_fast[index] = beta1 * exp_avg_fast[index] + (1.0 - beta1) * gradient
            else:
                exp_avg_fast[index] = gradient
            exp_avg_slow[index] = beta3_step * exp_avg_slow[index] + (1.0 - beta3_step) * gradient
            exp_avg_sq[index] = beta2 * exp_avg_sq[index] + (1.0 - beta2) * gradient * gradient
            bias_correction1 = 1.0 - beta1**step
            bias_correction2 = 1.0 - beta2**step
            denom = math.sqrt(exp_avg_sq[index] / bias_correction2) + epsilon
            update = (exp_avg_fast[index] / bias_correction1 + alpha * exp_avg_slow[index]) / denom
            weights[index] -= learning_rate * (update + weight_decay * weights[index])
        if beta1 > 0.0:
            state["bias_exp_avg_fast"] = beta1 * state["bias_exp_avg_fast"] + (1.0 - beta1) * bias_gradient
        else:
            state["bias_exp_avg_fast"] = bias_gradient
        state["bias_exp_avg_slow"] = beta3_step * state["bias_exp_avg_slow"] + (1.0 - beta3_step) * bias_gradient
        state["bias_exp_avg_sq"] = beta2 * state["bias_exp_avg_sq"] + (1.0 - beta2) * bias_gradient * bias_gradient
        bias_correction1 = 1.0 - beta1**step
        bias_correction2 = 1.0 - beta2**step
        denom = math.sqrt(state["bias_exp_avg_sq"] / bias_correction2) + epsilon
        update = (state["bias_exp_avg_fast"] / bias_correction1 + alpha * state["bias_exp_avg_slow"]) / denom
        return bias - learning_rate * (update + weight_decay * bias)

    if optimizer in SCHEDULE_FREE_OPTIMIZERS:
        # Schedule-Free (arXiv:2405.15682), transliterated from
        # `adamw_schedulefree_reference.py`: keep z (the point the update moves) and x (the
        # running average of z), evaluate at x, and take gradients at the interpolation
        # y = beta1*x + (1-beta1)*z. `epoch` plays the role of the reference's k+1.
        beta1 = float(config.get("beta1", 0.9))
        beta2 = float(config.get("beta2", 0.999))
        average_power = float(config.get("average_power", 0.0))
        weight_lr_power = float(config.get("weight_lr_power", 2.0))
        warmup_steps = int(config.get("warmup_steps", 0))
        weight_decay = float(config.get("weight_decay", 0.0))
        if "z" not in state:
            state["z"] = list(weights)
            state["x"] = list(weights)
            state["exp_avg_sq"] = [0.0] * len(weights)
            state["bias_z"] = bias
            state["bias_x"] = bias
            state["bias_exp_avg_sq"] = 0.0
            state["lr_max"] = 0.0
            state["weight_sum"] = 0.0
        step = epoch
        schedule = (step / warmup_steps) if (warmup_steps and step <= warmup_steps) else 1.0
        learning_rate = float(config.get("learning_rate", 0.15)) * schedule
        state["lr_max"] = max(learning_rate, state["lr_max"])
        weight = (step ** average_power) * (state["lr_max"] ** weight_lr_power)
        state["weight_sum"] += weight
        ckp1 = (weight / state["weight_sum"]) if state["weight_sum"] else 0.0
        bias_correction2 = 1.0 - beta2**step
        z_values = state["z"]
        x_values = state["x"]
        squared = state["exp_avg_sq"]
        for index, gradient in enumerate(gradients):
            if weight_decay:
                # decay_at_y is the reference default
                z_values[index] -= learning_rate * weight_decay * weights[index]
            if optimizer == "schedule_free_adamw":
                squared[index] = beta2 * squared[index] + (1.0 - beta2) * gradient * gradient
                denom = math.sqrt(squared[index] / bias_correction2) + epsilon
                z_values[index] -= learning_rate * gradient / denom
            else:
                z_values[index] -= learning_rate * gradient
            x_values[index] = (1.0 - ckp1) * x_values[index] + ckp1 * z_values[index]
            weights[index] = beta1 * x_values[index] + (1.0 - beta1) * z_values[index]
        if weight_decay:
            state["bias_z"] -= learning_rate * weight_decay * bias
        if optimizer == "schedule_free_adamw":
            state["bias_exp_avg_sq"] = (
                beta2 * state["bias_exp_avg_sq"] + (1.0 - beta2) * bias_gradient * bias_gradient
            )
            denom = math.sqrt(state["bias_exp_avg_sq"] / bias_correction2) + epsilon
            state["bias_z"] -= learning_rate * bias_gradient / denom
        else:
            state["bias_z"] -= learning_rate * bias_gradient
        state["bias_x"] = (1.0 - ckp1) * state["bias_x"] + ckp1 * state["bias_z"]
        return beta1 * state["bias_x"] + (1.0 - beta1) * state["bias_z"]

    # plain stochastic gradient descent
    for index, gradient in enumerate(gradients):
        weights[index] -= learning_rate * gradient
    return bias - learning_rate * bias_gradient


def eval_params(
    optimizer: str,
    weights: List[float],
    bias: float,
    state: Dict[str, Any],
) -> tuple:
    """The parameters to *report*: the averaged sequence for schedule-free rules.

    The reference implementation evaluates in `.eval()` mode at `x`, never at `y`; using the
    training point for metrics would make the comparison with scheduled baselines unfair in
    the method's favour, because `y` is the point the update was just pulled towards.
    """
    if optimizer in SCHEDULE_FREE_OPTIMIZERS and "x" in state:
        return state["x"], state["bias_x"]
    return weights, bias
