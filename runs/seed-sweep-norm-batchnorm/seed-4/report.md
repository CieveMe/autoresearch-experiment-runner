# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], batchnorm on the hidden pre-activations (Xavier init): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (batchnorm on the hidden pre-activations (Xavier init)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`4d9dc8476032d2b32bc3bcfeb1d5605497c8de8fa174b33791e3c39fcca9c237`

## 最优方案

`adamw_constant`：主指标 `test_loss` = **0.083544**，测试准确率 **96.50%**，测试损失 `0.0835445`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_constant | 96.50% | 0.0835445 | 200 | 7 | 10946.288 |
| adam | 96.50% | 0.0835445 | 200 | 7 | 12485.71 |
| ademamix | 96.50% | 0.08354893 | 200 | 7 | 12624.174 |
| adamw_cosine | 96.50% | 0.0835687 | 200 | 7 | 11000.823 |
| schedule_free_adamw | 96.50% | 0.08369922 | 200 | 3 | 12970.562 |
| adagrad | 97.50% | 0.08380817 | 200 | 4 | 12048.206 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
