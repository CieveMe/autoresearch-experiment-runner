# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `test_loss` (lower is better)
- base config: `examples\schedule-free.json` (SHA-256 `3592a75bdfd388764ba55cf75fe77af25b2e25a7ce4240eb5c9f226259f0d779`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | test_loss mean | test_loss stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| adamw_constant | 0.12448148 | 0.02004526 | 0.08398865 | 0.15593921 | 10/10 | 94.30% | 7/10 | 70% |
| adamw_cosine | 0.12609693 | 0.01946999 | 0.08637586 | 0.15520851 | 10/10 | 94.30% | 3/10 | 30% |
| schedule_free_adamw | 0.12641856 | 0.01951518 | 0.08651179 | 0.15544331 | 10/10 | 94.30% | 0/10 | 0% |
| schedule_free_sgd | 0.19638962 | 0.01936207 | 0.15849437 | 0.22138863 | 10/10 | 94.65% | 0/10 | 0% |
| sgd_cosine | 0.21655121 | 0.01913303 | 0.17983007 | 0.24178287 | 10/10 | 94.50% | 0/10 | 0% |

Paired per-seed improvement over `adamw_cosine` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adamw_constant | 7/10 | 3 | 0 | 0.00161545 | 0.00181455 | -0.0007307000000000008 | 0.004419300000000015 |
| schedule_free_adamw | 0/10 | 10 | 0 | -0.00032163 | 0.00020836 | -0.0007201899999999817 | -0.00013593000000000632 |
| schedule_free_sgd | 0/10 | 10 | 0 | -0.07029268 | 0.00799792 | -0.08321255999999999 | -0.059412960000000015 |
| sgd_cosine | 0/10 | 10 | 0 | -0.09045427 | 0.00871597 | -0.10467137999999998 | -0.07919467999999999 |

Paired per-seed improvement over `schedule_free_adamw` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adamw_constant | 7/10 | 3 | 0 | 0.00193708 | 0.00197234 | -0.0005600699999999958 | 0.0051394899999999966 |
| adamw_cosine | 10/10 | 0 | 0 | 0.00032163 | 0.00020836 | 0.00013593000000000632 | 0.0007201899999999817 |
| schedule_free_sgd | 0/10 | 10 | 0 | -0.06997105 | 0.00791722 | -0.08291456999999999 | -0.05923123999999999 |
| sgd_cosine | 0/10 | 10 | 0 | -0.09013264 | 0.00864036 | -0.10437338999999998 | -0.07886256 |
