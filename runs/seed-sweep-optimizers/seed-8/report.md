# AutoResearch Lite 实验报告

- 任务：optimizer convergence speed on a fixed synthetic task
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：At a matched epoch budget, and with each optimizer family tuned by the same coarse learning-rate sweep, Adam reaches a training-loss target close to the converged floor in as few epochs as SGD, SGD with momentum, AdaGrad and RMSProp — and disabling Adam's bias correction changes when the target is reached.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`9daa598ba57fb59c8b8018fac3024abce04752f7885349158acbcb14c4820388`

## 最优方案

`adagrad`：主指标 `epochs_to_target` = **3**，测试准确率 **94.00%**，测试损失 `0.15537609`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 94.00% | 0.15537609 | 120 | 3 | 126.698 |
| adam_no_bias_correction | 94.00% | 0.15732041 | 120 | 9 | 126.9 |
| sgd_momentum | 94.00% | 0.15461732 | 120 | 15 | 126.111 |
| adam | 94.00% | 0.15508106 | 120 | 19 | 130.751 |
| rmsprop | 93.00% | 0.15707863 | 120 | 36 | 129.331 |
| baseline | 93.50% | 0.22834292 | 120 | 未达标 | 125.875 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.16` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
