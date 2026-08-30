<div align="right"><a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/README.md">简体中文</a> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.en.md">English</a> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.ja.md">日本語</a> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.ko.md">한국어</a> · <strong>繁體中文</strong></div>

# pyquant-roadmap / Python 量化實戰路線圖

[![Python 3.11](https://img.shields.io/badge/python-3.11-2563eb)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-0f766e)](https://github.com/xystudio-ai/pyquant-roadmap/blob/main/LICENSE)

`pyquant-roadmap` 是一套可以依序執行的 Python 量化學習專案。14 個 Jupyter Notebook 共用一條主線案例，帶你把資料、因子、投資組合、回測、評估和訊號輸出真正串起來。

它適合第一次有系統地學習量化交易的人。你不必先讀完一本教材，也不用一開始就挑選複雜框架；先在本機跑完整個流程，再回頭理解每一步為什麼這樣做，後續學習會容易許多。

## 它解決什麼問題

量化入門的難點往往不是某個公式或 Python 函式，而是知識點彼此分散：會計算報酬率，卻不知道怎樣進入因子研究；能寫策略規則，卻說不清投資組合、交易成本和績效報告如何銜接。

這個儲存庫用一組前後連貫的 Notebook，把個人量化研究的基本流程放進同一個專案：

```text
取得與整理資料
→ 建立並檢驗因子
→ 把因子分數轉成投資組合權重
→ 加入再平衡和交易成本進行回測
→ 對照基準評估結果
→ 輸出目標權重、訂單建議和複盤資料
```

每一章只推進其中一段，但輸入和輸出會交給後面的章節。你看到的不是 14 個互不相關的範例，而是一條可以重複執行和修改的研究流程。

## 你會得到什麼

| 內容 | 用途 |
| --- | --- |
| 14 個依序編排的 Notebook | 從環境檢查開始，逐步完成研究、回測和複盤 |
| 小型真實 ETF 日線範例 | 不必連線也能開始執行並理解資料結構 |
| `lib/` 共用函式 | 查看 Notebook 邏輯如何整理成可重複呼叫的程式碼 |
| 資料來源與策略設定 | 理解如何分開管理資料、參數和研究程式碼 |
| 本機執行產物 | 產生圖表、指標、目標權重、訂單建議和報告 |

完成後，你應該能看懂 Python 量化專案的主要環節，知道因子、投資組合和回測之間如何傳遞資料，也能判斷下一步更需要補強資料處理、策略研究、工程化或 AI 輔助研究。

## 快速開始

需要 Git、Conda 和 Python 3.11。建議使用儲存庫提供的 Conda 環境：

```bash
git clone https://github.com/xystudio-ai/pyquant-roadmap.git
cd pyquant-roadmap
conda env create -f environment.yml
conda activate pyquant-roadmap
jupyter lab
```

開啟 `notebooks/`，從 `01_quant_workflow_overview.ipynb` 開始，依照檔名前綴執行到 `14_ai_helper_and_next_steps.ipynb`。

如果你已有 Python 3.11 環境，也可以直接安裝相依套件：

```bash
python -m pip install pandas numpy matplotlib scipy statsmodels pyarrow pyyaml akshare bt quantstats ta notebook jupyterlab
jupyter lab
```

儲存庫中的範例資料足以支援前半段學習。第 04 章也會示範透過 AKShare 取得並快取同類行情資料，這一步需要網路連線。

## Notebook 路線

| 順序 | 主題 | 完成後你會知道 |
| --- | --- | --- |
| 01 | 量化交易完整流程與主線案例 | 一次完整研究大致包含哪些步驟 |
| 02 | 環境、專案結構與第一次執行 | 如何確認本機環境和路徑正常 |
| 03 | pandas / NumPy 夠用部分 | 怎樣處理量化研究中的表格和陣列 |
| 04 | 資料取得、欄位標準化與快取 | 如何把行情整理成可重複使用的資料 |
| 05 | 資料清理、對齊與報酬率 | 怎樣處理時間對齊、缺漏值和報酬率 |
| 06 | 因子建立 | 如何把策略直覺寫成可計算特徵 |
| 07 | 因子有效性檢驗 | 如何用 IC 和分層結果初步檢查因子 |
| 08 | 投資組合建立 | 如何把因子分數轉成目標權重 |
| 09 | 回測引擎 | 交易規則、成本與開源回測框架怎樣配合 |
| 10 | 績效評估與策略報告 | 如何閱讀指標、淨值曲線和基準比較 |
| 11 | 工程化流程 | 怎樣把一次實驗整理成可重現流程 |
| 12 | 策略分類圖 | 常見策略之間有什麼結構差異 |
| 13 | 經典策略 | 幾類代表性入門策略如何落到程式碼 |
| 14 | AI 輔助與下一步 | AI 適合加速哪些環節，下一步學什麼 |

建議依序執行。後面的 Notebook 會用到前面建立的資料約定、目錄和研究思路。

## 專案結構

```text
pyquant-roadmap/
├── notebooks/        # 14 個 Notebook，主要學習入口
├── lib/              # 資料、因子、投資組合、回測和評估函式
├── configs/          # 資料來源、策略和章節設定
├── data/sample/      # 隨儲存庫提供的小型真實範例資料
├── data/raw/         # 下載或匯入的原始資料
├── data/processed/   # 清理後的研究資料
├── outputs/          # 本機執行結果，預設不提交
├── assets/           # README 圖片和社群帳號 QR Code
├── environment.yml
└── pyproject.toml
```

`notebooks/` 是學習主線。理解一段邏輯後，可以到 `lib/` 查看它怎樣被封裝，並透過 `configs/` 修改資料範圍和策略參數。

## 資料與輸出

`data/sample/` 中包含一個小型真實 ETF 日線資料集，方便先離線執行。你也可以在第 04 章使用 AKShare 取得新資料；外部介面發生變化時，請以 AKShare 目前的文件和回傳欄位為準。

執行 Notebook 後，結果會寫入 `outputs/results/`，包括圖表、績效指標、目標權重、訂單建議和複盤資料。這些是本機研究產物，預設不會提交到儲存庫。

## 作者與意見回饋

由 [xyQuant](https://github.com/xystudio-ai) 維護。

- 微信公眾號：[作者介紹與專案動態](https://mp.weixin.qq.com/s/k3NEph_JbMYwbCYn2ts8Dw)
- 小紅書：[xyQuant](https://www.xiaohongshu.com/user/profile/6718edb7000000001d0326cd)

<p>
  <img src="../../assets/qr/gzh-1.png" alt="xyQuant 微信公眾號 QR Code" width="180" />
  <img src="../../assets/qr/xhs-1.png" alt="xyQuant 小紅書 QR Code" width="180" />
</p>

發現錯誤、執行問題或有改進建議，歡迎提交 [GitHub Issue](https://github.com/xystudio-ai/pyquant-roadmap/issues)。

## 授權條款

本專案採用 [MIT License](https://github.com/xystudio-ai/pyquant-roadmap/blob/main/LICENSE)。

本專案用於量化學習與研究。Notebook 中的回測、指標和訂單建議需要依照資料口徑自行驗證，不應直接當作真實交易依據。
