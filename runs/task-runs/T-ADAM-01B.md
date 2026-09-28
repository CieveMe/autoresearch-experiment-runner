# T-ADAM-01B — implement Algorithm 1 from the paper; pass the same expectations

Solved: **yes**.

| state | submission score | tier | submission exit | controls detected | mutation points live |
|---|---:|---|---:|---|---|
| given state: Adam branch stubbed out | 0.0/100 | tier=core; NOT run: capacity-h32, capacity-h8x8, capacity-h64, capacity-h16x16, activation-relu, activation-gelu, norm-layernorm, norm-batchnorm, init-he, init-plain | 1 | not run | not checked |
| attempt 2: Algorithm 1 implemented from the paper, arithmetic folded differently | 100.0/100 | tier=core; NOT run: capacity-h32, capacity-h8x8, capacity-h64, capacity-h16x16, activation-relu, activation-gelu, norm-layernorm, norm-batchnorm, init-he, init-plain | 1 | not run | **NO** |
| attempt 3: implementation kept drop-in at the harness's mutation points | 100.0/100 | tier=core; NOT run: capacity-h32, capacity-h8x8, capacity-h64, capacity-h16x16, activation-relu, activation-gelu, norm-layernorm, norm-batchnorm, init-he, init-plain | 0 | not run | yes |
| final: full scorer including the negative controls | 100.0/100 | tier=core; NOT run: capacity-h32, capacity-h8x8, capacity-h64, capacity-h16x16, activation-relu, activation-gelu, norm-layernorm, norm-batchnorm, init-he, init-plain | 0 | 4/4 | not checked |

## Raw scorer output

### given state: Adam branch stubbed out

```
submission score: 0.0/100 (tier=core; NOT run: capacity-h32, capacity-h8x8, capacity-h64, capacity-h16x16, activation-relu, activation-gelu, norm-layernorm, norm-batchnorm, init-he, init-plain) (0/0 checks, exit 1)
  FAIL main: no results.json produced
  FAIL optimizers: no results.json produced
  FAIL ablation-adam-no-first-moment: no results.json produced
  FAIL ademamix: no results.json produced
  FAIL optimizers-mlp: no results.json produced
  FAIL ademamix-mlp: no results.json produced
  FAIL schedule-free: no results.json produced
  FAIL schedule-free-mlp: no results.json produced

TASK RESULT: FAIL
```

### attempt 2: Algorithm 1 implemented from the paper, arithmetic folded differently

```
submission score: 100.0/100 (tier=core; NOT run: capacity-h32, capacity-h8x8, capacity-h64, capacity-h16x16, activation-relu, activation-gelu, norm-layernorm, norm-batchnorm, init-he, init-plain) (184/184 checks, exit 1)

TASK RESULT: FAIL
```

### attempt 3: implementation kept drop-in at the harness's mutation points

```
submission score: 100.0/100 (tier=core; NOT run: capacity-h32, capacity-h8x8, capacity-h64, capacity-h16x16, activation-relu, activation-gelu, norm-layernorm, norm-batchnorm, init-he, init-plain) (184/184 checks, exit 0)

TASK RESULT: PASS
```

### final: full scorer including the negative controls

```
submission score: 100.0/100 (tier=core; NOT run: capacity-h32, capacity-h8x8, capacity-h64, capacity-h16x16, activation-relu, activation-gelu, norm-layernorm, norm-batchnorm, init-he, init-plain) (184/184 checks, exit 0)
control[no-bias-correction]: detected (score 83.7/100, exit 1)
control[no-adaptive-scaling]: detected (score 82.1/100, exit 1)
control[ademamix-without-slow-ema]: detected (score 94.0/100, exit 1)
control[schedule-free-without-averaging]: detected (score 94.6/100, exit 1)

TASK RESULT: PASS
```
