# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [64]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Pre-registered in docs/capacity-expansion-preregistration.md before this run: AdaGrad keeps strengthening (H1), the schedule-free architecture effect continues (H2), AdEMAMix still has no advantage (H3), train/test divergence grows (H4), the noise-correlation claim holds (H5), Adam is still not the fastest (H6).
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`3996c5818b89e2de77e2f200b3046b5781bd7c7babcee81a25d46ba04a8b0160`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.122571**，测试准确率 **94.50%**，测试损失 `0.12257057`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 94.50% | 0.12257057 | 200 | 8 | 18546.344 |
| adagrad | 94.00% | 0.12416088 | 200 | 4 | 18545.156 |
| adamw_cosine | 93.50% | 0.13062828 | 200 | 45 | 18506.283 |
| adamw_constant | 93.00% | 0.13453496 | 200 | 44 | 18518.15 |
| adam | 93.00% | 0.13453496 | 200 | 44 | 18712.483 |
| ademamix | 93.00% | 0.13519817 | 200 | 44 | 19174.935 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
