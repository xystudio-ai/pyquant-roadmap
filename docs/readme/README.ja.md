<div align="right"><a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/README.md">简体中文</a> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.en.md">English</a> · <strong>日本語</strong> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.ko.md">한국어</a> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.zh-TW.md">繁體中文</a></div>

# pyquant-roadmap / Python クオンツ実践ロードマップ

[![Python 3.11](https://img.shields.io/badge/python-3.11-2563eb)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-0f766e)](https://github.com/xystudio-ai/pyquant-roadmap/blob/main/LICENSE)

`pyquant-roadmap` は、順番に実行しながら学ぶ Python クオンツリサーチの入門プロジェクトです。14 本の Jupyter Notebook が一つのケースを共有し、データ、ファクター、ポートフォリオ構築、バックテスト、評価、シグナル出力までをつなぎます。

クオンツ取引を初めて体系的に学ぶ人を対象にしています。最初に教科書を読み切ったり、高機能なフレームワークを選んだりする必要はありません。まずローカルで一連の流れを動かし、その後で各処理の理由を理解していく構成です。

## 解決する課題

入門時につまずきやすいのは、一つの数式や Python 関数より、別々に覚えた知識をつなぐ部分です。リターンを計算できてもファクター研究への渡し方が分からない、売買ルールを書けてもポートフォリオ、取引コスト、評価レポートとの関係が見えない、といった問題があります。

このリポジトリでは、個人のクオンツリサーチに必要な基本フローを一連の Notebook で実行します。

```text
データの取得と整形
→ ファクターの作成と検証
→ ファクタースコアをポートフォリオウェイトに変換
→ リバランスと取引コストを含めてバックテスト
→ ベンチマークと比較して評価
→ 目標ウェイト、注文案、振り返り資料を出力
```

各章は一つの工程を進め、その出力を後の章で使います。14 個の独立したサンプルではなく、繰り返し実行して変更できる一つのリサーチパイプラインです。

## 含まれるもの

| 内容 | 用途 |
| --- | --- |
| 順序付きの 14 本の Notebook | 環境確認からリサーチ、バックテスト、振り返りまで進む |
| 小規模な実 ETF 日足サンプル | ダウンロードせずに実行し、データ構造を確認する |
| `lib/` の再利用関数 | Notebook の処理を再利用可能な Python コードにする方法を読む |
| データソースと戦略の設定 | データ、パラメータ、リサーチコードを分けて管理する |
| ローカル出力 | チャート、指標、目標ウェイト、注文案、レポートを生成する |

一通り終えると、Python クオンツプロジェクトの主要な工程、ファクター・ポートフォリオ・バックテスト間のデータの流れが分かります。次にデータ処理、戦略研究、再現可能なワークフロー、AI 支援のどこを深めるべきかも判断しやすくなります。

## クイックスタート

Git、Conda、Python 3.11 が必要です。用意されている Conda 環境の利用を推奨します。

```bash
git clone https://github.com/xystudio-ai/pyquant-roadmap.git
cd pyquant-roadmap
conda env create -f environment.yml
conda activate pyquant-roadmap
jupyter lab
```

`notebooks/` を開き、`01_quant_workflow_overview.ipynb` から `14_ai_helper_and_next_steps.ipynb` まで番号順に実行してください。

Python 3.11 の環境がすでにある場合は、依存関係を直接インストールできます。

```bash
python -m pip install pandas numpy matplotlib scipy statsmodels pyarrow pyyaml akshare bt quantstats ta notebook jupyterlab
jupyter lab
```

同梱のサンプルデータで前半の章を進められます。第 04 章では AKShare から同種の市場データを取得してキャッシュするため、その処理にはネットワーク接続が必要です。

## Notebook の順序

| 番号 | テーマ | 分かるようになること |
| --- | --- | --- |
| 01 | クオンツ取引の全体像とメインケース | 一回のリサーチを構成する主な工程 |
| 02 | 環境、プロジェクト構成、初回実行 | ローカル環境とパスの確認方法 |
| 03 | 実用範囲の pandas / NumPy | リサーチで使う表と配列の扱い方 |
| 04 | データ取得、スキーマ統一、キャッシュ | 市場データを再利用可能な形に整える方法 |
| 05 | クリーニング、時点合わせ、リターン | 日付、欠損値、リターン系列の扱い方 |
| 06 | ファクター構築 | 戦略の着想を計算可能な特徴量にする方法 |
| 07 | ファクター検証 | IC とグループ別リターンによる初期検証 |
| 08 | ポートフォリオ構築 | ファクタースコアを目標ウェイトに変換する方法 |
| 09 | バックテストエンジン | ルール、コスト、OSS エンジンの組み合わせ方 |
| 10 | パフォーマンス評価とレポート | 指標、資産曲線、ベンチマーク比較の読み方 |
| 11 | 再現可能なパイプライン | 一回限りの実験を繰り返せる処理にする方法 |
| 12 | 戦略の分類 | 一般的な戦略群の構造上の違い |
| 13 | 代表的な戦略 | 初学者向け戦略をコードにする方法 |
| 14 | AI 支援と次の学習 | AI が役立つ工程と次に学ぶ内容 |

番号順に進めることを推奨します。後半の Notebook は、前半で導入するデータ規約、ディレクトリ、リサーチ手順を使います。

## リポジトリ構成

```text
pyquant-roadmap/
├── notebooks/        # 14 本の Notebook と学習の主ルート
├── lib/              # データ、ファクター、ポートフォリオ、バックテスト、評価関数
├── configs/          # データソース、戦略、章の設定
├── data/sample/      # リポジトリに同梱する小規模な実データ
├── data/raw/         # ダウンロードまたは取り込んだ元データ
├── data/processed/   # クリーニング済みのリサーチデータ
├── outputs/          # ローカルの実行結果（既定ではコミットしない）
├── assets/           # README 素材と SNS の QR コード
├── environment.yml
└── pyproject.toml
```

学習の中心は `notebooks/` です。処理を理解したら `lib/` で再利用可能な形へのまとめ方を確認し、`configs/` でデータ範囲や戦略パラメータを変更できます。

## データと出力

`data/sample/` には、オフラインで使える小規模な実 ETF 日足データがあります。第 04 章では AKShare から新しいデータを取得できます。外部 API は変わることがあるため、サンプルと現在の動作が合わない場合は AKShare の最新ドキュメントと返却フィールドを確認してください。

Notebook の結果は `outputs/results/` に保存されます。チャート、パフォーマンス指標、目標ウェイト、注文案、振り返り資料が含まれ、既定ではリポジトリにコミットされません。

## メンテナーとフィードバック

[xyQuant](https://github.com/xystudio-ai) がメンテナンスしています。

- WeChat 公式アカウント：[作者紹介とプロジェクト更新](https://mp.weixin.qq.com/s/k3NEph_JbMYwbCYn2ts8Dw)
- 小紅書：[xyQuant](https://www.xiaohongshu.com/user/profile/6718edb7000000001d0326cd)

<p>
  <img src="../../assets/qr/gzh-1.png" alt="xyQuant WeChat 公式アカウント QR コード" width="180" />
  <img src="../../assets/qr/xhs-1.png" alt="xyQuant 小紅書 QR コード" width="180" />
</p>

誤り、実行時の問題、改善案は [GitHub Issues](https://github.com/xystudio-ai/pyquant-roadmap/issues) へお寄せください。

## ライセンス

本プロジェクトは [MIT License](https://github.com/xystudio-ai/pyquant-roadmap/blob/main/LICENSE) で公開しています。

このリポジトリは学習と研究を目的としています。Notebook のバックテスト、指標、注文案を実取引の判断に使う場合は、前提となるデータと計算条件を自分で検証してください。
