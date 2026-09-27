# Reproduction Report — Adam: A Method for Stochastic Optimization

| Field | Value |
|---|---|
| Paper | *Adam: A Method for Stochastic Optimization* — Diederik P. Kingma, Jimmy Ba (arXiv:1412.6980, 2014; ICLR 2015) |
| Artifact | `autoresearch-lite` v0.2.0 — `https://github.com/CieveMe/autoresearch-experiment-runner` |
| Reproduction level | **mechanism-level** (algorithm re-implementation + controlled head-to-head), not benchmark-level |
| Config revision | `examples/classification.json`, SHA-256 `cc85ba76ddcdff91f561bb0366fd3228c00e5b46541af8e4cdc04563926e040f` |
| One command | `python scripts/repro.py` (cross-platform) or `make repro` |
| Verified on | 2026-09-28, CPython 3.12.5, Windows 11 (x64), no network, no third-party packages |
| Expected numbers | `expected/expected_metrics.json`, 17 machine-checked assertions |

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

## 6. Deviations from the paper (and why)

| # | Deviation | Reason | Risk to validity |
|---|---|---|---|
| D1 | Full-batch instead of mini-batch gradients | keeps the run deterministic, offline and dependency-free | bias correction matters most in the first steps; stochastic-gradient effects are **not** exercised |
| D2 | α = 0.08 instead of the default 0.001 | 80 full-batch steps on an 800-row problem is a very short budget | the paper's "default settings work well" claim is not tested |
| D3 | Both optimizers evaluated by final test loss / accuracy only (no per-epoch curve) | the runner records final metrics | **convergence speed itself is not measured**; "lower loss at equal budget" is not "faster convergence" |
| D4 | L2 added to the gradient, not decoupled weight decay | matches the 2014 paper's formulation | the regularized variant is not an AdamW test |
| D5 | `ε` added after the square root, as in the original Algorithm 1 | faithfulness to the 2014/2015 text; later revisions restate the denominator with an ε̂ term | numerically irrelevant here (ε = 1e-8) |

## 7. Limitations and threats to validity

- **Task scale.** 800 rows, 2 features, 80 epochs. This cannot speak to ImageNet-scale behaviour.
- **No convergence-speed measurement** (D3). The reproduced claim is "lower loss at a fixed budget".
- **Tuning asymmetry.** `sgd_control` uses a hand-picked lr = 0.35 and is the *stronger* SGD arm; the
  `baseline` at lr = 0.15 is weaker. Both are reported so the reader can see the asymmetry, but no
  exhaustive SGD learning-rate sweep was run. A reviewer should treat "Adam wins" as "Adam wins
  against these two SGD settings".
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

CI (`.github/workflows/repro.yml`) runs the same reproduction on Python 3.10 and 3.12 on Linux plus a
container run, and uploads `runs/demo` as an artifact.

## 10. Provenance and artifacts

| Artifact | Path |
|---|---|
| Experiment config (single source of truth) | `examples/classification.json` |
| Expected numbers + tolerances | `expected/expected_metrics.json` |
| Verified single-seed result | `runs/demo-verified/results.json`, `runs/demo-verified/report.md` |
| Verified 10-seed aggregate | `runs/demo-verified/seed-sweep-summary.json`, `.md` |
| Fresh run (regenerated by the one command, not committed) | `runs/demo/`, `runs/seed-sweep/` |
| Environment of a run | `runs/demo/environment.json` |

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

## References

1. D. P. Kingma, J. Ba. *Adam: A Method for Stochastic Optimization.* arXiv:1412.6980, 2014; ICLR 2015.
2. I. Loshchilov, F. Hutter. *Decoupled Weight Decay Regularization.* arXiv:1711.05101, 2017/2019
   (cited only for the L2/adaptive interaction noted in §5.2).
3. Repository: `https://github.com/CieveMe/autoresearch-experiment-runner` (see `CITATION.cff`).
