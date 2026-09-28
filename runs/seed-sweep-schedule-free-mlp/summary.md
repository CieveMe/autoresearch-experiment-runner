# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `test_loss` (lower is better)
- base config: `examples\schedule-free-mlp.json` (SHA-256 `e420acd848306e2138a703ca937279b4abf79fb2e0c2868b2ccbf75ac59a233f`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | test_loss mean | test_loss stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| schedule_free_sgd | 0.12589449 | 0.02133564 | 0.08226629 | 0.15987465 | 10/10 | 94.40% | 3/10 | 30% |
| sgd_cosine | 0.12603229 | 0.01990798 | 0.08566149 | 0.15602591 | 10/10 | 94.35% | 4/10 | 40% |
| schedule_free_adamw | 0.13093784 | 0.02572348 | 0.07837142 | 0.17194125 | 10/10 | 94.25% | 2/10 | 20% |
| adamw_cosine | 0.13222054 | 0.02460391 | 0.08190946 | 0.16577598 | 10/10 | 94.15% | 0/10 | 0% |
| adamw_constant | 0.13796459 | 0.02615545 | 0.08387601 | 0.17947897 | 10/10 | 94.05% | 1/10 | 10% |

Paired per-seed improvement over `adamw_cosine` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| schedule_free_sgd | 9/10 | 1 | 0 | 0.00632605 | 0.00465969 | -0.0003568300000000024 | 0.01456093 |
| sgd_cosine | 8/10 | 2 | 0 | 0.00618825 | 0.0058277 | -0.0037520300000000034 | 0.015629580000000004 |
| schedule_free_adamw | 9/10 | 1 | 0 | 0.0012827 | 0.00313089 | -0.0061652700000000005 | 0.006281519999999985 |
| adamw_constant | 1/10 | 9 | 0 | -0.00574405 | 0.0060264 | -0.01701242 | 0.001978110000000005 |

Paired per-seed improvement over `schedule_free_adamw` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| schedule_free_sgd | 7/10 | 3 | 0 | 0.00504335 | 0.00502782 | -0.0038948700000000086 | 0.012066599999999983 |
| sgd_cosine | 8/10 | 2 | 0 | 0.00490555 | 0.00676339 | -0.00729007000000001 | 0.01591534 |
| adamw_cosine | 1/10 | 9 | 0 | -0.0012827 | 0.00313089 | -0.006281519999999985 | 0.0061652700000000005 |
| adamw_constant | 1/10 | 9 | 0 | -0.00702675 | 0.00570843 | -0.018364770000000002 | 5.0269999999991155e-05 |
