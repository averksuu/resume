# 혈당 수치 예측 (Terra AI & EndolainAI)

**Slides:** [Google Slides 발표 자료](https://docs.google.com/presentation/d/1dSC61bIsJKEDsOcXXpTBXMmDkMtHvblmJZduMcj_CVw/edit?usp=sharing)  
**Gratitude Letter:** [감사장(감사 편지)](https://drive.google.com/file/d/1iTA5zQrCbilhcllsPVDLOFZytPdhnZJi/view?usp=sharing)  
**Landing page:** https://ai-hunter.ru/endolainai

---

## 📝 프로젝트 개요
- **목표(Objective):** 연속혈당측정(CGM) 데이터를 기반으로 혈당 수치를 예측하고 인슐린 투여량을 추천합니다.  
- **데이터(Data):** CGM 시계열, 인슐린 치료 정보, 영양(식이) 및 활동 로그.  
- **모델(Models):** 15분 슬라이딩 윈도우 특징을 사용한 LightGBM & XGBoost.  
- **성능(Performance):** RMSE ≈ 1.93, R² ≈ 0.38.

## 🛠 기술 스택
- **언어 & 라이브러리:** Python, pandas, NumPy, LightGBM, XGBoost  
- **배포(Deployment):** Telegram Bot API, FastAPI, Docker

## 🚀 사용 방법
1. `endolainai_glucose_prediction.ipynb`를 실행하여 데이터 로드, 모델 학습 및 평가를 수행합니다.  
2. Telegram 봇을 빌드하고 실행합니다:
   ```bash
   cd projects/glucose-prediction
   docker build -t glucose-bot -f Dockerfile .
   docker run -e TELEGRAM_BOT_TOKEN=<your_token> glucose-bot
