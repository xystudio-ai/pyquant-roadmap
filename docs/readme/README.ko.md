<div align="right"><a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/README.md">简体中文</a> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.en.md">English</a> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.ja.md">日本語</a> · <strong>한국어</strong> · <a href="https://github.com/xystudio-ai/pyquant-roadmap/blob/main/docs/readme/README.zh-TW.md">繁體中文</a></div>

# pyquant-roadmap / Python 퀀트 실습 로드맵

[![Python 3.11](https://img.shields.io/badge/python-3.11-2563eb)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-0f766e)](https://github.com/xystudio-ai/pyquant-roadmap/blob/main/LICENSE)

`pyquant-roadmap`는 순서대로 실행하며 배우는 Python 퀀트 리서치 입문 프로젝트입니다. 14개의 Jupyter Notebook이 하나의 사례를 공유하며 데이터, 팩터, 포트폴리오 구성, 백테스트, 평가, 신호 출력을 한 흐름으로 연결합니다.

퀀트 트레이딩을 처음 체계적으로 배우는 사람을 위한 프로젝트입니다. 시작 전에 교재 한 권을 끝내거나 복잡한 프레임워크를 고를 필요는 없습니다. 먼저 로컬에서 전체 흐름을 실행한 뒤 각 단계가 왜 필요한지 돌아보는 방식으로 학습할 수 있습니다.

## 해결하는 문제

입문 단계에서 어려운 것은 개별 수식이나 Python 함수보다 흩어진 지식을 연결하는 일입니다. 수익률을 계산할 수 있어도 팩터 연구로 어떻게 이어지는지 모르거나, 전략 규칙을 작성해도 포트폴리오 비중, 거래 비용, 성과 보고서가 어떻게 맞물리는지 알기 어려울 수 있습니다.

이 저장소는 개인 퀀트 리서치의 기본 흐름을 연결된 Notebook으로 실행합니다.

```text
데이터 수집과 정리
→ 팩터 생성과 검증
→ 팩터 점수를 포트폴리오 비중으로 변환
→ 리밸런싱과 거래 비용을 반영한 백테스트
→ 벤치마크와 비교해 결과 평가
→ 목표 비중, 주문 제안, 검토 자료 출력
```

각 장은 흐름의 한 부분을 진행하고 그 결과를 뒤의 장에서 사용합니다. 서로 무관한 14개 예제가 아니라 다시 실행하고 수정할 수 있는 하나의 리서치 파이프라인입니다.

## 제공 내용

| 내용 | 용도 |
| --- | --- |
| 순서가 있는 14개 Notebook | 환경 확인부터 리서치, 백테스트, 검토까지 진행 |
| 소규모 실제 ETF 일봉 샘플 | 다운로드 없이 시작하고 데이터 구조 확인 |
| `lib/`의 재사용 함수 | Notebook 로직을 호출 가능한 Python 코드로 정리하는 방식 학습 |
| 데이터 소스와 전략 설정 | 데이터, 파라미터, 리서치 코드 분리 관리 |
| 로컬 실행 결과 | 차트, 지표, 목표 비중, 주문 제안, 보고서 생성 |

전체 경로를 마치면 Python 퀀트 프로젝트의 주요 단계를 파악하고 팩터, 포트폴리오, 백테스트 사이에서 데이터가 어떻게 이동하는지 이해할 수 있습니다. 이후 데이터 처리, 전략 연구, 재현 가능한 워크플로, AI 보조 연구 중 무엇을 더 공부할지도 판단하기 쉬워집니다.

## 빠른 시작

Git, Conda, Python 3.11이 필요합니다. 저장소에서 제공하는 Conda 환경 사용을 권장합니다.

```bash
git clone https://github.com/xystudio-ai/pyquant-roadmap.git
cd pyquant-roadmap
conda env create -f environment.yml
conda activate pyquant-roadmap
jupyter lab
```

`notebooks/`를 열어 `01_quant_workflow_overview.ipynb`부터 `14_ai_helper_and_next_steps.ipynb`까지 번호 순서대로 실행하세요.

이미 Python 3.11 환경이 있다면 의존성을 직접 설치할 수 있습니다.

```bash
python -m pip install pandas numpy matplotlib scipy statsmodels pyarrow pyyaml akshare bt quantstats ta notebook jupyterlab
jupyter lab
```

포함된 샘플 데이터만으로 초반 장을 진행할 수 있습니다. 04장에서는 AKShare로 같은 종류의 시장 데이터를 내려받아 캐시하는 방법도 다루며, 이 단계에는 네트워크 연결이 필요합니다.

## Notebook 경로

| 번호 | 주제 | 이해하게 되는 내용 |
| --- | --- | --- |
| 01 | 퀀트 트레이딩 전체 흐름과 메인 사례 | 한 번의 리서치를 구성하는 주요 단계 |
| 02 | 환경, 프로젝트 구조, 첫 실행 | 로컬 환경과 경로를 확인하는 방법 |
| 03 | 실무에 필요한 pandas / NumPy | 퀀트 리서치의 표와 배열을 다루는 방법 |
| 04 | 데이터 수집, 스키마 표준화, 캐시 | 시장 데이터를 재사용 가능한 형태로 정리하는 방법 |
| 05 | 정제, 정렬, 수익률 | 날짜, 결측치, 수익률 시계열 처리 방법 |
| 06 | 팩터 생성 | 전략 아이디어를 계산 가능한 특성으로 바꾸는 방법 |
| 07 | 팩터 검증 | IC와 그룹별 수익률로 팩터를 1차 검증하는 방법 |
| 08 | 포트폴리오 구성 | 팩터 점수를 목표 비중으로 변환하는 방법 |
| 09 | 백테스트 엔진 | 규칙, 비용, 오픈소스 엔진을 함께 사용하는 방법 |
| 10 | 성과 평가와 보고서 | 지표, 자산 곡선, 벤치마크 비교를 읽는 방법 |
| 11 | 재현 가능한 파이프라인 | 일회성 실험을 반복 가능한 흐름으로 정리하는 방법 |
| 12 | 전략 분류 | 일반적인 전략 유형의 구조적 차이 |
| 13 | 대표 전략 | 입문용 전략을 코드로 구현하는 방법 |
| 14 | AI 보조와 다음 단계 | AI가 도움이 되는 단계와 다음 학습 방향 |

번호 순서대로 실행하는 것을 권장합니다. 뒤쪽 Notebook은 앞에서 정한 데이터 규약, 디렉터리, 리서치 방식을 사용합니다.

## 저장소 구조

```text
pyquant-roadmap/
├── notebooks/        # 14개 Notebook과 기본 학습 경로
├── lib/              # 데이터, 팩터, 포트폴리오, 백테스트, 평가 함수
├── configs/          # 데이터 소스, 전략, 장별 설정
├── data/sample/      # 저장소에 포함된 소규모 실제 샘플 데이터
├── data/raw/         # 다운로드하거나 가져온 원본 데이터
├── data/processed/   # 정제한 리서치 데이터
├── outputs/          # 로컬 실행 결과, 기본적으로 커밋하지 않음
├── assets/           # README 자료와 소셜 계정 QR 코드
├── environment.yml
└── pyproject.toml
```

학습의 중심은 `notebooks/`입니다. 로직을 이해한 뒤 `lib/`에서 재사용 가능한 코드로 정리한 방식을 확인하고, `configs/`에서 데이터 범위와 전략 파라미터를 바꿀 수 있습니다.

## 데이터와 출력

`data/sample/`에는 오프라인으로 사용할 수 있는 소규모 실제 ETF 일봉 데이터가 있습니다. 04장에서는 AKShare로 새 데이터를 가져올 수 있습니다. 외부 API는 변경될 수 있으므로 예제가 현재 동작과 맞지 않으면 AKShare 최신 문서와 반환 필드를 확인하세요.

Notebook 결과는 `outputs/results/`에 저장됩니다. 차트, 성과 지표, 목표 비중, 주문 제안, 검토 자료가 포함되며 기본적으로 저장소에 커밋하지 않습니다.

## 유지관리와 피드백

[xyQuant](https://github.com/xystudio-ai)가 유지관리합니다.

- WeChat 공식 계정: [작성자 소개와 프로젝트 업데이트](https://mp.weixin.qq.com/s/k3NEph_JbMYwbCYn2ts8Dw)
- Xiaohongshu: [xyQuant](https://www.xiaohongshu.com/user/profile/6718edb7000000001d0326cd)

<p>
  <img src="../../assets/qr/gzh-1.png" alt="xyQuant WeChat 공식 계정 QR 코드" width="180" />
  <img src="../../assets/qr/xhs-1.png" alt="xyQuant Xiaohongshu QR 코드" width="180" />
</p>

오류, 실행 문제, 개선 제안은 [GitHub Issues](https://github.com/xystudio-ai/pyquant-roadmap/issues)에 남겨 주세요.

## 라이선스

이 프로젝트는 [MIT License](https://github.com/xystudio-ai/pyquant-roadmap/blob/main/LICENSE)로 배포됩니다.

이 저장소는 학습과 연구를 위한 자료입니다. Notebook의 백테스트, 지표, 주문 제안을 실제 거래 판단에 사용하기 전에 데이터 가정과 계산 조건을 직접 검증하세요.
