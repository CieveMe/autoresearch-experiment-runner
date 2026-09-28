# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `test_loss` (lower is better)
- base config: `examples\activation-gelu.json` (SHA-256 `d5e45d7d66df60263aae5d5132c7aa54a93ad15f4e90ac89823521cef90ca965`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | test_loss mean | test_loss stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 0.12616659 | 0.02175749 | 0.08284631 | 0.1599419 | 10/10 | 94.40% | 6/10 | 60% |
| schedule_free_adamw | 0.1268743 | 0.02175874 | 0.08345792 | 0.16178401 | 10/10 | 94.45% | 3/10 | 30% |
| adamw_constant | 0.12691145 | 0.02255809 | 0.08198748 | 0.16216111 | 10/10 | 94.35% | 0/10 | 0% |
| adam | 0.12691145 | 0.02255809 | 0.08198748 | 0.16216111 | 10/10 | 94.35% | 0/10 | 0% |
| ademamix | 0.12705791 | 0.02266084 | 0.08193332 | 0.16243147 | 10/10 | 94.35% | 0/10 | 0% |
| adamw_cosine | 0.12960383 | 0.02501806 | 0.0816826 | 0.17414973 | 10/10 | 94.25% | 1/10 | 10% |

Paired per-seed improvement over `adamw_cosine` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 9/10 | 1 | 0 | 0.00343724 | 0.00479156 | -0.0011637100000000122 | 0.014207830000000005 |
| schedule_free_adamw | 8/10 | 2 | 0 | 0.00272953 | 0.00416618 | -0.0017753200000000108 | 0.012365719999999997 |
| adamw_constant | 7/10 | 3 | 0 | 0.00269238 | 0.00437305 | -0.0007139200000000068 | 0.011988620000000005 |
| adam | 7/10 | 3 | 0 | 0.00269238 | 0.00437305 | -0.0007139200000000068 | 0.011988620000000005 |
| ademamix | 6/10 | 4 | 0 | 0.00254592 | 0.00430292 | -0.0010751700000000142 | 0.011718260000000008 |

Paired per-seed improvement over `schedule_free_adamw` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 7/10 | 3 | 0 | 0.00070771 | 0.00169871 | -0.0020938100000000015 | 0.0041928399999999755 |
| adamw_constant | 4/10 | 6 | 0 | -3.715e-05 | 0.0022413 | -0.0041588200000000075 | 0.00416511 |
| adam | 4/10 | 6 | 0 | -3.715e-05 | 0.0022413 | -0.0041588200000000075 | 0.00416511 |
| ademamix | 4/10 | 6 | 0 | -0.00018361 | 0.00224059 | -0.004520070000000015 | 0.003807939999999982 |
| adamw_cosine | 2/10 | 8 | 0 | -0.00272953 | 0.00416618 | -0.012365719999999997 | 0.0017753200000000108 |
