"""
Data Service for Round 4.

Provides high-level dataset querying, filtering, search, and summary aggregations
for the application presentation layers.
"""

from typing import Dict, Any, List, Optional
import pandas as pd

from pathlib import Path
import sys

_ROUND4_DIR = str(Path(__file__).resolve().parents[1])
if _ROUND4_DIR not in sys.path:
    sys.path.insert(0, _ROUND4_DIR)

from repositories.dataset_repository import DatasetRepository

class DataService:
    """Business logic for querying and filtering multi-round tabular records."""

    @staticmethod
    def get_system_scale_metrics() -> Dict[str, Any]:
        """Calculates executive KPI counts across all rounds."""
        posts = DatasetRepository.load_round1_posts()
        users = DatasetRepository.load_round1_users()
        train = DatasetRepository.load_round2_training()
        reactions = DatasetRepository.load_round3_reactions()

        total_likes = int(posts["likes"].sum())
        total_shares = int(posts["shares"].sum())
        total_comments = int(posts["comments"].sum())
        avg_engagement = round(float((posts["likes"] + posts["shares"] + posts["comments"]).mean()), 1)

        return {
            "total_cleaned_posts": len(posts),
            "total_registered_users": len(users),
            "total_nlp_training_records": len(train),
            "total_reaction_records": len(reactions),
            "total_likes": total_likes,
            "total_shares": total_shares,
            "total_comments": total_comments,
            "avg_engagement_per_post": avg_engagement,
            "post_date_span": f"{posts['timestamp'].min().strftime('%Y-%m')} to {posts['timestamp'].max().strftime('%Y-%m')}",
            "reaction_date_span": f"{reactions['date'].min().strftime('%Y-%m')} to {reactions['date'].max().strftime('%Y-%m')}",
        }

    @staticmethod
    def filter_posts(
        platforms: Optional[List[str]] = None,
        date_range: Optional[tuple] = None,
        min_likes: int = 0,
        search_query: str = "",
        limit: int = 50,
    ) -> pd.DataFrame:
        """Filters Round 1 cleaned posts with user-specified criteria."""
        df = DatasetRepository.load_round1_posts().copy()

        if platforms:
            df = df[df["platform"].isin(platforms)]
        
        if date_range and len(date_range) == 2:
            start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
            df = df[(df["timestamp"] >= start_date) & (df["timestamp"] <= end_date)]
        
        if min_likes > 0:
            df = df[df["likes"] >= min_likes]
        
        if search_query.strip():
            q = search_query.strip().lower()
            df = df[df["text_content"].str.lower().str.contains(q, na=False)]
        
        return df.head(limit)

    @staticmethod
    def get_platform_distribution() -> pd.DataFrame:
        """Computes post volume and aggregate engagement by platform."""
        df = DatasetRepository.load_round1_posts()
        grouped = df.groupby("platform").agg(
            total_posts=("post_id", "count"),
            avg_likes=("likes", "mean"),
            avg_shares=("shares", "mean"),
            avg_comments=("comments", "mean"),
        ).reset_index()
        grouped["avg_likes"] = grouped["avg_likes"].round(1)
        grouped["avg_shares"] = grouped["avg_shares"].round(1)
        grouped["avg_comments"] = grouped["avg_comments"].round(1)
        return grouped.sort_values(by="total_posts", ascending=False)
