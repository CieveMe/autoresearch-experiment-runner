# AutoResearch Lite 实验报告

- 任务：AdEMAMix convergence speed against AdamW and momentum on a fixed synthetic task
- 论文：AdEMAMix: A Smarter Learning Rate Schedule for Adam
- 论文标识：arXiv:2409.03137
- 假设：AdEMAMix's slow EMA, mixed in with a growing coefficient, should reach a training-loss target in fewer epochs than AdamW at a matched budget. Each arm - including the warmup length that only AdEMAMix has - is tuned by the same rule used for the earlier optimizer suite: lowest final training loss inside the grid, ties to the smaller value.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`b799e3347ae68bda871cd6716bbd46e4e2ec252feea12dc929d01511b4568544`

## 最优方案

`adamw`：主指标 `epochs_to_target` = **11**，测试准确率 **94.00%**，测试损失 `0.15747417`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw | 94.00% | 0.15747417 | 120 | 11 | 180.618 |
| ademamix_no_slow_ema | 94.00% | 0.15747417 | 120 | 11 | 186.379 |
| ademamix_tuned | 94.00% | 0.15794816 | 120 | 11 | 183.942 |
| sgd_momentum | 94.00% | 0.15461732 | 120 | 17 | 171.218 |
| ademamix_paper_warmups | 94.50% | 0.15707412 | 120 | 50 | 178.819 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
