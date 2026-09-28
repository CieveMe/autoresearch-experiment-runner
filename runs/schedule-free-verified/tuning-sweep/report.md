# AutoResearch Lite 实验报告

- 任务：tuning sweep for the schedule-free comparison (learning rate x schedule settings)
- 论文：Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages
- 论文标识：arXiv:2405.15682
- 假设：The paper's claim is that a schedule-free method matches a well-tuned cosine schedule without needing one. That claim is only testable if the cosine baseline is actually tuned, so both the learning rate and the minimum-learning-rate factor of the baseline get a grid, and the schedule-free arms get the same learning-rate grid.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`908dfc7a0ce54c60ca7fbdfc76e318e930cbf1200782f445ec2aa524a861bff9`

## 最优方案

`adamw_constant_lr0.4`：主指标 `test_loss` = **0.122283**，测试准确率 **93.50%**，测试损失 `0.12228349`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_constant_lr0.4 | 93.50% | 0.12228349 | 200 | 未达标 | 207.491 |
| adamw_cosine_lr0.4_min0.1 | 93.50% | 0.12381987 | 200 | 未达标 | 215.454 |
| schedule_free_adamw_lr0.4 | 93.50% | 0.12395906 | 200 | 未达标 | 215.058 |
| adamw_cosine_lr0.4_min0.0 | 93.50% | 0.12435706 | 196 | 未达标 | 195.644 |
| adamw_constant_lr0.2 | 93.50% | 0.12565338 | 200 | 未达标 | 207.087 |
| adamw_cosine_lr0.2_min0.1 | 93.00% | 0.13446028 | 200 | 未达标 | 218.899 |
| schedule_free_adamw_lr0.2 | 93.50% | 0.13625326 | 200 | 未达标 | 219.69 |
| adamw_cosine_lr0.2_min0.0 | 93.50% | 0.13673813 | 198 | 未达标 | 199.5 |
| adamw_constant_lr0.1 | 93.50% | 0.14008435 | 200 | 未达标 | 200.382 |
| adamw_cosine_lr0.1_min0.1 | 93.50% | 0.16346004 | 200 | 未达标 | 215.17 |
| schedule_free_adamw_lr0.1 | 93.50% | 0.16813225 | 200 | 未达标 | 214.431 |
| adamw_cosine_lr0.1_min0.0 | 93.50% | 0.16885404 | 199 | 未达标 | 199.258 |
| adamw_constant_lr0.05 | 93.50% | 0.17447888 | 200 | 未达标 | 216.94 |
| schedule_free_sgd_lr0.6 | 94.00% | 0.1954666 | 200 | 未达标 | 211.135 |
| sgd_cosine_lr0.6_min0.0 | 93.50% | 0.2159042 | 199 | 未达标 | 213.976 |
| adamw_cosine_lr0.05_min0.1 | 94.00% | 0.22103173 | 200 | 未达标 | 209.053 |
| schedule_free_adamw_lr0.05 | 94.00% | 0.22975731 | 200 | 未达标 | 216.225 |
| adamw_cosine_lr0.05_min0.0 | 94.00% | 0.23101563 | 199 | 未达标 | 207.384 |
| schedule_free_sgd_lr0.3 | 94.00% | 0.25143304 | 200 | 未达标 | 212.235 |
| sgd_cosine_lr0.3_min0.0 | 93.50% | 0.27456324 | 199 | 未达标 | 211.021 |
| schedule_free_sgd_lr0.1 | 93.50% | 0.39370268 | 200 | 未达标 | 215.419 |
| sgd_cosine_lr0.1_min0.0 | 93.00% | 0.40943221 | 199 | 未达标 | 213.606 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
