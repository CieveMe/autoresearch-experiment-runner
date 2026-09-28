# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `test_loss` (lower is better)
- base config: `examples\capacity-h16x16.json` (SHA-256 `c1fa52ce7ab0acb6e47343c4657974452af36a4fdb4a0a7af036964411720644`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | test_loss mean | test_loss stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| schedule_free_adamw | 0.14634485 | 0.03697037 | 0.08261873 | 0.21663818 | 10/10 | 93.85% | 6/10 | 60% |
| adagrad | 0.15047676 | 0.03812327 | 0.10185254 | 0.21957264 | 10/10 | 94.00% | 4/10 | 40% |
| adamw_cosine | 0.17611076 | 0.05244028 | 0.1103921 | 0.27527534 | 10/10 | 93.85% | 0/10 | 0% |
| adamw_constant | 0.22110983 | 0.06965675 | 0.1248198 | 0.36680311 | 10/10 | 93.25% | 0/10 | 0% |
| adam | 0.22110983 | 0.06965675 | 0.1248198 | 0.36680311 | 10/10 | 93.25% | 0/10 | 0% |
| ademamix | 0.22438617 | 0.06519932 | 0.12027642 | 0.34175118 | 10/10 | 92.95% | 0/10 | 0% |

Paired per-seed improvement over `adamw_cosine` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| schedule_free_adamw | 10/10 | 0 | 0 | 0.02976592 | 0.02473422 | 0.0010623900000000103 | 0.08101301 |
| adagrad | 9/10 | 1 | 0 | 0.025634 | 0.03183189 | -0.02068210000000001 | 0.08855278 |
| adamw_constant | 0/10 | 10 | 0 | -0.04499906 | 0.02459832 | -0.09152777000000001 | -0.013745659999999993 |
| adam | 0/10 | 10 | 0 | -0.04499906 | 0.02459832 | -0.09152777000000001 | -0.013745659999999993 |
| ademamix | 0/10 | 10 | 0 | -0.04827541 | 0.0247288 | -0.09593926 | -0.009202279999999993 |

Paired per-seed improvement over `schedule_free_adamw` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 4/10 | 6 | 0 | -0.00413192 | 0.01720813 | -0.025107110000000002 | 0.03294807000000001 |
| adamw_cosine | 0/10 | 10 | 0 | -0.02976592 | 0.02473422 | -0.08101301 | -0.0010623900000000103 |
| adamw_constant | 0/10 | 10 | 0 | -0.07476498 | 0.03797809 | -0.15016492999999997 | -0.028931509999999994 |
| adam | 0/10 | 10 | 0 | -0.07476498 | 0.03797809 | -0.15016492999999997 | -0.028931509999999994 |
| ademamix | 0/10 | 10 | 0 | -0.07804132 | 0.03424513 | -0.12694970000000003 | -0.03104309999999999 |
