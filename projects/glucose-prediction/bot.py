import logging
import joblib
import pandas as pd
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN, LGBM_MODEL_PATH, XGB_MODEL_PATH, NEW_DATA_PATH
from model_inference import load_models, predict
from update_model import update_model

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

lgb_model, xgb_model = load_models()

def save_new_data(features, true_value=None):
    """Append new feature data (and optional ground-truth) for incremental training."""
    new_entry = features.copy()
    new_entry.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    new_entry.append(true_value if true_value is not None else "")

    num_features = len(features)
    columns = [f"feature_{i}" for i in range(num_features)] + ["timestamp", "true_value"]
    df_new = pd.DataFrame([new_entry], columns=columns)

    try:
        df_new.to_csv(NEW_DATA_PATH, mode="a", index=False,
                      header=not pd.io.common.file_exists(NEW_DATA_PATH))
    except Exception as e:
        print("Error saving new data:", e)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm a prediction bot. Send me comma-separated features.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send a list of comma-separated features. "
        "If you have a ground-truth value, append it after a space. "
        "Example: '1.2,3.4,5.6 7.8'."
    )

async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update_model()
    await update.message.reply_text("Model has been retrained on new data.")

async def predict_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        parts = text.split()
        features = list(map(float, parts[0].split(',')))
        X = pd.DataFrame([features])
        pred_lgb, pred_xgb = predict((lgb_model, xgb_model), X)
        response = (
            f"LightGBM prediction: {pred_lgb[0]:.2f}\n"
            f"XGBoost prediction: {pred_xgb[0]:.2f}"
        )
        if len(parts) > 1:
            try:
                true_value = float(parts[1])
                save_new_data(features, true_value)
            except:
                save_new_data(features)
        else:
            save_new_data(features)
    except Exception as e:
        response = f"Error processing input: {e}"
    await update.message.reply_text(response)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("update", update_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, predict_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
