# AutoResearch Lite 实验报告

- 任务：coarse learning-rate sweep used to tune each optimizer before the head-to-head comparison
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：Each optimizer family has its own usable learning-rate range; comparing families at a single hand-picked rate would compare tuning luck rather than the update rules.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`65094f8ff2ad2f1812ece3abf1f37b9e6f01afebfbfcdcb509db9493d0c5eaa4`

## 最优方案

`adagrad_lr4.00`：主指标 `epochs_to_target` = **2**，测试准确率 **93.50%**，测试损失 `0.12246563`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad_lr4.00 | 93.50% | 0.12246563 | 120 | 2 | 124.284 |
| adam_nbc_lr0.40 | 93.50% | 0.12253432 | 120 | 2 | 125.885 |
| adagrad_lr2.00 | 93.50% | 0.12531898 | 120 | 2 | 128.147 |
| rmsprop_lr0.40 | 94.00% | 0.11874004 | 120 | 4 | 125.697 |
| adam_nbc_lr0.15 | 93.50% | 0.12187267 | 65 | 5 | 68.646 |
| adagrad_lr1.00 | 93.50% | 0.13675906 | 120 | 6 | 151.784 |
| sgd_momentum_lr0.80 | 93.50% | 0.123455 | 120 | 7 | 128.841 |
| adam_lr0.40 | 93.50% | 0.12346246 | 120 | 7 | 128.193 |
| rmsprop_lr0.20 | 93.00% | 0.12431982 | 120 | 10 | 130.095 |
| adam_lr0.25 | 93.50% | 0.12844443 | 120 | 11 | 127.965 |
| sgd_momentum_lr0.40 | 93.00% | 0.12994884 | 120 | 11 | 129.011 |
| sgd_momentum_lr0.20 | 94.00% | 0.14444219 | 120 | 17 | 128.483 |
| adagrad_lr0.50 | 93.50% | 0.1678067 | 120 | 17 | 130.015 |
| adam_lr0.15 | 93.50% | 0.14145737 | 120 | 19 | 135.273 |
| rmsprop_lr0.10 | 93.50% | 0.12910914 | 120 | 23 | 134.2 |
| sgd_momentum_lr0.10 | 94.00% | 0.16995618 | 120 | 29 | 128.346 |
| adam_lr0.08 | 93.50% | 0.17371239 | 120 | 37 | 136.642 |
| sgd_lr0.60 | 94.00% | 0.20381571 | 120 | 46 | 125.878 |
| rmsprop_lr0.05 | 93.50% | 0.17089443 | 120 | 51 | 131.903 |
| sgd_momentum_lr0.05 | 94.00% | 0.21036346 | 120 | 53 | 126.45 |
| adagrad_lr0.20 | 93.50% | 0.25751043 | 120 | 82 | 126.102 |
| sgd_lr0.30 | 93.50% | 0.25706848 | 120 | 92 | 129.261 |
| adam_lr0.03 | 94.00% | 0.27537688 | 120 | 110 | 133.918 |
| rmsprop_lr0.02 | 93.50% | 0.30063486 | 120 | 未达标 | 127.888 |
| baseline | 93.50% | 0.33170476 | 120 | 未达标 | 128.285 |
| sgd_lr0.05 | 93.50% | 0.47952919 | 120 | 未达标 | 120.659 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.3` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
