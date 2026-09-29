This release closes the correction series that started with v0.10.0, and repairs the continuous
integration that the first correction exposed. It is deliberately self-contained: the three corrections
it carries are stated here in full even where an earlier body already carried them, so that a reader of
this version does not have to reconstruct the series from two release notes.

### Correction 1 — the σ correlation (case 5)

v0.7.0 published a table whose column was headed "test-loss σ of the best arm" and a claim resting on it:
that a suite's per-seed noise predicts whether its fixed-threshold ranking reproduces across ten seeds.
The column was assembled by hand and is not reproducible under its own heading — five of its ten rows
carry a *different arm's* σ (0.0646 for `capacity-h8x8` is `adamw_constant`'s, while the suite's best arm
is `adagrad` at 0.02271). Recomputed from the committed files under one stated definition, the
relationship is not monotone: `optimizers-mlp` has the second-lowest noise in the corpus (0.02019) and
**five** different winners, while the two activation suites sit at 0.0217 with **one** each.

So §5.11's finding 7 and §5.13's H5 are withdrawn, and with them the second half of §5.15's N4 — the part
v0.9.0 stated as "refuted on the mechanism, **confirmed on the correlation**". What survives is narrower
and still useful: *the per-seed noise of a suite is measurable, and on this corpus it does not predict
whether its fixed-threshold ranking reproduces*. The audited table is `runs/figures/stability.csv`,
emitted by `scripts/figures.py` and pinned by
`tests/test_figures.py::test_the_noise_statistics_are_reproducible_and_disagree_with_the_old_table`.
This was first carried in v0.10.0's body; it is restated here because this release is the one that closes
the series.

### Correction 2 — the checker that stopped checking, and two copies that were not the repository (case 6)

**6a.** Running the T-ADAM-01B task variant produced the sharpest failure of the series: an implementation
that was numerically correct, passed every pinned expectation and scored **100/100** had left the original
branch behind as dead code — and the harness's four negative controls, which mutate by replacing *text*,
silently stopped detecting anything. Two of the four came back `missed`; the repository's own guard
checked only that the fragments were *present*, which dead code satisfies. The guard is now behavioural
(`test_every_control_fragment_changes_the_numbers_it_mutates`), and the variant's acceptance criterion
requires pinned 100/100 **and** a clean exit **and** all four controls detected.

**6b.** The same lesson applied to copies of the repository, twice. First, the scorer's own copy dropped
the committed per-seed sweeps, so a perfect submission reported `exit 1` and two controls were reported
missed — a verdict about the copy rather than the submission
(`test_the_scored_copy_can_run_the_repositorys_own_tests`). Then, after the tolerance below was repaired
and the CI's `python 3.10` job went green, the `docker` job was *still* red because the image ran
`scripts/repro.py` — which ends by running the repository's own suite — without ever carrying `TODO.md`,
which a document guard reads. The image now copies `TODO.md` and its own build recipe, and a guard derives
the required file list from the test sources and fails if the recipe does not copy one — with a negative
control that proves the guard fails when `TODO.md` is removed from the recipe.

Both members were carried in v0.10.0's body; 6b's second half is new here.

### Correction 3 — one pin was tighter than the thing it pinned, and the CI that showed it (case 7)

The public CI had been failing on every run since `main` #33 — six runs, all three jobs — while the same
commit was green locally. The failing assertion was one expectation:

```
FAIL  trial[schedule_free_adamw].test_loss: expected 0.12506323, got 0.12526376
FAILED: 1 expectation(s) not met in suite `schedule-free-mlp`
```

Every other one of the 474 assertions matched on both platforms. Reproduced in Linux
(`python:3.12-slim`), which gave that number exactly and turned up three more of the same kind
(`norm-layernorm` −5.36e-5, `init-he` +1.69e-5, `capacity-h32` −1.47e-6) — **all four the same arm**.
The mechanism is `libm`, not threading or BLAS (there is none in this path): nudging
`math.exp/sqrt/tanh/erf` by **one ULP** on a single machine moves that arm by up to **9.8e-4** while every
other arm moves by exactly 0.

The repair widens **that one trial's** tolerance to `loss_abs = 0.005` — five times the largest movement
measured by either method — while every other expectation in the same files keeps `1e-6`. The verifier
prints the tolerance it used, and a test pins the scope from both sides. Nothing was deleted or skipped,
and the cost is stated rather than hidden: a regression below 5e-3 in that one arm's final loss is no
longer caught by that expectation, while its integer `epochs_to_target` pin, its accuracy pin and the
schedule-free negative control all remain exact.

The CI work that followed is part of this correction rather than a separate story: the long job was split
into parallel jobs (`scorer`, `sweeps`, `thresholds`, alongside the `repro` matrix and `docker`) without
removing a step or lowering a tier, and superseded runs on a branch are now cancelled
(`concurrency.cancel-in-progress`) so that three quick pushes no longer look like a permanently red
repository. **A cancelled run is not evidence and may not be cited**; what may be cited is the run on a
tag, or the one quoted below. Measurements in §5.17, case 7 in `docs/defect-family.md`, and the gate runs
in `runs/task-runs/FULL-TIER-ci-fix.md`.

### Also carried in this version

* **Metadata hygiene, in two passes.** `pyproject.toml`, `autoresearch/__init__.py`, `CITATION.cff` and
  the README's citation line had all still described version `0.2.0`; the README now names the concept DOI
  as the always-latest one and lists the version DOIs. `.zenodo.json` and the release checklist lost their
  hard-coded version numbers rather than having them refreshed — the duplicated fact was deleted, not
  updated, because that duplication is case 5's disease in miniature. The smallest member of that family
  is recorded too: the checklist's own line telling the releaser to confirm three files "all say `0.2.0`"
  was already false the moment those files were bumped.
* **§5.16's comparison count.** The prose and v0.10.0's body said "78 comparisons"; the artifact says 79,
  because the corpus grew by one when the T-ADAM-01C ablation suite was registered. The claim is
  unaffected and the smallest adjusted p is 0.1543 — but the count is now quoted from `make stats` rather
  than from memory, and a test enforces that the live documents point at the artifact instead of
  restating counts.
* **`docs/a3-data-pack.md`** — the material the methods paper asked this repository for: §5.16's headline
  wording with the field path of every number behind it, the seven-case appendix table with the check name
  and test file for each, how each case was found, and the measured platform-sensitivity table above.
* **`docs/release-corrections-pending.md`** now opens with the citation checklist this body is written
  against, so a later release cannot silently drop one of the three.

### Full-tier verification for this release

```
$ python scripts/score_task.py --tier full
submission score: 100.0/100 (tier=full (all suites)) (474/474 checks, exit 0)
control[no-bias-correction]: detected (score 74.9/100, exit 1)
control[no-adaptive-scaling]: detected (score 77.0/100, exit 1)
control[ademamix-without-slow-ema]: detected (score 94.9/100, exit 1)
control[schedule-free-without-averaging]: detected (score 92.8/100, exit 1)

TASK RESULT: PASS
```

**Provenance, stated plainly: this is the run recorded in the repository, not the run on this tag.**
The body was written and committed before the tag existed, which is what hard rule 1 requires. The
recorded run is the Windows full-tier scorer at commit `0f3ce2f`; the same commit was reproduced under
Linux in a container (`474 checks, 0 failures`, against four failures before the tolerance fix) and
through the CI's own `docker` path on a fresh clone (`RESULT: PASS`), and CI run #39 on `0f3ce2f`
completed with **all three jobs green** — the first fully green run since #12. Run #39 is a branch run,
and branch runs can be cancelled as superseded; tag runs never are.

### Known limitations

Mechanism-level reproduction throughout; no number from any paper's table is claimed. One dataset family,
full-batch gradients, ten seeds, and §5.16 mostly *bounds* what ten seeds can see (the minimal detectable
effect is ≈ 0.99 σ_d). One arm's final loss is pinned only to ≈1e-3 because that is what it reproduces to
across platforms (§5.17). The six scope axes are frozen; further axes only on a reviewer's request. The
version metadata now matches this release.

Archived on Zenodo; the concept DOI is 10.5281/zenodo.23003610 and each version has its own version DOI.
