# Seed sweep summary (10 seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

- metric: `test_loss` (lower is better)
- base config: `examples\norm-batchnorm.json` (SHA-256 `9166f25495ece439c4022465c234e238d865a239200712a0d8e996af695b549c`)
- per-seed config copies are written next to each run and hashed in `summary.json`

| trial | test_loss mean | test_loss stdev | min | max | reached | test_accuracy mean | wins | win rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| schedule_free_adamw | 0.13323101 | 0.03059877 | 0.08369922 | 0.19139783 | 10/10 | 94.00% | 2/10 | 20% |
| adagrad | 0.13323497 | 0.0307189 | 0.08380817 | 0.19211937 | 10/10 | 94.15% | 4/10 | 40% |
| adamw_cosine | 0.13417101 | 0.03135338 | 0.0835687 | 0.19395374 | 10/10 | 94.05% | 2/10 | 20% |
| adamw_constant | 0.13446993 | 0.03116588 | 0.0835445 | 0.19271318 | 10/10 | 93.95% | 2/10 | 20% |
| adam | 0.13446993 | 0.03116588 | 0.0835445 | 0.19271318 | 10/10 | 93.95% | 0/10 | 0% |
| ademamix | 0.13452586 | 0.03117894 | 0.08354893 | 0.19275804 | 10/10 | 93.95% | 0/10 | 0% |

Paired per-seed improvement over `adamw_cosine` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| schedule_free_adamw | 5/10 | 5 | 0 | 0.00094 | 0.001703 | -0.0008784099999999961 | 0.003986199999999995 |
| adagrad | 6/10 | 4 | 0 | 0.00093604 | 0.00142495 | -0.0010649699999999984 | 0.003285659999999996 |
| adamw_constant | 3/10 | 7 | 0 | -0.00029892 | 0.00078884 | -0.001952010000000004 | 0.0012405600000000017 |
| adam | 3/10 | 7 | 0 | -0.00029892 | 0.00078884 | -0.001952010000000004 | 0.0012405600000000017 |
| ademamix | 3/10 | 7 | 0 | -0.00035485 | 0.00081347 | -0.0020919699999999986 | 0.0011957000000000217 |

Paired per-seed improvement over `schedule_free_adamw` (positive = better `test_loss`):

| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| adagrad | 6/10 | 4 | 0 | -3.96e-06 | 0.00082086 | -0.0017192799999999897 | 0.0013107700000000166 |
| adamw_cosine | 5/10 | 5 | 0 | -0.00094 | 0.001703 | -0.003986199999999995 | 0.0008784099999999961 |
| adamw_constant | 4/10 | 6 | 0 | -0.00123892 | 0.00202927 | -0.005938209999999999 | 0.000525570000000003 |
| adam | 4/10 | 6 | 0 | -0.00123892 | 0.00202927 | -0.005938209999999999 | 0.000525570000000003 |
| ademamix | 4/10 | 6 | 0 | -0.00129484 | 0.00208392 | -0.006078169999999994 | 0.0005120399999999914 |
