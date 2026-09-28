# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], He initialisation (no normalisation): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (He initialisation (no normalisation)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`327563626702f487560e5aba7a047fffc38ca016c66faccb4335a5ec80eb462d`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.126796**，测试准确率 **95.00%**，测试损失 `0.12679563`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 95.00% | 0.12679563 | 200 | 3 | 8227.486 |
| adagrad | 94.50% | 0.13004898 | 200 | 17 | 8257.041 |
| adamw_constant | 93.50% | 0.13288191 | 200 | 17 | 8174.462 |
| adam | 93.50% | 0.13288191 | 200 | 17 | 8251.597 |
| adamw_cosine | 94.50% | 0.13296309 | 200 | 17 | 8181.41 |
| ademamix | 93.50% | 0.1333777 | 200 | 17 | 8028.536 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
