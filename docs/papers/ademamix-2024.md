# Paper card — AdEMAMix (arXiv:2409.03137, 2024)

| Field | Value |
|---|---|
| Paper | *AdEMAMix: A Smarter Learning Rate Schedule for Adam* — Matteo Pagliardini, Pierre Ablin, David Grangier (Apple), 2024 |
| Reference implementation | `apple/ml-ademamix` (MIT), cloned and read on 2026-09-28; it contains the optimizer only — no data, no experiment scripts |
| Reproduction level | **mechanism-level** (algorithm re-implementation + matched-budget comparison). No number from the paper's tables is claimed |
| Config | `examples/ademamix.json` (SHA-256 `c046217aa4a239a4db2c685c4162efc4ae5cda90fc9e69b03fe28d8417972962`) |
| Tuning sweep | `examples/ademamix-sweep.json` (20 trials: learning rate × warmup length, plus AdamW and momentum) |
| One command | `python scripts/repro.py --suite ademamix` |
| Expected numbers | `expected/expected_ademamix.json` |

## Claim under test

AdEMAMix keeps two EMAs of the gradient — a fast one (`m1`, β1 = 0.9) and a slow one (`m2`, β3 = 0.9999) —
and mixes the slow one in with a coefficient `α` that grows over training, while the second moment is
bias-corrected as in Adam. The paper's claim is that this converges faster (and to a better optimum)
than AdamW, particularly on long training runs. The statement reproduced here is narrower and
checkable: **at a matched epoch budget, does AdEMAMix reach a training-loss target in fewer epochs
than AdamW?**

## Update rule as implemented

Verified line by line against `pytorch/ademamix.py`:

```
m1 ← β1·m1 + (1−β1)·g
m2 ← β3·m2 + (1−β3)·g
v  ← β2·v + (1−β2)·g²
update = (m1/(1−β1ᵗ) + α·m2) / (√(v/(1−β2ᵗ)) + ε)
θ ← θ − lr·(update + λ·θ)
```

with optional `α` linear warmup and `β3` warmup interpolated in half-life space
(`f(β) = log(0.5)/log(β+ε) − 1`). Decoupled weight decay, as in the reference.

## Setup

* Trainer: `logistic` (the same 800-row synthetic task used by the other suites), 120-epoch budget,
  seed 7 for the reference run and seeds 0–9 for the paired comparison.
* Metric: `epochs_to_target` against **0.148**, just above the converged floor (~0.143).
* **Weight decay is set to 0.** The paper's default λ = 0.1 assumes lr ≈ 1e-3; this task runs at
  lr ≈ 0.1–0.8 (full-batch), so the same λ would apply ~100× more decay per step. Setting λ = 0 keeps
  the comparison about the update rule instead of about regularisation. This is a deviation and is
  listed below.
* **Tuning rule (same as every other suite in this repository):** each arm uses the learning rate that
  produced the lowest final training loss inside the grid, ties breaking toward the smaller value.
  AdEMAMix's extra hyper-parameter (warmup length: none / 45 / 120 steps) is tuned by the same rule —
  giving the method its best shot within a documented grid is the only way the comparison is fair.

## Results

Reference run (seed 7):

| arm | tuned learning rate | epochs to 0.148 | final test loss |
|---|---|---:|---:|
| adamw (baseline) | 0.8 | **23** | 0.12255737 |
| **ademamix_tuned** | 0.8 | **23** | 0.12202320 |
| ademamix_no_slow_ema (α = 0) | 0.8 | **23** | 0.12255737 |
| sgd_momentum | 0.8 | 47 | 0.12345500 |
| ademamix_paper_warmups (warmups = 120) | 0.2 | 105 | 0.12415636 |

Ten-seed paired comparison (`runs/ademamix-verified/seed-sweep-summary.md`):

| arm | epochs mean | stdev | range | reached | paired gain vs adamw |
|---|---:|---:|---|---:|---:|
| adamw | 13.7 | 4.69 | 8–23 | 10/10 | — |
| ademamix_tuned | 13.7 | 4.69 | 8–23 | 10/10 | **0.0 ± 0.0 (identical in 10/10 seeds)** |
| ademamix_no_slow_ema | 13.7 | 4.69 | 8–23 | 10/10 | 0.0 ± 0.0 |
| sgd_momentum | 23.3 | 10.88 | 13–47 | 10/10 | −9.6 ± 6.42 |
| ademamix_paper_warmups | 66.5 | 23.49 | 38–105 | 10/10 | −52.8 ± 18.92 |

## Findings

1. **The claim is not reproduced at this scale.** AdEMAMix reaches the target in exactly the same
   epoch as AdamW in **10/10 seeds** (paired difference 0.0), and improves the final test loss by
   0.0005 absolute (0.4% relative) on a single seed. "Faster" is not what this task shows.
2. **The slow EMA does not change when the target is reached**, only the floor it settles on: the
   `α = 0` ablation reproduces AdamW's trajectory and reported loss to all eight printed decimals
   (0.12255737 both) and in the 10-seed sweep its `epochs_to_target` is identical in every seed. That
   identity is the implementation's correctness check — switching the slow EMA off recovers the
   baseline, so the difference measured in the tuned arm really is the slow EMA. (It is equal up to
   floating-point rounding, not bit for bit: the two rules associate their operations differently.
   `tests/test_ademamix.py` pins it at 1e-12 relative, and the paper card says so rather than
   overclaiming.)
3. **The paper's own warmup scheme is budget-sensitive.** With `β3_warmup = α_warmup = 120` (mimicking
   the paper's practice of spreading the warmups over the whole run, which there means 256k steps),
   the arm is **4.5× slower** to the target (105 epochs vs 23) and worse at the floor (0.12416 vs
   0.12256). At a 120-epoch budget the ramps never finish, so the slow EMA mostly contributes an
   extra push to an already adaptive-normalised step.
4. **Momentum is slower, and always has been** in these suites (47 epochs here; it never reaches the
   tighter targets used by the earlier optimizer suite). The interesting comparison is between the
   adaptive methods, and there the honest answer is "indistinguishable".

## Why this is a finding about scale, not a verdict on the method

The slow EMA is designed to pay off over a long horizon (the paper reports language-model training in
the hundreds of thousands of steps at lr ≈ 1e-3). This task is a 120-epoch full-batch convex problem
whose parameters converge in ~20–100 steps; there is simply no long horizon for a second, slower
moving average to exploit, and the paper's `α`/`β3` ramps — designed for the full run — turn into a
transient distortion at this length. The repository therefore reports **"no advantage measured in
this regime"**, not "the method does not work", and any claim about the paper's regime would require
the paper's regime (long-horizon training, mini-batches, and its own harness), which is explicitly
out of scope here.

## Deviations from the paper

| # | Deviation | Reason | Risk |
|---|---|---|---|
| D1 | λ = 0 instead of 0.1 | λ=0.1 with lr≈0.1–0.8 applies ~100× the per-step decay of the paper's lr≈1e-3 setting | the regularisation comparison is untested; the update-rule comparison is cleaner |
| D2 | Logistic-regression trainer, 2 features, 800 rows | keeps the run offline, dependency-free and bit-reproducible | no hidden-layer or matrix-aware behaviour is exercised (that is what `trainers/mlp.py` is for) |
| D3 | Full-batch gradients, 120 epochs | determinism and a two-second runtime | the slow EMA's intended long-horizon regime is not reached |
| D4 | Warmup lengths 0 / 45 / 120 steps | 45 comes from the paper's own usage example, 120 is "spread over the whole run" | the paper's exact schedule for its reported runs is not replayed |
| D5 | `epochs_to_target` at 0.148 | the paper reports loss curves and final metrics, not time-to-target | the metric is a proxy; a loose target would have measured the first step instead |

## Verification and negative control

* `python scripts/repro.py --suite ademamix` → expected numbers verified (`expected/expected_ademamix.json`).
* `python scripts/seed_sweep.py --config examples/ademamix.json --seeds 0-9` → the paired table above.
* Negative control: `scripts/score_task.py` mutates the update rule to drop the slow EMA
  (`alpha * exp_avg_slow[index]` removed) and requires the pinned expectations to fail. A control that
  stops being detected means the task has become unfalsifiable.
* Correctness identity: `tests/test_ademamix.py` asserts that α = 0 reproduces AdamW's curve to
  within 1e-12 relative (same value, differently associated arithmetic), and the 10-seed sweep shows
  identical `epochs_to_target`.
