# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `epochs_to_target` (lower is better)
- base config: `examples\optimizers-mlp.json` (SHA-256 `be7ead0661fdd714d0e46405badfc9d8ba84353ca4cf3122f4f1b5f1b12d7b5b`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | epochs_to_target mean | epochs_to_target stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 6.2 | 3.99444058 | 3 | 14 | 10/10 | 94.35% | 7/10 | 70% |
| sgd_momentum | 7.0 | 1.33333333 | 5 | 9 | 10/10 | 94.40% | 2/10 | 20% |
| adam | 20.3 | 13.23337531 | 4 | 43 | 10/10 | 93.90% | 1/10 | 10% |
| rmsprop | 33.3 | 14.2987956 | 16 | 51 | 10/10 | 94.50% | 0/10 | 0% |
| sgd | 36.1 | 17.77920133 | 17 | 70 | 10/10 | 94.35% | 0/10 | 0% |

Paired per-seed improvement over `adam` (positive = better `epochs_to_target`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 8/10 | 1 | 0 | 14.1 | 12.51177223 | -2.0 | 37.0 |
| sgd_momentum | 8/10 | 2 | 0 | 13.3 | 12.86727114 | -4.0 | 35.0 |
| rmsprop | 2/10 | 7 | 0 | -13.0 | 15.202339 | -33.0 | 8.0 |
| sgd | 1/10 | 9 | 0 | -15.8 | 15.16428553 | -43.0 | 5.0 |

Paired per-seed improvement over `sgd_momentum` (positive = better `epochs_to_target`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 7/10 | 2 | 0 | 0.8 | 3.01109061 | -6.0 | 3.0 |
| adam | 2/10 | 8 | 0 | -13.3 | 12.86727114 | -35.0 | 4.0 |
| rmsprop | 0/10 | 10 | 0 | -26.3 | 13.06437055 | -43.0 | -11.0 |
| sgd | 0/10 | 10 | 0 | -29.1 | 16.71625955 | -62.0 | -12.0 |
