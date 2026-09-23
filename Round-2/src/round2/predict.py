"""Load a complete saved pipeline and make predictions on new social posts."""
from pathlib import Path
import joblib


def predict_texts(model_path: str | Path, texts: list[str]):
    pipeline = joblib.load(model_path)
    return pipeline.predict(texts).tolist()
