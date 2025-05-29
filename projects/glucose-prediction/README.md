# Glucose Level Prediction (Terra AI & EndolainAI)

**Slides:** [Google Slides Presentation](https://docs.google.com/presentation/d/1dSC61bIsJKEDsOcXXpTBXMmDkMtHvblmJZduMcj_CVw/edit?usp=sharing)  
**Gratitude Letter:** [Letter of Appreciation](https://drive.google.com/file/d/1iTA5zQrCbilhcllsPVDLOFZytPdhnZJi/view?usp=sharing)  
**Landing page:** https://ai-hunter.ru/endolainai

---

## 📝 Project Overview
- **Objective:** Predict blood glucose levels from continuous glucose monitoring data and recommend insulin doses.  
- **Data:** CGM time series, insulin therapy, nutrition, and activity logs.  
- **Models:** LightGBM & XGBoost using 15-minute sliding windows.  
- **Performance:** RMSE ≈ 1.93, R² ≈ 0.38.

## 🛠 Tech Stack
- **Languages & Libraries:** Python, pandas, NumPy, LightGBM, XGBoost  
- **Deployment:** Telegram Bot API, FastAPI, Docker

## 🚀 Usage
1. Run `endolainai_glucose_prediction.ipynb` to load data, train and evaluate models.  
2. Build and launch the Telegram bot:
   ```bash
   cd projects/glucose-prediction
   docker build -t glucose-bot -f Dockerfile .
   docker run -e TELEGRAM_BOT_TOKEN=<your_token> glucose-bot
