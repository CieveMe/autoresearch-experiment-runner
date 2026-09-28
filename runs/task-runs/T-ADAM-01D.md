# T-ADAM-01D — find the defect from the failing assertion alone; the scorer must return to 100

Solved: **yes**.

| state | submission score | tier | submission exit | controls detected | mutation points live |
|---|---:|---|---:|---|---|
| given state: negative control `no-adaptive-scaling` already applied | 82.1/100 | tier=core; NOT run: capacity-h32, capacity-h8x8, capacity-h64, capacity-h16x16, activation-relu, activation-gelu, norm-layernorm, norm-batchnorm, init-he, init-plain | 1 | not run | not checked |
| recovered: defect undone from the failing assertion alone | 100.0/100 | tier=core; NOT run: capacity-h32, capacity-h8x8, capacity-h64, capacity-h16x16, activation-relu, activation-gelu, norm-layernorm, norm-batchnorm, init-he, init-plain | 0 | not run | not checked |
| final: full scorer including the negative controls | 100.0/100 | tier=core; NOT run: capacity-h32, capacity-h8x8, capacity-h64, capacity-h16x16, activation-relu, activation-gelu, norm-layernorm, norm-batchnorm, init-he, init-plain | 0 | 4/4 | not checked |

## Raw scorer output

### given state: negative control `no-adaptive-scaling` already applied

```
submission score: 82.1/100 (tier=core; NOT run: capacity-h32, capacity-h8x8, capacity-h64, capacity-h16x16, activation-relu, activation-gelu, norm-layernorm, norm-batchnorm, init-he, init-plain) (151/184 checks, exit 1)
  FAIL main: best.name: expected adam_reproduction, got sgd_control
  FAIL main: trial[adam_reproduction].test_loss: expected 0.20216034, got 0.4646439
  FAIL main: trial[adam_regularized].test_loss: expected 0.31407811, got 0.44953644
  FAIL optimizers: trial[adam].test_loss: expected 0.12346246, got 0.22236247
  FAIL optimizers: trial[adam].epochs_to_target: expected 33, got None
  FAIL optimizers: trial[adam_no_bias_correction].test_loss: expected 0.12187267, got 0.33155543
  FAIL optimizers: trial[adam_no_bias_correction].epochs: expected 65, got 120
  FAIL optimizers: trial[adam_no_bias_correction].epochs_to_target: expected 13, got None
  FAIL ablation-adam-no-first-moment: trial[adam].test_loss: expected 0.12346246, got 0.22236247
  FAIL ablation-adam-no-first-moment: trial[adam].epochs_to_target: expected 33, got None
  FAIL ablation-adam-no-first-moment: trial[adam_beta1_0].test_loss: expected 0.12646126, got 0.23420879
  FAIL ablation-adam-no-first-moment: trial[adam_beta1_0].epochs_to_target: expected 61, got None
  FAIL ademamix: trial[adamw].test_loss: expected 0.12255737, got 0.17808045
  FAIL ademamix: trial[adamw].epochs: expected 72, got 120
  FAIL ademamix: trial[adamw].epochs_to_target: expected 23, got None
  FAIL optimizers-mlp: trial[adam].test_accuracy: expected 0.93, got 0.935
  FAIL optimizers-mlp: trial[adam].test_loss: expected 0.12363451, got 0.12721656
  FAIL optimizers-mlp: trial[adam].epochs_to_target: expected 36, got 56
  FAIL ademamix-mlp: trial[adamw].test_accuracy: expected 0.93, got 0.935
  FAIL ademamix-mlp: trial[adamw].test_loss: expected 0.12697878, got 0.13640149
  FAIL ademamix-mlp: trial[adamw].epochs_to_target: expected 62, got None
  FAIL schedule-free: best.name: expected adamw_constant, got schedule_free_adamw
  FAIL schedule-free: trial[adamw_cosine].test_accuracy: expected 0.935, got 0.93
  FAIL schedule-free: trial[adamw_cosine].test_loss: expected 0.12381987, got 0.23029594
  FAIL schedule-free: trial[adamw_cosine].epochs_to_target: expected 80, got None
  FAIL schedule-free: trial[adamw_constant].test_loss: expected 0.12228349, got 0.19192348
  FAIL schedule-free: trial[adamw_constant].epochs_to_target: expected 70, got None
  FAIL schedule-free-mlp: best.name: expected adamw_constant, got sgd_cosine
  FAIL schedule-free-mlp: trial[adamw_cosine].test_loss: expected 0.12699107, got 0.13997714
  FAIL schedule-free-mlp: trial[adamw_cosine].epochs_to_target: expected 23, got None
  FAIL schedule-free-mlp: trial[adamw_constant].test_accuracy: expected 0.93, got 0.935
  FAIL schedule-free-mlp: trial[adamw_constant].test_loss: expected 0.12501296, got 0.12790861
  FAIL schedule-free-mlp: trial[adamw_constant].epochs_to_target: expected 22, got 193

TASK RESULT: FAIL
```

### recovered: defect undone from the failing assertion alone

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
