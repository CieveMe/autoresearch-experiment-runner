# Reproduction Report — Adam: A Method for Stochastic Optimization

| Field | Value |
|---|---|
| Paper | *Adam: A Method for Stochastic Optimization* — Diederik P. Kingma, Jimmy Ba (arXiv:1412.6980, 2014; ICLR 2015) |
| Artifact | `autoresearch-lite` v0.2.0 — `https://github.com/CieveMe/autoresearch-experiment-runner` |
| Reproduction level | **mechanism-level** (algorithm re-implementation + controlled head-to-head), not benchmark-level |
| Config revision | `examples/classification.json`, SHA-256 `cc85ba76ddcdff91f561bb0366fd3228c00e5b46541af8e4cdc04563926e040f` |
| Second experiment | `examples/optimizers.json` — convergence speed (epochs to a tight target) against SGD, SGD+momentum, AdaGrad and RMSProp; SHA-256 `808b4c1692271929dd61293f66bf97c0682f9907e8724713d9570a1f94eaeddf` |
| Third experiment | `examples/ademamix.json` — a **2024 paper** (AdEMAMix, arXiv:2409.03137) tested against AdamW on the same time-to-target metric; SHA-256 `c046217aa4a239a4db2c685c4162efc4ae5cda90fc9e69b03fe28d8417972962` |
| One command | `python scripts/repro.py` (runs all three experiments, cross-platform) or `make repro` |
| Verified on | 2026-09-28, CPython 3.12.5, Windows 11 (x64), no network, no third-party packages |
| Expected numbers | `expected/expected_metrics.json` (17 assertions), `expected/expected_optimizers.json` (28) and `expected/expected_ademamix.json` (26), all machine-checked |

## Verdict in one paragraph

The Adam update rule (first/second moment estimates with bias correction) was re-implemented from the
paper's Algorithm 1 in dependency-free Python and compared against a fixed-learning-rate SGD baseline
on a fixed synthetic binary-classification task. Across 10 seeds Adam reaches a **lower test loss in
10/10 seeds**, with a paired per-seed improvement over the strongest SGD control of
**0.07670 ± 0.00554** (mean ± stdev, paired t-style effect size ≈ 13.9). The direction of the claim is
reproduced; the *magnitude* of the paper's own numbers is not claimed, because the paper's
datasets/architectures (MNIST, CIFAR-10, IMDB) were deliberately not used. Adam's advantage here is in
the loss (probability calibration), not in accuracy: the SGD control is 0.25 pp *more* accurate on
average. Everything above is regenerated and re-checked by one command, and the checking harness was
itself validated against two deliberately broken implementations (see §9).

**The second experiment produced a negative result, and it is the more interesting half.** The
paper's headline claim is *faster convergence*, not "lower loss at a fixed budget", so a second
experiment measures epochs-to-target with every optimizer family tuned by the same coarse
learning-rate sweep. There **Adam is not the fastest**: AdaGrad reaches a target close to the
converged floor first in **10/10 seeds** (mean 4.7 epochs vs Adam's 22.6), SGD with momentum beats
Adam 10/10 as well, and plain SGD never reaches the floor at any swept rate. The two experiments
answer different questions and must not be quoted interchangeably; §5.4 gives the numbers and §7
lists what remains unmeasured.

## 1. Claim under test

The paper introduces per-parameter adaptive step sizes driven by exponentially decaying averages of
the gradient (`m_t`) and the squared gradient (`v_t`), plus a bias-correction term that compensates
for the initialization of those averages at zero:

```
m_t = b1*m_{t-1} + (1-b1)*g_t
v_t = b2*v_{t-1} + (1-b2)*g_t^2
m_hat = m_t / (1 - b1^t)
v_hat = v_t / (1 - b2^t)
theta = theta - alpha * m_hat / (sqrt(v_hat) + eps)
```

The paper's headline claims are that this update gives faster convergence, is robust to
hyper-parameter choice, and handles noisy/sparse/non-stationary gradients well. Reported evidence
comes from logistic regression and multi-layer nets on MNIST, a convolutional net on CIFAR-10, and a
word-embedding model on IMDB, always hedged against SGD+momentum, AdaGrad and RMSProp.

**The single falsifiable statement reproduced here** (configuration field `hypothesis`):

> Adam's first/second moment estimation with bias correction reaches a lower test loss than a
> fixed-learning-rate SGD baseline on the same task, with the same seed, same data and the same
> epoch budget.

The runner ranks all trials by the primary metric `test_loss`; the hypothesis is stated in terms of
loss, not accuracy, so the verdict below is about the loss.

## 2. What is reproduced, and what is not

| | Status |
|---|---|
| Adam update rule (moments + bias correction) implemented from the paper text | ✅ reproduced |
| Deterministic data, fixed seed, baseline + 2 treatment variants under one runner | ✅ reproduced |
| Paired multi-seed comparison with variance, instead of a single anecdote | ✅ added (10 seeds) |
| Paper's datasets and architectures (MNIST / CIFAR-10 / IMDB) | ❌ **not reproduced** |
| Paper's figures and tables, reported wall-clock speedups | ❌ **not reproduced** |
| Claims about sparse gradients and non-stationary objectives | ❌ out of scope (no sparse data here) |

This is a mechanism reproduction on a controllable task. No cell of the paper's tables is claimed to
be reproduced, and the numbers below must not be quoted as "the paper's numbers".

## 3. Environment

- Python ≥ 3.10; nothing else. The experiment path uses only the standard library
  (`random`, `math`, `json`), so the reproduction needs **no network access and no `pip install`**.
- Verified on CPython 3.12.5 / Windows 11 x64 and, via CI, on CPython 3.10 and 3.12 / Linux (Ubuntu).
- Container path: `docker compose up --build` (Dockerfile `python:3.12-slim`).
- Hardware: no GPU, no accelerator. The full sweep takes ~4 s; one seed takes ~1 s.

## 4. How to reproduce (one command)

```bash
python scripts/repro.py        # any OS with Python >= 3.10
make repro                     # Linux/macOS
docker compose up --build      # container, writes to ./runs
```

`scripts/repro.py` runs four steps and exits non-zero if any of them fails:

1. environment report → `runs/demo/environment.json` (interpreter, platform, config hash);
2. `validate-config` on `examples/classification.json`;
3. the experiment run → `runs/demo/results.json` + `runs/demo/report.md`;
4. `scripts/verify_results.py` comparing the produced numbers against
   `expected/expected_metrics.json` (17 assertions), followed by the unit suite (8 tests).

The multi-seed sweep is a separate command, so the fast path stays fast:

```bash
python scripts/seed_sweep.py --seeds 0-9 --output runs/seed-sweep
```

Verification commands used for this report:

```
$ python scripts/repro.py
verified:  17 checks, 0 failures
RESULT: PASS                       # exit code 0

$ python -m unittest discover -s tests
Ran 8 tests in 0.7s
OK
```

## 5. Results

### 5.1 Reference run (seed 7, fixed 80-epoch budget)

Committed as `runs/demo-verified/`. Primary metric: `test_loss` (lower is better); 600 train / 200 test
rows.

| trial | optimizer | lr | weight decay | epochs | test loss | test accuracy |
|---|---|---:|---:|---:|---:|---:|
| **adam_reproduction** | adam | 0.08 | 0.0 | 80 | **0.20216034** | 94.00% |
| sgd_control | sgd | 0.35 | 0.0 | 80 | 0.28128893 | 94.50% |
| adam_regularized | adam | 0.08 | 0.01 | 100 | 0.31407811 | 93.50% |
| baseline | sgd | 0.15 | 0.0 | 80 | 0.38416828 | 93.50% |

### 5.2 Ten-seed sweep (the number that actually supports a conclusion)

One seed only proves repeatability. Re-running the same configuration for `seed in 0..9`
(`runs/demo-verified/seed-sweep-summary.md`) gives:

| trial | test loss mean | stdev | min | max | mean accuracy | best in |
|---|---:|---:|---:|---:|---:|---:|
| **adam_reproduction** | **0.20368012** | 0.01816425 | 0.16660726 | 0.22882864 | 94.30% | **10/10** |
| sgd_control | 0.28037568 | 0.01838522 | 0.24736677 | 0.30370702 | 94.55% | 0/10 |
| adam_regularized | 0.31730997 | 0.01843015 | 0.28119885 | 0.34124891 | 94.30% | 0/10 |
| baseline | 0.38165322 | 0.01586304 | 0.35596295 | 0.40227566 | 94.05% | 0/10 |

Seeds are paired (the same seed drives every trial), so the per-seed difference is the right statistic.
Positive = better `test_loss` than the reference:

| comparison | better in | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|
| adam_reproduction vs sgd_control | 10/10 | **+0.07669556** | 0.00553513 | 0.06845981 | 0.08713680 |
| adam_reproduction vs baseline | 10/10 | +0.17797310 | 0.00771465 | 0.16861319 | 0.18948606 |
| sgd_control vs baseline | 10/10 | +0.10127754 | 0.00354625 | 0.09701005 | 0.10859618 |
| adam_regularized vs sgd_control | 0/10 | −0.03693428 | 0.00382122 | −0.04275977 | −0.03101776 |

**Findings.**

1. Adam beats *both* SGD settings on test loss in every seed, and the per-seed gain over the strong
   SGD control is an order of magnitude larger than its own spread (|mean|/stdev ≈ 13.9), so the
   direction of the paper's convergence claim survives on this task.
2. Loss and accuracy rank the optimizers differently: Adam has the better loss, the tuned SGD control
   has the better accuracy (94.55% vs 94.30%). A "which optimizer is better" claim is therefore
   metric-dependent here, and the report states the metric explicitly instead of hiding the conflict.
3. Adding L2 to the gradient of an adaptive method *hurt* here (`adam_regularized` is 0.037 worse
   than Adam without decay, 0/10 seeds better than the SGD control). This is consistent with the known
   interaction between adaptive updates and L2 penalties that motivated decoupled weight decay
   (AdamW); it is a finding of this reproduction, not a claim of the 2014 paper.

### 5.3 How this compares with the numbers reported in the paper

| Aspect | Paper | This reproduction |
|---|---|---|
| Tasks | logistic regression / MLP on MNIST, CNN on CIFAR-10, IMDB word embeddings | synthetic 2-feature binary classification (800 rows) |
| Optimizer baseline | SGD, SGD+momentum, AdaGrad, RMSProp | SGD at two fixed learning rates (0.15, 0.35) |
| Default hyper-parameters | α = 0.001, β1 = 0.9, β2 = 0.999, ε = 1e-8 | β1, β2, ε as in the paper; **α = 0.08** (documented deviation) |
| Gradients | mini-batch stochastic | **full-batch deterministic** (documented deviation) |
| Evidence reported | learning curves, final metrics, wall-clock | 10-seed paired test loss with mean ± stdev |
| Numbers | e.g. MNIST/CIFAR accuracies, IMDB error rates | **not comparable — different task; no paper number is claimed as reproduced** |

Because the tasks differ, there is no honest column here that says "paper said X, we got Y". What is
compared is the **directional claim** and the **mechanism**: the update rule behaves as the paper
describes on a task whose optimum is known and reproducible, and the conclusion holds under noise
injected through the data seed.

### 5.4 Convergence speed with the optimizer family (and a negative result)

Section 5.1–5.3 answer "which optimizer ends up with the lower loss at a fixed epoch budget". The
paper's actual claim is **faster convergence**, so this second experiment measures *when* each method
gets there:

* **metric**: `epochs_to_target` — the first epoch whose training loss is ≤ the target.
* **target**: `0.16`, deliberately close to the converged floor (~0.12–0.14). With a *loose* target
  (0.30) the metric mostly measures the size of the first steps: AdaGrad at lr = 4 "reaches" it in
  epoch 2. Both regimes are committed — see `runs/optimizers-verified/lr-sweep/`.
* **fair tuning**: each family uses the learning rate that produced the lowest final training loss in
  `examples/optimizers-sweep.json` (a 24-trial coarse sweep over 5 families, curves committed as CSV).
  Ties break toward the smaller rate. Without this step the comparison would be measuring tuning luck.
* **budget**: 120 epochs, fixed seed 7 for the reference run and seeds 0–9 for the sweep.

Reference run (seed 7):

| trial | test accuracy | test loss | epochs to 0.16 |
|---|---:|---:|---:|
| adagrad (lr 4.0) | 93.50% | 0.12246563 | **12** |
| adam_no_bias_correction (lr 0.15) | 93.50% | 0.12187267 | 13 |
| sgd_momentum (lr 0.8) | 93.50% | 0.12345500 | 23 |
| adam (lr 0.4) | 93.50% | 0.12346246 | 33 |
| rmsprop (lr 0.2) | 93.00% | 0.12431982 | 57 |
| sgd (lr 0.6) | 94.00% | 0.20381571 | never |

Ten-seed sweep (`runs/optimizers-verified/seed-sweep-summary.md`):

| trial | epochs mean | stdev | min–max | reached | best in |
|---|---:|---:|---|---:|---:|
| **adagrad** | **4.7** | 3.33 | 2–12 | 10/10 | **10/10** |
| adam_no_bias_correction | 10.1 | 1.79 | 8–13 | 10/10 | 0/10 |
| sgd_momentum | 16.7 | 3.92 | 12–23 | 10/10 | 0/10 |
| adam | 22.6 | 6.40 | 15–33 | 10/10 | 0/10 |
| rmsprop | 42.0 | 9.64 | 29–57 | 10/10 | 0/10 |
| sgd | — | — | — | 0/10 | 0/10 |

Paired per-seed comparison (positive = fewer epochs than the reference):

| comparison | better in | mean improvement | stdev |
|---|---:|---:|---:|
| adagrad vs adam | 10/10 | +17.9 epochs | 3.45 |
| adam_no_bias_correction vs adam | 10/10 | +12.5 epochs | 4.62 |
| sgd_momentum vs adam | 10/10 | +5.9 epochs | 2.51 |
| adam vs rmsprop | 10/10 | +19.4 epochs | 3.41 |
| adam vs sgd | — | not comparable: SGD never reached the target in 10/10 seeds | — |

**Findings.**

1. **The paper's "Adam converges faster" claim is not reproduced in this setup.** AdaGrad and
   momentum reach a near-floor target meaningfully sooner; RMSProp is the slowest of the adaptive
   methods; plain SGD never gets to the floor even at a 4× larger learning rate than the fixed
   baseline. On this task the honest summary is "adaptive and momentum methods beat plain SGD;
   among them Adam is not the fastest to the target".
2. **Bias correction costs time here.** Disabling it makes Adam reach the target in 10/10 seeds
   sooner (12.5 ± 4.62 epochs) and leaves the final loss marginally *lower* (0.12187 vs 0.12346).
   Bias correction matters most in the first few steps, and its effect is largest when the budget is
   short; with a 120-epoch budget on a convex problem, the extra early-time scaling is not obviously
   a benefit. This is a property of *this* configuration, not a refutation of the paper's reasoning.
3. **Accuracy is unaffected.** Every method lands between 93.0% and 94.6% mean test accuracy, and the
   plain-SGD baseline is the most accurate — the differences here are optimization dynamics, not
   generalisation.
4. **Section 5.1 is not contradicted, it is a different question.** At a fixed 80-epoch budget Adam
   had the lowest test loss; measured by time-to-a-tight-target it is mid-pack. Quoting either number
   as "Adam vs SGD" without saying which question was asked would be misleading.

### 5.5 A 2024 paper, same metric: AdEMAMix (negative result again)

Section 5.4 measures convergence speed with methods older than the paper; this experiment points the
same machinery at a **2024 paper**. AdEMAMix (arXiv:2409.03137, Apple) keeps a second, slower EMA of
the gradient (β3 = 0.9999) and mixes it in with a coefficient α that grows over training, on top of
Adam's bias-corrected second moment. Its claim is that this converges faster than AdamW on long runs.

Setup, and the two decisions that keep it fair:

* every arm — including the α/β3 warmup length, a hyper-parameter AdamW does not have — is tuned by
  the same rule used everywhere in this repository (lowest final training loss inside the grid
  `examples/ademamix-sweep.json`, 20 trials, ties to the smaller value);
* **weight decay is 0**. The paper's default λ = 0.1 assumes lr ≈ 1e-3; this full-batch task runs at
  lr ≈ 0.1–0.8, so the same λ would apply roughly 100× more decay per step and the comparison would
  be about regularisation rather than about the update rule.

Reference run (seed 7, target 0.148, just above the converged floor ~0.143):

| arm | tuned lr | epochs to target | final test loss |
|---|---:|---:|---:|
| adamw (baseline) | 0.8 | **23** | 0.12255737 |
| ademamix (tuned, no warmups) | 0.8 | **23** | 0.12202320 |
| ademamix with α = 0 (ablation) | 0.8 | **23** | 0.12255737 |
| sgd + momentum | 0.8 | 47 | 0.12345500 |
| ademamix with the paper's warmups scaled to this budget (α/β3 ramp over 120 steps) | 0.2 | 105 | 0.12415636 |

Ten seeds (`runs/ademamix-verified/seed-sweep-summary.md`): adamw, the tuned AdEMAMix and the α = 0
ablation all average **13.7 ± 4.69** epochs (range 8–23) and the paired difference against AdamW is
**exactly 0.0 in 10/10 seeds**; momentum averages 23.3, and the paper-warmup arm 66.5.

**Findings.**

1. **The 2024 claim is not reproduced either.** On this task AdEMAMix does not reach the target in
   fewer epochs than AdamW — it reaches it in the *same* epoch in every one of ten seeds — and its
   final loss improvement is 0.4% relative (0.0005 absolute) on the reference seed.
2. **The slow EMA changes the floor, not the timing.** With α = 0 the arm reproduces AdamW's curve to
   the printed precision, which is the implementation's correctness check: the only difference between
   the two rules is the term that was switched off. (Equality is to within floating-point rounding,
   not bit for bit — the two rules associate their arithmetic differently — and the test pins it at
   1e-12 relative rather than claiming exactness.)
3. **The paper's own warmup scheme is budget-sensitive.** Spreading the α/β3 ramps over the whole run
   (as the paper does over its 256k steps) makes the arm **4.5× slower** here (105 epochs vs 23) and
   worse at the floor. At a 120-epoch budget the ramps never finish, so the slow EMA mostly adds an
   early-phase push to an already adaptive-normalised step.
4. **This is a statement about scale, not about the method.** The slow EMA needs a long horizon to pay
   off; a 120-epoch full-batch convex task that converges in ~20 steps has none. The card
   (`docs/papers/ademamix-2024.md`) says exactly that, and testing the paper's regime would need the
   paper's regime — long training, mini-batches, its own harness — which is out of scope here.
   **Read §5.6 before quoting anything from this section**: the same suites were re-run on the MLP
   trainer, the conclusions there agree with these, and that section also documents a single-seed trap
   that would let a careless reader report the opposite of the ten-seed result.

### 5.6 Does any of this survive a bigger model? (the self-scepticism run)

Sections 5.1–5.5 all used a logistic head with two weights and a bias — an almost-convex model that
converges in tens of steps. That is the strongest objection to every result above: "Adam is mid-pack on
speed" and "the slow EMA does not help" could both be artefacts of a model with almost no curvature.
So both suites were re-run with `trainer: "mlp"` (two-layer tanh, 8 hidden units), and **every family
was retuned for that model** by the same rule (`examples/optimizers-mlp-sweep.json`, 24 trials, and
`examples/ademamix-mlp-sweep.json`, 17 trials; lowest final training loss, ties to the smaller value).

One implementation detail mattered enough to fix before believing any of it: the MLP initialises from
the seed, but a trial config did not inherit the experiment's `seed`, so a "10-seed" run varied the
data split while every run started from the same weights. `TRIAL_INHERITED_KEYS` now includes `seed`,
and the numbers below are from after that fix (the logistic trainer never read the seed, so suites
5.1–5.5 are unaffected and still verify).

Ten-seed results, MLP trainer:

| suite | arm | metric mean | stdev | best in |
|---|---|---:|---:|---:|
| `optimizers-mlp` | **adagrad** | **6.2 epochs** | 3.99 | 7/10 |
| `optimizers-mlp` | sgd_momentum | 7.0 epochs | 1.33 | 2/10 |
| `optimizers-mlp` | **adam** | **20.3 epochs** | 13.23 | 1/10 |
| `optimizers-mlp` | rmsprop | 33.3 epochs | 14.30 | 0/10 |
| `optimizers-mlp` | sgd | 36.1 epochs | 17.78 | 0/10 |
| `ademamix-mlp` | sgd_momentum | 0.13026 test loss | 0.02343 | 6/10 |
| `ademamix-mlp` | adamw (baseline) | 0.13218 | 0.02473 | 1/10 |
| `ademamix-mlp` | ademamix, no warmups | 0.13249 | 0.02483 | 0/10 |
| `ademamix-mlp` | ademamix, warmups = 45 | 0.14269 | 0.03485 | 3/10 |
| `ademamix-mlp` | ademamix, warmups = 120 | 0.15261 | 0.03962 | 0/10 |

Paired per-seed comparison against AdamW (positive = lower test loss): AdEMAMix without warmups
**−0.00018 ± 0.00020** (3/10 seeds better), warmups = 45 **−0.00509 ± 0.00946** (3/10), warmups = 120
**−0.00966 ± 0.01279** (2/10). At seed 7 the MLP also reproduces the earlier loss ordering: Adam has
the lowest final loss of the family suite (`train 0.13620`, `test 0.12363` against momentum's
`0.14078 / 0.12545`).

**Findings.**

1. **Both negative results survive the model change.** On the MLP, Adam is again mid-pack on
   time-to-target (20.3 epochs; AdaGrad 6.2, momentum 7.0 — roughly a 3× gap, larger than on the
   logistic head), and it again has the lowest final loss. The slow-EMA method is again not faster:
   AdEMAMix and AdamW reach the target within a few epochs of each other, and momentum beats both.
2. **The harm from the paper's warmup scheme also survives.** At this budget (120 epochs, lr ≈ 0.3)
   the ramped-warmup arms are the two worst on the MLP by a wide margin (0.14269 and 0.15261 against
   0.13218), which is the same direction as the logistic suite. The two trainers disagree about the
   *magnitude*, not about the sign.
3. **The no-warmup AdEMAMix is indistinguishable from AdamW on both trainers** (MLP: 0.13249 versus
   0.13218, i.e. −0.14% relative, 3/10 seeds better; logistic: identical to the printed precision).
   That is the cleanest statement this repository can make about the method: the slow EMA, as
   configured here, does not change the outcome.
4. **The single-seed trap, demonstrated in this very repository.** At seed 7 the MLP suite's pinned
   numbers favour `ademamix_warmup_45` (test loss 0.12124) — an arm that is the **second worst of five
   over ten seeds**. This is exactly why the `expected/` files are regression baselines rather than
   evidence, and why every claim in this report quotes a seed sweep. The trap is left in the repository
   on purpose: `expected/expected_ademamix_mlp.json` carries a warning that points at the sweep.

Still not measured, and unchanged from §7: full-batch gradients, one dataset family, one hidden-layer
size, and ten seeds with a test-loss standard deviation around 0.023 — enough to separate "0.13 from
0.15", not enough to resolve a 0.0003 difference.

### 5.7 Schedule-Free AdamW against a *tuned* cosine schedule (2024)

The earlier suites compared optimizers at a fixed learning rate. The 2024 Schedule-Free paper
(arXiv:2405.15682) makes a claim about *schedules*: no decay is needed, and the method "typically
out-performs, or at worst matches" a tuned cosine decay. Testing that requires the baseline to be
tuned, or the comparison is free advertisement, so `examples/schedule-free-sweep.json` (21 trials)
sweeps the cosine baseline's learning rate **and** its minimum-learning-rate factor, and a constant
learning rate is included because that is what schedule-free is meant to replace.

The rule was transliterated from `adamw_schedulefree_reference.py` and is cross-checked step by step
against a literal re-implementation of that reference in `tests/test_schedule_free.py`. Reported
metrics use the averaged sequence `x` (the reference's eval point), never the training point `y`;
measuring at `y` would flatter the method.

Seed 7, 200-epoch budget, target 0.148:

| arm | test loss | epochs to target |
|---|---:|---:|
| adamw + tuned cosine (baseline) | 0.12381987 | 80 |
| adamw, constant learning rate | **0.12228349** | **70** |
| schedule-free AdamW | 0.12395906 | 154 |
| SGD + cosine | 0.21590420 | never |
| schedule-free SGD | 0.19546660 | never |

Ten seeds: mean test loss 0.12448 (constant), 0.12610 (tuned cosine), **0.12642 (schedule-free)**; the
tuned cosine beats schedule-free in **10/10 seeds** (mean +0.00032 ± 0.00021), and the constant rate
beats it 7/10 (+0.00194).

**Findings.**

1. **"At worst matches" is close to what happens; "out-performs" is not.** Schedule-free is 0.3%
   behind on mean test loss and behind in every seed — consistent, but small.
2. **It is clearly slower to the target at this budget** (154 epochs against 80): the averaged
   sequence moves more slowly by construction, and a 200-epoch run is short enough for that to show.
3. **A constant learning rate beats both** on final loss. If the task does not need a decay, removing
   the decay is not a benefit — true here, and the honest limit of what this repository can say.
4. **Schedule-free SGD is far behind schedule-free AdamW** (0.196 vs 0.126), so the averaging does not
   substitute for adaptive per-parameter scaling.

### 5.8 The schedule-free comparison on the MLP: the direction flips

The logistic-only schedule-free result was a single-model conclusion, which is the failure mode this
report criticises elsewhere, so the suite was repeated on the two-layer MLP with every arm retuned for
that model (`examples/schedule-free-mlp-sweep.json`, 15 trials), same 200-epoch budget and target.

Seed 7: schedule-free AdamW reaches the target **first** (11 epochs, against 22–23 for the constant and
cosine AdamW arms), and its test loss (0.12506323) is within 0.04% of the best arm. Ten seeds
(`runs/schedule-free-verified/mlp/seed-sweep-summary.md`): mean test loss 0.12589 (schedule-free SGD),
0.12603 (SGD + cosine), **0.13094 (schedule-free AdamW)**, 0.13222 (tuned cosine), 0.13796 (constant).
Paired per seed, **schedule-free AdamW beats the tuned cosine in 9/10 seeds** (+0.00128 ± 0.00313) —
the opposite direction from the logistic head — while **the constant rate beats schedule-free AdamW in
9/10 seeds** (+0.00703 ± 0.00571).

**What is stable across the two models, and what is not.**

| statement | logistic head | two-layer MLP | stable? |
|---|---|---|---|
| schedule-free beats a tuned cosine | no (10/10 losses, by 0.00032) | yes (9/10 wins, by 0.00128) | **no — direction flips** |
| a constant learning rate wins | yes (7/10 over schedule-free) | yes (9/10 over schedule-free) | **yes** |
| schedule-free is faster to the target | no (154 vs 80 epochs) | yes (11 vs 23) | **no — depends on where the target sits** |
| schedule-free SGD is competitive with schedule-free AdamW | no (0.196 vs 0.126) | yes (0.12589 vs 0.13094 on the mean, 3/10 per-seed wins) | **no** |

The paper's weak claim ("no schedule needed; at worst matches a tuned schedule") therefore survives on
both models. Its strong claim ("typically out-performs") does not: the comparison's sign depends on the
model, and in the one model where schedule-free wins, a plain constant learning rate still wins by more.
The honest summary is that at this budget a decay is not needed at all, so a method whose selling point
is removing the need for one has nothing to gain — a statement about this regime, not about long
non-convex training where the paper's argument lives.

### 5.9 The speed metric is a function of the threshold, so here are the curves

Every "who is fastest" statement in §5.4–5.8 is an `epochs_to_target` number, and that number is a
function of the threshold it is measured at. The two models already disagreed at one threshold (§5.8),
which is a warning that the metric, not the method, may be deciding the answer. `scripts/threshold_curve.py`
therefore reads the committed loss curves and reports, for a 13-point grid of thresholds from the best
converged floor to the worst arm's own floor, which arm arrives first, which never arrives, and where the
ranking changes. Outputs are committed in `runs/threshold-curves/` (Markdown table, CSV and an SVG with
the suite's pinned threshold drawn as a dashed line).

| suite | ranking changes on the grid | crossing | is the *pinned* threshold on the stable side? |
|---|---:|---|---|
| `optimizers` (logistic) | 1 | 0.1634: `adam_no_bias_correction` → `adagrad` | **no** — pinned 0.16 names the loser of the looser region |
| `optimizers-mlp` | 1 | 0.1422: `adam` → `sgd_momentum` | **no** — pinned 0.147 sits in the momentum region |
| `schedule-free` (logistic) | 0 | — | yes: `adamw_constant` wins at every threshold |
| `schedule-free-mlp` | 1 | 0.1434: `adamw_constant` → `schedule_free_adamw` | **no** — pinned 0.148 sits in the loose region where schedule-free wins |
| `ademamix` (logistic) | 5 | oscillates between 0.1435 and 0.1449 | not applicable: the two arms are tied inside noise there |
| `ademamix-mlp` | 0 | — | yes, on its (narrow) grid: `ademamix_warmup_45` wins throughout |

**Findings.**

1. **Four of the six suites have a threshold-dependent winner.** "Fastest optimizer" without a threshold
   is not a claim this repository can make; it can make "fastest optimizer *at threshold X*, with the
   crossing at Y" — which the committed tables and SVGs now support.
2. **Three suites' pinned thresholds sit on the fragile side of a crossing.** The head-line numbers in
   §5.4 and §5.8 were correct *for their pinned threshold* and are now also bounded: e.g. in
   `schedule-free-mlp` the schedule-free arm wins at 0.148 only because the constant-rate arm, which
   converges deeper, has not yet been separated by the threshold.
3. **Two suites are stable, and the tool says so** — that distinction is the point. `schedule-free`
   (logistic) has the constant rate winning at all thirteen thresholds, which is a much stronger
   statement than the single number it replaces; `ademamix-mlp` is stable across its own floor range.
4. **In `ademamix` (logistic) the winner oscillates five times inside a 0.0014-wide band.** That is not
   a ranking at all; it means the two arms are tied in that region, and the §5.5 verdict for that suite
   rests on final loss and on the 10-seed comparison, not on speed.
   **§5.11 answers the obvious follow-up**: whether those crossings are stable across seeds, and whether
   the winner at each pinned threshold is the same every time. Two of the five pairs tested there turn
   out never to have had a crossing at all.
5. **This does not change any conclusion, it changes their scope.** AdEMAMix is still not faster in a
   stable sense, schedule-free's strong claim is still unsupported, and Adam is still mid-pack on both
   models — but each of those is now attached to a threshold rather than to a single number that happened
   to be picked in advance.

### 5.10 Capacity: do the answers survive a wider or deeper model?

Every conclusion so far was measured on an 8-unit hidden layer (or on the two-parameter logistic
head). Two more capacities were added — `[32]` and a two-layer `[8,8]` — with **every arm retuned for
the model it runs on** (`examples/capacity-h32-sweep.json` and `examples/capacity-h8x8-sweep.json`,
21 trials each), 200 epochs, target 0.147 and ten seeds.

Ten-seed test loss, paired against the tuned-cosine baseline:

| arm | `[8]` (from §5.7) | `[32]` | `[8,8]` |
|---|---:|---:|---:|
| adagrad | — | **0.12555** (9/10 wins, +0.01032 vs cosine, 9/10 better) | **0.12845** (7/10 wins, +0.03949, 10/10 better) |
| schedule-free AdamW | 0.13094 | 0.13214 (0/10, +0.00373, 8/10 better) | 0.14479 (2/10, +0.02314, 8/10 better) |
| adamw + tuned cosine (baseline) | 0.13222 | 0.13587 | 0.16794 |
| adamw constant / adam (identical, no weight decay) | 0.13796 | 0.14425 (−0.00838 vs cosine, 1/10 better) | 0.19479 (−0.02685, 1/10 better) |
| ademamix | — | 0.14508 (−0.00921, 1/10 better) | 0.19793 (−0.02999, 1/10 better) |

Seed-7 speed, for the record (`epochs_to_target` at 0.147): `[32]` schedule-free 9, adam/constant/
ademamix 37, cosine 38, adagrad 44; `[8,8]` schedule-free 20, everything else 26.

**Findings.**

1. **AdEMAMix's "no advantage" verdict is stable across all three capacities and both model families.**
   It is better than the AdamW baseline in only 1 of 10 seeds at `[32]` and 1 of 10 at `[8,8]`, and worse
   on mean test loss in both (0.14508 vs 0.13587; 0.19793 vs 0.16794). Combined with §5.5 this is the
   most robust negative result in the repository.
2. **The schedule-free "direction flip" is an architecture effect, not a capacity effect.** On the MLP
   it beats the tuned cosine at *every* capacity tested (8: 9/10 seeds; 32: 8/10; [8,8]: 8/10), while on
   the logistic head it loses 10/10. §5.9 explains why: the two arms cross at a threshold, and the
   logistic run's pinned threshold sits on the wrong side of its crossing. So the flip is not "some
   models favour it" — it is "the comparison is threshold-scoped, and the two model families have
   different crossings and different floors".
3. **A new, capacity-dependent result: AdaGrad wins on final test loss once the model has room to
   overfit** (9/10 and 10/10 seeds better than the tuned cosine). At `[8]` AdaGrad was only an also-ran.
   This is the first conclusion in the report that *does* change with capacity, and it changes in favour
   of the oldest method in the suite.
4. **Train-loss and test-loss rankings diverge as capacity grows.** At `[8,8]`, adam/constant/ademamix
   reach the lowest *train* losses (0.1332/0.1332/0.1330) and the worst *test* losses
   (0.1411/0.1411/0.1418), while schedule-free reaches the best test loss (0.1247). A suite that ranked
   by training loss would invert the answer at this capacity, which is why both numbers are pinned.
5. **The consistency check reproduces at every capacity**: `adam` and `adamw` with weight decay 0 are
   bit-identical (0.14425/0.14425 at `[32]`, 0.19479/0.19479 at `[8,8]`), the same way AdEMAMix with
   α = 0 reduced to AdamW in §5.5.
6. **Threshold structure exists at every capacity, but it is a tie band, not a crossing.** On both new
   grids the tightest thresholds are won strictly by `ademamix` (its floor is the lowest); above ~0.1417
   on `[32]` and above ~0.1374 on `[8,8]` the leading arms reach the same threshold on **the same epoch**,
   so the region is a tie rather than a change of leader. §5.11 shows why the earlier phrasing ("the lead
   passes to `adam`") was wrong: ties were being resolved alphabetically in the analysis code. The
   conclusion that survives is the weaker, correct one — "fastest optimizer" always needs its threshold
   attached, and a tie is not a ranking.

**Which statements survive which change of facet** (✓ = direction held, ✗ = it flipped, — = not tested):

| statement | logistic head | MLP `[8]` | MLP `[32]` | MLP `[8,8]` | threshold change | verdict |
|---|---|---|---|---|---|---|
| AdEMAMix has no advantage over AdamW | ✓ | ✓ | ✓ | ✓ | ✓ | **stable** |
| Adam is not the fastest optimizer | ✓ | ✓ | ✓ | ✓ | ✗ (crossings exist) | stable in direction, not in ranking |
| schedule-free beats a tuned cosine | ✗ | ✓ | ✓ | ✓ | ✗ (crossing at 0.1434) | **architecture- and threshold-scoped** |
| a constant learning rate wins | ✓ | ✓ | ✗ (adagrad/cosine win) | ✗ | — | capacity-scoped |
| AdaGrad is competitive | ✗ | ✗ | ✓ | ✓ | — | capacity-scoped |

The point of the table is the middle column set: the repository reports four model sizes, two model
families and a threshold grid, and a claim is only stated at the scope where it was measured. Nothing
in §5.1–5.9 was retracted by the capacity runs; two claims (constant-rate dominance, AdaGrad) turned out
to be capacity-scoped and are now labelled that way.

### 5.11 Is the crossing itself stable? (ten seeds, and a bug in the analysis)

§5.9 located crossings on the seed-7 curves. A crossing that exists in one seed and moves, or
disappears, in the others is not a statement a conclusion can carry — so the crossing detector was
applied to all ten per-seed result files, and it is worth separating two questions: *does* a crossing
exist, and *is the winner at the pinned threshold the same every time*.

| suite | pair | crossings found | mean position | spread across seeds | winner at the pinned threshold |
|---|---|---:|---:|---:|---|
| `optimizers` (logistic) | adam_no_bias_correction vs adagrad | **10/10** | 0.1370 | 0.0456 | **consistent: `adagrad`** |
| `optimizers-mlp` | adam vs sgd_momentum | 7/10 | 0.1167 | 0.0530 | **inconsistent** |
| `schedule-free-mlp` | adamw_constant vs schedule_free_adamw | **10/10** | 0.1192 | 0.0505 | **inconsistent** |
| `capacity-h32` | ademamix vs adam | **0/10** | — | — | consistent: **`tie`** |
| `capacity-h8x8` | ademamix vs adam | 5/10 | 0.0947 | 0.0528 | consistent: **`tie`** |

Positions are located on each seed's own grid (`runs/threshold-curves/*-crossing-stability.md`), which
is why the means sit below the converged floors: on curves that overfit, the tightest reachable point
is an early minimum, not the final loss.

**Findings.**

1. **"A crossing exists" and "the crossing is stable" are different claims, and only the second one is
   usable.** `optimizers` (logistic) has a crossing in every seed but its position moves across a
   0.0456 band — quoting "the crossing is at 0.137" would be a single-seed artefact. What *is* stable
   there is the practical statement: `adagrad` is faster at the pinned threshold in every seed.
2. **`schedule-free-mlp` fails the stronger test.** The crossing exists in 10/10 seeds, but the arm
   that is faster at the suite's pinned threshold (0.148) **changes between seeds**. The seed-7 line
   "schedule-free reaches the target in 11 epochs against the constant rate's 23" is therefore a
   single-seed statement and is now labelled as one; §5.8's *test-loss* result (schedule-free beats the
   tuned cosine in 9/10 seeds) is a different measurement and stands.
3. **Two of the five pairs never had a crossing at all.** On `capacity-h32` the three leading arms reach
   every loose threshold on exactly the same epoch, and the crossing this report previously quoted at
   0.1417 was an artefact of breaking ties alphabetically inside the analysis code (see below). The
   corrected reading is "`ademamix` is strictly faster below ~0.1417; above it the leading arms are
   tied", and on `capacity-h8x8` the loose region is a four-way tie.
4. **The tool had to be fixed to say any of this.** `scripts/threshold_curve.py` resolved ties with
   `min()` over `(epoch, name)` tuples, i.e. alphabetically, in two places. That manufactured a
   "crossing" for `capacity-h32` and would have let a sort order decide a published ranking. Ties are
   now reported as `tie: a, b, c`, the crossing detector skips tied thresholds instead of breaking
   them, and `tests/test_threshold_curve.py` pins both behaviours (`test_identical_curves_have_no_crossing`).
   This is the third defect of the same family in this repository — after a metric direction that
   inverted a ranking and a seed that reached only the data split — and the shared lesson is that a
   number can come from the tooling rather than from the experiment.
5. **Where this leaves the speed claims.** Adam-mid-pack survives capacity and model changes; what it
   does *not* survive is being stated as one number. The repository now reports speed as
   "arm A is faster than arm B at threshold T, in N/10 seeds", which is what the curves, the crossing
   tables and the per-seed tables together support.

## 6. Deviations from the paper (and why)

| # | Deviation | Reason | Risk to validity |
|---|---|---|---|
| D1 | Full-batch instead of mini-batch gradients | keeps the run deterministic, offline and dependency-free | bias correction matters most in the first steps; stochastic-gradient effects are **not** exercised |
| D2 | α = 0.08 instead of the default 0.001 | 80 full-batch steps on an 800-row problem is a very short budget | the paper's "default settings work well" claim is not tested |
| D3 | Section 5.1–5.3 evaluate final test loss / accuracy only | that experiment asks "which floor is lower at a fixed budget" | those numbers do **not** measure convergence speed; §5.4 is the experiment that does |
| D4 | L2 added to the gradient, not decoupled weight decay | matches the 2014 paper's formulation | the regularized variant is not an AdamW test |
| D5 | `ε` added after the square root, as in the original Algorithm 1 | faithfulness to the 2014/2015 text; later revisions restate the denominator with an ε̂ term | numerically irrelevant here (ε = 1e-8) |
| D6 | AdaGrad / RMSProp / SGD+momentum implemented from their published descriptions, not from a shared framework | keeps the run dependency-free and auditable | framework-specific details (e.g. exact ε placement, momentum conventions) may differ from other implementations |
| D7 | §5.4 learning rates chosen by a coarse grid, target 0.16 chosen by hand | a fixed hand-picked rate per family would compare tuning luck; the target must sit near the floor to measure convergence rather than the first step | both choices change the ranking; the sweep curves are committed so the choice can be redone |

## 7. Limitations and threats to validity

- **Task scale.** 800 rows, 2 features, 80 epochs. This cannot speak to ImageNet-scale behaviour.
- **Convergence speed is measured in §5.4 only**, and its ranking is sensitive to the target and to
  the swept rate grid. §5.1's "Adam wins" must be read as "Adam wins against these two SGD settings
  at a fixed budget".
- **Tuning asymmetry in §5.1.** `sgd_control` uses a hand-picked lr = 0.35 and is the *stronger* SGD
  arm; the `baseline` at lr = 0.15 is weaker. §5.4 removes this asymmetry by sweeping all families,
  and there Adam is mid-pack.
- **The rate grid is not saturated.** In §5.4 the best loss for every adaptive family sits at or
  beyond the largest swept rate (AdaGrad 4.0, Adam 0.40, RMSProp 0.20–0.40, momentum 0.80), so "the
  tuned rate" is "the best rate inside this grid", not a global optimum. A finer/edge-extended sweep
  is a stated next step.
- **A loose target inverts the story.** At target 0.30 the metric is dominated by the first step
  (AdaGrad lr = 4 reaches it in 2 epochs) and the ranking flattens. Reporting a single
  `epochs_to_target` number without the target would be misleading; both regimes are committed.
- **One dataset family.** Conclusions are specific to this synthetic linear-margin task.
- **Ten seeds, no formal test.** Seeds are paired, so a paired test would be defensible; this report
  reports mean/stdev/min/max and win counts instead of a p-value.
- **Cross-platform tolerance.** `math.exp`/`math.sqrt` may differ by a few ULP across libm builds,
  hence explicit tolerances (`expected/expected_metrics.json`): loss 1e-6, accuracy 0.005 (one test
  sample). `duration_ms` is excluded from verification.

## 8. Defect found and fixed while producing this report

`config_sha256` was computed from raw file bytes. Because Git on Windows (`core.autocrlf=true`)
rewrites LF to CRLF at checkout, the *same revision* produced two different hashes — the Windows
checkout of the very commit that recorded `cc85ba76…` reported `ff335de1…`, i.e. the provenance
identifier was platform-dependent and silently unusable. Fixed in `autoresearch/runner.py`
(`config_sha256()` normalizes newlines) and covered by
`tests/test_harness.py::ConfigHashTests::test_newline_style_does_not_change_the_config_hash`.
The Windows checkout now reports the recorded hash, which is why `scripts/repro.py` verifies the
config hash at all.

## 9. Is the verification harness itself trustworthy?

A passing check is only meaningful if the check can fail. `scripts/score_task.py` therefore runs the
scoring contract against deliberately broken copies of the implementation (negative controls) and
requires each of them to be **detected**:

| control | mutation | expected | observed |
|---|---|---|---|
| `no-bias-correction` | drop `/(1 - b1^t)` and `/(1 - b2^t)` | fail | detected — 82.4/100, exit 1 |
| `no-adaptive-scaling` | update by `α·m̂` without `/√v̂` | fail | detected — 82.4/100, exit 1 |

Both controls are detected at a partial score of 82.4/100, which is also the partial-credit behaviour
described in `TASK.md`: a broken attempt is scored, not just rejected. `tests/test_harness.py` asserts
that the mutation fragments still exist in `model.py`, so a refactor cannot silently turn a control
into a no-op.

One honest detail worth stating: removing the bias correction (`no-bias-correction`) *lowers* this
task's test loss further (0.12533693 vs the recorded 0.20216034). The expectation is therefore
anchored to the **paper-faithful implementation**, not to the best number obtainable — the recorded
value is a regression baseline that proves the code still implements Algorithm 1, and it is
deliberately not "tuned" to look good. This is also why the assertion must be a numeric comparison
against a pinned artifact rather than a "did it improve?" check: on a small synthetic task, a wrong
implementation can look better.

A second defect was found the same way, by cross-checking two outputs instead of trusting one: the
seed-sweep table reported RMSProp as the per-seed winner for §5.4 while the per-seed data clearly
showed AdaGrad. `epochs_to_target` had been added to the runner's "lower is better" set but not to the
copy of that set inside `scripts/seed_sweep.py`, which inverted the ranking. The set now lives once
(`LOWER_IS_BETTER_METRICS` in `autoresearch/runner.py`) and `tests/test_metric_direction.py` fails if a
metric is added without a declared direction.

CI (`.github/workflows/repro.yml`) runs the same reproduction on Python 3.10 and 3.12 on Linux plus a
container run, and uploads `runs/demo` and `runs/seed-sweep` as artifacts.

## 10. Provenance and artifacts

| Artifact | Path |
|---|---|
| Experiment configs (single source of truth) | `examples/classification.json`, `examples/optimizers.json`, `examples/ademamix.json` |
| Tuning sweeps used by §5.4 and §5.5 | `examples/optimizers-sweep.json` (24 trials), `examples/ademamix-sweep.json` (20 trials) |
| Expected numbers + tolerances | `expected/expected_metrics.json`, `expected/expected_optimizers.json`, `expected/expected_ademamix.json` |
| Verified single-seed results | `runs/demo-verified/`, `runs/optimizers-verified/`, `runs/ademamix-verified/` (`results.json`, `report.md`, `loss-curves.csv`) |
| Verified 10-seed aggregates | `runs/*-verified/seed-sweep-summary.json`, `.md` |
| Committed tuning curves (recompute any target) | `runs/optimizers-verified/lr-sweep/loss-curves.csv`, `runs/ademamix-verified/tuning-sweep/loss-curves.csv` |
| Trainer / optimizer source | `autoresearch/trainers/`, `autoresearch/optimizers.py`, `autoresearch/schedules.py`, `autoresearch/datasets.py` |
| Fresh runs (regenerated by the one command, not committed) | `runs/demo/`, `runs/optimizers/`, `runs/ademamix/`, `runs/seed-sweep*/` |
| Environment of a run | `runs/<suite>/environment.json` |

Everything in `runs/demo-verified/` is generated, not hand-written; the tests assert that the committed
result still matches `expected/expected_metrics.json`, so a regeneration that changes a number fails CI.

## 11. 中文摘要

本文档是对 Kingma & Ba《Adam: A Method for Stochastic Optimization》（arXiv:1412.6980）的**机制级复现**：
用纯标准库 Python 按论文 Algorithm 1 实现一阶/二阶矩估计与偏差修正，在固定数据、固定随机种子的
二分类任务上与固定学习率 SGD 做对照。**10 个种子上 Adam 的测试损失全部更低**（相对较强 SGD 对照的
配对提升 `0.07670 ± 0.00554`，均值/标准差比约 13.9），方向性结论成立；但**没有**复现论文的
MNIST / CIFAR-10 / IMDB 实验，因此不宣称复现论文表格中的任何具体数字。已知差异：本复现用全批量梯度、
学习率取 0.08、只记录最终指标（不测收敛速度），详见第 6 节。同时修正了一个真实缺陷：
配置哈希原先按原始字节计算，Windows 检出（CRLF）会把同一版本算成两个不同的哈希。
`python scripts/repro.py` 一条命令即可重跑并断言 17 项预期数值。

**第二个实验（收敛速度）给出了负结果**：论文的主张是"更快收敛"，而不只是"同等轮数下损失更低"，
所以第二个实验测量"达到目标损失的轮数"，并且**每个优化器家族都用同一套粗粒度学习率扫描选出自己的
学习率**（扫描 24 组，曲线已提交）。结论是 **Adam 并不最快**：AdaGrad 在 **10/10 个种子**上最先达标
（平均 4.7 轮 vs Adam 22.6 轮），带动量的 SGD 也 10/10 快于 Adam，朴素 SGD 在扫描过的所有学习率下
**从未**到达该目标。附带发现：关闭偏差修正后 Adam 反而 10/10 更快达标（快 12.5 ± 4.6 轮），最终损失
也略低——说明偏差修正的收益在**极短训练预算**下最明显，在 120 轮的全批量凸任务上不一定划算。
两个实验回答的是**不同问题**（固定轮数下的损失水平 vs 达到目标的轮数），不能互相替代引用；
第 7 节列出了仍未测量的部分（学习率网格未饱和、目标阈值人工选定、仍是全批量凸任务）。

## References

1. D. P. Kingma, J. Ba. *Adam: A Method for Stochastic Optimization.* arXiv:1412.6980, 2014; ICLR 2015.
2. I. Loshchilov, F. Hutter. *Decoupled Weight Decay Regularization.* arXiv:1711.05101, 2017/2019
   (cited only for the L2/adaptive interaction noted in §5.2).
3. J. Duchi, E. Hazan, Y. Singer. *Adaptive Subgradient Methods for Online Learning and Stochastic
   Optimization.* JMLR 12:2121–2159, 2011 (AdaGrad, the §5.4 baseline that reaches the target first).
4. T. Tieleman, G. Hinton. *Lecture 6.5 — rmsprop: Divide the gradient by a running average of its
   recent magnitude.* COURSERA: Neural Networks for Machine Learning, 2012 (RMSProp).
5. B. T. Polyak. *Some methods of speeding up the convergence of iteration methods.* USSR
   Computational Mathematics and Mathematical Physics, 1964 (heavy-ball momentum, used in §5.4).
6. Repository: `https://github.com/CieveMe/autoresearch-experiment-runner` (see `CITATION.cff`).
