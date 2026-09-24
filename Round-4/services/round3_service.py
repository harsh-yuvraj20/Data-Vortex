"""
Round 3 Service: Temporal Signal Tracking & Anomaly Mining.

Encapsulates Round 3 temporal trajectories, monthly net sentiment index calculation,
candidate sentiment shifts (SS1, SS2), engagement spikes (ES1, ES2, ES3), and entity mentions.
Adheres strictly to the non-causality rule and historical archive sampling boundaries.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

from pathlib import Path
import sys

_ROUND4_DIR = str(Path(__file__).resolve().parents[1])
if _ROUND4_DIR not in sys.path:
    sys.path.insert(0, _ROUND4_DIR)

from repositories.dataset_repository import DatasetRepository

class Round3Service:
    """Business logic for Round 3 temporal signals and shift detection."""

    # Authoritative Candidate Shifts (SS1, SS2)
    CANDIDATE_SHIFTS = [
        {
            "id": "SS1",
            "period": "September 2025 → October 2025",
            "prev_index": -0.2000,
            "next_index": -1.0000,
            "delta": -0.8000,
            "sample_size": "5 posts (Sep) → 3 posts (Oct)",
            "primary_topic": "European AI Act / Algorithm Compliance",
            "empirical_finding": (
                "Net sentiment dropped by -0.8000 following European AI/profiling compliance discussions. "
                "Causality is disclaimed due to low monthly archive volume."
            ),
            "finding": (
                "Net sentiment dropped by -0.8000 following European AI/profiling compliance discussions. "
                "Causality is disclaimed due to low monthly archive volume."
            ),
        },
        {
            "id": "SS2",
            "period": "October 2024 → November 2024",
            "prev_index": -1.0000,
            "next_index": -0.2000,
            "delta": 0.8000,
            "sample_size": "4 posts (Oct) → 5 posts (Nov)",
            "primary_topic": "Recommendation Algorithm Source Code / Open Source",
            "empirical_finding": (
                "Sharp positive sentiment rebound (+0.8000) from unanimous negative sentiment. "
                "Corresponds to technical discussions of recommendation algorithm architectures."
            ),
            "finding": (
                "Sharp positive sentiment rebound (+0.8000) from unanimous negative sentiment. "
                "Corresponds to technical discussions of recommendation algorithm architectures."
            ),
        },
    ]

    # Authoritative Engagement Spikes (ES1, ES2, ES3)
    ENGAGEMENT_SPIKES = [
        {
            "id": "ES1",
            "date": "2023-03-31",
            "observed_score": 1704.0,
            "baseline_mean": 6.00,
            "ratio": 284.0,
            "title": "Twitter's Recommendation Algorithm",
            "sentiment": "Negative",
            "topic": "Algorithm_Release / Open_Source",
        },
        {
            "id": "ES2",
            "date": "2026-02-15",
            "observed_score": 338.0,
            "baseline_mean": 6.00,
            "ratio": 56.3,
            "title": "NewPipe: YouTube client without vertical videos and algorithmic feed",
            "sentiment": "Negative",
            "topic": "Feed_Control / Client_Alternatives",
        },
        {
            "id": "ES3",
            "date": "2025-09-09",
            "observed_score": 265.0,
            "baseline_mean": 6.00,
            "ratio": 44.2,
            "title": "Source code for the X recommendation algorithm",
            "sentiment": "Positive",
            "topic": "Algorithm_Source / Technical_Audit",
        },
    ]

    # Target Entity Gazetteer
    GAZETTEER = ["Twitter", "Reddit", "Meta", "Google", "TikTok", "YouTube", "Instagram", "Hacker News"]

    @staticmethod
    def get_monthly_trajectory() -> pd.DataFrame:
        """
        Computes monthly post volume and Net Sentiment Index: (Pos - Neg) / Total.
        """
        df = DatasetRepository.load_round3_reactions().copy()
        
        # Aggregate by year_month and predicted_sentiment
        grouped = df.groupby(["year_month", "predicted_sentiment"]).size().unstack(fill_value=0)
        for col in ["Positive", "Negative", "Neutral"]:
            if col not in grouped.columns:
                grouped[col] = 0
        
        grouped["total"] = grouped["Positive"] + grouped["Negative"] + grouped["Neutral"]
        grouped["net_sentiment_index"] = (grouped["Positive"] - grouped["Negative"]) / grouped["total"]
        grouped["net_sentiment_index"] = grouped["net_sentiment_index"].round(4)
        
        res = grouped.reset_index()
        res["date"] = pd.to_datetime(res["year_month"] + "-01")
        return res.sort_values(by="date")

    @classmethod
    def get_entity_frequencies(cls) -> pd.DataFrame:
        """Counts occurrences of gazetteer entities across text fields."""
        df = DatasetRepository.load_round3_reactions()
        text_corpus = (df["text"].fillna("") + " " + df["title"].fillna("")).str.lower()

        counts = []
        for entity in cls.GAZETTEER:
            c = text_corpus.str.count(entity.lower()).sum()
            counts.append({"entity": entity, "mentions": int(c)})
        
        res = pd.DataFrame(counts).sort_values(by="mentions", ascending=False)
        return res[res["mentions"] > 0]

    @staticmethod
    def get_candidate_shifts() -> pd.DataFrame:
        """Returns dataframe of verified candidate shifts."""
        return pd.DataFrame(Round3Service.CANDIDATE_SHIFTS)

    @staticmethod
    def get_engagement_spikes() -> pd.DataFrame:
        """Returns dataframe of verified engagement spikes."""
        return pd.DataFrame(Round3Service.ENGAGEMENT_SPIKES)
