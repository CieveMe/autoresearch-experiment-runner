# TODO

这些事项是后续真实开发计划，不代表当前版本已经完成：

- [ ] 增加可插拔数据集接口，并为数据集版本记录哈希。
- [x] 增加更多优化器和消融实验（SGD+momentum / AdaGrad / RMSProp / 偏差修正消融），并统一输出均值、标准差与配对提升。
- [ ] 配对显著性检验（当前只给均值/标准差/配对提升与最优次数，未报 p 值或置信区间）。
- [x] 增加"收敛速度"指标（逐轮损失曲线 + 达标轮数），把论文"更快收敛"的说法变成可检验对象——结论是**Adam 不是最快**（见 `REPRODUCTION.md` 5.4）。
- [ ] 增加稀疏梯度场景（论文声称的优势场景之一），当前实验是稠密小批量等价的全批量。
- [x] 增加学习率扫描，消除"各优化器只在手选学习率上比较"这一质疑（`examples/optimizers-sweep.json`，24 组）。
- [ ] 把学习率网格向大值方向延伸并加密：当前每个自适应家族的最优都在网格边缘，说明网格未饱和。
- [ ] 用同一套 `epochs_to_target` 跑多个目标阈值（如 0.30 / 0.20 / 0.16）并画成"达标轮数 vs 阈值"曲线。
- [x] 按 Roadmap 接入第一篇 2024 年论文（AdEMAMix）：适配器重构（`trainers/` + `optimizers.py` + `schedules.py` + `datasets.py`）、20 组调参扫描、10 种子配对、论文卡与负向控制，结论为负（不更快）。见 `docs/papers/ademamix-2024.md`。
- [x] 第二篇论文：Schedule-Free AdamW（2024，arXiv:2405.15682）。已按 reference 实现移植并做"**无计划 vs 调过的 cosine 计划**"对照（21 组扫描同时调 lr 与 min_lr_factor，另加常数学习率基线）：**"打平"勉强成立、"超过"不成立**（10/10 种子败给调过的 cosine；常数学习率最好）。见 `docs/papers/schedule-free-2024.md`。
- [ ] 把 Schedule-Free 套件也在 MLP trainer 上跑一遍（当前只在 logistic 上做，200 轮凸任务对"计划"最不敏感）。
- [x] 用 MLP trainer 复跑优化器套件与 AdEMAMix（含"每个家族为 MLP 重新调参"和"初始化随种子变化"两处修正）：**结论没有被推翻** —— Adam 在两套模型上速度都居中（MLP：20.3 轮 vs AdaGrad 6.2 / 动量 7.0），论文 warmup 在两套模型上都更差，无 warmup 的 AdEMAMix 与 AdamW 无差别。见 `REPRODUCTION.md` 5.6 与 `runs/mlp-verified/`。
- [ ] 多隐藏层尺寸（如 [8] vs [32] vs [8,8]）复跑同一问题：检查"慢 EMA 无优势"是否也随容量变化（当前只有一种容量）。
- [ ] 增加失败实验重试、断点恢复和超时控制。
- [ ] 增加 PyTorch 适配器，同时保持标准库示例可离线运行。
- [ ] 增加实验结果可视化和 HTML 报告导出。
- [x] 增加 CI，在干净环境中运行配置校验、单元测试和确定性检查（`.github/workflows/repro.yml`，Python 3.10/3.12 + 容器）。
- [x] 增加一键复现入口与期望数值校验（`scripts/repro.py`、`scripts/verify_results.py`、`expected/expected_metrics.json`）。
- [x] 增加任务评分与负向控制（`scripts/score_task.py`、`TASK.md`）。
- [ ] 运行 `T-ADAM-01B/01C/01D` 三个任务变体各一轮，记录智能体实际表现（尝试次数、得分曲线）。
