# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with GELU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Same pre-registered A1-A3 as the ReLU run, with GELU instead of tanh: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should survive the change of activation.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`fd9fee05432384c260140fdaf7feb1fd4cf66c48c8718ee62f1b27e7e099548f`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.141254**，测试准确率 **92.00%**，测试损失 `0.14125401`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 92.00% | 0.14125401 | 200 | 37 | 9883.388 |
| adagrad | 92.00% | 0.14147221 | 200 | 19 | 9917.086 |
| ademamix | 92.00% | 0.141992 | 200 | 19 | 9898.195 |
| adamw_constant | 92.00% | 0.14199549 | 200 | 19 | 9744.322 |
| adam | 92.00% | 0.14199549 | 200 | 19 | 9886.103 |
| adamw_cosine | 92.00% | 0.1437796 | 200 | 6 | 10141.598 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
