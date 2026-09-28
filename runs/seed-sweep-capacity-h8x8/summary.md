# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `test_loss` (lower is better)
- base config: `examples\capacity-h8x8.json` (SHA-256 `dd1fe09b9b043e414434101f48c02990836eac467bd58ac8566caf3b477c9d6e`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | test_loss mean | test_loss stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 0.12844838 | 0.02271356 | 0.08331469 | 0.16433016 | 10/10 | 94.40% | 7/10 | 70% |
| schedule_free_adamw | 0.14479273 | 0.04553769 | 0.07173358 | 0.25220781 | 10/10 | 94.00% | 2/10 | 20% |
| adamw_cosine | 0.16793582 | 0.04994094 | 0.08433127 | 0.24595399 | 10/10 | 93.65% | 0/10 | 0% |
| adamw_constant | 0.19478799 | 0.06461822 | 0.09495689 | 0.27989469 | 10/10 | 93.50% | 1/10 | 10% |
| adam | 0.19478799 | 0.06461822 | 0.09495689 | 0.27989469 | 10/10 | 93.50% | 0/10 | 0% |
| ademamix | 0.19792794 | 0.06709388 | 0.09868575 | 0.28849731 | 10/10 | 93.35% | 0/10 | 0% |

Paired per-seed improvement over `adamw_cosine` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 10/10 | 0 | 0 | 0.03948745 | 0.03020075 | 0.001016580000000003 | 0.08162383000000001 |
| schedule_free_adamw | 8/10 | 2 | 0 | 0.0231431 | 0.02307997 | -0.0062538199999999655 | 0.05291520000000002 |
| adamw_constant | 1/10 | 9 | 0 | -0.02685217 | 0.02256446 | -0.06675276 | 0.01794967 |
| adam | 1/10 | 9 | 0 | -0.02685217 | 0.02256446 | -0.06675276 | 0.01794967 |
| ademamix | 1/10 | 9 | 0 | -0.02999212 | 0.02310442 | -0.07110449999999999 | 0.013330809999999998 |

Paired per-seed improvement over `schedule_free_adamw` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 8/10 | 2 | 0 | 0.01634435 | 0.02758874 | -0.011581109999999992 | 0.08787764999999997 |
| adamw_cosine | 2/10 | 8 | 0 | -0.0231431 | 0.02307997 | -0.05291520000000002 | 0.0062538199999999655 |
| adamw_constant | 1/10 | 9 | 0 | -0.04999527 | 0.03868301 | -0.09837655000000001 | 0.02282803 |
| adam | 1/10 | 9 | 0 | -0.04999527 | 0.03868301 | -0.09837655000000001 | 0.02282803 |
| ademamix | 1/10 | 9 | 0 | -0.05313521 | 0.03977562 | -0.10272829 | 0.018209169999999997 |
