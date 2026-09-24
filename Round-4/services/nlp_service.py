"""
NLP Service: Dual-Head Model Inference & Benchmark Intelligence.

Provides Round 2 model evaluation metrics, training distributions, and live
text classification with strict calibration separation between Logistic Regression
and Linear SVM.
"""

from typing import Dict, Any, List, Optional
import pandas as pd

from pathlib import Path
import sys

_ROUND4_DIR = str(Path(__file__).resolve().parents[1])
if _ROUND4_DIR not in sys.path:
    sys.path.insert(0, _ROUND4_DIR)

from repositories.model_repository import ModelRepository
from repositories.dataset_repository import DatasetRepository

class NLPService:
    """Business logic for Round 2 NLP models and live predictions."""

    # Presets for interactive testing
    PRESET_EXAMPLES = [
        {
            "name": "Security Breach Alert",
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

    @staticmethod
    def get_training_distributions() -> Dict[str, pd.DataFrame]:
        """Returns class distribution tables for Round 2 training corpus."""
        df = DatasetRepository.load_round2_training()
        
        sent_dist = df["sentiment_label"].value_counts().reset_index()
        sent_dist.columns = ["sentiment", "count"]
        sent_dist["percentage"] = (sent_dist["count"] / len(df) * 100).round(1)

        topic_dist = df["topic_category"].value_counts().reset_index()
        topic_dist.columns = ["topic", "count"]
        topic_dist["percentage"] = (topic_dist["count"] / len(df) * 100).round(1)

        return {
            "sentiment": sent_dist,
            "topic": topic_dist,
            "total_records": len(df),
        }

    @staticmethod
    def get_benchmarks() -> Dict[str, Any]:
        """Returns official frozen held-out test benchmarks."""
        return ModelRepository.get_benchmark_metrics()

    @staticmethod
    def predict_text(text: str) -> Dict[str, Any]:
        """
        Runs dual-head classification for input text with calibrated metrics.
        """
        sentiment_res = ModelRepository.predict_sentiment(text)
        topic_res = ModelRepository.predict_topic(text)

        return {
            "input_text": text,
            "sentiment": sentiment_res,
            "topic": topic_res,
            "disclaimer": (
                "Predictions reflect trained statistical associations from social media text "
                "and should not be treated as absolute ground truth."
            ),
        }
