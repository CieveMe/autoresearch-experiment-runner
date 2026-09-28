# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with GELU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Same pre-registered A1-A3 as the ReLU run, with GELU instead of tanh: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should survive the change of activation.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`5f341ce7e3f4db4c94678b48bf4143344fb6ed7da7626fa719f4c289496d6a4b`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.104608**，测试准确率 **95.50%**，测试损失 `0.10460779`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 95.50% | 0.10460779 | 200 | 12 | 9896.862 |
| ademamix | 95.50% | 0.10467608 | 200 | 18 | 9922.661 |
| adamw_constant | 95.50% | 0.10470321 | 200 | 18 | 9883.946 |
| adam | 95.50% | 0.10470321 | 200 | 18 | 9922.717 |
| schedule_free_adamw | 95.50% | 0.10494353 | 200 | 30 | 10156.835 |
| adamw_cosine | 95.50% | 0.10494954 | 200 | 6 | 9987.647 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
