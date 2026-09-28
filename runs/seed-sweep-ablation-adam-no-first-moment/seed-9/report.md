# AutoResearch Lite 实验报告

- 任务：T-ADAM-01C ablation: what does Adam's first moment actually buy on this task?
- 论文：Adam (Kingma & Ba 2014) - momentum ablation on the pinned optimizer suite
- 论文标识：internal-ablation-first-moment
- 假设：PRE-REGISTERED BEFORE THE RUN. With both arms at the learning rate tuned for Adam in examples/optimizers.json (0.4) and the same 120-epoch budget and 0.16 target, removing the first moment (beta1 = 0, so the update collapses to g / (sqrt(v_hat) + eps) - a sign-like step) reaches the target in FEWER epochs but ends at a WORSE final test loss than the default Adam (beta1 = 0.9). Reasoning: the sign-like step is larger early, but the averaged first moment is the part that survives gradient noise, and this task's floor is what the recent capacity and normalisation work kept finding to be the harder number. Refuted if beta1 = 0 is slower to the target, or if it ends at a better final test loss. Matched-rate on purpose: re-tuning each arm would turn a one-line ablation into a second tuning study, and the grid is not re-swept (listed as a limitation in the record).
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`09c96a6e67bc27769b77738a00429a148a0a4a3469e1b23194cda855e13d96d9`

## 最优方案

`adam`：主指标 `epochs_to_target` = **19**，测试准确率 **93.00%**，测试损失 `0.14397553`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adam | 93.00% | 0.14397553 | 120 | 19 | 154.02 |
| adam_beta1_0 | 93.00% | 0.14581899 | 120 | 34 | 148.593 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.16` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
