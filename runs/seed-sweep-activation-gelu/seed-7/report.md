# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with GELU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Same pre-registered A1-A3 as the ReLU run, with GELU instead of tanh: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should survive the change of activation.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`15299dc615ac3b83250dc80e787222dea6481cd0a0f0b2ecbd6096e66e89b62b`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.122565**，测试准确率 **93.50%**，测试损失 `0.12256457`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.50% | 0.12256457 | 200 | 33 | 8968.717 |
| schedule_free_adamw | 93.50% | 0.12273812 | 200 | 49 | 8927.518 |
| adamw_constant | 93.50% | 0.12305048 | 200 | 25 | 9098.959 |
| adam | 93.50% | 0.12305048 | 200 | 25 | 8996.091 |
| ademamix | 93.50% | 0.12317559 | 200 | 25 | 8863.856 |
| adamw_cosine | 93.50% | 0.12437396 | 200 | 8 | 9223.238 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
