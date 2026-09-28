# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with GELU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Same pre-registered A1-A3 as the ReLU run, with GELU instead of tanh: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should survive the change of activation.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`1c605a769752387f357728178fd7965d27566f4a6edd2bed817af2831cbe666e`

## 最优方案

`adamw_cosine`：主指标 `test_loss` = **0.081683**，测试准确率 **98.00%**，测试损失 `0.0816826`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_cosine | 98.00% | 0.0816826 | 200 | 5 | 9838.021 |
| ademamix | 98.00% | 0.08193332 | 200 | 15 | 9918.42 |
| adamw_constant | 98.00% | 0.08198748 | 200 | 15 | 9829.527 |
| adam | 98.00% | 0.08198748 | 200 | 15 | 9894.915 |
| adagrad | 98.00% | 0.08284631 | 200 | 14 | 9835.619 |
| schedule_free_adamw | 98.00% | 0.08345792 | 200 | 31 | 9984.422 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
