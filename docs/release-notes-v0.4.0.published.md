This release adds a second 2024 paper to the harness — Schedule-Free learning — and, because a
single-model answer is not an answer, runs its comparison on **both** model families. The most
interesting thing that came out of it is that the direction of the comparison flips between them.

### What is new

- **Schedule-Free AdamW and schedule-free SGD** (`autoresearch/optimizers.py`), transliterated from
  `facebookresearch/schedule_free` (Apache-2.0) and cross-checked step by step against a literal
  re-implementation of that reference in `tests/test_schedule_free.py`.
- **The averaged sequence is the evaluated model.** Schedule-free keeps two iterates: the point the
  update moves (`z`, interpolated into `y` where gradients are taken) and the running average `x`.
  The reference implementation evaluates at `x`, so this repository reports `x` too — in both trainers,
  through `optimizers.eval_params()` — because measuring at the training point would flatter the method
  in any comparison against a scheduled baseline.
- **A comparison whose baseline is actually tuned.** The claim under test is comparative ("at worst
  matches a tuned cosine decay"), so the cosine arm is swept over both its learning rate and its
  minimum-learning-rate factor (21 trials on the logistic head, 15 on the MLP), and a constant
  learning rate is included because that is what schedule-free replaces.
- **A fourth negative control**: mutating the averaging step to `x = z` (schedule-free without the
  average) must fail the pinned expectations, like the other three.
- 39 unit tests, seven experiment suites, 171 asserted checks.

### Results

Ten seeds, 200-epoch budget, target 0.148, every arm tuned for the model it runs on:

| comparison | logistic head | two-layer MLP | stable? |
|---|---|---|---|
| schedule-free AdamW vs tuned cosine | tuned cosine wins **10/10** (by 0.00032) | **schedule-free wins 9/10** (by 0.00128) | **no — the direction flips** |
| constant learning rate vs schedule-free | constant wins 7/10 | constant wins 9/10 | **yes** |
| epochs to target | 154 vs 80 (schedule-free slower) | 11 vs 23 (schedule-free faster) | no — target-position dependent |

The paper's weak claim — no schedule needed, and the method at worst matches a tuned one — survives
both runs. Its strong claim ("typically out-performs") does not: the sign of the comparison depends on
the model, and in the model where schedule-free wins, a plain constant learning rate still wins by
more. The honest reading is that at this budget a decay is not needed at all, so a method whose selling
point is removing the need for one has nothing to gain here — which says something about this regime,
not about the long non-convex training the paper is about.

**Reporting only one of the two models would have produced a confident and wrong headline in either
direction**, which is why both are in the repository, in the paper card and in `REPRODUCTION.md` §5.7–5.8.

### Fixed and hardened

- Trial configs now inherit the experiment's `seed`, and `tests/test_seed_contract.py` asserts the
  contract (the seed is an inherited key; every suite's trials carry it; ten seeds produce ten distinct
  seeds; the MLP initialises differently per seed). A "10-seed" run that only varied the data split
  looked like a measurement without being one.
- The MLP trainer now tracks the evaluation point separately from the training point, so
  schedule-free rules are evaluated at the averaged sequence there as well; the non-schedule-free MLP
  suites are unchanged and still verify.

### Known limitations

Mechanism-level reproduction: no number from any paper's tables is claimed. Full-batch gradients, one
dataset family, one hidden-layer size, ten seeds and no formal significance test. The schedule-free
comparison inherits the earlier caveat that a 200-epoch run on a small task is the regime where
schedules matter least, and the speed metric demonstrably depends on where the target sits relative to
the converged floors — both regimes are committed so the analysis can be redone.

### Verify it yourself

```bash
python scripts/repro.py        # seven suites, 171 asserted checks, exit 0
python scripts/score_task.py   # 100/100, and all four negative controls must be detected
python -m unittest discover -s tests -v
```

Archived on Zenodo; the concept DOI is 10.5281/zenodo.23003610 and each version has its own version DOI.
