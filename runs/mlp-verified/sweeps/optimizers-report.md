# AutoResearch Lite 实验报告

- 任务：learning-rate sweep for the optimizer family on the MLP trainer
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：The two-parameter logistic head may be too small to separate the optimizer families. This sweep retunes every family for the two-layer MLP so the comparison is not carried over from a different model.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`08245013358fc8e2fba6db5e003cf3ee68eadf2cad5bb3801c1c953b101a0420`

## 最优方案

`rmsprop_lr0.1`：主指标 `test_loss` = **0.121178**，测试准确率 **94.00%**，测试损失 `0.12117824`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| rmsprop_lr0.1 | 94.00% | 0.12117824 | 120 | 未达标 | 1343.827 |
| adam_lr1.0 | 93.00% | 0.12363451 | 120 | 未达标 | 1361.194 |
| adam_lr0.03 | 93.50% | 0.12394506 | 120 | 未达标 | 1356.315 |
| adagrad_lr0.3 | 93.50% | 0.12410226 | 120 | 未达标 | 1390.638 |
| sgd_lr1.0 | 93.50% | 0.12460319 | 120 | 未达标 | 1390.449 |
| sgd_momentum_lr0.1 | 93.50% | 0.12463694 | 120 | 未达标 | 1318.73 |
| sgd_momentum_lr0.3 | 93.50% | 0.12505434 | 120 | 未达标 | 1319.396 |
| sgd_momentum_lr1.0 | 93.00% | 0.12544684 | 120 | 未达标 | 1383.913 |
| adam_lr0.1 | 93.50% | 0.12573518 | 120 | 未达标 | 1336.265 |
| adagrad_lr0.1 | 93.50% | 0.12573774 | 120 | 未达标 | 1409.761 |
| rmsprop_lr0.01 | 93.50% | 0.12591145 | 120 | 未达标 | 1373.188 |
| adam_lr0.3 | 93.00% | 0.12697878 | 120 | 未达标 | 1419.991 |
| adagrad_lr1.0 | 93.50% | 0.12775166 | 120 | 未达标 | 1446.966 |
| rmsprop_lr0.03 | 93.00% | 0.12958927 | 120 | 未达标 | 1404.858 |
| sgd_momentum_lr0.03 | 93.00% | 0.13708485 | 120 | 未达标 | 1306.911 |
| sgd_lr0.3 | 93.50% | 0.13979508 | 120 | 未达标 | 1317.664 |
| rmsprop_lr0.3 | 93.50% | 0.14052265 | 120 | 未达标 | 1308.624 |
| adam_lr0.01 | 93.00% | 0.14252384 | 120 | 未达标 | 1356.443 |
| adagrad_lr0.03 | 94.00% | 0.21120326 | 120 | 未达标 | 1341.702 |
| sgd_lr0.1 | 93.50% | 0.21373729 | 120 | 未达标 | 1342.782 |
| sgd_momentum_lr0.01 | 94.00% | 0.21466201 | 120 | 未达标 | 1299.354 |
| sgd_lr0.03 | 93.50% | 0.38612865 | 120 | 未达标 | 1315.008 |
| adagrad_lr0.01 | 93.50% | 0.40994631 | 120 | 未达标 | 1317.084 |
| sgd_lr0.01 | 90.00% | 0.53410282 | 120 | 未达标 | 1327.526 |
| rmsprop_lr1.0 | 89.00% | 0.56305833 | 120 | 未达标 | 1388.99 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
