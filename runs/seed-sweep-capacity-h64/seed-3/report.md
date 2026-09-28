# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [64]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Pre-registered in docs/capacity-expansion-preregistration.md before this run: AdaGrad keeps strengthening (H1), the schedule-free architecture effect continues (H2), AdEMAMix still has no advantage (H3), train/test divergence grows (H4), the noise-correlation claim holds (H5), Adam is still not the fastest (H6).
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`caa72ae085a837315bb9386788ec4f276a1a33cc040e98d6d2ed9d6b4ed01981`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.126969**，测试准确率 **93.50%**，测试损失 `0.12696862`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.50% | 0.12696862 | 200 | 5 | 18770.042 |
| schedule_free_adamw | 94.00% | 0.13168457 | 200 | 4 | 17765.226 |
| adamw_cosine | 94.00% | 0.13632594 | 200 | 36 | 18616.204 |
| adamw_constant | 94.00% | 0.14139885 | 200 | 36 | 18372.798 |
| adam | 94.00% | 0.14139885 | 200 | 36 | 18627.937 |
| ademamix | 94.00% | 0.14235439 | 200 | 36 | 18365.538 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
