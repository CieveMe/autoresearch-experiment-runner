# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `test_loss` (lower is better)
- base config: `examples\init-he.json` (SHA-256 `1da336133e6fe169760deb46442b6c28571f229918362460375c807342feedb0`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | test_loss mean | test_loss stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 0.136635 | 0.02771504 | 0.08276766 | 0.19144076 | 10/10 | 93.80% | 5/10 | 50% |
| schedule_free_adamw | 0.14293313 | 0.03186853 | 0.08252144 | 0.20754148 | 10/10 | 93.95% | 3/10 | 30% |
| adamw_cosine | 0.14859646 | 0.03623732 | 0.08789095 | 0.22916305 | 10/10 | 94.00% | 1/10 | 10% |
| adamw_constant | 0.159186 | 0.04998941 | 0.08930891 | 0.28232302 | 10/10 | 93.85% | 0/10 | 0% |
| adam | 0.159186 | 0.04998941 | 0.08930891 | 0.28232302 | 10/10 | 93.85% | 0/10 | 0% |
| ademamix | 0.1615612 | 0.05177062 | 0.08972378 | 0.28907951 | 10/10 | 93.70% | 1/10 | 10% |

Paired per-seed improvement over `adamw_cosine` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 9/10 | 1 | 0 | 0.01196145 | 0.013057 | -0.004454790000000014 | 0.03772229000000002 |
| schedule_free_adamw | 9/10 | 1 | 0 | 0.00566332 | 0.00716143 | -6.757000000001678e-05 | 0.021621570000000007 |
| adamw_constant | 2/10 | 8 | 0 | -0.01058954 | 0.01643203 | -0.05315996999999997 | 0.004011040000000007 |
| adam | 2/10 | 8 | 0 | -0.01058954 | 0.01643203 | -0.05315996999999997 | 0.004011040000000007 |
| ademamix | 1/10 | 9 | 0 | -0.01296474 | 0.01853226 | -0.05991645999999998 | 0.004163819999999999 |

Paired per-seed improvement over `schedule_free_adamw` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 6/10 | 4 | 0 | 0.00629813 | 0.01059467 | -0.004387219999999997 | 0.029000959999999992 |
| adamw_cosine | 1/10 | 9 | 0 | -0.00566332 | 0.00716143 | -0.021621570000000007 | 6.757000000001678e-05 |
| adamw_constant | 1/10 | 9 | 0 | -0.01625286 | 0.02185054 | -0.07478153999999998 | 0.0028862899999999997 |
| adam | 1/10 | 9 | 0 | -0.01625286 | 0.02185054 | -0.07478153999999998 | 0.0028862899999999997 |
| ademamix | 1/10 | 9 | 0 | -0.01862807 | 0.0238953 | -0.08153802999999998 | 0.003039069999999991 |
