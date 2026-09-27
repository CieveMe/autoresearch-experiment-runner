# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-09-28

First public release. Every number in this repository is regenerated and asserted by one command
(`python scripts/repro.py`), and the assertion harness is itself checked against deliberately broken
implementations.

### Added

- **Adam mechanism reproduction** (`examples/classification.json`): the first/second moment estimates
  and bias correction from Algorithm 1 of arXiv:1412.6980, implemented in dependency-free Python and
  compared against fixed-learning-rate SGD under a fixed seed and epoch budget.
- **Convergence-speed experiment** (`examples/optimizers.json`): SGD, heavy-ball momentum, AdaGrad,
  RMSProp and Adam compared by *epochs to reach a target training loss*.
- **Learning-rate sweep** (`examples/optimizers-sweep.json`, 24 trials) so every optimizer family is
  tuned by the same procedure instead of comparing hand-picked rates.
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
  `CITATION.cff` and 17 unit tests.

### Fixed

- `config_sha256` was computed from raw bytes, so a Windows checkout (`core.autocrlf=true`) reported a
  different hash for the same revision. The hash now normalizes line endings, with a regression test.
- `epochs_to_target` was missing from one copy of the "lower is better" metric list, which inverted the
  seed-sweep ranking (RMSProp was reported as the per-seed winner instead of AdaGrad). The set now has
  a single definition plus a test that fails when a new metric has no declared direction.

### Known limitations

- Mechanism-level, not benchmark-level: the paper's MNIST / CIFAR-10 / IMDB experiments are **not**
  reproduced and no number from the paper's tables is claimed.
- Full-batch gradients, no learning-rate schedules, one dataset family, ten seeds, no formal
  significance test.
- The convergence-speed ranking depends on the chosen target (0.16) and on a learning-rate grid that is
  not saturated. Both regimes and the raw curves are committed so the analysis can be redone.
