"""
Model Repository for Round 4.

Loads and caches the canonical Round 2 sentiment and topic classification pipelines
via joblib. Provides safe inference methods adhering to strict calibration honesty:
- Sentiment: True calibrated posterior probabilities via predict_proba.
- Topic: Hyperplane decision margin distances via decision_function with explicit
  labeled softmax approximation.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import joblib
import streamlit as st

from pathlib import Path
import sys

_ROUND4_DIR = str(Path(__file__).resolve().parents[1])
if _ROUND4_DIR not in sys.path:
    sys.path.insert(0, _ROUND4_DIR)

from config.settings import (
    ROUND2_SENTIMENT_MODEL,
    ROUND2_TOPIC_MODEL,
    FROZEN_SENTIMENT_METRICS,
    FROZEN_TOPIC_METRICS,
)
from utils.validation import validate_model_pipeline
from utils.logging_config import logger

class ModelRepository:
    """Manages cached access to trained scikit-learn pipelines."""

    @staticmethod
    @st.cache_resource(show_spinner=False)
    def load_sentiment_pipeline():
        """Loads canonical sentiment classification pipeline."""
        if not ROUND2_SENTIMENT_MODEL.exists():
            raise FileNotFoundError(f"Sentiment pipeline not found: {ROUND2_SENTIMENT_MODEL}")
        pipeline = joblib.load(ROUND2_SENTIMENT_MODEL)
        validate_model_pipeline(
            pipeline,
            required_classes=["Negative", "Neutral", "Positive"],
            name="Sentiment Pipeline",
        )
        return pipeline

    @staticmethod
    @st.cache_resource(show_spinner=False)
    def load_topic_pipeline():
        """Loads canonical topic classification pipeline."""
        if not ROUND2_TOPIC_MODEL.exists():
            raise FileNotFoundError(f"Topic pipeline not found: {ROUND2_TOPIC_MODEL}")
        pipeline = joblib.load(ROUND2_TOPIC_MODEL)
        validate_model_pipeline(
            pipeline,
            required_classes=["Account_Security", "Community_Discussion", "Feature_Feedback", "Technical_Issues"],
            name="Topic Pipeline",
        )
        return pipeline

    @classmethod
    def predict_sentiment(cls, text: str) -> Dict[str, Any]:
        """
        Infers sentiment label and calibrated probabilities for input text.
        """
        pipeline = cls.load_sentiment_pipeline()
        clean_input = text.strip()
        if not clean_input:
            return {"label": "Neutral", "confidence": 0.3333, "probabilities": {"Negative": 0.3333, "Neutral": 0.3334, "Positive": 0.3333}}
        
        pred_label = pipeline.predict([clean_input])[0]
        probs = pipeline.predict_proba([clean_input])[0]
        classes = pipeline.classes_
        
        prob_dict = {str(c): float(p) for c, p in zip(classes, probs)}
        confidence = prob_dict.get(pred_label, float(np.max(probs)))
        
        return {
            "label": pred_label,
            "confidence": confidence,
            "probabilities": prob_dict,
            "calibration_type": "Calibrated Posterior Probability (predict_proba)",
        }

    @classmethod
    def predict_topic(cls, text: str) -> Dict[str, Any]:
        """
        Infers topic category and margin distances with explicit softmax approximation.
        """
        pipeline = cls.load_topic_pipeline()
        clean_input = text.strip()
        if not clean_input:
            return {"label": "Community_Discussion", "confidence": 0.25, "margins": {}, "softmax_scores": {}}
        
        pred_label = pipeline.predict([clean_input])[0]
        classes = pipeline.classes_
        
        if hasattr(pipeline, "decision_function"):
            raw_scores = pipeline.decision_function([clean_input])[0]
            # Convert to dictionary of signed margin distances
            margin_dict = {str(c): float(s) for c, s in zip(classes, raw_scores)}
            # Softmax approximation for visual comparison
            exp_scores = np.exp(raw_scores - np.max(raw_scores))
            softmax_probs = exp_scores / np.sum(exp_scores)
            softmax_dict = {str(c): float(p) for c, p in zip(classes, softmax_probs)}
            confidence = softmax_dict.get(pred_label, float(np.max(softmax_probs)))
        else:
            margin_dict = {}
            softmax_dict = {}
            confidence = 1.0
        
        return {
            "label": pred_label,
            "confidence": confidence,
            "margins": margin_dict,
            "softmax_scores": softmax_dict,
            "calibration_type": "Linear SVM Margin (decision_function) with Labeled Softmax Approximation",
        }

    @staticmethod
    def get_benchmark_metrics() -> Dict[str, Any]:
        """Returns the official frozen held-out test benchmarks from Round 2."""
        return {
            "sentiment": FROZEN_SENTIMENT_METRICS,
            "topic": FROZEN_TOPIC_METRICS,
        }

@st.cache_resource
def get_model_repo() -> ModelRepository:
    """Returns singleton model repository."""
    return ModelRepository()
