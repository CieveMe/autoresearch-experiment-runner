# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with GELU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Same pre-registered A1-A3 as the ReLU run, with GELU instead of tanh: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should survive the change of activation.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`29ddb2a1c49a7e31aaf7b1c108d991b6e00f311a3810eac199b342bc32c16b8e`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.122721**，测试准确率 **95.00%**，测试损失 `0.1227206`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 95.00% | 0.1227206 | 200 | 29 | 9930.707 |
| adagrad | 95.00% | 0.12275727 | 200 | 12 | 9930.474 |
| adamw_constant | 95.00% | 0.12453224 | 200 | 16 | 10097.78 |
| adam | 95.00% | 0.12453224 | 200 | 16 | 10173.741 |
| ademamix | 95.00% | 0.12461962 | 200 | 16 | 9971.801 |
| adamw_cosine | 95.00% | 0.12771383 | 200 | 5 | 10107.58 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
