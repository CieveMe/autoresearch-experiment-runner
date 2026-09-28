# Paper card — AdEMAMix (arXiv:2409.03137, 2024)

| Field | Value |
|---|---|
| Paper | *AdEMAMix: A Smarter Learning Rate Schedule for Adam* — Matteo Pagliardini, Pierre Ablin, David Grangier (Apple), 2024 |
| Reference implementation | `apple/ml-ademamix` (MIT), cloned and read on 2026-09-28; it contains the optimizer only — no data, no experiment scripts |
| Reproduction level | **mechanism-level** (algorithm re-implementation + matched-budget comparison). No number from the paper's tables is claimed |
| Trainers tested | **Two model families and five capacities**: the logistic head (2 weights + bias) and tanh MLPs at `[8]`, `[32]`, `[8,8]`, `[64]` and `[16,16]`. All point the same way — see "Two model families, one direction" below and `REPRODUCTION.md` §5.13 |
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

### The MLP re-run (added 2026-09-28, same session)

Everything above used the logistic head, which is almost convex and converges in tens of steps — so
"the slow EMA does not help" could have been an artefact of the model, not of the method. The suite was
therefore re-run with `trainer: "mlp"` (two-layer tanh, 8 hidden units, retuned for that model via
`examples/ademamix-mlp-sweep.json`), and the answer is that **the conclusion survives**:

| arm (10 seeds, MLP) | mean test loss | stdev | seeds beating AdamW |
|---|---:|---:|---:|
| adamw | 0.13218 | 0.02473 | — |
| ademamix, no warmups | 0.13249 | 0.02483 | 3/10 |
| ademamix, warmups = 45 | 0.14269 | 0.03485 | 3/10 |
| ademamix, warmups = 120 | 0.15261 | 0.03962 | 2/10 |

On speed the MLP is if anything harsher: Adam averages 20.3 epochs to the target against AdaGrad's 6.2
and momentum's 7.0, and AdEMAMix again matches AdamW rather than beating it.

**A trap worth recording.** At seed 7 the MLP numbers favour `ademamix_warmup_45` (test loss 0.12124),
which is the second-worst arm over ten seeds. Anyone quoting the pinned single-seed file — including
whoever wrote it — would have reported the opposite of the 10-seed result. The pinned file keeps a
warning pointing at `runs/mlp-verified/ademamix/seed-sweep-summary.md` for exactly that reason, and this
is the clearest illustration in the repository of why a single run is not evidence.

**A second trap, of the same family: a tied band is not a ranking.** The threshold curves
(`REPRODUCTION.md` §5.9) show the logistic suite's two leading arms trading the lead **five times inside
a 0.0014-wide threshold band** (0.1435–0.1449). Inside that band they are tied, and "which one is
faster at reaching the target" has no answer — so this card does **not** pick a threshold from that band
to make either arm look better, and the AdEMAMix verdict rests on the final-loss comparison plus the
ten-seed paired test, not on `epochs_to_target`. The same discipline applies to the schedule-free card,
where the flip between models turned out to be a threshold crossing rather than a property of the
method.

### Two model families, one direction

The two trainers differ in capacity and curvature, so the honest summary is stated per family rather
than pooled:

| claim | logistic head | two-layer MLP | agreement |
|---|---|---|---|
| AdEMAMix reaches the target sooner than AdamW | no (identical epochs in 10/10 seeds) | no (matches AdamW; AdaGrad and momentum are faster than both) | **same direction** |
| AdEMAMix ends at a better loss than AdamW | no (0.4% worse on the printed metric) | no over 10 seeds (0.13249 vs 0.13218; 3/10 seeds better) | **same direction** |
| The paper's α/β3 warmup scheme helps at this budget | no (4.5× slower to target) | no (worst two arms: 0.14269 and 0.15261 vs 0.13218) | **same direction** |
| Adam is the fastest optimizer | no (AdaGrad 4.7, momentum 16.7, Adam 22.6 epochs) | no (AdaGrad 6.2, momentum 7.0, Adam 20.3 epochs) | **same direction** |
| Adam reaches the lowest final loss | yes at a fixed 80-epoch budget | yes (seed 7: 0.13620 train / 0.12363 test, best of the five) | not contradicted |

So the strongest available objection to this card — "a two-parameter model cannot show an effect of a
second moving average" — is answered on an MLP as well, with the caveat that both models are still
small, full-batch and short-horizon compared with the paper's regime.

**Five capacities now agree.** The pre-registered expansion in `REPRODUCTION.md` §5.13 added `[64]` and a
two-layer `[16,16]`, and the no-advantage verdict held at both: AdEMAMix beat the AdamW baseline in 1/10
seeds at `[64]` and 0/10 at `[16,16]`, and was worse on mean test loss in both (0.14568 vs 0.14480;
0.22439 vs 0.22111). The `[16,16]` run is also the sharpest illustration of the metric trap in §5.12 —
AdEMAMix reaches the lowest **training** loss of any arm there (0.0944) and the worst **test** loss. This
is the repository's most robust negative result: five capacities, both model families, ten seeds each.

### The wording the activation expansion forced (§5.14)

The `[32]` capacity was re-run with ReLU and with GELU, and the pre-registered prediction "AdEMAMix has no
advantage over the AdamW baseline" came out **refuted as written** — which is the most useful result of
that run. Under ReLU and GELU, AdEMAMix beats a *cosine-scheduled* AdamW in 9/10 and 7/10 seeds… because
under those activations the scheduled baseline is the weakest arm, not because AdEMAMix improved. Against
AdamW **at the same learning rate** the difference is 4 × 10⁻⁵ and −1.7 × 10⁻⁴, i.e. still a tie.

So this card's claim is now stated at the precision the evidence supports:

> **AdEMAMix shows no advantage over AdamW at matched settings** — same optimizer, same learning rate —
> on both model families and five capacities, ten seeds each, with the α = 0 identity (§5.5) as the
> correctness check. Against a *scheduled* AdamW the outcome depends on the activation, because which
> baseline is strong is activation-scoped: under tanh the tuned cosine is the best test-loss arm of the
> AdamW variants, under ReLU/GELU it has the lowest training loss and the worst test loss.

This is a scope correction, not a retraction: the original verdict was measured under tanh, where the
reference was the strongest AdamW variant, and it holds there. What the new runs remove is the
generalisation from "no advantage over the baseline" to "no advantage over AdamW".

### The normalisation/initialisation check (§5.15) — and the criterion that failed

The last two never-varied modelling choices were normalisation of the hidden pre-activations and the
weight-initialisation scaling. The `[32]` capacity was re-run with layernorm, with batchnorm, with He
initialisation and with a plain fixed 0.05 initialisation, every arm retuned on the reference grid,
pre-registered N1-N4 (`docs/normalization-init-preregistration.md`).

**The direction of the verdict holds in three of the four variants**: against AdamW at the same rate the
mean test loss is worse under batchnorm (+0.00006), He (+0.00238) and plain init (+0.00195), and
marginally better under layernorm (−0.00009). So "no advantage at matched settings" is the reproducible
part, and nothing here revives the paper's faster-convergence claim.

**The pre-registered win-count criterion is the thing that failed, and it is worth more than the
hypothesis it tested.** N2 asked for "at most 2/10 seeds better". Under layernorm AdEMAMix is better in
**8 of 10 seeds** while the mean difference is 0.00009 — three orders of magnitude below the per-seed
spread (σ ≈ 0.025). A consistent sign and a nil effect; a criterion written in wins alone cannot tell
those apart. That is the third arrival of the same lesson (A2 in §5.14 and H5 in §5.13 were the other
two), and it is now a reporting rule in the pre-registration file rather than a footnote: **a win count
without a magnitude is not evidence.**

### The paired tests (§5.16) — and why this card says "no advantage detected", not "no advantage"

With a test in hand the case above resolves the way the win count alone could not: 8/10 seeds, median
difference −0.00005, raw p = 0.1309 — a consistent sign and no effect. Across the eleven suites that
test this claim at matched settings, **no comparison survives a family correction** (smallest adjusted
p = 0.2363, and that one has AdEMAMix worse).

A test that fails to reject cannot confirm a null, so the claim this card makes is now stated as a
bound:

> **No advantage over AdamW at matched settings was detected.** Across eleven suites (two model
> families, five capacities, three activations, five normalisation/initialisation settings) the
> per-seed median difference runs from −0.00005 to +0.00411 — indistinguishable or slightly worse —
> and with ten seeds the design could have detected an advantage of about 0.0003 to 0.008 depending on
> the suite's per-seed spread.

That is a weaker verb than "has no advantage", and it is the one the evidence supports. It does not
weaken the practical conclusion (there is nothing here to justify using AdEMAMix at this scale), and it
does not touch the α = 0 identity, which is a correctness check rather than a comparison.

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
