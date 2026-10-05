# A3 data pack: the two things the methods paper asks this repository for

Prepared on request (`§5.16`'s headline wording, and the seven-case appendix table). Everything here is
quoted or computed from committed artifacts; nothing new was run to produce it, and every row says how to
check it. If a number below disagrees with the artifact, **the artifact is right and this file is stale**
— which is the rule the family in `docs/defect-family.md` exists to enforce.

Regenerate the two sources:

```bash
make stats      # runs/paired-tests/paired-tests.{md,json}
make figures    # runs/figures/*.svg + runs/figures/stability.csv
```

## 1. §5.16 headline wording (verbatim, `REPRODUCTION.md` §5.16)

> **The conservative screen first.** Across all 79 comparisons, **not one** survives a family-wise
> correction (smallest adjusted p = 0.1543).

> **1. The schedule-free result is established at exactly one suite, and it is the deepest one.**
> `capacity-h16x16` wins 10/10 seeds, median difference −0.02692 [−0.04536, −0.01102], d_z = −1.20,
> adjusted p = 0.0195 — the one comparison in the family that survives its own family correction. Two
> more have a raw p ≤ 0.05 and do not survive it (`capacity-h64`: 0.0098 → 0.1934; `init-he`: 0.0039 →
> 0.1934). Everything else … is **no evidence of a difference at this budget**, with MDE between 0.0013
> and 0.0094.

> **2. The AdEMAMix verdict is non-detection with uncertainty, not equality.**
> No comparison in that family survives (smallest adjusted p = 0.2363, and that one,
> `init-he` with a raw p of 0.0215, has AdEMAMix *worse*). A null hypothesis cannot be confirmed by a
> test that fails to reject, so "AdEMAMix has no advantage" is not something these ten seeds can
> establish.

The 2026-10-05 internal review clarified the interpretation in §5.16: an approximate MDE is a
design-sensitivity quantity, not a confidence bound inferred from a non-significant result. Quote
effect estimates and their pointwise intervals alongside non-detection; do not infer equivalence or
certify that every effect larger than MDE is absent. The calculation is not an 80%-power guarantee
for the exact-test/Holm procedure. No statistic or pin changed.

**Numbers behind the headline** (`runs/paired-tests/paired-tests.json`, field paths given so a reviewer
can check rather than trust):

| quantity | value | where |
|---|---:|---|
| comparisons in the corpus | 79 | `comparisons_tested` |
| surviving Holm within the declared family, schedule-free | 1 of 10 | `claim_families[0].survivors` / `.members` |
| surviving Holm within the declared family, AdEMAMix | 0 of 11 | `claim_families[1].survivors` / `.members` |
| smallest raw / adjusted p, schedule-free family | 0.0020 / 0.0195 | `claim_families[0].smallest_*_p` |
| smallest raw / adjusted p, AdEMAMix family | 0.0215 / 0.2363 | `claim_families[1].smallest_*_p` |
| comparisons surviving the all-79 screen | 0 | computed: `holm_p <= 0.05` over `comparisons` |

**Known drift, already corrected in the prose:** §5.16 and the v0.10.0 release body said "78"; the
corpus became 79 when the T-ADAM-01C ablation suite was registered. The claim is unchanged, the smallest
adjusted p is 0.1543 (rounded to 0.15 in that body). `make stats` owns the number.

**The wording rule, if the draft quotes it:** a test that fails to reject is reported as *no evidence of a
difference at this budget*, **never** as "no difference", and the closed set of allowed verdicts is
enforced in code and tested
(`tests/test_paired_stats.py::test_every_verdict_comes_from_the_closed_set_of_phrasings`).

## 2. The defect family: seven cases, each with the check that caught it

One row per case, `docs/defect-family.md` is the prose, and every check name below was verified against
the tree (`rg -n "def <name>" tests`).

| # | what the number/verdict was | what it should have been | check that catches it | test file |
|---|---|---|---|---|
| 1 | a ranking in the wrong direction | a ranking in the declared direction | `test_every_metric_the_runner_can_rank_has_a_known_direction` | `tests/test_metric_direction.py:12` |
| 2 | ten runs, one initialisation | ten runs, ten seeds | `test_a_multi_seed_sweep_produces_distinct_seeds_not_a_fixed_value` | `tests/test_seed_contract.py:41` |
| 3 | a leader produced by alphabetical order | a tie | `test_identical_curves_have_no_crossing` | `tests/test_threshold_curve.py:97` |
| 4 | gradients of a deep network doubled by a refactor | gradients of the same network as before | `test_gradients_match_numerical_differences` (two depths) | `tests/test_ademamix.py:78` |
| 5 | a table column assembled by hand, not reproducible under its own heading | every statistic produced by a function with its definition named | `test_the_noise_statistics_are_reproducible_and_disagree_with_the_old_table` | `tests/test_figures.py:80` |
| 6a | four "detected" verdicts produced by fragments that had moved into dead code | a control that demonstrably changes the code that runs | `test_every_control_fragment_changes_the_numbers_it_mutates` | `tests/test_harness.py:117` |
| 6b | "exit 1, two controls missed" produced by a copier that dropped the inputs | a scored copy isomorphic to the repository it claims to score | `test_the_scored_copy_can_run_the_repositorys_own_tests` | `tests/test_harness.py:128` |
| 7 | a green local run and a red CI run from the same code | a tolerance at or above the quantity's measured cross-platform reproducibility | `test_a_trial_tolerance_widens_that_trial_and_nothing_else` | `tests/test_harness.py` (see `rg -n`) |

**How each case was found** (the column a reviewer will like, because it is where the cases differ):

| # | found by |
|---|---|
| 1, 3 | a purpose-built check |
| 2 | re-reading a contract |
| 4 | a pinned expectation of an *unrelated* suite failing on a fresh run |
| 5 | drawing a figure that disagreed with a published column |
| 6a | running the T-ADAM-01B variant and seeing 100/100 next to two missed controls |
| 6b | the same tree scoring `exit 0` with `--skip-controls` and `exit 1` with them |
| 7 | somebody else's machine — the public CI — which is the one detector this project cannot run locally |

**The one-sentence form of each generalisation** (from `docs/defect-family.md`):

1. every metric declares its direction, in one place;
2. a sweep that claims N seeds must show that N distinct seeds reached the model;
3. a tie is a result, and a tie-break is a choice that has to be visible;
4. a check that covers one shape covers one shape;
5. a number typed into a table has no generator;
6. **a check that can be satisfied without changing what runs is not a check** (6a), and a copy is not
   the thing it claims to score (6b);
7. a tolerance below the quantity's own reproducibility measures the machine, not the code.

**Case 7's numbers, for §6's platform section** (full table and mechanism in `REPRODUCTION.md` §5.17):

| suite | pinned (Windows) | Linux | difference | one-ULP probe, same machine |
|---|---:|---:|---:|---:|
| `schedule-free-mlp` | 0.12506323 | 0.12526376 | +2.01e-4 | +2.02e-4 |
| `norm-layernorm` | 0.12414847 | 0.12409491 | −5.36e-5 | **−9.78e-4** |
| `init-he` | 0.12610458 | 0.12612148 | +1.69e-5 | +1.30e-5 |
| `capacity-h32` | 0.12452343 | 0.12452196 | −1.47e-6 | −2.50e-5 |
| every other arm, every suite | — | identical | 0 | **0.000e+00** |

Chosen tolerance: `loss_abs = 0.005` for that one trial in the twelve files that pin the arm — five times
the largest movement seen by either method — with every other pin left at 1e-6. The honest sentence for a
paper is the one in §5.17: this arm's *test loss* is reproducible only to about 1e-3 across `libm` builds,
so the repository pins it coarsely and pins its integer speed and its accuracy exactly.

**The family note in miniature** (worth one sentence in §5, not a case): the release checklist's own
line telling the releaser to confirm three files "all say `0.2.0`" became false the moment those files
were bumped; §5.16's "78 comparisons" outlived the corpus reaching 79. Same disease — one fact maintained
in two places — and the same repair: name the artifact that owns the number and quote it from there.

**Third member, and the strongest one to cite, because the repair itself only spread to one place.** That
"78" lived in four files — `README.md`, `TODO.md`, `CHANGELOG.md` and a comment in
`scripts/paired_stats.py`, the producer itself — and when the corpus grew to 79 exactly one of them was
corrected, which is as far as somebody remembered to look. The repairs: the two live documents now
**point at the artifact instead of restating the count**, the producer's comment carries no numbers, the
CHANGELOG keeps its text as a historical record, and a check enforces the rule from now on
(`test_live_documents_do_not_hard_code_the_corpus_size`, plus companions that the artifact owns the count
and that the live documents still point at it). Writing that guard immediately tripped case 6b's guard,
because the artifact it reads was not copied into the scored tree — the family checking itself.
