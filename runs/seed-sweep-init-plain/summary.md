# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `test_loss` (lower is better)
- base config: `examples\init-plain.json` (SHA-256 `15eb8d5ab8f4bb921d5db3ae939237008a83be691efba5d50379c87ff681b1fd`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | test_loss mean | test_loss stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| schedule_free_adamw | 0.12555073 | 0.02155086 | 0.08180586 | 0.15996797 | 10/10 | 94.40% | 4/10 | 40% |
| adamw_cosine | 0.12607403 | 0.02206524 | 0.080648 | 0.15965272 | 10/10 | 94.45% | 4/10 | 40% |
| adagrad | 0.13372011 | 0.02534975 | 0.09096551 | 0.17395064 | 10/10 | 94.15% | 1/10 | 10% |
| adamw_constant | 0.13699482 | 0.03137388 | 0.07529784 | 0.20089607 | 10/10 | 94.10% | 0/10 | 0% |
| adam | 0.13699482 | 0.03137388 | 0.07529784 | 0.20089607 | 10/10 | 94.10% | 0/10 | 0% |
| ademamix | 0.13894744 | 0.03240213 | 0.07479193 | 0.20222834 | 10/10 | 94.15% | 1/10 | 10% |

Paired per-seed improvement over `adamw_cosine` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| schedule_free_adamw | 5/10 | 5 | 0 | 0.0005233 | 0.00130929 | -0.0011578599999999967 | 0.003319590000000011 |
| adagrad | 1/10 | 9 | 0 | -0.00764608 | 0.01016195 | -0.027886439999999985 | 0.004976389999999997 |
| adamw_constant | 1/10 | 9 | 0 | -0.01092079 | 0.01228732 | -0.04124335000000001 | 0.005350159999999993 |
| adam | 1/10 | 9 | 0 | -0.01092079 | 0.01228732 | -0.04124335000000001 | 0.005350159999999993 |
| ademamix | 1/10 | 9 | 0 | -0.01287341 | 0.0130178 | -0.04257562000000001 | 0.005856069999999991 |

Paired per-seed improvement over `schedule_free_adamw` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adamw_cosine | 5/10 | 5 | 0 | -0.0005233 | 0.00130929 | -0.003319590000000011 | 0.0011578599999999967 |
| adagrad | 2/10 | 8 | 0 | -0.00816938 | 0.00956467 | -0.02801605999999998 | 0.001656799999999986 |
| adamw_constant | 1/10 | 9 | 0 | -0.01144409 | 0.01221597 | -0.04092810000000002 | 0.006508019999999989 |
| adam | 1/10 | 9 | 0 | -0.01144409 | 0.01221597 | -0.04092810000000002 | 0.006508019999999989 |
| ademamix | 1/10 | 9 | 0 | -0.01339671 | 0.01319752 | -0.04226037000000002 | 0.007013929999999988 |
