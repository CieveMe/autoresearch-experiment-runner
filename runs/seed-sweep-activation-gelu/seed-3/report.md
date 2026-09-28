# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with GELU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Same pre-registered A1-A3 as the ReLU run, with GELU instead of tanh: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should survive the change of activation.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`2d930366fee45cb184d01d6a32f8b07b7eb5c39e17fe621e482f8cdbe44817bd`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.126733**，测试准确率 **93.50%**，测试损失 `0.12673347`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.50% | 0.12673347 | 200 | 26 | 9831.716 |
| adamw_constant | 93.50% | 0.12705892 | 200 | 22 | 9900.248 |
| adam | 93.50% | 0.12705892 | 200 | 22 | 9816.847 |
| adamw_cosine | 93.50% | 0.1273294 | 200 | 8 | 9933.639 |
| ademamix | 93.50% | 0.12733278 | 200 | 22 | 9934.015 |
| schedule_free_adamw | 93.50% | 0.12898189 | 200 | 45 | 10053.968 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
