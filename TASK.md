# TASK.md — the reproduction expressed as an agent-retryable experiment task

This file is the *task specification* for this repository: it defines what an agent must
accomplish, which actions are allowed, how the attempt is scored, how failure shows up, and
how many times the agent may retry. It exists because a reproduction is only useful to an
automated research loop when it is expressed as an objective with a machine-checkable verdict.

`README.md` explains the software. `REPRODUCTION.md` reports the scientific result. **This file
is the contract** that makes the result re-derivable, scoreable and falsifiable.

```yaml
task_id: T-ADAM-01
title: Reproduce the mechanism-level Adam vs SGD comparison and prove it is verifiable
repo: autoresearch-experiment-runner
entry_point: python scripts/repro.py
scorer: python scripts/score_task.py
expected_numbers: expected/expected_metrics.json
primary_metric: test_loss        # lower is better
network_required: false
wall_clock_budget: 300s          # per attempt, on a laptop-class CPU
max_attempts: 5
```

## 1. Objective

Produce a repository state in which all of the following hold at once, on the machine the agent
runs on, with no network access:

1. the experiment runs end to end from one command;
2. the produced numbers match the recorded expectations within the recorded tolerances;
3. the unit suite passes;
4. the recorded provenance (config hash) is the one the config actually has on this platform;
5. the negative controls still fail (a broken implementation must not be scored as a success).

## 2. Given to the agent

| Input | Path | Notes |
|---|---|---|
| Reference implementation | `autoresearch/` | Adam + SGD, full batch, standard library only |
| Experiment definition | `examples/classification.json` | hypothesis, seed, data sizes, baseline, variants |
| Expected numbers | `expected/expected_metrics.json` | 17 assertions + tolerances |
| Verification entry | `scripts/repro.py` | the one command |
| Report template | `REPRODUCTION.md` | what the final report must contain |

The agent is **not** given permission to change items 3 and 4 above to make an attempt pass.

## 3. Commands (the whole task surface)

```bash
python scripts/repro.py                       # must exit 0
python scripts/repro.py --skip-tests          # faster loop while iterating
python scripts/seed_sweep.py --seeds 0-9      # multi-seed aggregate (10 seeds)
python -m unittest discover -s tests -v       # unit suite
python scripts/score_task.py                  # score + negative controls
make repro && make verify && make test        # Linux/macOS equivalents
```

## 4. Success criteria

| # | Criterion | Machine check |
|---|---|---|
| K1 | One command runs the whole pipeline and exits 0 | `python scripts/repro.py; echo $?` → `0` |
| K2 | Produced `test_loss` / `test_accuracy` / `epochs` match expectations | `scripts/verify_results.py` → `17 checks, 0 failures` |
| K3 | Best trial by `test_loss` is `adam_reproduction` | checked in K2 (`best.name`) |
| K4 | Config hash equals the recorded hash on a CRLF or LF checkout | checked in K2 (`config_sha256`) |
| K5 | Unit suite green | `python -m unittest discover -s tests` → `OK` |
| K6 | Negative controls are still detected | `scripts/score_task.py` reports `detected` for every control |
| K7 | Report artifacts are regenerated, not hand-edited | `runs/demo/report.md` and `results.json` are rewritten by K1 |

## 5. Scoring contract (0–100, partial credit)

```
score = 100 × (verified_checks_passed / verified_checks_total)      # 17 checks from K2
```

* `100` — the run exits 0 and every expected number matches inside tolerance (K1–K7 all hold).
* `1–99` — partial credit; the shortfall names the exact assertion that failed
  (for example a broken Adam update yields `82.4/100`).
* `0` — no `results.json` was produced (crash, import error, interrupted run).

The score is a diagnostic, not a pass/fail gate. A submission is **accepted** only when
`score == 100` *and* every negative control is detected; the agent may keep retrying until the
attempt budget is exhausted.

Hard override: if a forbidden action (§7) is detected, the attempt scores **0** regardless of the
numbers, because the comparison is then no longer evidence of anything.

## 6. Failure modes the agent will actually hit

| Failure mode | How it shows up | Correct response |
|---|---|---|
| Non-determinism between runs | `verify` fails on some checks that passed before | remove the source (unseeded RNG, dict/set iteration order, wall-clock in a compared field); never widen the tolerance |
| Platform-dependent provenance | `config_sha256` mismatch on Windows but not Linux | normalize newline style before hashing (see `REPRODUCTION.md` §8); never delete the hash check |
| Tolerance seduced into meaninglessness | a real code change produces a tiny numeric shift and still "passes" | check the negative controls (`scripts/score_task.py`); if a control stops being detected, the task is unfalsifiable and must be fixed |
| Timing leaked into the metrics | `duration_ms` differs every run | keep timing out of every compared field; it is informational only |
| Adam update silently degraded | `best.name` flips or loss rises well above the expectation | compare against the paper's Algorithm 1 line by line before touching hyper-parameters |
| Data/search-space change instead of a bug fix | numbers move toward the expectation because the task got easier | config changes are a *different* experiment: create a new config and new expectations, never edit the recorded pair |
| Environment drift | different Python version, missing module | keep the experiment on the standard library; record the interpreter in `runs/demo/environment.json` |

## 7. Allowed and forbidden actions

**Allowed:** edit `autoresearch/`, `scripts/`, `tests/`, `README.md`, `REPRODUCTION.md`,
`TASK.md`, `Makefile`, CI workflow; add new `examples/*.json` experiments with their own
expectation files; run any command in §3 as often as the budget allows; read the paper.

**Forbidden** (violation ⇒ score 0):

* editing `expected/*.json` to match a wrong result, or deleting/weakening an assertion;
* editing `tests/` to skip or trivialize a check;
* changing the seed, dataset size or epoch budget *inside the recorded experiment* to hit the
  number (a new experiment is allowed; editing the recorded revision is not);
* writing numbers into any report that the run did not produce;
* network access, `pip install`, or downloading datasets during an attempt;
* touching `runs/demo-verified/` by hand — those artifacts must be regenerated by the command;
* publishing credentials, personal data, or third-party client material into the repository.

## 8. Retry protocol

1. Attempt a fix, then run `python scripts/repro.py --skip-tests` (fast loop).
2. Run `python scripts/repro.py` before declaring success; both must agree.
3. Run `python scripts/score_task.py`; success also requires every negative control to be *detected*.
4. Append one line per attempt to `runs/attempts.md` (git-ignored), starting from the template in
   `docs/attempt-log-template.md`: attempt number, command, exit code, score, first failing
   assertion, what changed.
5. After 5 failed attempts, stop and report the blocking assertion verbatim. Do not relax the
   acceptance criteria to escape the loop — that converts a research task into a metric-hacking
   exercise, and the negative controls exist precisely to catch it.

## 9. Task variants (same harness, different difficulty)

The AutoResearch framing wants tasks an agent can *attempt repeatedly and improve on*, so the
family below reuses the same scorer at increasing difficulty:

| Variant | Initial state given to the agent | Extra requirement |
|---|---|---|
| **T-ADAM-01A — verify** | this repository as shipped | make one command pass; explain each number |
| **T-ADAM-01B — implement** | `model.py` Adam branch replaced by a stub that raises | implement Algorithm 1 from the paper; pass the same expectations, **as a drop-in replacement** (see the note below) |
| **T-ADAM-01C — ablate** | this repository as shipped | add one new ablation config with its own expectation file and justify the predicted direction |
| **T-ADAM-01D — recover** | one negative control already applied | find the defect from the failing assertion alone; the scorer must return to 100 |

T-ADAM-01D is directly supported today: `python scripts/score_task.py` shows exactly how a mutated
implementation scores (82.4/100), so the agent gets a gradient to climb instead of a binary verdict.

**Note for T-ADAM-01B: "drop-in" is part of the requirement, and it was learned the hard way.** The
harness's negative controls work by replacing *text* in `autoresearch/optimizers.py`. An implementation
that is numerically correct but leaves the original branch behind as dead code satisfies every fragment
check while the code that actually runs is untouched — the controls then report that a broken
implementation passed, and the harness has silently lost its teeth. A first attempt at this variant did
exactly that: it scored 100/100 on the pinned numbers and two of the four controls came back *missed*.
The accepted solution therefore has to keep the mutation points live, which `scripts/task_variants.py`
verifies behaviourally (apply the fragments, run the main suite, require the pinned numbers to move)
rather than by substring search. `REPRODUCTION.md` §5.16 and `docs/defect-family.md` case 5 have the
same rule in general form: a check that can be satisfied without changing what runs is not a check.

## 10. What must stay human

This task never requires, and the agent must never perform: account creation, DOI/Zenodo
registration, arXiv endorsement, journal submission, or job application. Those are recorded as
Next Checks in the project knowledge base instead. Agent output is limited to code, data,
configuration, reports and scores inside this repository.

## 11. Natural next tasks (not part of T-ADAM-01)

1. **T-ADAM-02** — replace the synthetic task with a real paper implementation (PyTorch adapter)
   while keeping the offline standard-library path reproducible.
2. **T-ADAM-03** — measure convergence *speed* (loss-vs-step curves, steps to a target loss) so the
   paper's "faster convergence" claim can be tested rather than approximated.
3. **T-ADAM-04** — budget-aware search: let an agent propose hyper-parameters under a fixed compute
   budget, and score it on the same expected-numbers contract plus a wall-clock cap.
