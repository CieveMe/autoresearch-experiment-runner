# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with GELU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Same pre-registered A1-A3 as the ReLU run, with GELU instead of tanh: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should survive the change of activation.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`626d84e18927c8527659d04f5a1baa314be5262a922f5ab290cca0c3804f9744`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.159942**，测试准确率 **94.50%**，测试损失 `0.1599419`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 94.50% | 0.1599419 | 200 | 13 | 8872.709 |
| schedule_free_adamw | 94.50% | 0.16178401 | 200 | 33 | 8970.721 |
| adamw_constant | 94.00% | 0.16216111 | 200 | 18 | 8907.553 |
| adam | 94.00% | 0.16216111 | 200 | 18 | 8918.321 |
| ademamix | 94.00% | 0.16243147 | 200 | 18 | 8927.301 |
| adamw_cosine | 92.50% | 0.17414973 | 200 | 6 | 8982.333 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
