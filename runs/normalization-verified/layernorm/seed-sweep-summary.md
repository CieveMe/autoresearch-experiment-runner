# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `test_loss` (lower is better)
- base config: `examples\norm-layernorm.json` (SHA-256 `0fd7d766b5349f34822ca006bb93024f7735bc8aa8f00feba6906043df0b3309`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | test_loss mean | test_loss stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| adamw_cosine | 0.13250776 | 0.02367173 | 0.08311056 | 0.17518164 | 10/10 | 94.05% | 3/10 | 30% |
| ademamix | 0.13379276 | 0.0249594 | 0.08227596 | 0.17935586 | 10/10 | 93.95% | 2/10 | 20% |
| adagrad | 0.13382467 | 0.02307671 | 0.08327266 | 0.17359218 | 10/10 | 94.15% | 1/10 | 10% |
| adamw_constant | 0.13387822 | 0.02496662 | 0.08232065 | 0.17968908 | 10/10 | 93.95% | 1/10 | 10% |
| adam | 0.13387822 | 0.02496662 | 0.08232065 | 0.17968908 | 10/10 | 93.95% | 0/10 | 0% |
| schedule_free_adamw | 0.13624952 | 0.02626187 | 0.08481521 | 0.18991776 | 10/10 | 94.10% | 3/10 | 30% |

Paired per-seed improvement over `adamw_cosine` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| ademamix | 5/10 | 5 | 0 | -0.00128499 | 0.00228352 | -0.004174220000000006 | 0.0013820699999999991 |
| adagrad | 4/10 | 6 | 0 | -0.0013169 | 0.00318021 | -0.008436599999999989 | 0.001589459999999987 |
| adamw_constant | 5/10 | 5 | 0 | -0.00137046 | 0.00235363 | -0.0045074400000000014 | 0.00129957 |
| adam | 5/10 | 5 | 0 | -0.00137046 | 0.00235363 | -0.0045074400000000014 | 0.00129957 |
| schedule_free_adamw | 3/10 | 7 | 0 | -0.00374176 | 0.00679818 | -0.016108010000000006 | 0.005068749999999997 |

Paired per-seed improvement over `schedule_free_adamw` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adamw_cosine | 7/10 | 3 | 0 | 0.00374176 | 0.00679818 | -0.005068749999999997 | 0.016108010000000006 |
| ademamix | 6/10 | 4 | 0 | 0.00245677 | 0.00544723 | -0.00395056000000002 | 0.012212279999999992 |
| adagrad | 6/10 | 4 | 0 | 0.00242485 | 0.00668363 | -0.006057089999999987 | 0.01632557999999998 |
| adamw_constant | 6/10 | 4 | 0 | 0.0023713 | 0.00524621 | -0.003973999999999991 | 0.011691919999999995 |
| adam | 6/10 | 4 | 0 | 0.0023713 | 0.00524621 | -0.003973999999999991 | 0.011691919999999995 |
