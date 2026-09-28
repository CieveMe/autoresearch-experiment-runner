# The defect family: three ways a number came from the tooling instead of the experiment

This is a named section, not an appendix: it is the part of this repository a reviewer should read
first, because every empirical claim elsewhere depends on it. Three defects were found here, all of the
same kind — **a reported number was produced by the harness rather than by the experiment** — and each
one was caught by a *different* mechanical check. That is the argument for building those checks before
trusting any result.

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

## What the three cases have in common

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

None of the three would have been caught by looking harder at the *results*: all three produced tables
that looked reasonable. What caught them was a check on the *machinery* — a declaration of direction, a
contract on the seed, and a negative control for the tie. That is the pattern this repository
recommends: for every derived number, assert the property that makes it a number about the experiment
rather than about the code, and prefer a check that fails loudly when a new input arrives without a
declaration.

## How to apply it to a new experiment

1. Name the metric and declare its direction in one place.
2. If the experiment claims N seeds, assert that N distinct seeds reach every layer that has a random
   state.
3. If the output contains a ranking, assert what happens when two candidates are equal.
4. Keep one negative control per new method: a deliberately broken implementation that the pinned
   expectations must reject (see `scripts/score_task.py`, four controls at the time of writing).
