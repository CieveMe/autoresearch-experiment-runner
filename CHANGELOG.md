# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Trainer adapter** (`autoresearch/trainers/`): the original model moved, unchanged, into
  `trainers/logistic.py`; a second, dependency-free `trainers/mlp.py` (two-layer tanh, deterministic
  initialisation) proves the adapter is real, and `trainers/registry.py` selects by config key.
  `autoresearch/model.py` is now a compatibility shim.
- **Optimizer registry** (`autoresearch/optimizers.py`): every update rule in one place, written
  against a plain parameter vector so both trainers share it. Adds `adamw` (decoupled weight decay)
  and `ademamix`.
- **Schedules** (`autoresearch/schedules.py`): constant (default, exactly 1.0 so existing arithmetic is
  untouched), cosine, warmup+cosine, and AdEMAMix's α / β3 warmups.
- **Data sources** (`autoresearch/datasets.py`): synthetic (default) plus local CSV/JSON; URLs are
  refused before they are opened.
- **AdEMAMix (arXiv:2409.03137) suite**: `examples/ademamix.json` + `examples/ademamix-sweep.json` +
  `expected/expected_ademamix.json` + `docs/papers/ademamix-2024.md`. Result: the paper's
  faster-than-AdamW claim **is not reproduced** at this scale (identical epochs-to-target in 10/10
  seeds; the paper's own warmup scheme scaled to this budget is 4.5× slower).
- Thirteen more unit tests (30 total), including an MLP gradient check against finite differences and
  the α = 0 identity with AdamW.
- **The self-scepticism re-run**: both suites were repeated with the MLP trainer, with every family
  retuned for that model (`examples/optimizers-mlp.json`, `examples/ademamix-mlp.json` plus their
  sweeps). The logistic-head conclusions survive: Adam is mid-pack on time-to-target on both models
  (MLP: 20.3 epochs against AdaGrad 6.2 and momentum 7.0) and the paper's warmup scheme is the worst
  arm on both (MLP mean test loss 0.14269 / 0.15261 against AdamW's 0.13218).
- `examples/optimizers-mlp-sweep.json` (24 trials) and `examples/ademamix-mlp-sweep.json` (17 trials),
  committed with their curves, so the MLP rates can be re-derived rather than trusted.

### Changed

- `scripts/repro.py` runs **five** suites (121 asserted checks, ~18 s); `scripts/score_task.py`
  aggregates over all suites and its negative controls now name the file they mutate.

### Added (schedule-free follow-up, same release)

- **Schedule-Free AdamW / SGD** (`autoresearch/optimizers.py`, transliterated from
  `facebookresearch/schedule_free`, Apache-2.0) with the averaged-sequence evaluation point wired
  through `optimizers.eval_params()`; `examples/schedule-free.json` compares it against a **tuned**
  cosine baseline (21-trial sweep over learning rate × min-LR factor) and a constant-rate baseline, at
  a 200-epoch budget. Result: "at worst matches" is roughly right, "out-performs" is not — schedule-free
  is 0.3% behind the tuned cosine and loses all ten seeds, while a constant rate beats both.
- `tests/test_schedule_free.py`: the port is cross-checked step by step against a literal
  re-implementation of the reference rule, plus warmup, determinism and eval-point checks (39 tests
  total).
- `docs/papers/schedule-free-2024.md`.

### Fixed

- Trial configs did not inherit the experiment's `seed`, so a "10-seed" MLP run varied the data split
  while initialising from identical weights. `TRIAL_INHERITED_KEYS` now includes `seed`; the logistic
  trainer never read it, so the earlier pinned numbers are unaffected and still verify.

## [0.2.0] — 2026-09-28

The release that turns the paper's actual headline claim — *faster convergence* — into a measurable
experiment, and reports the result even though it contradicts the paper.

### Added

- **Convergence-speed experiment** (`examples/optimizers.json`): `epochs_to_target` (the first epoch
  whose training loss reaches a target near the converged floor) for Adam against SGD, heavy-ball
  momentum, AdaGrad and RMSProp, all at a matched 120-epoch budget.
- **Learning-rate sweep** (`examples/optimizers-sweep.json`, 24 trials): each optimizer family picks
  its learning rate by the same rule (lowest final training loss, ties to the smaller rate), so the
  comparison does not measure tuning luck. Curves are committed, so any other target can be re-scored.
- **Bias-correction ablation**: `bias_correction: false` on Adam, so the paper's correction term can
  be switched off and measured.
- **Per-epoch loss curves** in every result, exported to `loss-curves.csv`.
- **Release metadata**: `CHANGELOG.md`, `.zenodo.json`, `docs/release-checklist.md`.
- Five more unit tests (17 total) covering the new optimizers, target reaching and metric direction.

### Changed

- `scripts/repro.py` now runs **both** experiment suites in one command (46 asserted checks) and takes
  `--suite main|optimizers|all`; its table prints `epochs_to_target`.
- `scripts/seed_sweep.py` handles "never reached the target" (`null`) in means, ranking and paired
  comparisons instead of crashing or silently dropping the trial.

### Fixed

- `config_sha256` was computed from raw bytes, so a Windows checkout (`core.autocrlf=true`) reported a
  different hash for the same revision. The hash now normalizes line endings, with a regression test.
- `epochs_to_target` was missing from one copy of the "lower is better" metric list, which inverted the
  seed-sweep ranking (RMSProp was reported as the per-seed winner instead of AdaGrad). The set now has
  a single definition plus a test that fails when a new metric has no declared direction.

### Result reported by this release

AdaGrad reached the target first in **10/10 seeds** (mean 4.7 epochs vs Adam's 22.6); SGD with momentum
beat Adam 10/10 as well; RMSProp was the slowest adaptive method; plain SGD never reached the floor at
any swept rate. Disabling Adam's bias correction reached the target 10/10 faster (12.5 ± 4.6 epochs)
with a marginally lower final loss. Full analysis, caveats and the raw curves are in
`REPRODUCTION.md` §5.4 and `runs/optimizers-verified/`.

### Known limitations

- Mechanism-level, not benchmark-level: the paper's MNIST / CIFAR-10 / IMDB experiments are **not**
  reproduced and no number from the paper's tables is claimed.
- Full-batch gradients, no learning-rate schedules, one dataset family, ten seeds, no formal
  significance test, and a learning-rate grid that is not saturated (every adaptive family's best rate
  sits at or beyond the largest swept value).
- The convergence-speed ranking depends on the chosen target (0.16); both the tight and a looser
  target regime are committed so the analysis can be redone.

## [0.1.0] — 2026-09-28

First public release (tag `v0.1.0`, commit `0dd90e3`). Every number in this repository is regenerated
and asserted by one command (`python scripts/repro.py`), and the assertion harness is itself checked
against deliberately broken implementations.

### Added

- **Adam mechanism reproduction** (`examples/classification.json`): the first/second moment estimates
  and bias correction from Algorithm 1 of arXiv:1412.6980, implemented in dependency-free Python and
  compared against fixed-learning-rate SGD under a fixed seed and epoch budget.
- **One-command entry point** (`scripts/repro.py`): environment report, config validation, run,
  expected-number verification, unit tests; non-zero exit on any mismatch.
  `make repro` and `docker compose up --build` run the same path.
- **Expected-number contract**: `expected/expected_metrics.json` (17 assertions) and
  `expected/expected_optimizers.json` (28 assertions) pin every reported number with explicit
  tolerances; `scripts/verify_results.py` enforces them.
- **Multi-seed aggregation** (`scripts/seed_sweep.py`): means, standard deviations, per-seed win
  counts and paired per-seed improvements, so no claim rests on a single run.
- **Task contract** (`TASK.md` / `TASK.zh.md`): objective, command surface, K1–K7 acceptance criteria,
  0–100 partial-credit scoring, failure modes with detection, retry protocol, four task variants.
- **Falsifiability checks** (`scripts/score_task.py`): scores a submission and runs negative controls
  (drop bias correction; drop adaptive scaling) that must be detected.
- **Reproduction report** (`REPRODUCTION.md`): what is and is not reproduced, deviations from the
  paper, limitations, and the negative result in the convergence-speed experiment.
- CI on Python 3.10/3.12 plus a container job, `Dockerfile`, `compose.yaml`, `Makefile`, MIT licence,
  `CITATION.cff` and 8 unit tests.
