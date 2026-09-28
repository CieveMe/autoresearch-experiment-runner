# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `test_loss` (lower is better)
- base config: `examples\activation-relu.json` (SHA-256 `a9d5d7d964bddd6fde64cf82ba4176a4665e44c2f55b7d39e88d6af16a562ce7`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | test_loss mean | test_loss stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 0.12562069 | 0.02171516 | 0.08222949 | 0.15990574 | 10/10 | 94.35% | 5/10 | 50% |
| schedule_free_adamw | 0.12717582 | 0.02283511 | 0.08274705 | 0.16535767 | 10/10 | 94.45% | 1/10 | 10% |
| ademamix | 0.12824233 | 0.02646054 | 0.0825481 | 0.18138288 | 10/10 | 94.20% | 2/10 | 20% |
| adamw_constant | 0.12828446 | 0.02613279 | 0.08252366 | 0.18043398 | 10/10 | 94.15% | 1/10 | 10% |
| adam | 0.12828446 | 0.02613279 | 0.08252366 | 0.18043398 | 10/10 | 94.15% | 0/10 | 0% |
| adamw_cosine | 0.13277336 | 0.02962191 | 0.08263973 | 0.19666076 | 10/10 | 94.20% | 1/10 | 10% |

Paired per-seed improvement over `adamw_cosine` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 9/10 | 1 | 0 | 0.00715268 | 0.01075789 | -0.0011782500000000196 | 0.03675502 |
| schedule_free_adamw | 8/10 | 2 | 0 | 0.00559754 | 0.00946293 | -0.002474290000000018 | 0.03130308999999998 |
| ademamix | 9/10 | 1 | 0 | 0.00453104 | 0.00531297 | -0.0011146200000000106 | 0.015277879999999994 |
| adamw_constant | 9/10 | 1 | 0 | 0.0044889 | 0.0052913 | -0.0008919700000000197 | 0.016226779999999996 |
| adam | 9/10 | 1 | 0 | 0.0044889 | 0.0052913 | -0.0008919700000000197 | 0.016226779999999996 |

Paired per-seed improvement over `schedule_free_adamw` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 9/10 | 1 | 0 | 0.00155513 | 0.002042 | -0.0013962999999999892 | 0.0054519300000000215 |
| ademamix | 6/10 | 4 | 0 | -0.00106651 | 0.00653579 | -0.016025209999999984 | 0.008305140000000003 |
| adamw_constant | 6/10 | 4 | 0 | -0.00110864 | 0.00602689 | -0.015076309999999982 | 0.006374630000000006 |
| adam | 6/10 | 4 | 0 | -0.00110864 | 0.00602689 | -0.015076309999999982 | 0.006374630000000006 |
| adamw_cosine | 2/10 | 8 | 0 | -0.00559754 | 0.00946293 | -0.03130308999999998 | 0.002474290000000018 |
