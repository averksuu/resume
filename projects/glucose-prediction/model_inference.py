# model_inference.py
import joblib
import pandas as pd
from config import LGBM_MODEL_PATH, XGB_MODEL_PATH

def load_models():
    lgb_model = joblib.load(LGBM_MODEL_PATH)
    xgb_model = joblib.load(XGB_MODEL_PATH)
    return lgb_model, xgb_model

def predict(models, X: pd.DataFrame):
    lgb_model, xgb_model = models
    pred_lgb = lgb_model.predict(X)
    pred_xgb = xgb_model.predict(X)
    return pred_lgb, pred_xgb
