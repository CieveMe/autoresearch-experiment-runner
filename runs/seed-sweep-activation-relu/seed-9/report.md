# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with ReLU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Pre-registered A1-A3: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should not depend on the hidden activation. This suite is the tanh [32] suite with ReLU instead, same budget, every arm retuned.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`63f20e13708709a8c6684423d6f7e8b60081d626151f663f607289dc1567b8c1`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.147002**，测试准确率 **93.50%**，测试损失 `0.1470018`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.50% | 0.1470018 | 200 | 14 | 8289.207 |
| schedule_free_adamw | 93.00% | 0.1487526 | 200 | 32 | 8360.83 |
| adamw_constant | 92.50% | 0.15063253 | 200 | 19 | 8279.227 |
| adam | 92.50% | 0.15063253 | 200 | 19 | 8219.235 |
| ademamix | 92.50% | 0.15108494 | 200 | 19 | 8262.388 |
| adamw_cosine | 93.00% | 0.15123409 | 200 | 7 | 8382.001 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
