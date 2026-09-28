# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with ReLU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Pre-registered A1-A3: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should not depend on the hidden activation. This suite is the tanh [32] suite with ReLU instead, same budget, every arm retuned.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`1b0a51a4d466405fb837a5c8bc4bd8fa764e5c9bc0085a98a3920657a59e4441`

## 最优方案

`ademamix`：主指标 `test_loss` = **0.140995**，测试准确率 **92.00%**，测试损失 `0.14099509`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| ademamix | 92.00% | 0.14099509 | 200 | 17 | 8199.427 |
| adamw_constant | 92.00% | 0.14113877 | 200 | 17 | 8138.786 |
| adam | 92.00% | 0.14113877 | 200 | 17 | 8174.517 |
| adagrad | 92.00% | 0.14174625 | 200 | 16 | 8384.112 |
| schedule_free_adamw | 92.50% | 0.14216491 | 200 | 35 | 8170.596 |
| adamw_cosine | 92.00% | 0.14768928 | 200 | 6 | 8309.32 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
