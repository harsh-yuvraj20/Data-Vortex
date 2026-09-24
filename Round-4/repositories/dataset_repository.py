"""
Dataset Repository for Round 4.

Loads and caches canonical datasets from Rounds 1, 2, and 3 via relative paths
without duplicating data. Performs schema validation and provides deterministic views.
"""

from typing import Dict, Any, Optional
import pandas as pd
import streamlit as st

from pathlib import Path
import sys

_ROUND4_DIR = str(Path(__file__).resolve().parents[1])
if _ROUND4_DIR not in sys.path:
    sys.path.insert(0, _ROUND4_DIR)

from config.settings import (
    ROUND1_POSTS_CSV,
    ROUND1_USERS_CSV,
    ROUND1_RAW_POSTS_CSV,
    ROUND2_TRAIN_CSV,
    ROUND3_REACTIONS_CSV,
)
from utils.validation import validate_dataframe
from utils.logging_config import logger

class DatasetRepository:
    """Manages cached access to tabular project datasets."""

    @staticmethod
    @st.cache_data(show_spinner=False)
    def load_round1_posts() -> pd.DataFrame:
        """Loads canonical cleaned posts dataset (12,000 records)."""
        if not ROUND1_POSTS_CSV.exists():
            raise FileNotFoundError(f"Cleaned posts not found: {ROUND1_POSTS_CSV}")
        df = pd.read_csv(ROUND1_POSTS_CSV)
        validate_dataframe(
            df,
            required_columns=["post_id", "user_id", "platform", "text_content", "timestamp", "likes", "shares", "comments"],
            min_rows=12000,
            name="Round-1 Cleaned Posts",
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["year_month"] = df["timestamp"].dt.to_period("M").astype(str)
        return df

    @staticmethod
    @st.cache_data(show_spinner=False)
    def load_round1_users() -> pd.DataFrame:
        """Loads canonical cleaned users dataset (1,500 records)."""
        if not ROUND1_USERS_CSV.exists():
            raise FileNotFoundError(f"Cleaned users not found: {ROUND1_USERS_CSV}")
        df = pd.read_csv(ROUND1_USERS_CSV)
        validate_dataframe(
            df,
            required_columns=["user_id", "location", "language", "account_created", "follower_count"],
            min_rows=1500,
            name="Round-1 Cleaned Users",
        )
        df["account_created"] = pd.to_datetime(df["account_created"])
        return df

    @staticmethod
    @st.cache_data(show_spinner=False)
    def load_round1_corrupted() -> pd.DataFrame:
        """Loads raw corrupted posts (for forensic comparison)."""
        if not ROUND1_RAW_POSTS_CSV.exists():
            raise FileNotFoundError(f"Raw corrupted posts not found: {ROUND1_RAW_POSTS_CSV}")
        return pd.read_csv(ROUND1_RAW_POSTS_CSV)

    @staticmethod
    @st.cache_data(show_spinner=False)
    def load_round2_training() -> pd.DataFrame:
        """Loads canonical NLP training dataset (9,000 records, balanced 1:1:1)."""
        if not ROUND2_TRAIN_CSV.exists():
            raise FileNotFoundError(f"NLP training dataset not found: {ROUND2_TRAIN_CSV}")
        df = pd.read_csv(ROUND2_TRAIN_CSV)
        validate_dataframe(
            df,
            required_columns=["post_text", "sentiment_label", "topic_category"],
            min_rows=9000,
            name="Round-2 NLP Training Data",
        )
        return df

    @staticmethod
    @st.cache_data(show_spinner=False)
    def load_round3_reactions() -> pd.DataFrame:
        """Loads canonical reaction archive dataset (204 records)."""
        if not ROUND3_REACTIONS_CSV.exists():
            raise FileNotFoundError(f"Reaction dataset not found: {ROUND3_REACTIONS_CSV}")
        df = pd.read_csv(ROUND3_REACTIONS_CSV)
        validate_dataframe(
            df,
            required_columns=["id", "source_type", "date", "text", "predicted_sentiment"],
            min_rows=200,
            name="Round-3 Reactions",
        )
        df["date"] = pd.to_datetime(df["date"])
        df["year_month"] = df["date"].dt.to_period("M").astype(str)
        return df

    @classmethod
    def get_dataset_inventory(cls) -> Dict[str, Dict[str, Any]]:
        """Returns structured metadata across all canonical datasets."""
        posts = cls.load_round1_posts()
        users = cls.load_round1_users()
        train = cls.load_round2_training()
        reactions = cls.load_round3_reactions()

        return {
            "round1_posts": {
                "name": "Social Engine Posts (Cleaned)",
                "round": "Round 1 Phase 1",
                "rows": len(posts),
                "columns": len(posts.columns),
                "date_range": f"{posts['timestamp'].min().strftime('%Y-%m-%d')} to {posts['timestamp'].max().strftime('%Y-%m-%d')}",
            },
            "round1_users": {
                "name": "Social Engine Users (Cleaned)",
                "round": "Round 1 Phase 1",
                "rows": len(users),
                "columns": len(users.columns),
                "date_range": "Platform User Registry",
            },
            "round2_training": {
                "name": "Labeled NLP Training Corpus",
                "round": "Round 2",
                "rows": len(train),
                "columns": len(train.columns),
                "balance": "Exact 1:1:1 (3k Neg / 3k Neu / 3k Pos)",
            },
            "round3_reactions": {
                "name": "Algorithm Reaction Archive",
                "round": "Round 3",
                "rows": len(reactions),
                "columns": len(reactions.columns),
                "date_range": f"{reactions['date'].min().strftime('%Y-%m-%d')} to {reactions['date'].max().strftime('%Y-%m-%d')}",
            },
        }

@st.cache_resource
def get_dataset_repo() -> DatasetRepository:
    """Returns a singleton dataset repository."""
    return DatasetRepository()
