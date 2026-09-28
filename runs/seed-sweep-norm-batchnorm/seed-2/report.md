# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], batchnorm on the hidden pre-activations (Xavier init): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (batchnorm on the hidden pre-activations (Xavier init)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`cda794341d39a0476be6706fb9a82dcdcc1bba9a6b3d44add21a9cf6cea3ff37`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.132735**，测试准确率 **93.50%**，测试损失 `0.13273461`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 93.50% | 0.13273461 | 200 | 3 | 16636.454 |
| adagrad | 93.50% | 0.13445389 | 200 | 5 | 17108.571 |
| adamw_cosine | 94.00% | 0.13672081 | 200 | 3 | 18252.43 |
| adamw_constant | 93.50% | 0.13867282 | 200 | 3 | 19184.693 |
| adam | 93.50% | 0.13867282 | 200 | 3 | 16357.71 |
| ademamix | 93.50% | 0.13881278 | 200 | 3 | 17264.138 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
