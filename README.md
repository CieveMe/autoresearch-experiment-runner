# AutoResearch Lite MVP

> GitHub repository: `https://github.com/CieveMe/autoresearch-experiment-runner`  
> 当前版本：`v0.2.0`｜定位：论文复现 + 可验证的实验任务（作品集 / 研究产出）

**文档分工**：[`REPRODUCTION.md`](REPRODUCTION.md) = 复现报告（英文，含与论文的差异分析）；
[`TASK.md`](TASK.md) / [`TASK.zh.md`](TASK.zh.md) = 把复现转成"智能体可反复尝试、可评分"的任务契约；
本文件 = 软件怎么用。

一个离线、可复现的“论文想法 → 实验任务 → 多方案运行 → 指标评估 → 自动选优 → 报告生成”最小闭环。

这个 MVP 用纯 Python 实现一个可替换的二分类训练器，并以 Adam 论文为例完成优化器机制复现；后续只需替换 `autoresearch/model.py`，即可接入其他论文代码、PyTorch 模型或 LLM 评测任务。

## 工程能力

- JSON 实验配置：记录假设、数据规模、随机种子、基线和对照方案。
- 可复现实验：固定随机种子、配置 SHA-256、结构化 `results.json`。
- 自动评估：比较测试准确率、测试损失、训练轮数和耗时，自动生成 Markdown 报告。
- 论文复现：以 Adam 为例，将论文中的矩估计和偏差修正映射为可运行实现，并与 SGD baseline 做对照。
- 环境可迁移：标准库实现，支持 Python 3.10+，提供 Dockerfile 和 Linux Shell 入口。
- 可验证：包含配置校验、确定性运行和结果产物测试。

## 快速运行

一条命令（推荐）：

```bash
python scripts/repro.py        # 校验配置 → 运行实验 → 对照期望数值 → 跑单测，失败则退出码非 0
make repro                     # Linux/macOS 等价入口
docker compose up --build      # 容器内跑同一套流程，产物写到 ./runs
```

分步运行：

```bash
python -m autoresearch.cli validate-config --config examples/classification.json
python -m autoresearch.cli run --config examples/classification.json --output runs/demo
cat runs/demo/report.md
python -m unittest discover -s tests -v
```

Windows PowerShell 可将 `cat` 换成 `Get-Content`。

Windows 也可以直接运行 `scripts/run_demo.ps1`。

## 已验证数值（可机器校验）

`expected/expected_metrics.json` 记录了期望数值与容差，`scripts/verify_results.py` 逐项断言
（共 17 项）。当前记录值（种子 7，配置 SHA-256 `cc85ba76…`）：

| 方案 | 测试损失 | 测试准确率 |
|---|---:|---:|
| **adam_reproduction** | **0.20216034** | 94.00% |
| sgd_control | 0.28128893 | 94.50% |
| adam_regularized | 0.31407811 | 93.50% |
| baseline | 0.38416828 | 93.50% |

10 个种子的聚合与配对比较（`python scripts/seed_sweep.py --seeds 0-9`）：
Adam 在 **10/10** 个种子上测试损失最低，相对较强 SGD 对照的配对提升为
`0.07669556 ± 0.00553513`。完整分析见 [`REPRODUCTION.md`](REPRODUCTION.md) 第 5 节。

任务评分与负向控制（故意改坏的实现必须被判失败）：

```bash
python scripts/score_task.py   # 当前仓库 100/100；两个负向控制各得 82.4/100 并被识别为失败
```

## Docker

```bash
docker build -t autoresearch-lite .
docker run --rm -v "$PWD/runs:/app/runs" autoresearch-lite    # 默认跑 scripts/repro.py
```

## 论文复现流程

当前示例完整走通：论文元信息 → 研究假设 → baseline → 论文方法实现 → 固定数据和随机种子 → 指标对比 → 复现边界说明。具体记录见 `docs/papers/adam-2014.md`。

## 下一步接入真实论文

1. 将论文的研究问题写成 `hypothesis`，把评测指标写入 `metric`。
2. 在 `model.py` 实现论文方法的训练或推理适配器。
3. 在 JSON 中增加 baseline、ablation 和超参数变体。
4. 为数据集、评测指标和失败案例补充测试。
5. 把实验报告、配置和结果一起提交，保留配置哈希以支持复盘。

## 项目申请材料

申请准备清单见 `docs/feishu-expert-guide.md`，工程过程和复现约束分别见 `docs/process/initial-design.md`、`docs/reproducibility.md`、`MILESTONES.md` 和 `TODO.md`。这些文档只记录当前真实状态；提交外部申请前，应补充真实 Git commit 区间和对应验证证据。

> ⚠️ `docs/feishu-expert-guide.md` 含第三方平台内部文档链接与准入要求，属**内部材料**：
> 若本仓库要转为公开，必须先移除该文件（以及任何带内部链接的段落），再对外发布。

## 推送与发布

远端已配置为 `https://github.com/CieveMe/autoresearch-experiment-runner`（当前为**私有**仓库）。
推送前请确认本机 Git 已登录 GitHub：

```bash
git push origin main
```

如果远程仓库已经有初始化提交，应先执行 `git pull --rebase origin main`，确认内容后再推送。

**发布红线**：转公开、打 release、连 Zenodo 取 DOI 都需要先做一次脱敏检查——
不得出现客户名称、真实地址、凭据、客户数据或第三方未公开材料。当前 `docs/feishu-expert-guide.md`
与本文档内部章节需先处理。

## 简历表述

**AutoResearch Lite：Adam 论文机制复现与自动实验 MVP**｜Python / Git / Linux / Docker

- 阅读并拆解 Adam 论文，将一阶/二阶矩估计与偏差修正转化为纯 Python 训练器，与固定学习率 SGD baseline 进行可复现实验对比。
- 设计并实现实验运行器，将研究假设、基线、对照方案和评测指标统一配置化，自动完成多方案训练、指标排序和 Markdown 报告生成。
- 通过固定随机种子、配置 SHA-256、结构化结果和 Docker 运行环境保证实验可复现，补齐从论文阅读到工程验证的闭环。
- 内置配置校验、确定性运行和结果产物测试，后续可替换训练器接入真实论文、PyTorch 模型或 LLM 评测任务。
