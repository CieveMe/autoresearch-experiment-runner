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
- [x] 把 Schedule-Free 套件也在 MLP trainer 上跑一遍（15 组扫描 + 10 种子）：**方向翻转** —— Schedule-Free 赢调过的 cosine 9/10，但常数学习率仍 9/10 赢 Schedule-Free ⇒ 弱形式两模型成立、强形式不成立。见 `REPRODUCTION.md` 5.8 与 `docs/papers/schedule-free-2024.md`。
- [x] 用"多阈值"把速度指标从单点升级为曲线：`scripts/threshold_curve.py` + `runs/threshold-curves/`（13 点网格、交叉阈值、SVG 标注固定阈值）。结论：**6 个套件里 4 个的"最快者"依赖阈值**，其中 3 个的固定阈值正好落在交叉点的脆弱一侧；`schedule-free`（logistic）在全部 13 个阈值上稳定，`ademamix`（logistic）在 0.0014 宽区间内翻转 5 次（那两个 arm 在该区间本质持平）。见 `REPRODUCTION.md` 5.9。
- [x] 用 MLP trainer 复跑优化器套件与 AdEMAMix（含"每个家族为 MLP 重新调参"和"初始化随种子变化"两处修正）：**结论没有被推翻** —— Adam 在两套模型上速度都居中（MLP：20.3 轮 vs AdaGrad 6.2 / 动量 7.0），论文 warmup 在两套模型上都更差，无 warmup 的 AdEMAMix 与 AdamW 无差别。见 `REPRODUCTION.md` 5.6 与 `runs/mlp-verified/`。
- [ ] 多隐藏层尺寸（如 [8] vs [32] vs [8,8]）复跑同一问题：检查"慢 EMA 无优势"是否也随容量变化（当前只有一种容量）。
- [x] 多容量扫描完成（`[32]`、`[8,8]`，每个容量重新调参 + 10 种子）：**AdEMAMix 无优势在三个容量上都稳定**（各 1/10 种子更好）；**SF 的方向翻转是架构/阈值效应而非容量效应**（三种 MLP 容量上都赢调过的 cosine）；**容量变大后 AdaGrad 在测试损失上胜出**（9/10、10/10）；训练/测试损失排名随容量分家。见 `REPRODUCTION.md` 5.10。
- [ ] 阈值曲线与容量扫描的交叉：目前"交叉点"只在 seed 7 的曲线上定位，应把 10 个种子的曲线都画出来，看交叉点本身的稳定性（当前结论只到"存在交叉"这一层）。
- [x] 10 种子交叉稳定性完成：`optimizers`(logistic) 交叉 10/10 种子但位置散布 0.0456（可用的是"固定阈值下 adagrad 每个种子都更快"）；`schedule-free-mlp` 交叉 10/10 但**固定阈值胜者逐种子变化** ⇒ 该卡里 seed-7 的速度句改为"单种子陈述"；`capacity-h32/h8x8` 实为**并列带而非交叉**。同时修掉第三例"数字来自工具"的缺陷（并列被字母序裁决）。见 `REPRODUCTION.md` 5.11。
- [x] 交叉稳定性补齐到 8 对（含 schedule-free logistic、ademamix logistic、ademamix-mlp）：**5 对在固定阈值下逐种子稳定、3 对不稳定，且 3 对不稳定的全是 MLP 套件**。
- [x] 指标口径成节（`REPRODUCTION.md` 5.12）：训练/测试损失的 top-1 只在两个更大容量上分家，排名扰动随容量增长（0→2→3→4→5 个 arm 移动 ≥2 位）；`epochs_to_target` 基于训练曲线，故"更快"与"更好"必须分开陈述。
- [x] 具名小节材料：`docs/defect-family.md`（三例同族缺陷 + 每例的检查名与测试文件）。
- [x] 容量再扩到 `[64]` 与 `[16,16]`（假设先写入 `docs/capacity-expansion-preregistration.md` 再跑）：逐条判定见 `REPRODUCTION.md` §5.13；`[16,16]` 上过拟合主导（最低训练损失的 AdEMAMix 同时是测试损失最差的）。
- [x] 换激活函数完成（ReLU/GELU，`[32]` 容量，各 18 组调参 + 10 种子，预注册 A1–A3）：**A1 确认**（SF 在两种激活下都赢调过的 cosine，8/10）；**A2 按字面被证伪且最有信息量**（对同学习率 AdamW 仍持平，但对"调过 cosine 的 AdamW"反而赢 9/10、7/10 ⇒ **动的是基线**）；**A3 确认**。见 `REPRODUCTION.md` 5.14。
- [x] 归一化/初始化选择（batchnorm/layernorm、Xavier vs He、固定 0.05）是否会改变那两条负结果（预注册 N1–N4，`docs/normalization-init-preregistration.md`）：**N1 被证伪**（SF 赢调过的 cosine 只在 He 下更强、batchnorm/朴素初始化下是平局、layernorm 下反向）、**N2 方向 3/4 成立但胜场数标准被证伪**（8/10 胜而均值差 9e-5）、**N3 确认**、**N4 被证伪**（没有变体把 σ 降到 0.0210 以下 ⇒ "norm 降低噪声"不成立）。见 `REPRODUCTION.md` §5.15。
- [x] **实验维度到此冻结（2026-09-28）**：scope 表共六轴——threshold / model family / capacity / metric / activation / normalization-init。除审稿人明确要求，不再加新轴；精力转向 A3 写作与内审。（`REPRODUCTION.md` §5.15 末尾）
- [ ] 增加失败实验重试、断点恢复和超时控制。
- [ ] 增加 PyTorch 适配器，同时保持标准库示例可离线运行。
- [ ] 增加实验结果可视化和 HTML 报告导出。
- [x] 增加 CI，在干净环境中运行配置校验、单元测试和确定性检查（`.github/workflows/repro.yml`，Python 3.10/3.12 + 容器）。
- [x] 增加一键复现入口与期望数值校验（`scripts/repro.py`、`scripts/verify_results.py`、`expected/expected_metrics.json`）。
- [x] 增加任务评分与负向控制（`scripts/score_task.py`、`TASK.md`）。
- [ ] 运行 `T-ADAM-01B/01C/01D` 三个任务变体各一轮，记录智能体实际表现（尝试次数、得分曲线）。
