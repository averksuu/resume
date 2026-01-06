# 🧬 AI Model for Predicting Drug Effects Using Single-Cell Transcriptomic Data
본 레포지터리는 대규모 세포–약물 Perturbation 데이터(Tahoe-100M)를 기반으로  
약물 처리로 유도되는 유전자 발현 변화(ΔExpression)를 학습하고,
  
- **Forward task**: 약물 + 세포주 → 유전자 발현 변화 예측  
- **Inverse task**: 원하는 발현 변화를 가장 잘 재현하는 약물 **Ranking / Retrieval**
  
을 동시에 다루는 **Transformer 기반 딥러닝 연구 프로젝트**입니다.
<br/>
<br/>

## ✨ Key Contributions
- **Cell-aware Drug Retrieval**: 동일한 약물이라도 세포주에 따라 반응이 달라진다는 점을 명시적으로 모델링
  
- **Dual Perspective Evaluation**: ΔExpression 회귀 성능과 약물 Retrieval 성능을 동시에 평가
  
- **Scalable Design**: Parquet 기반 대규모 perturbation 데이터를 직접 로딩하여 학습 가능
  
- **Representation Alignment**: 유전자 발현 변화 공간과 약물 SMILES 표현 공간 간 정렬 실험 수행
<br/>
<br/>

## 📁 Repository Structure
```
genespeak-drug-discovery/
├── f_p/
│   └── f_p_smalltargets.ipynb  #DRUG CANDIDATE 모듈 학습 코드
├── f_r/
│   └── f_r_onalldata_withcellline.ipynb  #RESPONSE PREDICTION 모듈 코드
└── repository-root/
└── making_data/
    ├── README.md                   
    ├── analysis1.ipynb              # exploratory analysis / preparation notebook
    ├── cell2id.csv                  # mapping: cell_name -> integer id
    ├── cell_embeddings.npy          # precomputed cell embeddings 
    ├── cell_line_metadata.parquet   # cell line metadata table
    ├── drug_metadata.parquet        # drug metadata table
    ├── drug_smiles_emb_all.pt       # SMILES/drug embeddings
    └── gene_metadata.parquet        # gene metadata table

```
<br/>
<br/>

## 🧪 Dataset & Preprocessing

### Data Source
- [TAHOE-100M](https://huggingface.co/datasets/tahoebio/Tahoe-100M) single-cell perturbation dataset (Parquet format)
- 각 샘플은 `(drug, cell line, gene)` 단위의 발현 반응 정보를 포함
<br/>

---

### Imbalance Analysis (`making_data/analysis1.ipynb`)
데이터 불균형을 다음 세 가지 수준에서 분석합니다.
  
- Drug-level
- Cell-line-level
- Drug–Cell-line pair-level
  
분석 결과, 강한 **Long-tail 분포**가 관찰되었으며 이를 바탕으로:
  
- 최소 샘플 수 기준 임계값 설정
- 학습 안정성을 위한 pair 단위 필터링
  
을 적용했습니다.
<br/>
<br/>

## 🧠 Methods (Two-Module Bidirectional Pipeline)

본 프로젝트는 단일세포 전사체 데이터에서 관측되는 **발현 변화(ΔX)** 를 활용해  
(1) **역문제(Drug Candidate; DC)** 로 탐색 공간을 먼저 줄이고,  
(2) **정문제(Response Prediction; RP)** 로 후보를 정밀 검증·재랭킹하는 **양방향 예측 파이프라인**을 구성합니다.

---

### Data Preprocessing
- 원시 발현 카운트에 대해 **log 변환 및 정규화** 수행
- 약물 처리군과 DMSO 대조군의 차이로 **발현 변화 시그니처(ΔX)** 계산
- 노이즈 감소 및 학습 효율을 위해 **상위 4,000 HVG(고분산 유전자)** 선택
- 두 모듈은 목적에 따라 **서로 다른 방식으로 토큰화**됩니다.
  - DC: **ΔX 패턴 자체** 중심
  - RP: **세포 기저 발현 + 약물 정보 + 세포 정보**를 함께 입력

---

## 1) Drug Candidate Module (DC) — Inverse Problem (Retrieval / 후보 생성)
**목표:** “이런 발현 변화(ΔX)를 만들었거나 되돌릴 수 있는 약물은 무엇인가?”라는 **역문제**를 해결합니다.  
아직 약물이 주어지지 않은 상태에서 시작하며, 관측된 **ΔX 시그니처만**으로 약물 특성을 거꾸로 추론합니다.

- **입력:** 특정 조건에서 관측된 **ΔExpression signature (ΔX)**
- **출력:** 하나의 Transformer 인코더에서 두 개의 헤드로 분기
  - **Target head:** 약물의 **생물학적 표적(target) 벡터** 예측
  - **Structure head:** 약물의 **구조적 특징(SMILES) 벡터** 예측
- **역할:** 수만 개 약물 후보를 **≤50개 수준**으로 줄이는 1차 필터(탐색 공간 축소)

### DC Training (복합 손실 학습)
약물의 본질을 여러 관점에서 학습하기 위해 **복합 손실 구조**를 사용합니다.
- **Cosine Similarity Loss:** 표적 표현의 **의미적 안정성** 학습
- **Binary Cross-Entropy (BCE) Loss:** 표적의 **존재 유무(멀티라벨)** 학습
- **InfoNCE Ranking Loss:** 후보 탐색에서 **정답 표적/특성을 상위로 랭킹**하도록 유도
- **CLIP-style Loss:** 약물의 **화학 구조(“구조 언어”)**와 전사체 반응(“효과 언어”)을  
  **같은 잠재 공간에서 정렬**하여 구조–효과 관계를 의미적으로 연결

> 핵심: DC는 “하나를 맞히는 분류기”가 아니라, **탐색 공간을 효과적으로 압축하는 retrieval 모듈**입니다.

---

## 2) Response Prediction Module (RP) — Forward Problem (Response Modeling / 검증)
**목표:** 후보 약물이 주어졌을 때, 병든 세포의 현재 상태를 기준으로  
약물 처리 후 **유전자 발현 변화(ΔX)** 를 직접 예측하는 **정문제** 모듈입니다.

- **입력(3가지 정보):**
  1) `[CELL]` 토큰: 세포주의 유전적 배경(세포 컨텍스트)
  2) `[DRUG]` 토큰: 후보 약물의 화학 구조 정보(예: SMILES 기반 표현)
  3) 병든 세포의 **기저 발현 프로파일(X_base)**  
     - **Cell2Sentence 스타일**로 유전자 토큰 시퀀스(유전자 ID + 발현값 표현)로 주입
- **출력:** 약물 처리 후 **ΔExpression 벡터(ΔX)** 생성
- **역할:** DC가 제안한 후보가 실제로 의미 있는 반응을 유도하는지 **정량 검증** 및 재랭킹

### RP Training (2-stage: 안정적 수렴 → 핵심 유전자 강조)
RP의 목표는 평균적으로만 맞추는 것이 아니라, **약물 효과를 대표하는 핵심 유전자**까지 포착하는 것입니다.
- **Stage 1: MSE Loss**
  - 전체 유전자 발현(또는 ΔX)의 전반적인 패턴을 **안정적으로 근사**하도록 학습
- **Stage 2: MSE + Gene Ranking Loss (점진적 추가)**
  - 약물로 인해 크게 변하는 유전자들이 **상위에 오르도록** 랭킹 손실을 추가
  - 초기에는 MSE만으로 수렴을 확보한 뒤, 이후 랭킹 손실을 **점진적으로 강화**하여
    “전체 근사”와 “핵심 유전자 포착”의 균형을 맞춤

---

## End-to-End Inference (파이프라인 동작)
1) 건강한 세포 vs 병든 세포 발현을 비교해 **병리적 지문(ΔX_query)** 생성  
2) **DC 모듈**이 ΔX_query로부터 표적/구조 특성을 추론 → **후보 약물 Top-K(≤50)** 생성  
3) **RP 모듈**이 각 후보 약물에 대해 반응(ΔX)을 시뮬레이션하고,  
   건강한 상태에 얼마나 가까워지는지 평가 → **최종 치료 후보 랭킹 출력**

---


### Metrics

#### Regression Metrics
- MSE
- MAE
- Cosine Similarity
- Pearson Correlation
- Spearman Correlation
  
#### Ranking / Retrieval Metrics
- Precision@K
- Recall@K
- NDCG@K
- mAP@K
<br/>

---

### Key Observations
- 세포주 토큰을 명시적으로 사용하는 것이 retrieval 안정성을 크게 향상시킴
- 랭킹 손실을 점진적으로 도입하면 학습 수렴이 더 부드러워짐
- 학습된 유전자 임베딩은 명시적 pathway supervision 없이도
  구조화된 다양체(manifold)를 형성함
<br/>
<br/>

## ▶️ How to Run

1. 데이터 불균형 분석
```
making_data/analysis1.ipynb
```

2. Fast prototyping (Inverse task)
```
f_p/f_p_smalltargets.ipynb
```

3. Full forward prediction & retrieval
```
f_r/f_r_onalldata_withcellline.ipynb
```
<br/>
<br/>


