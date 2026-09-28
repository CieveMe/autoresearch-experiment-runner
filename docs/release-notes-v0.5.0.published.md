This release finishes turning the repository's speed numbers into statements with explicit scope: the
threshold they were measured at, the model family, and now the capacity. It also adds two more
capacities to the cross-paper check, which produced one new positive result and no retractions.

### What is new

- **Threshold curves** (`scripts/threshold_curve.py`, committed output in `runs/threshold-curves/`).
  Every "who is fastest" number in the report is an `epochs_to_target`, and that number is a function
  of the threshold it is measured at. The tool reads the committed loss curves — nothing is re-trained —
  and reports a 13-point threshold grid per suite: who arrives first, who never arrives, and where the
  ranking changes, with a CSV and an SVG that draws the suite's pinned threshold.
- **Two more capacities**, `[32]` and a two-layer `[8,8]`, alongside the existing `[8]` and the logistic
  head. Every arm is retuned for the model it runs on (21-trial sweeps each), 200 epochs, ten seeds.
- Nine suites, 229 asserted checks, 45 unit tests, four negative controls.

### Results

**The threshold curves changed the scope of four earlier claims, not their content.** Four of six
suites have a threshold-dependent winner, and three of those have their *pinned* threshold on the
fragile side of a crossing: `optimizers` (pinned 0.16, crossing 0.1634), `optimizers-mlp` (pinned 0.147,
crossing 0.1422) and `schedule-free-mlp` (pinned 0.148, crossing 0.1434). Two suites are stable and the
tool says so (`schedule-free` on the logistic head has the constant rate winning at all thirteen
thresholds; `ademamix-mlp` is stable across its own range).

**The schedule-free "direction flip" is a threshold and architecture effect, not a model-quality
statement.** The crossing at 0.1434 on the MLP means the pinned threshold sits where schedule-free looks
fast; tighter thresholds favour the constant-rate arm, which converges deeper. On the logistic head the
crossing sits on the other side of its pinned threshold. "Schedule-free beat the cosine on one model and
lost on the other" is therefore really "two arms cross at a threshold, and the two model families have
different floors and different crossings".

**The capacity check produced one new result and no retractions.**

| claim | logistic | MLP `[8]` | MLP `[32]` | MLP `[8,8]` |
|---|---|---|---|---|
| AdEMAMix has no advantage over AdamW | no advantage | no advantage | 1/10 seeds better, worse on test loss | 1/10 seeds better, worse on test loss |
| schedule-free beats a tuned cosine | loses 10/10 | wins 9/10 | wins 8/10 | wins 8/10 |
| AdaGrad competitive on final test loss | no | no | **9/10 wins** | **7/10 wins, 10/10 better than cosine** |
| a constant learning rate wins | yes | yes | no | no |

Two claims that earlier looked general turned out to be capacity-scoped and are now labelled that way:
the constant learning rate's dominance, and AdaGrad's standing. The AdEMAMix verdict is now the most
robust negative result in the repository: no advantage at any capacity, on either model family, and in
the ten-seed paired tests.

**A metric effect worth naming**: at `[8,8]` the arms with the lowest *training* loss (adam, constant
AdamW, AdEMAMix) have the worst *test* loss, while schedule-free has the best test loss. A suite that
ranked by training loss would invert the answer at that capacity, so both numbers are pinned and
reported.

### Known limitations

Mechanism-level reproduction: no number from any paper's tables is claimed. Full-batch gradients, one
dataset family, four model configurations and ten seeds with test-loss standard deviations around
0.02–0.06 — enough to separate 0.13 from 0.19, not enough to resolve a 0.0003 difference. The
crossing points are located on seed-7 curves only; whether the crossings themselves are stable across
seeds is the next open question and is listed in `TODO.md`.

### Verify it yourself

```bash
python scripts/repro.py        # nine suites, 229 asserted checks, exit 0
make thresholds                # the threshold curves, from the committed loss curves
python scripts/score_task.py   # 100/100, four negative controls must be detected
python -m unittest discover -s tests -v
```

Archived on Zenodo; the concept DOI is 10.5281/zenodo.23003610 and each version has its own version DOI.
