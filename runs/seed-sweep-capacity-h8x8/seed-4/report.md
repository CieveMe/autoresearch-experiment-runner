# AutoResearch Lite 实验报告

- 任务：capacity check, hidden [8,8]: does depth change the answers that width did not?
- 论文：Cross-paper capacity check (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-check
- 假设：Same capacity question as the [32] run, for a two-layer [8,8] network: do the directions survive a change of depth as well as width, and does the train-loss ranking continue to diverge from the test-loss ranking as capacity grows?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`531c0f68aa815749be921a0eb9870c07afe8a0844092e9eca6836ec6f790fdda`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.071734**，测试准确率 **97.50%**，测试损失 `0.07173358`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 97.50% | 0.07173358 | 200 | 5 | 7263.246 |
| adagrad | 97.50% | 0.08331469 | 200 | 12 | 7414.301 |
| adamw_cosine | 96.50% | 0.08433127 | 200 | 24 | 7658.045 |
| ademamix | 96.50% | 0.09868575 | 200 | 24 | 7459.643 |
| adamw_constant | 96.50% | 0.10140978 | 200 | 24 | 7690.243 |
| adam | 96.50% | 0.10140978 | 200 | 24 | 7309.21 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
