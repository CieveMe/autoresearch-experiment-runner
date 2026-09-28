# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [64]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Pre-registered in docs/capacity-expansion-preregistration.md before this run: AdaGrad keeps strengthening (H1), the schedule-free architecture effect continues (H2), AdEMAMix still has no advantage (H3), train/test divergence grows (H4), the noise-correlation claim holds (H5), Adam is still not the fastest (H6).
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`eb7953047679165819bb0e536b9885832306c4d4319aabca9d119f4ea2a282d4`

## 最优方案

`ademamix`：主指标 `test_loss` = **0.077684**，测试准确率 **97.50%**，测试损失 `0.07768366`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| ademamix | 97.50% | 0.07768366 | 200 | 24 | 18902.354 |
| adamw_constant | 97.50% | 0.0779946 | 200 | 24 | 19036.917 |
| adam | 97.50% | 0.0779946 | 200 | 24 | 17967.384 |
| adamw_cosine | 97.50% | 0.08064984 | 200 | 25 | 17961.082 |
| schedule_free_adamw | 96.00% | 0.08339573 | 200 | 3 | 18085.523 |
| adagrad | 98.00% | 0.08347175 | 200 | 5 | 18824.588 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
