import pandas as pd
import joblib
import lightgbm as lgb
from config import LGBM_MODEL_PATH, NEW_DATA_PATH

def update_model():
    try:
        df_new = pd.read_csv(NEW_DATA_PATH)
    except Exception as e:
        print("No new data for incremental training found:", e)
        return

    # Assumes df_new contains features in columns "feature_0", "feature_1", ...,
    # as well as "timestamp" and "true_value".
    if "true_value" not in df_new.columns:
        print("New dataset does not contain 'true_value'. No retraining performed.")
        return

    df_new = df_new[df_new["true_value"] != ""]
    if df_new.empty:
        print("No records with ground-truth values for retraining.")
        return

    y_new = df_new["true_value"].astype(float)
    X_new = df_new.drop(columns=["true_value", "timestamp"])

    train_data = lgb.Dataset(X_new, label=y_new)
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'verbosity': -1
    }
    init_model = joblib.load(LGBM_MODEL_PATH)
    updated_model = lgb.train(
        params,
        train_data,
        num_boost_round=200,
        init_model=init_model
    )
    joblib.dump(updated_model, LGBM_MODEL_PATH)
    print("Model updated and saved to", LGBM_MODEL_PATH)
