# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `epochs_to_target` (lower is better)
- base config: `examples\optimizers.json` (SHA-256 `808b4c1692271929dd61293f66bf97c0682f9907e8724713d9570a1f94eaeddf`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | epochs_to_target mean | epochs_to_target stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 4.7 | 3.33499958 | 2 | 12 | 10/10 | 94.30% | 10/10 | 100% |
| adam_no_bias_correction | 10.1 | 1.79195734 | 8 | 13 | 10/10 | 94.30% | 0/10 | 0% |
| sgd_momentum | 16.7 | 3.91719855 | 12 | 23 | 10/10 | 94.35% | 0/10 | 0% |
| adam | 22.6 | 6.39791633 | 15 | 33 | 10/10 | 94.30% | 0/10 | 0% |
| rmsprop | 42.0 | 9.6378882 | 29 | 57 | 10/10 | 94.45% | 0/10 | 0% |
| baseline | None | 0.0 | None | None | 0/10 | 94.60% | 0/10 | 0% |

Paired per-seed improvement over `adam` (positive = better `epochs_to_target`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 10/10 | 0 | 0 | 17.9 | 3.44641521 | 13.0 | 23.0 |
| adam_no_bias_correction | 10/10 | 0 | 0 | 12.5 | 4.62481231 | 7.0 | 20.0 |
| sgd_momentum | 10/10 | 0 | 0 | 5.9 | 2.51440296 | 3.0 | 10.0 |
| rmsprop | 0/10 | 10 | 0 | -19.4 | 3.40587727 | -24.0 | -14.0 |
| baseline | 0/10 | 0 | 10 | None | 0.0 | None | None |

Paired per-seed improvement over `sgd_momentum` (positive = better `epochs_to_target`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 10/10 | 0 | 0 | 12.0 | 1.41421356 | 10.0 | 14.0 |
| adam_no_bias_correction | 10/10 | 0 | 0 | 6.6 | 2.17050941 | 4.0 | 10.0 |
| adam | 0/10 | 10 | 0 | -5.9 | 2.51440296 | -10.0 | -3.0 |
| rmsprop | 0/10 | 10 | 0 | -25.3 | 5.83190459 | -34.0 | -17.0 |
| baseline | 0/10 | 0 | 10 | None | 0.0 | None | None |
