# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [64]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Pre-registered in docs/capacity-expansion-preregistration.md before this run: AdaGrad keeps strengthening (H1), the schedule-free architecture effect continues (H2), AdEMAMix still has no advantage (H3), train/test divergence grows (H4), the noise-correlation claim holds (H5), Adam is still not the fastest (H6).
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`09a3d95b6e18121b74189f025b83837a1a3e9c3d8811a9ebdefa62adb1351760`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.159836**，测试准确率 **94.00%**，测试损失 `0.15983617`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 94.00% | 0.15983617 | 200 | 4 | 18605.007 |
| schedule_free_adamw | 92.50% | 0.16828112 | 200 | 3 | 18680.547 |
| adamw_cosine | 93.00% | 0.19028869 | 200 | 28 | 18605.864 |
| adamw_constant | 93.00% | 0.20682161 | 200 | 28 | 18681.226 |
| adam | 93.00% | 0.20682161 | 200 | 28 | 18817.843 |
| ademamix | 93.00% | 0.20990173 | 200 | 28 | 19645.046 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
