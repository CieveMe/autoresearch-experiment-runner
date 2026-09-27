# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `test_loss` (lower is better)
- base config: `examples\ademamix-mlp.json` (SHA-256 `0acc10bdd3f96b3f301e426e80a54604063007f58f27b3f80684b1a9f296f68d`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | test_loss mean | test_loss stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sgd_momentum | 0.13025849 | 0.02342932 | 0.08058201 | 0.16283995 | 10/10 | 94.40% | 6/10 | 60% |
| adamw | 0.13218391 | 0.0247297 | 0.08174844 | 0.16607861 | 10/10 | 94.15% | 1/10 | 10% |
| ademamix_no_warmups | 0.13248842 | 0.02482561 | 0.08213844 | 0.16629654 | 10/10 | 94.20% | 0/10 | 0% |
| ademamix_warmup_45 | 0.14269105 | 0.03484904 | 0.09015425 | 0.19632853 | 10/10 | 94.00% | 3/10 | 30% |
| ademamix_warmup_120 | 0.1526129 | 0.03962154 | 0.09454079 | 0.2126496 | 10/10 | 93.80% | 0/10 | 0% |

Paired per-seed improvement over `adamw` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| sgd_momentum | 8/10 | 2 | 0 | 0.00192542 | 0.00295795 | -0.002949850000000004 | 0.00804286999999998 |
| ademamix_no_warmups | 2/10 | 8 | 0 | -0.00030451 | 0.00028027 | -0.0007053700000000107 | 0.00014885000000000592 |
| ademamix_warmup_45 | 3/10 | 7 | 0 | -0.01050714 | 0.01386963 | -0.031684110000000015 | 0.006438080000000013 |
| ademamix_warmup_120 | 2/10 | 8 | 0 | -0.02042899 | 0.02012738 | -0.04833072000000002 | 0.003300850000000008 |

Paired per-seed improvement over `sgd_momentum` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adamw | 2/10 | 8 | 0 | -0.00192542 | 0.00295795 | -0.00804286999999998 | 0.002949850000000004 |
| ademamix_no_warmups | 2/10 | 8 | 0 | -0.00222993 | 0.0030854 | -0.00874823999999999 | 0.002452679999999985 |
| ademamix_warmup_45 | 3/10 | 7 | 0 | -0.01243256 | 0.01537955 | -0.039726979999999995 | 0.006845970000000007 |
| ademamix_warmup_120 | 2/10 | 8 | 0 | -0.02235441 | 0.0211637 | -0.04980964999999998 | 0.003708740000000002 |
