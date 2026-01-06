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

## 🧠 Methods
### Inverse Retrieval (Drug Candidate Retrieval/Ranking; f_p 또는 DRUG CANDIDATE 모듈)
**목표:** 주어진 **쿼리 시그니처(ΔX_query)** 에 대해, 이를 가장 잘 설명(또는 재현)할 수 있는 **후보 약물**을 검색/랭킹합니다.

- **입력:** 쿼리 ΔExpression signature `ΔX_query`
- **출력:** 후보 약물들에 대한 점수/랭킹 `score(drug | ΔX_query)`
- **핵심 아이디어:**  
  ΔX_query를 임베딩으로 인코딩한 뒤, **정답 약물(positive)** 과는 가깝게, 다른 약물(negatives)과는 멀어지도록 학습합니다.

- **학습 데이터:** (drug, cell line) → 관측 ΔX 를 이용하여  
  `ΔX` 를 해당 drug의 **positive query** 로 사용하고, 동일 배치/라이브러리 내 다른 drug들을 **negative** 로 샘플링

- **학습 목적함수(예시):**
  - **Ranking/Contrastive 손실 (InfoNCE):**  
    `L_rank = -log exp(sim(q, d+)/τ) / Σ exp(sim(q, d_i)/τ)`
    - `q = Enc(ΔX)` : 시그니처 인코더 출력  
    - `d+` : 정답 약물 임베딩, `d_i` : negative 약물 임베딩  
    - `sim(·)` : cosine 또는 dot-product, `τ` : temperature
  - (선택) **BCE 기반 retrieval 손실:** 후보 약물 전체(또는 sampled set)에 대해 정답/비정답을 분류하도록 보조 학습

> inverse 모듈은 “이 ΔX를 만든(또는 반대로 만들 수 있는) 약이 무엇인가?”를 푸는 **검색/랭킹 모듈**입니다.

### Forward Prediction (Response Prediction; f_r)
**목표:** 특정 조건에서의 세포 상태(기저 발현)와 약물 정보를 바탕으로, 약물 처리 후 **유전자 발현 변화(ΔX)** 를 예측합니다.

- **입력:**
  - **기저 발현 프로필** `X_base` (예: DMSO / pre-treatment expression)
  - **약물 표현** (예: SMILES embedding 또는 drug embedding)
  - (선택) **cell-line 정보** (cell token/embedding)

- **표현 방식 (Cell2Sentence 스타일):**
  - 유전자들을 토큰 시퀀스로 구성하고, 각 토큰은
    - `gene id embedding` + `expression value embedding(또는 bin embedding)`  
    (+ 필요 시 positional/attribute embedding)
  - 시퀀스에 `[CELL]` 같은 컨텍스트 토큰을 포함해 cell-specific context를 주입할 수 있음

- **출력:**
  - 예측된 `\hat{ΔX} ∈ R^G` (G: 사용 유전자 수, 예: HVG)
  - (대안) `\hat{X_after} = X_base + \hat{ΔX}` 형태로 after-expression을 직접 구성

- **학습 데이터:** `(X_base, drug, cell)` → 관측 `ΔX = X_treated − X_base`
- **학습 목적함수(예시):**
  - **재구성(회귀) 손실:** `L_rec = MSE(ΔX, \hat{ΔX})` (또는 Huber)
  - (선택) **패턴 보존 보조 손실:** cosine 유사도 기반 항 등

---
### Inference (실사용 흐름)
1) 입력으로 받은 `ΔX_query` 에 대해 inverse 모듈로 **Top-K 후보 약물**을 검색  
2) 각 후보 약물에 대해 f_r로 `\hat{ΔX}(drug, cell)` 를 예측(또는 조건에 맞는 response 시뮬레이션)  
3) `ΔX_query` 와 `\hat{ΔX}` 의 유사도/오차를 기반으로 **재랭킹(re-ranking)** 하여 최종 후보를 출력

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


