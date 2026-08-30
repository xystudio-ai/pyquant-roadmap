<div align="right"><strong>简体中文</strong> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.en.md">English</a> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.ja.md">日本語</a> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.ko.md">한국어</a> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.zh-TW.md">繁體中文</a></div>

# pyquant-roadmap / Python 量化实战路线图

[![Python 3.11](https://img.shields.io/badge/python-3.11-2563eb)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-0f766e)](https://github.com/xystudio-ai/pyquant-roadmap/blob/main/LICENSE)

`pyquant-roadmap` 是一套可以按顺序运行的 Python 量化学习项目。14 个 Jupyter Notebook 共用一条主线案例，带你把数据、因子、组合、回测、评估和信号输出真正接起来。

它适合第一次系统学习量化交易的人。这套路线先让完整流程在本地跑起来，再回头理解每一步为什么这样做，省去开始阶段在教材和框架之间反复选择的时间。

## 它解决什么问题

量化入门时，最麻烦的是把分散的知识点接起来：会计算收益率，却不知道怎样进入因子研究；能写策略规则，却说不清组合、成交成本和绩效报告如何衔接。

这个仓库用一组前后连贯的 Notebook，把个人量化研究的基本流程放进同一个项目：

```text
获取与整理数据
→ 构建并检验因子
→ 把因子分数变成组合权重
→ 加入调仓和交易成本进行回测
→ 对照基准评估结果
→ 输出目标权重、订单建议和复盘材料
```

每一章只推进其中一段，输入和输出会继续传给后面的章节。14 个 Notebook 前后相接，组成一条可以重复运行的研究链路。

## 你会得到什么

| 内容 | 用途 |
| --- | --- |
| 14 个顺序式 Notebook | 从环境检查开始，逐步完成研究、回测和复盘 |
| 小型真实 ETF 日线样例 | 不依赖联网也能开始运行和理解数据结构 |
| `lib/` 复用函数 | 查看 Notebook 中的逻辑如何沉淀为可重复调用的代码 |
| 数据源与策略配置 | 理解如何把数据、参数和研究代码分开管理 |
| 本地运行产物 | 生成图表、指标、目标权重、订单建议和报告 |

跑完后，你应该能看懂一个 Python 量化项目的主要环节，知道因子、组合和回测之间如何传递数据，也能判断下一步更需要补数据处理、策略研究、工程化还是 AI 辅助研究。

## 快速开始

需要 Git、Conda 和 Python 3.11。推荐用仓库提供的 Conda 环境：

```bash
git clone https://github.com/xystudio-ai/pyquant-roadmap.git
cd pyquant-roadmap
conda env create -f environment.yml
conda activate pyquant-roadmap
jupyter lab
```

打开 `notebooks/`，从 `01_quant_workflow_overview.ipynb` 开始，按文件名前缀一直运行到 `14_ai_helper_and_next_steps.ipynb`。

如果你已有 Python 3.11 环境，也可以直接安装依赖：

```bash
python -m pip install pandas numpy matplotlib scipy statsmodels pyarrow pyyaml akshare bt quantstats ta notebook jupyterlab
jupyter lab
```

仓库中的样例数据足够支持前期学习。第 04 章还会演示通过 AKShare 获取并缓存同类行情数据，这一步需要联网。

## Notebook 路线

| 顺序 | 主题 | 完成后你会知道 |
| --- | --- | --- |
| 01 | 量化交易全流程与主线案例 | 一次完整研究大致包含哪些步骤 |
| 02 | 环境、项目结构与第一次运行 | 如何确认本地环境和项目路径正常 |
| 03 | pandas / NumPy 够用部分 | 怎样处理量化研究中的表格和数组 |
| 04 | 数据获取、字段标准化与缓存 | 如何把行情整理成可复用的数据 |
| 05 | 数据清洗、对齐与收益率 | 怎样处理时间对齐、缺失值和收益率 |
| 06 | 因子构建 | 如何把策略直觉写成可计算特征 |
| 07 | 因子有效性检验 | 如何用 IC 和分层结果初步检查因子 |
| 08 | 组合构建 | 如何把因子分数转换为目标权重 |
| 09 | 回测引擎 | 交易规则、成本与开源回测框架怎样配合 |
| 10 | 绩效评估与策略报告 | 如何阅读指标、净值曲线和基准对比 |
| 11 | 工程化流水线 | 怎样把一次实验整理成可复现流程 |
| 12 | 策略分类地图 | 常见策略之间有什么结构差异 |
| 13 | 经典策略 | 几类代表性入门策略如何落到代码 |
| 14 | AI 辅助与下一步 | AI 适合加速哪些环节，下一步学什么 |

建议按顺序运行。后面的 Notebook 会用到前面建立的数据约定、目录和研究思路。

## 项目结构

```text
pyquant-roadmap/
├── notebooks/        # 14 个 Notebook，学习主入口
├── lib/              # 数据、因子、组合、回测和评估函数
├── configs/          # 数据源、策略和章节配置
├── data/sample/      # 随仓库提供的小型真实样例数据
├── data/raw/         # 下载或导入的原始数据
├── data/processed/   # 清洗后的研究数据
├── outputs/          # 本地运行结果，默认不提交
├── assets/           # README 图片和社交账号二维码
├── environment.yml
└── pyproject.toml
```

`notebooks/` 是学习主线。等你理解一段逻辑后，可以到 `lib/` 查看它怎样被封装，并通过 `configs/` 修改数据范围和策略参数。

## 数据与输出

`data/sample/` 中包含一个小型真实 ETF 日线数据集，便于先离线运行。你也可以在第 04 章使用 AKShare 获取新的数据；外部接口发生变化时，请以 AKShare 当前文档和返回字段为准。

运行 Notebook 后，结果会写入 `outputs/results/`，包括图表、绩效指标、目标权重、订单建议和复盘材料。它们是本地研究产物，不会默认提交到仓库。

## 作者与反馈

由 [xyQuant](https://github.com/xystudio-ai) 维护。

- 微信公众号：[作者介绍与项目动态](https://mp.weixin.qq.com/s/k3NEph_JbMYwbCYn2ts8Dw)
- 小红书：[xyQuant](https://www.xiaohongshu.com/user/profile/6718edb7000000001d0326cd)

<p>
  <img src="assets/qr/gzh-1.png" alt="小圆量化公众号二维码" width="180" />
  <img src="assets/qr/xhs-1.png" alt="小圆量化小红书二维码" width="180" />
</p>

发现错误、运行问题或有改进建议，欢迎提交 [GitHub Issue](https://github.com/xystudio-ai/pyquant-roadmap/issues)。

## 许可证

本项目采用 [MIT License](https://github.com/xystudio-ai/pyquant-roadmap/blob/main/LICENSE)。

本项目面向量化学习与研究。Notebook 中的回测、指标和订单建议需要结合数据口径自行验证，不应直接当作真实交易依据。
