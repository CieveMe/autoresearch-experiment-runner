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

1. **"At worst matches" is roughly what happens, and only just.** Schedule-free is 0.3% behind the
   tuned cosine on mean test loss and 0.00032 behind on every single seed. It is a consistent loss,
   not noise, but it is small enough that calling it "matches" is defensible — while "out-performs" is
   not supported here.
2. **The speed metric is where it clearly loses at this budget**: 154 epochs to the target against the
   tuned schedule's 80. The averaging sequence moves more slowly by construction, and over a short run
   that delay is visible.
3. **The premise is also weak at this scale**: a plain *constant* learning rate beats both scheduled
   and schedule-free arms on final loss. If a decay is not needed for the task, removing the decay is
   not a benefit — which is a statement about a 200-epoch convex problem, not about long non-convex
   training where the paper's argument lives.
4. **Schedule-free SGD is far behind schedule-free AdamW** (0.196 vs 0.126). The averaging does not
   rescue a method whose per-parameter scaling is wrong for the problem; the paper's schedule-free
   machinery is orthogonal to adaptivity.

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
