<div align="right"><a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/README.md">简体中文</a> · <strong>English</strong> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.ja.md">日本語</a> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.ko.md">한국어</a> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.zh-TW.md">繁體中文</a></div>

# pyquant-roadmap / A Hands-on Python Quant Roadmap

[![Python 3.11](https://img.shields.io/badge/python-3.11-2563eb)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-0f766e)](https://github.com/xystudio-ai/pyquant-roadmap/blob/main/LICENSE)

`pyquant-roadmap` is a sequential, hands-on introduction to quantitative research with Python. Fourteen Jupyter Notebooks share one running example and connect data, factors, portfolio construction, backtesting, evaluation, and signal output in a single project.

It is designed for people learning quantitative trading systematically for the first time. You do not need to finish a textbook or choose a sophisticated framework before you begin. Run the complete workflow locally first, then return to understand why each step works the way it does.

## The problem it solves

The hardest part of getting started is often not a formula or a Python function. It is connecting separate pieces of knowledge. You may know how to calculate returns without knowing how they feed factor research, or know how to write a rule without knowing how portfolio weights, trading costs, and performance reports fit around it.

This repository puts the basic personal quant research workflow into one connected set of Notebooks:

```text
load and prepare data
→ build and test factors
→ turn factor scores into portfolio weights
→ backtest with rebalancing and trading costs
→ evaluate results against a benchmark
→ export target weights, order suggestions, and review material
```

Each chapter advances one part of the workflow, and its outputs feed later chapters. These are not fourteen unrelated demos; they form a research pipeline you can run again and modify.

## What you get

| Included | What it is for |
| --- | --- |
| 14 ordered Notebooks | Move from environment checks to research, backtesting, and review |
| Small real ETF daily dataset | Start offline and inspect the data contract without downloading anything |
| Reusable functions under `lib/` | See how Notebook logic becomes callable Python code |
| Data-source and strategy configuration | Keep data, parameters, and research code separate |
| Local outputs | Generate charts, metrics, target weights, order suggestions, and reports |

After completing the route, you should recognize the main parts of a Python quant project, understand how data moves between factors, portfolios, and backtests, and have a clearer idea of what to study next: data engineering, strategy research, reproducible workflows, or AI-assisted research.

## Quick start

You need Git, Conda, and Python 3.11. The provided Conda environment is the recommended setup:

```bash
git clone https://github.com/xystudio-ai/pyquant-roadmap.git
cd pyquant-roadmap
conda env create -f environment.yml
conda activate pyquant-roadmap
jupyter lab
```

Open `notebooks/`, start with `01_quant_workflow_overview.ipynb`, and continue in numeric order through `14_ai_helper_and_next_steps.ipynb`.

If you already have a Python 3.11 environment, install the dependencies directly:

```bash
python -m pip install pandas numpy matplotlib scipy statsmodels pyarrow pyyaml akshare bt quantstats ta notebook jupyterlab
jupyter lab
```

The bundled sample data is enough for the early chapters. Chapter 04 also shows how to download and cache similar market data through AKShare; that step requires a network connection.

## Notebook route

| No. | Topic | What you will understand |
| --- | --- | --- |
| 01 | Quant workflow and the running example | The main stages of a complete research run |
| 02 | Environment, project structure, and first run | How to verify the local environment and paths |
| 03 | Practical pandas and NumPy | How to work with the tables and arrays used in quant research |
| 04 | Data loading, schema normalization, and caching | How to turn market data into a reusable dataset |
| 05 | Cleaning, alignment, and returns | How to handle dates, missing values, and return series |
| 06 | Factor construction | How to turn a strategy intuition into a measurable feature |
| 07 | Factor validation | How to make an initial factor check with IC and grouped returns |
| 08 | Portfolio construction | How to convert factor scores into target weights |
| 09 | Backtest engines | How rules, costs, and an open-source engine work together |
| 10 | Performance evaluation and reporting | How to read metrics, equity curves, and benchmark comparisons |
| 11 | Reproducible pipelines | How to turn a one-off experiment into a repeatable workflow |
| 12 | Strategy taxonomy | How common strategy families differ structurally |
| 13 | Classic strategies | How representative beginner strategies translate into code |
| 14 | AI assistance and next steps | Where AI can help and what to study next |

Run the Notebooks in order. Later chapters rely on the data contracts, directories, and research conventions introduced earlier.

## Repository structure

```text
pyquant-roadmap/
├── notebooks/        # 14 Notebooks and the main learning route
├── lib/              # data, factor, portfolio, backtest, and evaluation functions
├── configs/          # data-source, strategy, and chapter configuration
├── data/sample/      # small real sample dataset included in the repository
├── data/raw/         # downloaded or imported raw data
├── data/processed/   # cleaned research data
├── outputs/          # local results, ignored by default
├── assets/           # README assets and social QR codes
├── environment.yml
└── pyproject.toml
```

`notebooks/` is the learning route. Once you understand a piece of logic, look under `lib/` to see how it is packaged for reuse, then edit `configs/` to change the data range or strategy parameters.

## Data and outputs

`data/sample/` contains a small real ETF daily dataset for offline use. Chapter 04 can fetch new data through AKShare. Because external interfaces can change, check the current AKShare documentation and returned fields if the example no longer matches the live API.

Notebook results are written to `outputs/results/`, including charts, performance metrics, target weights, order suggestions, and review material. These are local research artifacts and are not committed by default.

## Maintainer and feedback

Maintained by [xyQuant](https://github.com/xystudio-ai).

- WeChat Official Account: [author introduction and project updates](https://mp.weixin.qq.com/s/k3NEph_JbMYwbCYn2ts8Dw)
- Xiaohongshu: [xyQuant](https://www.xiaohongshu.com/user/profile/6718edb7000000001d0326cd)

<p>
  <img src="../../assets/qr/gzh-1.png" alt="xyQuant WeChat Official Account QR code" width="180" />
  <img src="../../assets/qr/xhs-1.png" alt="xyQuant Xiaohongshu QR code" width="180" />
</p>

Use [GitHub Issues](https://github.com/xystudio-ai/pyquant-roadmap/issues) to report an error, ask about a run problem, or suggest an improvement.

## License

This project is licensed under the [MIT License](https://github.com/xystudio-ai/pyquant-roadmap/blob/main/LICENSE).

This repository is for learning and research. Validate the data assumptions behind Notebook backtests, metrics, and order suggestions before using them in any real trading decision.
