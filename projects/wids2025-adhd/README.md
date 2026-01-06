# WiDS 2025 – ADHD & 성별 예측

WiDS Datathon 2025를 위한 Kaggle 대회 프로젝트입니다.

**Task:**  
뇌 영상(fMRI) 및 설문 데이터를 기반으로 두 개의 타깃을 예측합니다:  
- ADHD 진단 여부 (1/0)  
- 성별 (여성 = 1, 남성 = 0)

**Approach:**  
- 멀티 아웃풋(Multi-output) XGBoost 분류기  
- 클래스 불균형 완화를 위한 SMOTE 적용  
- 표형(tabular) + fMRI 기반 예측을 결합한 앙상블

**Result:**  
리더보드 상위 35% 달성 🎉

- **[Kaggle Notebook](https://www.kaggle.com/code/kseniiaaver/wids-2025-adhd-gender-classification-xgboost)**
