# AutoResearch Lite 实验报告

- 任务：capacity check, hidden [8,8]: does depth change the answers that width did not?
- 论文：Cross-paper capacity check (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-check
- 假设：Same capacity question as the [32] run, for a two-layer [8,8] network: do the directions survive a change of depth as well as width, and does the train-loss ranking continue to diverge from the test-loss ranking as capacity grows?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`b93d0ab61afed7b2a51cdb0505946aa85f9aeb50fad6ad1617710d4b8279829b`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.123983**，测试准确率 **95.00%**，测试损失 `0.12398257`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 95.00% | 0.12398257 | 200 | 10 | 7761.872 |
| schedule_free_adamw | 95.50% | 0.15673377 | 200 | 4 | 8153.009 |
| adamw_cosine | 94.50% | 0.18945186 | 200 | 4 | 8034.44 |
| adamw_constant | 92.50% | 0.21925963 | 200 | 4 | 8170.187 |
| adam | 92.50% | 0.21925963 | 200 | 4 | 8238.076 |
| ademamix | 92.50% | 0.22358174 | 200 | 4 | 8019.322 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
