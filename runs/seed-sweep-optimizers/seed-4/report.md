# AutoResearch Lite 实验报告

- 任务：optimizer convergence speed on a fixed synthetic task
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：At a matched epoch budget, and with each optimizer family tuned by the same coarse learning-rate sweep, Adam reaches a training-loss target close to the converged floor in as few epochs as SGD, SGD with momentum, AdaGrad and RMSProp — and disabling Adam's bias correction changes when the target is reached.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`af9108a19d1b5de0eb318cad0864cc609204bbab2f885448a013106c9e33b589`

## 最优方案

`adagrad`：主指标 `epochs_to_target` = **3**，测试准确率 **98.00%**，测试损失 `0.08440685`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 98.00% | 0.08440685 | 120 | 3 | 128.135 |
| adam_no_bias_correction | 98.00% | 0.08308862 | 120 | 10 | 126.708 |
| sgd_momentum | 98.00% | 0.08537823 | 120 | 16 | 123.772 |
| adam | 98.00% | 0.08589934 | 120 | 22 | 131.771 |
| rmsprop | 97.50% | 0.08524261 | 120 | 42 | 129.049 |
| baseline | 97.50% | 0.16747489 | 120 | 未达标 | 127.621 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.16` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
