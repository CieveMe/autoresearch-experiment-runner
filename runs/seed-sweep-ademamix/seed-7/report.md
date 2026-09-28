# AutoResearch Lite 实验报告

- 任务：AdEMAMix convergence speed against AdamW and momentum on a fixed synthetic task
- 论文：AdEMAMix: A Smarter Learning Rate Schedule for Adam
- 论文标识：arXiv:2409.03137
- 假设：AdEMAMix's slow EMA, mixed in with a growing coefficient, should reach a training-loss target in fewer epochs than AdamW at a matched budget. Each arm - including the warmup length that only AdEMAMix has - is tuned by the same rule used for the earlier optimizer suite: lowest final training loss inside the grid, ties to the smaller value.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`6b725ca27e76bcd32803f77a78bb31add12c40aae2ba622aebb1e55ce1bf369c`

## 最优方案

`ademamix_tuned`：主指标 `epochs_to_target` = **23**，测试准确率 **93.50%**，测试损失 `0.1220232`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| ademamix_tuned | 93.50% | 0.1220232 | 97 | 23 | 143.494 |
| adamw | 93.50% | 0.12255737 | 72 | 23 | 105.694 |
| ademamix_no_slow_ema | 93.50% | 0.12255737 | 72 | 23 | 121.335 |
| sgd_momentum | 93.50% | 0.123455 | 120 | 47 | 185.585 |
| ademamix_paper_warmups | 93.50% | 0.12415636 | 120 | 105 | 186.251 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
