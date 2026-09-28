# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with GELU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Same pre-registered A1-A3 as the ReLU run, with GELU instead of tanh: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should survive the change of activation.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`fe512ec192dc493e0363865239506d2c00d23dcc6840ce9069e20c6fb9bd670f`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.128227**，测试准确率 **95.00%**，测试损失 `0.12822683`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 95.00% | 0.12822683 | 200 | 11 | 9212.469 |
| adamw_constant | 95.00% | 0.12825456 | 200 | 16 | 9929.077 |
| adam | 95.00% | 0.12825456 | 200 | 16 | 9337.842 |
| ademamix | 95.00% | 0.12861173 | 200 | 16 | 9251.729 |
| schedule_free_adamw | 95.50% | 0.13241967 | 200 | 30 | 9303.307 |
| adamw_cosine | 94.50% | 0.13747814 | 200 | 6 | 10240.934 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
