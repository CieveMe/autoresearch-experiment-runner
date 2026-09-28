# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with GELU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Same pre-registered A1-A3 as the ReLU run, with GELU instead of tanh: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should survive the change of activation.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`c5db8c4399d4a8442fb885a102f899cb84e55a38ec8c9d10ae83f7973a7ad9d5`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.123784**，测试准确率 **94.00%**，测试损失 `0.12378365`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 94.00% | 0.12378365 | 200 | 23 | 10304.645 |
| schedule_free_adamw | 94.00% | 0.12380516 | 200 | 41 | 12832.319 |
| adamw_cosine | 94.50% | 0.1244985 | 200 | 7 | 9840.587 |
| adamw_constant | 94.00% | 0.12457411 | 200 | 21 | 9812.747 |
| adam | 94.00% | 0.12457411 | 200 | 21 | 10093.6 |
| ademamix | 94.00% | 0.12464836 | 200 | 21 | 10132.391 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
