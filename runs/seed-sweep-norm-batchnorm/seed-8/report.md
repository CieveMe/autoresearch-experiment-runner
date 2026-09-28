# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], batchnorm on the hidden pre-activations (Xavier init): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (batchnorm on the hidden pre-activations (Xavier init)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`fc3df3f848620d77eb06eb1c33606506746ba77ef4005906af457fe80c28161d`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.161524**，测试准确率 **94.00%**，测试损失 `0.16152366`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 94.00% | 0.16152366 | 200 | 4 | 10763.069 |
| schedule_free_adamw | 94.00% | 0.16209657 | 200 | 2 | 10652.771 |
| adamw_cosine | 94.00% | 0.16365644 | 200 | 2 | 10565.909 |
| adamw_constant | 94.00% | 0.16408181 | 200 | 2 | 10569.387 |
| adam | 94.00% | 0.16408181 | 200 | 2 | 10629.395 |
| ademamix | 94.00% | 0.164156 | 200 | 2 | 10663.122 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
