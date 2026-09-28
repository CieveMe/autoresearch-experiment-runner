# Crossing stability — `optimizers` (adam_no_bias_correction vs adagrad)

Crossings located in **10 of 10 seeds**, at 0.136984 on average (min 0.112061, max 0.157677, spread 0.045616).

At the suite's pinned threshold (0.16), the faster arm per seed was:

| seed | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| faster | adagrad | adagrad | adagrad | adagrad | adagrad | adagrad | adagrad | adagrad | adagrad | adagrad |

**Consistent**: `adagrad` is faster at the pinned threshold in every seed.

Per-seed crossing values:

| seed | crossing |
|---:|---|
| 0 | 0.113339 |
| 1 | 0.131602 |
| 2 | 0.14883 |
| 3 | 0.151821 |
| 4 | 0.141318 |
| 5 | 0.151406 |
| 6 | 0.112061 |
| 7 | 0.157677 |
| 8 | 0.127441 |
| 9 | 0.134349 |
