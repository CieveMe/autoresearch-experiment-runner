# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `test_loss` (lower is better)
- base config: `examples\capacity-h32.json` (SHA-256 `51d398e8b0413feca84c4d4457138da00bbb34fb607ba4cfd799ca4914fb062a`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | test_loss mean | test_loss stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 0.12554941 | 0.02103281 | 0.08323162 | 0.15948891 | 10/10 | 94.40% | 9/10 | 90% |
| schedule_free_adamw | 0.13213685 | 0.0242559 | 0.08352051 | 0.17507483 | 10/10 | 94.05% | 0/10 | 0% |
| adamw_cosine | 0.13587117 | 0.02483092 | 0.08092261 | 0.17677074 | 10/10 | 94.05% | 1/10 | 10% |
| adamw_constant | 0.14424775 | 0.03219722 | 0.08164428 | 0.20761412 | 10/10 | 94.10% | 0/10 | 0% |
| adam | 0.14424775 | 0.03219722 | 0.08164428 | 0.20761412 | 10/10 | 94.10% | 0/10 | 0% |
| ademamix | 0.14508448 | 0.03281871 | 0.08161851 | 0.20932956 | 10/10 | 94.10% | 0/10 | 0% |

Paired per-seed improvement over `adamw_cosine` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 9/10 | 1 | 0 | 0.01032176 | 0.00892583 | -0.0023090100000000002 | 0.030629210000000018 |
| schedule_free_adamw | 8/10 | 2 | 0 | 0.00373431 | 0.00674936 | -0.0025979 | 0.021285380000000007 |
| adamw_constant | 1/10 | 9 | 0 | -0.00837658 | 0.01147803 | -0.030843380000000004 | 0.0004103599999999985 |
| adam | 1/10 | 9 | 0 | -0.00837658 | 0.01147803 | -0.030843380000000004 | 0.0004103599999999985 |
| ademamix | 1/10 | 9 | 0 | -0.00921331 | 0.01220437 | -0.03255881999999999 | 0.0003069500000000003 |

Paired per-seed improvement over `schedule_free_adamw` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 10/10 | 0 | 0 | 0.00658744 | 0.00444221 | 0.00028889 | 0.015585919999999975 |
| adamw_cosine | 2/10 | 8 | 0 | -0.00373431 | 0.00674936 | -0.021285380000000007 | 0.0025979 |
| adamw_constant | 1/10 | 9 | 0 | -0.01211089 | 0.0162894 | -0.049922149999999985 | 0.0018762300000000065 |
| adam | 1/10 | 9 | 0 | -0.01211089 | 0.0162894 | -0.049922149999999985 | 0.0018762300000000065 |
| ademamix | 1/10 | 9 | 0 | -0.01294763 | 0.01705291 | -0.05234589999999999 | 0.001902000000000001 |
