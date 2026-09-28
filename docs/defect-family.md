# The defect family: six ways a number came from something other than the experiment

This is a named section, not an appendix: it is the part of this repository a reviewer should read
first, because every empirical claim elsewhere depends on it. Six defects were found here, all of the
same kind — **a reported number, or a reported verdict, was produced by something other than the
experiment: the harness, the person assembling the table, or the checker that stopped checking** — and
each one was caught by a *different* mechanical check. That is the argument for building those checks
before trusting any result.

## Case 1 — the metric direction was inverted

**Symptom.** The seed sweep reported RMSProp as the per-seed winner for `epochs_to_target` while the
per-seed data plainly showed AdaGrad.

**Cause.** The set of metrics where "smaller is better" existed in two copies. `epochs_to_target` was
added to the runner's copy and not to the seed sweep's, so the sweep ranked the new metric descending.
Nothing crashed; the table simply answered the opposite question.

**Fix.** One definition (`LOWER_IS_BETTER_METRICS` in `autoresearch/runner.py`) and one helper
(`is_lower_is_better`) used by the runner, the sweep and the one-command entry.

**Check that catches it.** `tests/test_metric_direction.py`:

* `test_every_metric_the_runner_can_rank_has_a_known_direction` — fails when a new metric is added
  without declaring its direction, which is exactly how the bug entered.
* `test_epochs_to_target_is_ranked_ascending` — pins the specific metric.

**Generalisation.** Any list that is duplicated across modules is a place where two components can
disagree about what a number means. The check has to be "every metric declares its direction", not "the
known metrics are fine".

## Case 2 — the seed reached the data split but not the model

**Symptom.** None. The ten-seed MLP results looked plausible; the spread across seeds was simply smaller
than it should have been.

**Cause.** Trial configs did not inherit the experiment's `seed`. The data generator was seeded from the
top-level config, so every seed produced a different split — but the MLP initialised from
`config.get("init_seed", config.get("seed", 0))` evaluated on the *trial* config, which had no `seed`.
Every run in a "ten-seed" sweep started from the same weights.

**Fix.** `seed` is now an inherited trial key (`TRIAL_INHERITED_KEYS`), and the merge was extracted into
`runner.merge_trial_config()` so the contract can be asserted directly instead of described in a
comment.

**Check that catches it.** `tests/test_seed_contract.py`:

* `test_seed_is_an_inherited_key`;
* `test_every_suite_trial_receives_the_experiment_seed` — for every suite in the runner;
* `test_a_multi_seed_sweep_produces_distinct_seeds_not_a_fixed_value` — ten seeds must be ten seeds;
* `test_mlp_initialisation_follows_the_seed` — two seeds must give different initial weights.

**Generalisation.** A sweep that claims N seeds must be able to *show* that N distinct seeds reached the
model. "It ran ten times" and "it measured ten things" are different statements, and only the second is
a result.

## Case 3 — ties were resolved alphabetically

**Symptom.** The threshold table reported that the lead "passes to `adam` at 0.1417" for the `[32]`
capacity suite. The published v0.5.0 release notes quote that sentence.

**Cause.** `scripts/threshold_curve.py` selected the fastest arm with `min()` over `(epoch, name)`
tuples. When two arms reached a threshold on the same epoch, the tuple's second element decided — i.e.
alphabetical order did. In the affected region `adam`, `adamw_constant` and `ademamix` were **tied**
(identical epochs at every threshold from 0.1417 upwards), so the "crossing" was manufactured entirely by
the sort key, in two separate places in the same file.

**Fix.** Ties are reported explicitly (`tie: adam, adamw_constant, ademamix`), the crossing detector
skips tied thresholds instead of breaking them, and the pinned-threshold check in the per-seed analysis
records `tie` rather than picking a winner.

**Check that catches it.** `tests/test_threshold_curve.py`:

* `test_identical_arms_are_reported_as_a_tie_not_a_winner`;
* `test_identical_curves_have_no_crossing` — the direct negative control for this bug;
* `test_a_real_crossing_is_still_found` — the fix must not disable the detector.

**Generalisation.** Any ranking computed from a key that includes an identifier can be decided by that
identifier. Ties are a result; a tie-break is a choice, and a choice has to be visible in the output.

## Case 4 — a refactor doubled the gradients of deep networks

**Symptom.** After adding configurable hidden activations, the pinned numbers of the two-hidden-layer
capacity suite stopped reproducing: the test losses moved by 1e-6 to 8e-4, in a code path whose
arithmetic was supposed to be unchanged.

**Cause.** A patch that was meant to add one derivative expression also re-indented the block that
accumulates the gradients, moving it *inside* the loop that computes the deltas. For a network with two
hidden layers that accumulation therefore ran twice, doubling every gradient; for a network with one
hidden layer the loop ran once and the results stayed correct. The existing finite-difference test used a
single hidden layer, so it passed while the deep path was wrong.

**How it was found.** Not by the tests: by the pinned expectations of a *deep* suite failing on a fresh
run. The diagnosis was then mechanical — an independent transliteration of the pre-refactor arithmetic
showed exactly a factor of two at the output layer, and a finite-difference check on a two-hidden-layer
net confirmed it (max |numerical − analytic| = 0.245 before the fix, 9.2 × 10⁻¹¹ after).

**Fix.** Accumulate once per row, after every delta is known, and **extend the gradient check to two
depths**: `test_gradients_match_numerical_differences` now runs `[3]` and `[3, 3]` for each of the three
activations, six checks instead of one.

**Check that catches it.** `tests/test_ademamix.py`:

* `test_gradients_match_numerical_differences` (parameterised over depth and activation);

plus, indirectly, every pinned expectation belonging to a two-hidden-layer suite.

**Generalisation.** A test that covers one shape covers one shape. When a dimension of the model is
varying (depth, activation, width), the check has to vary with it, and a refactor of an inner loop is the
kind of change that is invisible in a diff review but visible in a number.

| case | what the number was | what it should have been | check | test file |
|---|---|---|---|---|
| 1 | a ranking in the wrong direction | a ranking in the declared direction | `test_every_metric_the_runner_can_rank_has_a_known_direction` | `tests/test_metric_direction.py` |
| 2 | ten runs, one initialisation | ten runs, ten seeds | `test_a_multi_seed_sweep_produces_distinct_seeds_not_a_fixed_value` | `tests/test_seed_contract.py` |
| 3 | a leader produced by alphabetical order | a tie | `test_identical_curves_have_no_crossing` | `tests/test_threshold_curve.py` |
| 4 | gradients of a deep network doubled by a refactor | gradients of the same network as before | `test_gradients_match_numerical_differences` (two depths) | `tests/test_ademamix.py` |
| 5 | a table column assembled by hand, not reproducible under its own heading | every statistic produced by a function with its definition named | `test_the_noise_statistics_are_reproducible_and_disagree_with_the_old_table` | `tests/test_figures.py` |
| 6a | four "detected" verdicts produced by fragments that had moved into dead code | a control that demonstrably changes the code that runs | `test_every_control_fragment_changes_the_numbers_it_mutates` | `tests/test_harness.py` |
| 6b | a score of "exit 1, two controls missed" produced by a copier that dropped the inputs | a scored copy that is isomorphic to the repository it claims to score | `test_the_scored_copy_can_run_the_repositorys_own_tests` | `tests/test_harness.py` |

## Case 5 — a table column that came from the author, not from a definition

**Symptom.** §5.11's "finding 7" and §5.13's H5 made a claim the whole report leaned on: *a suite's
per-seed noise level predicts whether its fixed-threshold ranking reproduces across ten seeds.* The
supporting column was headed "test-loss σ of the best arm".

**Cause.** Nobody recomputed that column. When `scripts/figures.py` was written it computed the same
quantity from the committed files and got different numbers for five of the ten suites. The values turn
out to belong to *different arms in different rows*: §5.13 reports 0.0646 for `capacity-h8x8`, which is
`adamw_constant`'s σ (the suite's best arm is `adagrad`, σ = 0.02271), and 0.0381 for `capacity-h16x16`,
which is `adagrad`'s σ (the best arm is `schedule-free`, 0.03697). There is no single definition under
which the column is correct.

**How it was found.** Not by a test — by drawing the figure. The first version of the noise/stability
plot put every labelled suite in a scatter and was unreadable, so it was redrawn as one row per suite
ordered by noise; the order disagreed with the published table, and checking one row was enough to see
the column could not be reproduced.

**Consequence.** The correlation does not survive the audit. `optimizers-mlp` has the second-lowest noise
in the corpus (0.02019) and **five** different winners across ten seeds; the two activation suites sit at
0.0217 and have **one** winner in all ten. That is a non-monotone relationship, and §5.11's finding 7,
§5.13's H5 and §5.15's N4 are corrected accordingly in place, with the correction recorded in the next
release body (`v0.9.0` is already published and is not rewritten).

**Check that catches it.** `tests/test_figures.py`:

* `test_the_noise_statistics_are_reproducible_and_disagree_with_the_old_table` — pins both
  counterexamples and the `capacity-h8x8` value that the old column got wrong;
* `test_committed_figures_match_the_generator` — a committed figure that no longer matches the data
  fails the suite, the same way a stale pinned number does.

**Fix.** Every noise statistic is now emitted by code with its definition written next to it
(`runs/figures/stability.csv`: `sigma_best`, `sigma_modal`, `sigma_median`, winner counts and the modal
winner set), and a claim about them has to name which one it means.

**Generalisation.** A number typed into a table is a number with no generator. Every reported statistic
needs a function that produces it, a definition in prose next to it, and a test that fails when the two
drift apart — otherwise the number is a memory of the run, not a result of it. This case is also the
argument for drawing the figures early rather than last: the plot disagreed with the table, and the
table was wrong.

## Case 6 — the checker stopped checking (two members, found by running the task)

The first five cases are about a *number*. This one is about a *verdict*: the harness went on reporting
success while it had stopped testing anything. It has two members, both found while running the
T-ADAM-01 variants for real (`runs/task-runs/`), and they are numbered together because they share the
mechanism — the verdict was produced by the machinery around the experiment rather than by the
experiment — and the same repair shape: make the guard demonstrate its own liveness.

### 6a — four controls "detected" by fragments that had moved into dead code

**Symptom.** T-ADAM-01B's second attempt implemented Adam correctly, passed every pinned expectation and
scored **100/100** — while **two of the four negative controls came back `missed`**. A harness whose
controls report that a broken implementation passed has silently lost its teeth, and the failure showed up
on exactly the number everybody reads.

**Cause.** The implementation left the original branch behind as dead code. The controls mutate by
*replacing text*, so every fragment still matched, the replacements landed in code that never runs, and
the mutations had no effect. The repository's own guard,
`test_every_control_fragment_still_exists_in_the_source_it_names`, checks that the fragment is *present* —
which dead code satisfies.

**How it was found.** By running the variant: a score of 100/100 with two controls missed is not
ambiguous, but nothing short of executing the loop produces it. The static check was green the whole time.

**Check that catches it.** `tests/test_harness.py`:

* `test_every_control_fragment_changes_the_numbers_it_mutates` — the behavioural version: mutate a
  throwaway copy, run one six-epoch experiment with the optimizer the control targets, and require the
  loss to move.

**Fix.** The liveness probe also runs after every attempt of the T-ADAM-01B variant, and the variant's
acceptance criterion is no longer the score alone: pinned 100/100 **and** submission `exit 0` **and** every
control detected. `TASK.md` §9 now states that the implementation must stay drop-in at the mutation
points.

### 6b — "exit 1, two controls missed" produced by a copier that dropped the inputs

**Symptom.** A perfect submission reported `exit 1`, and the same two controls above were reported missed
in every scored copy — but for a completely different reason.

**Cause.** The scorer copies the repository before mutating it, and its copy filter kept only
`runs/*-verified` under `runs/`. The paired-statistics and figure tests read the committed per-seed
sweeps (`runs/seed-sweep-*/seed-*/results.json`), which were neither committed nor copied. So the copy was
not the repository: tests failed on missing inputs, the exit code was 1, and the control verdicts
described the copy rather than the submission.

**How it was found.** The two members were distinguished by a single experiment: the same tree scored
`exit 0` with `--skip-controls` and `exit 1` with them, which located the fault in the harness rather than
in the submission. (The same class of bug would have hit any fresh clone: the data was gitignored.)

**Check that catches it.** `tests/test_harness.py`:

* `test_the_scored_copy_can_run_the_repositorys_own_tests` — build the copy the scorer builds and require
  the repository's own suite to pass inside it.

**Fix.** The 7.4 MB of per-seed sweeps are committed, and the copy filter keeps them (`scripts/score_task.py`).

**Generalisation for the pair.** A guard has to be able to show that it is live: presence of a fragment is
not liveness of a mutation, and a copy is not the thing it claims to score. Both members were invisible to
static checks and obvious the moment the machinery was executed end to end, which is the same lesson as
case 5 — the audit has to be run, not asserted.

## What the six cases have in common

None of the six would have been caught by looking harder at the *results*: all six produced tables, or
verdicts, that looked reasonable. What caught them was a check on the *machinery* — a declaration of
direction, a contract on the seed, a negative control for the tie, a gradient check that varies with the
shape of the model, a generator for every statistic in a table, and a liveness probe for every guard.
That is the pattern this repository recommends: for every derived number, assert the property that makes
it a number about the experiment rather than about the code or the author, and prefer a check that fails
loudly when a new input arrives without a declaration.

The six also differ in *how* they were found, which is the more useful observation. Cases 1 and 3 were
caught by a purpose-built check; case 2 was caught by re-reading a contract; case 4 was caught by a
pinned expectation of an *unrelated* suite failing; case 5 was caught by drawing a figure; case 6 was
caught by running the task end to end. Cases 4–6 required nobody to have anticipated the problem, which
is why the pinned numbers, the plots and an actual run of the harness are a safety net and not just
regression tests.

## How to apply it to a new experiment

1. Name the metric and declare its direction in one place.
2. If the experiment claims N seeds, assert that N distinct seeds reach every layer that has a random
   state.
3. If the output contains a ranking, assert what happens when two candidates are equal.
4. Keep one negative control per new method: a deliberately broken implementation that the pinned
   expectations must reject (see `scripts/score_task.py`, four controls at the time of writing).
5. Never type a statistic into a table. Emit it from a function with the definition written next to it,
   and let a test compare the two — a number with no generator is a memory of the run, not a result.
6. Draw the figures before the prose. Case 5 was found by a plot disagreeing with a published column,
   and a plot is cheap to make once the numbers already exist.
7. Make every guard demonstrate its own liveness (case 6a). A mutation that lands in dead code, or a
   fragment that is only *present*, produces a green check over an untested implementation.
8. Make anything the harness copies isomorphic to the repository it claims to score (case 6b), and prove
   it by running the repository's own suite inside the copy.
9. Run the task itself. Cases 4, 5 and 6 were all found by executing the machinery rather than reading
   it, and none of them was visible to a static check that was already green.
