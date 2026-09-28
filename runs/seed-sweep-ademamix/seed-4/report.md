# AutoResearch Lite 实验报告

- 任务：AdEMAMix convergence speed against AdamW and momentum on a fixed synthetic task
- 论文：AdEMAMix: A Smarter Learning Rate Schedule for Adam
- 论文标识：arXiv:2409.03137
- 假设：AdEMAMix's slow EMA, mixed in with a growing coefficient, should reach a training-loss target in fewer epochs than AdamW at a matched budget. Each arm - including the warmup length that only AdEMAMix has - is tuned by the same rule used for the earlier optimizer suite: lowest final training loss inside the grid, ties to the smaller value.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`7c7abfdac0f8ba157d32a58967c11c4ecb0ad7be690ccdb95ee7270a16dc2f0a`

## 最优方案

`ademamix_tuned`：主指标 `epochs_to_target` = **14**，测试准确率 **98.00%**，测试损失 `0.08328878`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| ademamix_tuned | 98.00% | 0.08328878 | 94 | 14 | 104.537 |
| adamw | 98.00% | 0.08332108 | 98 | 14 | 101.037 |
| ademamix_no_slow_ema | 98.00% | 0.08332108 | 98 | 14 | 139.419 |
| sgd_momentum | 98.00% | 0.08537823 | 120 | 20 | 162.389 |
| ademamix_paper_warmups | 97.50% | 0.08739029 | 120 | 66 | 121.836 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
