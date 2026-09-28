# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with ReLU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Pre-registered A1-A3: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should not depend on the hidden activation. This suite is the tanh [32] suite with ReLU instead, same budget, every arm retuned.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`218e389ff08ecd2f4065c207bc8496184764fc1ae1a12a3a897c687147b126b0`

## 最优方案

`ademamix`：主指标 `test_loss` = **0.115833**，测试准确率 **94.50%**，测试损失 `0.11583264`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| ademamix | 94.50% | 0.11583264 | 200 | 19 | 8253.771 |
| adamw_constant | 94.50% | 0.11776315 | 200 | 19 | 8236.764 |
| adam | 94.50% | 0.11776315 | 200 | 19 | 8215.759 |
| adagrad | 94.50% | 0.12100515 | 200 | 20 | 8277.836 |
| schedule_free_adamw | 94.50% | 0.12413778 | 200 | 39 | 8262.776 |
| adamw_cosine | 94.50% | 0.12582024 | 200 | 6 | 8239.529 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
