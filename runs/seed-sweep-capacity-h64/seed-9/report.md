# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [64]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Pre-registered in docs/capacity-expansion-preregistration.md before this run: AdaGrad keeps strengthening (H1), the schedule-free architecture effect continues (H2), AdEMAMix still has no advantage (H3), train/test divergence grows (H4), the noise-correlation claim holds (H5), Adam is still not the fastest (H6).
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`71d1fb4718532c798663fd58bc6d90554b523db89eab4bb87c18e2a3c3c35b38`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.145405**，测试准确率 **93.50%**，测试损失 `0.14540455`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.50% | 0.14540455 | 200 | 4 | 18917.72 |
| schedule_free_adamw | 92.00% | 0.14876055 | 200 | 4 | 18814.639 |
| adamw_cosine | 93.00% | 0.15425702 | 200 | 3 | 18952.509 |
| adamw_constant | 94.00% | 0.16832692 | 200 | 3 | 19023.259 |
| adam | 94.00% | 0.16832692 | 200 | 3 | 18371.493 |
| ademamix | 94.00% | 0.16956499 | 200 | 3 | 18916.218 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
