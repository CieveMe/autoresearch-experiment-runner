# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `test_loss` (lower is better)
- base config: `examples\classification.json` (SHA-256 `cc85ba76ddcdff91f561bb0366fd3228c00e5b46541af8e4cdc04563926e040f`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | test_loss mean | test_loss stdev | min | max | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| adam_reproduction | 0.20368012 | 0.01816425 | 0.16660726 | 0.22882864 | 94.30% | 10/10 | 100% |
| sgd_control | 0.28037568 | 0.01838522 | 0.24736677 | 0.30370702 | 94.55% | 0/10 | 0% |
| adam_regularized | 0.31730997 | 0.01843015 | 0.28119885 | 0.34124891 | 94.30% | 0/10 | 0% |
| baseline | 0.38165322 | 0.01586304 | 0.35596295 | 0.40227566 | 94.05% | 0/10 | 0% |

Paired per-seed improvement over `baseline` (positive = better `test_loss`):

| trial | better in | worse in | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|
| adam_reproduction | 10/10 | 0 | 0.1779731 | 0.00771465 | 0.16861319 | 0.18948605999999998 |
| sgd_control | 10/10 | 0 | 0.10127754 | 0.00354625 | 0.09701005000000001 | 0.10859617999999999 |
| adam_regularized | 10/10 | 0 | 0.06434325 | 0.00637908 | 0.057393609999999984 | 0.0747641 |

Paired per-seed improvement over `sgd_control` (positive = better `test_loss`):

| trial | better in | worse in | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|
| adam_reproduction | 10/10 | 0 | 0.07669556 | 0.00553513 | 0.06845980999999998 | 0.08713679999999999 |
| adam_regularized | 0/10 | 10 | -0.03693428 | 0.00382122 | -0.04275977000000003 | -0.031017760000000005 |
| baseline | 0/10 | 10 | -0.10127754 | 0.00354625 | -0.10859617999999999 | -0.09701005000000001 |
