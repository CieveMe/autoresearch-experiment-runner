# Full-tier gate after the CI fix (case 7)

`docs/release-checklist.md` hard rule 2: a release body quotes a **full**-tier run. This is the gate for
the release that carries the CI correction, plus the two cross-platform runs that show the platform which
was failing now passes.

## 1. Full-tier score on the reference platform (Windows, commit `0f3ce2f`)

```
$ python scripts/score_task.py --tier full
submission score: 100.0/100 (tier=full (all suites)) (474/474 checks, exit 0)
control[no-bias-correction]: detected (score 74.9/100, exit 1)
control[no-adaptive-scaling]: detected (score 77.0/100, exit 1)
control[ademamix-without-slow-ema]: detected (score 94.9/100, exit 1)
control[schedule-free-without-averaging]: detected (score 92.8/100, exit 1)

TASK RESULT: PASS
```

**The sentence that matters is the last control.** Widening one arm's tolerance was accepted only because
the harness still detects a broken implementation in exactly that arm: `schedule-free-without-averaging`
scores 92.8/100, i.e. it still fails expectations rather than sliding inside the new band. Before the
widening it scored 92.4/100, so the fix cost the control nothing.

## 2. Full-tier reproduction on the platform that was failing (Linux, `python:3.12-slim`)

```
$ docker run --rm -e PYTHONPATH=/app -v <repo>:/app -w /app python:3.12-slim python scripts/repro.py --tier full
tier=full (all suites)
verified:  474 checks, 0 failures
RESULT: PASS
```

Before the tolerance fix the same command reported **474 checks, 4 failures** — the four
`schedule_free_adamw` expectations, with the `schedule-free-mlp` one at 0.12526376 against the pinned
0.12506323 (the exact number the public CI had been failing on).

## 3. The CI docker job, reproduced end to end on a fresh clone

```
$ git clone --depth 1 https://github.com/CieveMe/autoresearch-experiment-runner.git <tmp>
$ docker compose up --build --exit-code-from repro
repro-1  | verified:  474 checks, 0 failures
repro-1  | RESULT: PASS
compose exit: 0
```

This is the path the workflow's `docker` job takes, and it is where the second defect was found: with the
tolerance fixed the image still failed, because the image never carried `TODO.md` while `scripts/repro.py`
ends by running the repository's own suite (case 6b's third copy). Fixed in the same commit as this file's
subject; a static guard now derives the image's required files from the test sources.

## 4. Continuous integration, as observed

| run | commit | python 3.10 | python 3.12 | docker |
|---|---|---|---|---|
| #37 and earlier | up to `054f5fa` | failure | failure | failure |
| **#39** | **`0f3ce2f`** | **success** | running (see note) | **success** |

The `python 3.12` job is not failing — it is the only job that runs the scorer, the sweeps and the
threshold curves, and it had **never reached step 6 in any previous run** because the reproduction step
failed first. On a two-core runner that means 1.5–2 hours for that job alone. That is worth knowing before
reading a long queue as a red build; if it becomes annoying, the honest split is to run the full scorer on
tag and `workflow_dispatch` and the core tier on every push, rather than to delete the step.

## Provenance

| field | value |
|---|---|
| fix commits | `df54b64` (per-trial tolerance with measured basis), `0f3ce2f` (Dockerfile + guard) |
| gate runs | Windows `score_task --tier full` at `0f3ce2f`; Linux container `repro --tier full`; fresh-clone `docker compose up` |
| asserted checks | 474 (all suites; nothing skipped) |
| unit tests | 93 in the tree, all green on both platforms |
| `v0.10.0` | untouched — tag `54b391f` and its body are unchanged |
