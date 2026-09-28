# T-ADAM-01C — add one ablation config with its own expectation file, and justify the predicted direction

From `TASK.md` §9. Unlike 01B and 01D this variant is not a loop over a broken tree: it is a
repository change, so it was made here rather than in a throwaway copy.

## What was added

| artefact | what it is |
|---|---|
| `examples/ablation-adam-no-first-moment.json` | the ablation suite: `adam` (β1 = 0.9) against `adam_beta1_0` (β1 = 0), **both at the rate already tuned for Adam** in `examples/optimizers.json` (0.4), 120 epochs, target 0.16 |
| `expected/expected_ablation_adam_no_first_moment.json` | its pinned expectations, with the verdict in the notes |
| `scripts/repro.py` | registered as a suite, so the reproduction contract covers it (`make repro-ablation`) |
| `Makefile` | `repro-ablation`, plus a line in `make verify` |
| `runs/ablation-verified/` | the committed run, the report and the ten-seed summary |

## The prediction, written before the run

Committed in the config's own `hypothesis` field (commit `0c7d7b6`, one commit before the run), so it
can be refuted rather than explained afterwards:

> At the matched, already-tuned rate, removing the first moment (β1 = 0, so the update collapses to
> `g / (sqrt(v̂) + ε)` — a sign-like step) **reaches the target in fewer epochs but ends at a worse
> final test loss** than the default Adam. Reasoning: the sign-like step is larger early, but the
> averaged first moment is the part that survives gradient noise, and on this task the floor has been
> the harder number. Refuted if β1 = 0 is slower to the target, or if it ends at a better test loss.

## Result: the first half is refuted, the second half holds

Seed 7 (the pinned run):

| arm | epochs to 0.16 | test loss | train loss |
|---|---:|---:|---:|
| `adam` (β1 = 0.9) | **33** | **0.12346246** | 0.14443576 |
| `adam_beta1_0` | 61 | 0.12646126 | 0.14676323 |

Ten seeds (`runs/ablation-verified/seed-sweep-summary.md`): `adam` averages **22.6 epochs** and 0.12571
test loss, `adam_beta1_0` averages **41.1 epochs** and 0.12824 — and β1 = 0 is faster in **0/10** seeds
and better on test loss in **0/10**.

Paired test (`runs/paired-tests/paired-tests.md`): 0/10 seeds better, median difference +0.00268
[+0.00113, +0.00342], exact sign and Wilcoxon p = 0.0020 each, d_z = +1.75 — **evidence of a
difference**, and in the direction the prediction got right.

**Verdict: partially refuted.** "The sign-like step is faster" is wrong — it is slower, by a lot, in
every seed. "The averaged first moment is what survives the noise, and losing it costs you the floor" is
right. The first moment is doing work on both axes here, which is a more useful statement than the
prediction it replaced.

## What this shows about the task contract

The point of T-ADAM-01C is not that the ablation found something; it is that **a candidate can be scored
on a prediction it got wrong**. The config, its expectation file and its verdict all live in the same
contract as every other suite, the pinned numbers are re-derived by `make repro-ablation`, and the wrong
half of the prediction is written down instead of deleted.

## Limitations, stated rather than implied

* **Matched rate by design.** Both arms use the rate tuned for Adam, so this is a comparison about β1
  alone, not about each arm's best achievable result; the grid was not re-swept per arm. Re-tuning would
  turn a one-line ablation into a second tuning study, and it would also make the comparison about
  tuning luck.
* One dataset family, full batch, 120 epochs — the same regime and the same caveats as §5.4.
* Single confirmatory seed count (ten), so the effect is reported with its paired test and interval
  rather than as a p-value alone (`docs/defect-family.md` case 5's rule: every quoted statistic has a
  generator, a definition and a test).
