# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `epochs_to_target` (lower is better)
- base config: `examples\ablation-adam-no-first-moment.json` (SHA-256 `27392c22f2dc2f258d9e5d52d5b857efb84c5258cb9584763005aef4cc232f55`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | epochs_to_target mean | epochs_to_target stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| adam | 22.6 | 6.39791633 | 15 | 33 | 10/10 | 94.30% | 10/10 | 100% |
| adam_beta1_0 | 41.1 | 12.77541041 | 25 | 61 | 10/10 | 94.40% | 0/10 | 0% |

Paired per-seed improvement over `adam` (positive = better `epochs_to_target`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adam_beta1_0 | 0/10 | 10 | 0 | -18.5 | 6.41612552 | -28.0 | -10.0 |

Paired per-seed improvement over `adam_beta1_0` (positive = better `epochs_to_target`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adam | 10/10 | 0 | 0 | 18.5 | 6.41612552 | 10.0 | 28.0 |
