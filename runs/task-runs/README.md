# T-ADAM-01 variants, one round each

`TASK.md` §9 defines four variants of the same scored task. This directory records one round of the three
that can be executed mechanically, so the claim "the task contract is executable and gives a candidate a
gradient to climb" is backed by transcripts rather than by a description.

The transcripts are the raw output of `scripts/score_task.py`; the tier is printed inside the score line
and travels with the number. 01B and 01D run in a throwaway copy of the repository
(`scripts/task_variants.py`, `python scripts/task_variants.py`); 01C is a repository change and is
recorded in `T-ADAM-01C.md`.

## Scoreboard

| variant | given state | attempts | final | solved |
|---|---|---:|---|---|
| **T-ADAM-01B** implement | Adam branch stubbed out: **0.0/100** | 4 scorer runs | **100.0/100, all four controls detected** | yes |
| **T-ADAM-01C** ablate | repository as shipped | 1 run + 10-seed sweep | **100.0/100 with the new suite in the contract** | yes |
| **T-ADAM-01D** recover | `no-adaptive-scaling` applied: **82.1/100** | 3 scorer runs | **100.0/100, all four controls detected** | yes |

## Quotable output

**The quote a release body or any outward-facing claim must use is the full-tier one**, in
[`FULL-TIER.md`](FULL-TIER.md): `100.0/100 (tier=full (all suites)) (474/474 checks, exit 0)` with all
four controls detected. The core-tier lines below are process evidence — they show the score curve the
variants climb — and they say so in their own tier label.

`T-ADAM-01B`, after the implementation (identical for 01D, which converges on the same tree):

```
submission score: 100.0/100 (tier=core; NOT run: capacity-h32, capacity-h8x8, capacity-h64, capacity-h16x16, activation-relu, activation-gelu, norm-layernorm, norm-batchnorm, init-he, init-plain) (184/184 checks, exit 0)
control[no-bias-correction]: detected (score 83.7/100, exit 1)
control[no-adaptive-scaling]: detected (score 82.1/100, exit 1)
control[ademamix-without-slow-ema]: detected (score 94.0/100, exit 1)
control[schedule-free-without-averaging]: detected (score 94.6/100, exit 1)

TASK RESULT: PASS
```

The starting states:

```
control[no-adaptive-scaling] applied, before repair:  submission score: 82.1/100  (T-ADAM-01D)
Adam branch stubbed out, before implementation:       submission score:  0.0/100  (T-ADAM-01B)
```

## T-ADAM-01B — the attempt worth reading

| attempt | pinned score | submission exit | mutation points live | accepted |
|---|---:|---:|---|---|
| given: Adam branch stubbed out | 0.0/100 | 1 | — | — |
| **attempt 2**: Algorithm 1 from the paper, arithmetic folded differently | **100.0/100** | 1 | **no** | **rejected** |
| **attempt 3**: same algorithm, kept drop-in at the harness's mutation points | **100.0/100** | 0 | yes | **accepted** |
| final: full scorer including the controls | 100.0/100 | 0 | — | four controls detected |

**Attempt 2 is the finding.** It is numerically correct — every pinned expectation passes — and it still
scores 100/100, while **two of the four controls come back `missed`**. The reason is that it left the
original branch behind as dead code, and the controls mutate by replacing text: every fragment still
matched, so the mutation landed in code that never runs, and the harness silently lost its teeth. The
repository's guard for that (`test_every_control_fragment_still_exists_in_the_source_it_names`) checks
presence, which dead code satisfies.

Two fixes came out of it, both in this commit:

1. `tests/test_harness.py::test_every_control_fragment_changes_the_numbers_it_mutates` — a **behavioural**
   guard: mutate a throwaway copy, run one six-epoch experiment with the optimizer the control targets,
   and require the loss to move. Presence is not liveness.
2. The variant's acceptance criterion no longer stops at the score. `scripts/task_variants.py` requires,
   for a solve, all three of: pinned 100/100, submission `exit 0`, and every control detected — plus the
   liveness probe after each attempt. `TASK.md` §9 now states the drop-in requirement explicitly.

This is the same rule as `docs/defect-family.md` case 5, one level up: **a check that can be satisfied
without changing what runs is not a check.** The task contract is executable — and it took a run of it to
find out that its own sensitivity could be switched off by an innocent rewrite.

## T-ADAM-01C — the ablation

See [`T-ADAM-01C.md`](T-ADAM-01C.md). Summary: a pre-registered prediction about Adam's first moment came
out **half wrong** (β1 = 0 is *slower* to the target, 0/10 seeds faster, and worse on the floor, 0/10
better; paired p = 0.0020, median difference +0.00268 [+0.00113, +0.00342]), and the ablation is now part
of the reproduction contract (`make repro-ablation`, `expected/expected_ablation_adam_no_first_moment.json`).

## What these runs are not

* They are **core-tier** scores. The tier label is quoted with every number, and the full-tier gate for a
  release is a separate run (`docs/release-checklist.md` hard rule 2).
* They are **not** an estimate of what a language-model agent would score; a human wrote the
  implementation. They are evidence that the task is well-posed, scored, and solvable from its own
  failing assertions.
* 01B and 01D converge on the same final tree, so their quotable lines are identical by construction.
