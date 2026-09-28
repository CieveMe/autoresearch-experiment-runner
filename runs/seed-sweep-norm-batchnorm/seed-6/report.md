# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], batchnorm on the hidden pre-activations (Xavier init): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (batchnorm on the hidden pre-activations (Xavier init)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`8290ab2f7e84e74cbd9a628bacc7e999e922faae3b746a44111c6ceceb0e496f`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.191398**，测试准确率 **92.50%**，测试损失 `0.19139783`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 92.50% | 0.19139783 | 200 | 2 | 11142.64 |
| adagrad | 93.00% | 0.19211937 | 200 | 4 | 11541.697 |
| adamw_constant | 92.00% | 0.19271318 | 200 | 2 | 11370.957 |
| adam | 92.00% | 0.19271318 | 200 | 2 | 11335.286 |
| ademamix | 92.00% | 0.19275804 | 200 | 2 | 14730.184 |
| adamw_cosine | 92.50% | 0.19395374 | 200 | 2 | 11659.532 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
