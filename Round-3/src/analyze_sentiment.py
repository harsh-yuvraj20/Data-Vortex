from __future__ import annotations
import joblib, pandas as pd
from utils import MODELS, RESULTS, save_csv

def predict_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    model = joblib.load(MODELS/'sentiment_label_pipeline.pkl')
    out = df.copy(); out['predicted_sentiment'] = model.predict(out.cleaned_text)
    if hasattr(model, 'predict_proba'):
        probabilities = model.predict_proba(out.cleaned_text)
        for i, label in enumerate(model.classes_): out[f'{str(label).lower()}_probability'] = probabilities[:, i]
    save_csv(out, RESULTS/'sentiment_results.csv')
    return out
