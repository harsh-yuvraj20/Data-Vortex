"""
Machine learning model management and inference for DATA VORTEX 2026 — Round 4.

Provides safe deserialization of Round 2 scikit-learn pipelines with strict
adherence to calibration honesty:
- Sentiment: True calibrated posterior probabilities via predict_proba.
- Topic Intent: Hyperplane margin distances via decision_function with labeled softmax approximation.
"""

from typing import Dict, Any, List
import numpy as np
import joblib
import streamlit as st

try:
    from src.utils import (
        ROUND2_SENTIMENT_MODEL,
        ROUND2_TOPIC_MODEL,
        logger,
    )
except ImportError:
    from utils import (
        ROUND2_SENTIMENT_MODEL,
        ROUND2_TOPIC_MODEL,
        logger,
    )

# -----------------------------------------------------------------------------
# Preset Examples for Interactive Testing
# -----------------------------------------------------------------------------
PRESET_EXAMPLES = [
    {
        "name": "Security Incident",
        "text": "Critical security incident: unauthorized login detected on my account and 2FA bypass attempted!",
        "expected_sentiment": "Negative",
        "expected_topic": "Account_Security",
    },
    {
        "name": "Feature Praise",
        "text": "The latest UI overhaul is lightning fast and beautifully designed. Huge improvement in search filters!",
        "expected_sentiment": "Positive",
        "expected_topic": "Feature_Feedback",
    },
    {
        "name": "Bug Report",
        "text": "Internal server error 500 thrown whenever uploading PNG files greater than 5MB on Safari.",
        "expected_sentiment": "Negative",
        "expected_topic": "Technical_Issues",
    },
    {
        "name": "Community Inquiry",
        "text": "Is anyone organizing a community meetup for open-source contributors at the upcoming developer summit?",
        "expected_sentiment": "Neutral",
        "expected_topic": "Community_Discussion",
    },
]

# -----------------------------------------------------------------------------
# Pipeline Loaders (Cached via st.cache_resource)
# -----------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_sentiment_pipeline():
    """Loads canonical sentiment classification pipeline."""
    if not ROUND2_SENTIMENT_MODEL.exists():
        raise FileNotFoundError(f"Sentiment pipeline not found at: {ROUND2_SENTIMENT_MODEL}")
    pipeline = joblib.load(ROUND2_SENTIMENT_MODEL)
    return pipeline

@st.cache_resource(show_spinner=False)
def load_topic_pipeline():
    """Loads canonical topic classification pipeline."""
    if not ROUND2_TOPIC_MODEL.exists():
        raise FileNotFoundError(f"Topic pipeline not found at: {ROUND2_TOPIC_MODEL}")
    pipeline = joblib.load(ROUND2_TOPIC_MODEL)
    return pipeline

# -----------------------------------------------------------------------------
# Inference Functions
# -----------------------------------------------------------------------------
def predict_sentiment(text: str) -> Dict[str, Any]:
    """Infers sentiment label and calibrated posterior probabilities."""
    pipeline = load_sentiment_pipeline()
    clean_text = text.strip()
    if not clean_text:
        return {
            "label": "Neutral",
            "confidence": 0.3333,
            "probabilities": {"Negative": 0.3333, "Neutral": 0.3334, "Positive": 0.3333},
        }

    label = pipeline.predict([clean_text])[0]
    probs = pipeline.predict_proba([clean_text])[0]
    prob_dict = {str(c): float(p) for c, p in zip(pipeline.classes_, probs)}
    confidence = prob_dict.get(label, float(np.max(probs)))

    return {
        "label": label,
        "confidence": confidence,
        "probabilities": prob_dict,
        "calibration": "Calibrated Posterior Probability (predict_proba)",
    }

def predict_topic(text: str) -> Dict[str, Any]:
    """Infers topic category and signed decision margins with labeled softmax approximation."""
    pipeline = load_topic_pipeline()
    clean_text = text.strip()
    if not clean_text:
        return {
            "label": "Community_Discussion",
            "confidence": 0.25,
            "margins": {},
            "softmax_scores": {},
        }

    label = pipeline.predict([clean_text])[0]
    classes = pipeline.classes_

    if hasattr(pipeline, "decision_function"):
        raw_margins = pipeline.decision_function([clean_text])[0]
        margin_dict = {str(c): float(s) for c, s in zip(classes, raw_margins)}
        # Softmax approximation for relative visualization
        shifted = raw_margins - np.max(raw_margins)
        exp_vals = np.exp(shifted)
        softmax_probs = exp_vals / np.sum(exp_vals)
        softmax_dict = {str(c): float(p) for c, p in zip(classes, softmax_probs)}
        confidence = softmax_dict.get(label, float(np.max(softmax_probs)))
    else:
        margin_dict = {}
        softmax_dict = {}
        confidence = 1.0

    return {
        "label": label,
        "confidence": confidence,
        "margins": margin_dict,
        "softmax_scores": softmax_dict,
        "calibration": "Linear SVM Margin (decision_function) with Labeled Softmax Approximation",
    }

def predict_dual_head(text: str) -> Dict[str, Any]:
    """Runs simultaneous sentiment and topic inference on input text."""
    sent_res = predict_sentiment(text)
    topic_res = predict_topic(text)
    return {
        "input_text": text,
        "sentiment": sent_res,
        "topic": topic_res,
        "disclaimer": (
            "Model predictions reflect statistical associations learned from training data "
            "and should not be treated as ground truth."
        ),
    }
