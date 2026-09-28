# AutoResearch Lite 实验报告

- 任务：AdEMAMix convergence speed against AdamW and momentum on a fixed synthetic task
- 论文：AdEMAMix: A Smarter Learning Rate Schedule for Adam
- 论文标识：arXiv:2409.03137
- 假设：AdEMAMix's slow EMA, mixed in with a growing coefficient, should reach a training-loss target in fewer epochs than AdamW at a matched budget. Each arm - including the warmup length that only AdEMAMix has - is tuned by the same rule used for the earlier optimizer suite: lowest final training loss inside the grid, ties to the smaller value.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`8a7b11ae97404cbcbf8874ec5481617b4e28df7c55a736a69cd98f78fe95972f`

## 最优方案

`ademamix_tuned`：主指标 `epochs_to_target` = **8**，测试准确率 **95.00%**，测试损失 `0.10510392`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| ademamix_tuned | 95.00% | 0.10510392 | 120 | 8 | 123.962 |
| adamw | 95.00% | 0.10519771 | 120 | 8 | 123.528 |
| ademamix_no_slow_ema | 95.00% | 0.10519771 | 120 | 8 | 124.833 |
| sgd_momentum | 95.00% | 0.10815505 | 120 | 13 | 127.525 |
| ademamix_paper_warmups | 95.00% | 0.1107083 | 120 | 38 | 126.641 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
