# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `epochs_to_target` (lower is better)
- base config: `examples\ademamix.json` (SHA-256 `c046217aa4a239a4db2c685c4162efc4ae5cda90fc9e69b03fe28d8417972962`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | epochs_to_target mean | epochs_to_target stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| adamw | 13.7 | 4.69160006 | 8 | 23 | 10/10 | 94.35% | 4/10 | 40% |
| ademamix_tuned | 13.7 | 4.69160006 | 8 | 23 | 10/10 | 94.35% | 6/10 | 60% |
| ademamix_no_slow_ema | 13.7 | 4.69160006 | 8 | 23 | 10/10 | 94.35% | 0/10 | 0% |
| sgd_momentum | 23.3 | 10.88372894 | 13 | 47 | 10/10 | 94.35% | 0/10 | 0% |
| ademamix_paper_warmups | 66.5 | 23.49113308 | 38 | 105 | 10/10 | 94.30% | 0/10 | 0% |

Paired per-seed improvement over `adamw` (positive = better `epochs_to_target`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| ademamix_tuned | 0/10 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 |
| ademamix_no_slow_ema | 0/10 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 |
| sgd_momentum | 0/10 | 10 | 0 | -9.6 | 6.41525959 | -24.0 | -5.0 |
| ademamix_paper_warmups | 0/10 | 10 | 0 | -52.8 | 18.91971341 | -82.0 | -30.0 |

Paired per-seed improvement over `sgd_momentum` (positive = better `epochs_to_target`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adamw | 10/10 | 0 | 0 | 9.6 | 6.41525959 | 5.0 | 24.0 |
| ademamix_tuned | 10/10 | 0 | 0 | 9.6 | 6.41525959 | 5.0 | 24.0 |
| ademamix_no_slow_ema | 10/10 | 0 | 0 | 9.6 | 6.41525959 | 5.0 | 24.0 |
| ademamix_paper_warmups | 0/10 | 10 | 0 | -43.2 | 13.44784163 | -59.0 | -25.0 |
