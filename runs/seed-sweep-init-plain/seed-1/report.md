# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], plain fixed-0.05 initialisation (no normalisation): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (plain fixed-0.05 initialisation (no normalisation)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`710fdd5f7f2160b2454b61d0eb62db43fc6b9b4a60e49f190563ad1cfe88b04d`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.118823**，测试准确率 **95.50%**，测试损失 `0.11882307`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 95.50% | 0.11882307 | 200 | 11 | 8004.106 |
| adamw_cosine | 95.50% | 0.11965942 | 200 | 7 | 7893.763 |
| adamw_constant | 95.00% | 0.12668641 | 200 | 3 | 7973.614 |
| adam | 95.00% | 0.12668641 | 200 | 3 | 7935.787 |
| ademamix | 95.00% | 0.12674021 | 200 | 3 | 7959.076 |
| adagrad | 94.00% | 0.1309484 | 200 | 14 | 8017.195 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
