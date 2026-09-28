# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `test_loss` (lower is better)
- base config: `examples\capacity-h64.json` (SHA-256 `c4b4f81e427096bab98207f52a970e6fac2e95e02701a7b995be3df8ecb2fcaa`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | test_loss mean | test_loss stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 0.12570263 | 0.02108774 | 0.08347175 | 0.15983617 | 10/10 | 94.40% | 8/10 | 80% |
| schedule_free_adamw | 0.12904084 | 0.02322838 | 0.08339573 | 0.16828112 | 10/10 | 93.90% | 1/10 | 10% |
| adamw_cosine | 0.13808156 | 0.0276695 | 0.08064984 | 0.19028869 | 10/10 | 93.95% | 0/10 | 0% |
| adamw_constant | 0.14480195 | 0.03290995 | 0.0779946 | 0.20682161 | 10/10 | 93.95% | 0/10 | 0% |
| adam | 0.14480195 | 0.03290995 | 0.0779946 | 0.20682161 | 10/10 | 93.95% | 0/10 | 0% |
| ademamix | 0.14568073 | 0.03380907 | 0.07768366 | 0.20990173 | 10/10 | 93.95% | 1/10 | 10% |

Paired per-seed improvement over `adamw_cosine` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 9/10 | 1 | 0 | 0.01237893 | 0.01377757 | -0.002821909999999997 | 0.043245320000000004 |
| schedule_free_adamw | 9/10 | 1 | 0 | 0.00904072 | 0.01317701 | -0.002745890000000001 | 0.041532150000000004 |
| adamw_constant | 1/10 | 9 | 0 | -0.00672039 | 0.00638785 | -0.01653291999999998 | 0.002655240000000003 |
| adam | 1/10 | 9 | 0 | -0.00672039 | 0.00638785 | -0.01653291999999998 | 0.002655240000000003 |
| ademamix | 1/10 | 9 | 0 | -0.00759917 | 0.00733636 | -0.019613039999999998 | 0.002966179999999999 |

Paired per-seed improvement over `schedule_free_adamw` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 8/10 | 2 | 0 | 0.00333821 | 0.00306804 | -0.0015903099999999976 | 0.008444950000000007 |
| adamw_cosine | 1/10 | 9 | 0 | -0.00904072 | 0.01317701 | -0.041532150000000004 | 0.002745890000000001 |
| adamw_constant | 1/10 | 9 | 0 | -0.01576111 | 0.01721832 | -0.05202971999999999 | 0.005401130000000004 |
| adam | 1/10 | 9 | 0 | -0.01576111 | 0.01721832 | -0.05202971999999999 | 0.005401130000000004 |
| ademamix | 1/10 | 9 | 0 | -0.01663989 | 0.01808559 | -0.053722950000000005 | 0.00571207 |
