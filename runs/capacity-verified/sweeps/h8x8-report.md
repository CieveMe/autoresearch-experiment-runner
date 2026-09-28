# AutoResearch Lite 实验报告

- 任务：capacity check, hidden [8,8]: tuning sweep for the three claims
- 论文：Cross-paper capacity check (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-check
- 假设：Same capacity question as the [32] sweep, for a two-layer [8,8] network: does the ranking of Adam, AdEMAMix and schedule-free against their baselines survive a change of depth as well as width?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`3375809ea6a258fcbdae16280ebf55ae258c81c15c55353bde26f337cd48bec0`

## 最优方案

`adagrad_lr1.0`：主指标 `test_loss` = **0.113150**，测试准确率 **94.00%**，测试损失 `0.11314961`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad_lr1.0 | 94.00% | 0.11314961 | 200 | 未达标 | 8561.294 |
| sgd_momentum_lr1.0 | 93.50% | 0.12332899 | 200 | 未达标 | 8530.765 |
| ademamix_lr0.1 | 93.00% | 0.12341788 | 200 | 未达标 | 6779.715 |
| adamw_constant_lr0.1 | 93.00% | 0.12419346 | 200 | 未达标 | 8837.618 |
| adam_lr0.1 | 93.00% | 0.12419346 | 200 | 未达标 | 8493.406 |
| schedule_free_adamw_lr0.3 | 93.50% | 0.1246872 | 200 | 未达标 | 8548.044 |
| sgd_momentum_lr0.3 | 93.50% | 0.12667529 | 200 | 未达标 | 7710.46 |
| sgd_momentum_lr0.6 | 93.00% | 0.12669306 | 200 | 未达标 | 8785.772 |
| adagrad_lr0.1 | 93.50% | 0.12680418 | 200 | 未达标 | 8784.97 |
| ademamix_lr0.03 | 93.00% | 0.12688385 | 200 | 未达标 | 7915.844 |
| adamw_constant_lr0.03 | 93.00% | 0.12698907 | 200 | 未达标 | 8902.655 |
| adam_lr0.03 | 93.00% | 0.12698907 | 200 | 未达标 | 8403.675 |
| schedule_free_adamw_lr0.03 | 93.00% | 0.12728228 | 200 | 未达标 | 7194.0 |
| schedule_free_adamw_lr0.1 | 93.00% | 0.12749905 | 200 | 未达标 | 7723.659 |
| adamw_cosine_lr0.1 | 93.50% | 0.12791534 | 200 | 未达标 | 6482.431 |
| adamw_cosine_lr0.03 | 93.00% | 0.12818543 | 200 | 未达标 | 8640.581 |
| adagrad_lr0.3 | 93.00% | 0.13150835 | 200 | 未达标 | 9006.365 |
| adamw_cosine_lr0.3 | 93.50% | 0.13495187 | 200 | 未达标 | 8951.512 |
| adamw_constant_lr0.3 | 93.50% | 0.14107068 | 200 | 未达标 | 8957.905 |
| adam_lr0.3 | 93.50% | 0.14107068 | 200 | 未达标 | 8682.931 |
| ademamix_lr0.3 | 93.50% | 0.14184666 | 200 | 未达标 | 8563.88 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
