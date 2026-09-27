# Plan: adapter refactor + the next paper (2024–2025)

The repository claims that only `autoresearch/model.py` needs replacing to take on a real paper. That
claim is not yet true: there is one trainer, its parameters are two scalars and a bias, and the
optimizer set is hard-coded in one function. This document is the refactor that makes the claim true,
plus the concrete plan for the first 2024–2025 paper to run through it.

## 1. Why a refactor is needed before the next paper

| Current limitation | Consequence for a 2024–2025 paper |
|---|---|
| Logistic regression with 2 weights + 1 bias | Matrix-aware methods (Muon-style orthogonalisation, per-block second moments) degenerate; "hidden layers" claims cannot be tested at all |
| Optimizers hard-coded in `model.train()` | Every new paper edits the same function, so a regression in Adam is one careless edit away |
| No learning-rate schedule abstraction | Schedule-Free's claim is *about* schedules; it cannot be stated, let alone tested, without one |
| Determinism lives implicit in the trainer | A new trainer can silently break reproducibility without any test catching it |

## 2. Adapter refactor (target: one working day)

Keep the existing experiments bit-for-bit reproducible: `examples/classification.json` and
`examples/optimizers.json` and their pinned expectations must keep passing unchanged. Everything new is
additive.

```
autoresearch/
  trainers/
    __init__.py
    base.py        # Trainer protocol: fit(rows, config) -> FitResult(params, loss_curve, epochs_run)
    logistic.py    # current behaviour, moved verbatim (same arithmetic, same early stop)
    mlp.py         # pure-Python 2-layer tanh net, deterministic init from the config seed
    registry.py    # get_trainer(name)
  optimizers.py    # UPDATE_RULES: name -> (step_fn, state_init); operates on List[List[float]]
  schedules.py     # constant | cosine | warmup_cosine | ademamix_alpha | ademamix_beta3
  datasets.py      # synthetic (current) + local CSV/JSON; refuses network access by design
  model.py         # thin compatibility shim -> trainers.registry (keeps old imports working)
```

Rules that keep the repo honest while it grows:

1. **One update rule, one place.** `optimizers.py` holds every rule (including the Adam variants that
   exist today); `model.py` becomes a shim so the negative controls in `scripts/score_task.py` keep
   pointing at real code.
2. **Config schema stays backwards compatible.** New keys (`trainer`, `schedule`, `hidden_sizes`) are
   optional; absence means "current behaviour". A test asserts that both existing configs still hash to
   their recorded SHA-256 and still produce their pinned numbers.
3. **Every new trainer gets a gradient check.** A slow numerical-gradient test on a 10-row toy catches
   the classic backprop sign/index error, which is exactly the kind of defect that would otherwise look
   like "the paper's method doesn't work".
4. **Every new paper gets a negative control.** As with `no-bias-correction`, a deliberately mutated
   implementation must fail the pinned expectations. A paper card with no failure path is decoration.
5. **Determinism tests are mandatory per trainer**: same config + same seed ⇒ identical
   `loss_curve`, on Windows and in CI.

## 3. First paper: AdEMAMix (Apple, arXiv:2409.03137, 2024)

**Why this one first:** it is an optimizer-only change, so it reuses the whole existing harness
(`epochs_to_target`, loss curves, 10-seed paired comparison); it needs **no new dependency** (the
logistic trainer can implement it in the standard library); and its claim is exactly the claim the
harness already measures.

**Evidence checked on 2026-09-28** (repo cloned, `apple/ml-ademamix`, MIT, © 2024 Apple):
the repository contains the optimizer only (`pytorch/ademamix.py`, `optax/ademamix.py`) — no harness,
no dataset, no numbers. So this is a **mechanism-level** reproduction again, and no number from the
paper's tables may be claimed.

Update rule as implemented upstream (verified against the source, not against a summary):

```
m_fast ← β1·m_fast + (1−β1)·g                      # β1 = 0.9, allocated only if β1 > 0
m_slow ← β3·m_slow + (1−β3)·g                      # β3 = 0.9999, optional warmup
v      ← β2·v + (1−β2)·g²                          # β2 = 0.999
update = (m_fast / (1−β1ᵗ) + α·m_slow) / (√(v / (1−β2ᵗ)) + ε)
θ     ← θ − lr·(update + λ·θ)                      # AdamW-style decoupled decay
```

Plus two optional warmups: `α` linearly from 0 to its final value, and `β3` interpolated through
`f(β) = log(0.5)/log(β+ε) − 1` (the "linear-hl" schedule in their code).

**Deliverable per the existing contract**

| Item | Path |
|---|---|
| Experiment config | `examples/ademamix.json` |
| Expected numbers | `expected/expected_ademamix.json` |
| Paper card (claim → measurable → deviations → limits) | `docs/papers/ademamix-2024.md` |
| One-command entry | `python scripts/repro.py --suite ademamix` (added to `--suite all`) |
| Multi-seed claim | `python scripts/seed_sweep.py --config examples/ademamix.json --seeds 0-9` |
| Negative control | drop `m_slow` (i.e. α = 0) must fail the pinned numbers |

**Experiment design.** Five arms at the same budget, each tuned by the same rule already used for
`examples/optimizers.json` (best final training loss in a coarse sweep, ties to the smaller rate):
AdamW, AdEMAMix, AdEMAMix without the slow EMA (α = 0, the ablation), AdEMAMix without the two
warmups, and SGD+momentum as the weak control. Primary metric `epochs_to_target` against a tight
target, plus the final test loss. Report the paired per-seed comparison and state plainly whether the
paper's "faster convergence" claim holds here — including if it does not, which is the whole point of
the exercise.

**Risk to state up front:** the paper's regime is long-horizon language-model training where the slow
EMA has time to matter; a 120-epoch full-batch convex problem may be exactly the wrong scale to see
the effect. If the result is "no difference", that is a finding about *scale*, not about the method,
and the card must say so rather than implying the method is wrong.

## 4. Second paper: Schedule-Free learning (Meta, arXiv:2405.15682, 2024)

**Why second:** its claim is about schedules, which is a genuinely new axis for this harness, and its
repository ships `*_reference.py` files — a precise spec to port from (Apache-2.0, `requirements.txt`
only needs torch ≥ 2.0, which this machine does not have, so the port is to numpy/stdlib).

The README states the falsifiable claim directly: schedule-free learning "does not require a decreasing
learning rate schedule, yet typically out-performs, or at worst matches, SOTA schedules such as
cosine-decay and linear decay".

**Extra machinery needed:** `schedules.py` (constant / cosine / warmup+cosine) and one new experiment
that compares (a) a *tuned* cosine schedule against (b) schedule-free with no schedule, at matched
budget, on both trainers. This is also the honest answer to a reviewer's objection about the earlier
optimizer suite: "your baselines were not schedule-tuned" finally gets tested.

**Estimated effort:** 1.5–2 days (port the reference rule, add schedules, design the parity experiment,
pin expectations, add the negative control).

## 5. Considered and not chosen

| Candidate | Why not (checked, not guessed) |
|---|---|
| **Muon** (`kellerjordan/muon`, 2024; arXiv:2502.16982, 2025) | Needs ≥2-D parameters and a matrix orthogonalisation step, and its small-scale path is a GPU + tokenised-dataset nanogpt run. Offline-only budget and "alignable numbers" both fail today. Revisit once the numpy MLP trainer is merged — then it can at least be tested as a mechanism. |
| **TabPFN v2** (`automl/TabPFN`, 2024 / Nature 2025) | Requires downloading pretrained weights plus torch, and the work is *evaluating* a pretrained model rather than reimplementing a method, so the offline constraint and the "mechanism reproduction" framing both fail. |
| **Lion** (arXiv:2302.06675) | Outside the 2024–2025 window; cheap to add later as one more arm in the existing optimizer suite rather than as a paper. |

## 6. Acceptance criteria for "the next paper is done"

1. `python scripts/repro.py` runs every suite (existing two + the new one) and exits 0.
2. The new suite's numbers are pinned in `expected/` and verified by `scripts/verify_results.py`.
3. A 10-seed paired comparison exists, with the win count and mean ± stdev reported.
4. `docs/papers/<slug>.md` states the claim, the measurable proxy, the deviations from the paper's
   setup, the result (including a negative one), and the limitations that remain.
5. A negative control for the new method is detected by `scripts/score_task.py`.
6. `REPRODUCTION.md` gets a section; the README table gets one row; `CHANGELOG.md` gets an entry.
7. No number from the paper's tables is claimed unless the paper's own harness and data were used.
