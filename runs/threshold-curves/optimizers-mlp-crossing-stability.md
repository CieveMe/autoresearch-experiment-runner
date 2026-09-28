# Crossing stability — `optimizers-mlp` (adam vs sgd_momentum)

Crossings located in **7 of 10 seeds**, at 0.116718 on average (min 0.089123, max 0.142088, spread 0.052965).

At the suite's pinned threshold (0.147), the faster arm per seed was:

| seed | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| faster | sgd_momentum | sgd_momentum | adam | sgd_momentum | sgd_momentum | sgd_momentum | adam | sgd_momentum | sgd_momentum | sgd_momentum |

**Not consistent**: the winner at the pinned threshold changes between seeds, so a single-seed statement about that threshold would not survive the sweep.

Per-seed crossing values:

| seed | crossing |
|---:|---|
| 0 | 0.094175 |
| 1 | 0.115951 |
| 2 | none |
| 3 | 0.13318 |
| 4 | 0.129131 |
| 5 | none |
| 6 | 0.089123 |
| 7 | 0.142088 |
| 8 | none |
| 9 | 0.113375 |
