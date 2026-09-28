# Paper card — Schedule-Free Learning (arXiv:2405.15682, 2024)

| Field | Value |
|---|---|
| Paper | *Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages* — Defazio, Yang, Mehta, Mishchenko, Khaled, Cutkosky (Meta et al.), 2024 |
| Reference implementation | `facebookresearch/schedule_free` (Apache-2.0), cloned and read on 2026-09-28; `adamw_schedulefree_reference.py` was the specification used |
| Reproduction level | **mechanism-level**, with the one comparison the claim actually needs: schedule-free versus a **tuned** cosine schedule at matched budget |
| Config | `examples/schedule-free.json` (SHA-256 `3592a75bdfd388764ba55cf75fe77af25b2e25a7ce4240eb5c9f226259f0d779`) |
| Tuning sweep | `examples/schedule-free-sweep.json` (21 trials: learning rate × min-LR factor for the cosine baseline, learning rate for the schedule-free arms) |
| One command | `python scripts/repro.py --suite schedule-free` |
| Expected numbers | `expected/expected_schedule_free.json` |

## The claim under test

The repository's README states it directly: schedule-free learning "does not require a decreasing
learning rate schedule, yet typically out-performs, or at worst matches, SOTA schedules such as
cosine-decay and linear decay". This is a comparative claim, and it is only testable if the baseline
is *actually tuned* — an untuned cosine schedule would make the method look good for free. So the
baseline gets a grid over both its learning rate and its minimum-learning-rate factor, and the
strongest constant-learning-rate baseline is included too, because a constant rate is precisely what
schedule-free is meant to replace.

## Rule as implemented

Transliterated from `adamw_schedulefree_reference.py` (their `k+1` is our 1-based `epoch`):

```
sched = (t / warmup) if warmup and t <= warmup else 1
lr_t  = lr * sched ;  lr_max = max(lr_t, lr_max)
w_t   = t**average_power * lr_max**weight_lr_power ;  W += w_t ;  ckp1 = w_t / W
z     = z - lr_t * g / (sqrt(v_t / (1 - beta2^t)) + eps)      # Adam-style update on z
x     = (1 - ckp1) * x + ckp1 * z                             # running average
y     = beta1 * x + (1 - beta1) * z                           # where gradients are taken
```

Two details decide whether a comparison is fair, and both are implemented explicitly:

* **Metrics are computed at `x`, not at `y`.** The reference implementation evaluates in `.eval()`
  mode at the averaged sequence; reporting the training point would flatter the method. In this
  repository that means `optimizers.eval_params()` and the trainer returning `x` as the fitted
  parameters.
* **The reference arithmetic is cross-checked.** `tests/test_schedule_free.py` contains a literal
  re-implementation of the reference step and compares five steps of it against the library rule,
  parameter by parameter. Both were written from the same file, so this catches transcription and
  ordering errors rather than a shared misreading of the paper.

## Results (seed 7 and 10 seeds)

Budget: 200 epochs (twice the earlier suites, to give a decaying schedule room), target 0.148 for the
speed metric. Seed 7:

| arm | test loss | epochs to target |
|---|---:|---:|
| adamw + tuned cosine (baseline) | 0.12381987 | 80 |
| adamw, constant learning rate | **0.12228349** | **70** |
| **schedule-free AdamW** | 0.12395906 | 154 |
| SGD + cosine | 0.21590420 | never |
| schedule-free SGD | 0.19546660 | never |

Ten seeds (`runs/schedule-free-verified/seed-sweep-summary.md`): mean test loss 0.12448 for the
constant rate, 0.12610 for the tuned cosine, **0.12642 for schedule-free AdamW**; paired per seed,
the tuned cosine beats schedule-free in **10/10** seeds (mean +0.00032 ± 0.00021) and the constant rate
beats it in 7/10 (+0.00194).

## Findings

### The MLP re-run (same session, because a logistic-only answer is a single-model conclusion)

The comparison was repeated with `trainer: "mlp"` (two-layer tanh, 8 hidden units), every arm retuned
for that model (`examples/schedule-free-mlp-sweep.json`, 15 trials over learning rate × min-LR factor
for the cosine arm), same 200-epoch budget and target. Seed 7:

| arm (MLP) | test loss | epochs to target |
|---|---:|---:|
| adamw + tuned cosine (baseline) | 0.12699107 | 23 |
| adamw, constant learning rate | **0.12501296** | 22 |
| schedule-free AdamW | 0.12506323 | **11** |
| sgd + cosine | 0.12501563 | 71 |
| schedule-free SGD | 0.12530471 | 79 |

Ten seeds (`runs/schedule-free-verified/mlp/seed-sweep-summary.md`): mean test loss 0.12589
(schedule-free SGD), 0.12603 (SGD + cosine), **0.13094 (schedule-free AdamW)**, 0.13222 (tuned cosine),
0.13796 (constant). Paired per seed: **schedule-free AdamW beats the tuned cosine in 9/10 seeds**
(mean +0.00128 ± 0.00313) — the opposite direction from the logistic head — while **the constant rate
beats schedule-free AdamW in 9/10 seeds** (mean +0.00703 ± 0.00571).

### Findings across both models

0. **The flip is not a model dispute, it is a threshold dispute — and the curves locate it.**
   `scripts/threshold_curve.py` (`REPRODUCTION.md` §5.9) shows the two arms crossing at **0.1434** on
   the MLP: at thresholds *looser* than that, schedule-free arrives first; at thresholds *tighter*
   than that, the constant-rate arm wins because it converges deeper (0.1378 against 0.1412 floor).
   The MLP suite's pinned threshold (0.148) therefore sits in the region where schedule-free looks
   fast, and the logistic suite's pinned threshold (0.148) sits in the region where the tuned cosine
   has already won for good. So the earlier sentence "schedule-free beat the cosine on one model and
   lost on the other" is really "two arms cross at a threshold, and the two models have different
   floors and different crossings". That is a statement about the metric and the model, not about the
   optimizer, and it is the reason this card no longer quotes a bare speed number anywhere.
   **And the crossing itself is only stable in its existence, not in its position.** §5.11's per-seed
   analysis finds the crossing in 10/10 seeds but spread across a 0.0505-wide band, and the arm that is
   faster at the suite's pinned threshold (0.148) **changes between seeds**. So the seed-7 sentence
   "schedule-free reaches the target in 11 epochs against the constant rate's 23" is a single-seed
   statement, and this card treats it as one; the *test-loss* result (schedule-free beats the tuned
   cosine in 9/10 seeds, §5.8) is a different measurement and stands.
1. **"At worst matches" holds; "out-performs" is not established.** The direction of the
   schedule-free-versus-tuned-cosine comparison **flips with the model**: on the logistic head the tuned
   cosine wins 10/10 (by a tiny 0.00032), on the MLP schedule-free wins 9/10 (by 0.00128). Neither is a
   large effect, and a claim of superiority would not survive the model change.
2. **The stable finding on both models is that a constant learning rate wins.** 0.12448 on the
   logistic head and 0.13796 on the MLP, and it beats schedule-free in 7/10 and 9/10 seeds
   respectively. At a 200-epoch budget on these tasks a decay is not needed, so removing the need for
   one has nothing to buy — a statement about this regime, not about long non-convex training.
3. **The speed metric is also model-dependent, and therefore should not be quoted alone.** On the
   logistic head schedule-free needs 154 epochs to the target against the tuned schedule's 80; on the
   MLP it needs **11** against 23. The averaging sequence moves slowly, and whether that helps or hurts
   depends on where the target sits relative to the floors.
4. **Schedule-free SGD versus schedule-free AdamW is model-dependent too** (logistic: 0.196 vs 0.126,
   SGD far behind; MLP: 0.12589 vs 0.13094, SGD ahead on the mean but only 3/10 per-seed wins). The
   averaging does not substitute for adaptive scaling in general; it just is not the dominant effect
   here.
5. **What this means for the paper's claim.** The weak form — "no schedule needed, and the method at
   worst matches a tuned schedule" — is consistent with both runs. The strong form — "typically
   out-performs" — is not supported by either, and in the one model where schedule-free wins, a plain
   constant learning rate still wins by more. Reporting only one of the two models would have produced
   a confident and wrong headline in either direction.

The bullets that follow are the logistic-head-only reading of the same data, kept for the record; the
five findings above supersede them where the two models disagree.

1. *(logistic only)* Schedule-free was 0.3% behind the tuned cosine on mean test loss and behind in
   every seed — a consistent but small loss.
2. *(logistic only)* It needed 154 epochs to the target against the tuned schedule's 80.
3. *(logistic only)* A constant learning rate beat both, which is the premise-level observation.
4. *(logistic only)* Schedule-free SGD was far behind schedule-free AdamW (0.196 vs 0.126); on the MLP
   that ordering reverses, so it is not a property of the method.

## Deviations and limitations

| # | Deviation | Reason | Risk |
|---|---|---|---|
| D1 | `average_power = 0`, `weight_lr_power = 2` (reference defaults), `inner_momentum = 0` | faithful to the reference defaults | the paper's optional weighting is untested here |
| D2 | Weight decay 0 | as in the other suites, so the comparison is about the schedule | regularisation effects untested |
| D3 | Logistic trainer, 200 epochs, full batch, one dataset | offline, bit-reproducible, ~0.1 s per arm | the regime where schedules matter most is not reproduced |
| D4 | Target 0.148 | inside a few percent of the floors (0.143–0.145) | a looser target would measure the first step |
| D5 | Metrics at `x`, not `y` | matches the reference's eval mode | a reader expecting train-mode losses would see different curves |

Boundary of the claim: nothing here says schedule-free is a bad method. It says that on a short,
convex, full-batch task with a properly tuned cosine baseline, it does not beat that baseline, and
that the repository cannot test the regime where it is designed to win.

## Verification and negative control

* `python scripts/repro.py --suite schedule-free` verifies the pinned numbers; `make sweep` regenerates
  the 21-trial tuning curves.
* Negative control: `scripts/score_task.py` mutates the averaging step (`x = z`, i.e. schedule-free
  without the average) and requires the pinned expectations to fail.
* `tests/test_schedule_free.py` pins the port against the reference, the warmup ramp, determinism, and
  the fact that reported parameters are the averaged ones.
