# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [64]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Pre-registered in docs/capacity-expansion-preregistration.md before this run: AdaGrad keeps strengthening (H1), the schedule-free architecture effect continues (H2), AdEMAMix still has no advantage (H3), train/test divergence grows (H4), the noise-correlation claim holds (H5), Adam is still not the fastest (H6).
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`feb14e13fc44805cb9db5b50ebc0a33e2531929c7347eab1d653690b00e557a1`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.131131**，测试准确率 **95.00%**，测试损失 `0.13113051`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 95.00% | 0.13113051 | 200 | 4 | 18275.246 |
| schedule_free_adamw | 94.50% | 0.13484127 | 200 | 3 | 18654.357 |
| adamw_cosine | 95.50% | 0.13670867 | 200 | 4 | 18140.933 |
| adamw_constant | 95.50% | 0.14958848 | 200 | 4 | 18213.24 |
| adam | 95.50% | 0.14958848 | 200 | 4 | 18531.201 |
| ademamix | 95.50% | 0.15100921 | 200 | 4 | 18660.533 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
