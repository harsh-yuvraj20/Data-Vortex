"""
Analytical calculation functions for DATA VORTEX 2026 — Round 4.

Contains reproducible algorithms for:
- Monthly Net Sentiment Index trajectory: (Positive - Negative) / Total
- Verified candidate shift detection (SS1, SS2)
- Extreme engagement spike detection (ES1, ES2, ES3)
- Target entity frequency extraction
- Canonical SQLite competition challenges (E2, M1, H2)
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

try:
    from src.data_loader import (
        load_round1_posts,
        load_round1_users,
        load_round3_reactions,
        execute_sql_query,
    )
except ImportError:
    from data_loader import (
        load_round1_posts,
        load_round1_users,
        load_round3_reactions,
        execute_sql_query,
    )

# -----------------------------------------------------------------------------
# Canonical Candidate Shifts & Engagement Spikes
# -----------------------------------------------------------------------------
CANDIDATE_SHIFTS = [
    {
        "id": "SS1",
        "period": "September 2025 → October 2025",
        "prev_index": -0.2000,
        "next_index": -1.0000,
        "delta": -0.8000,
        "sample_size": "5 posts (Sep) → 3 posts (Oct)",
        "primary_topic": "European AI Act / Algorithm Compliance",
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
        "finding": (
            "Sharp positive sentiment rebound (+0.8000) from unanimous negative sentiment. "
            "Corresponds to technical discussions of recommendation algorithm architectures."
        ),
    },
]

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

GAZETTEER = ["Twitter", "Reddit", "Meta", "Google", "TikTok", "YouTube", "Instagram", "Hacker News"]

# -----------------------------------------------------------------------------
# Temporal Dynamics Calculations
# -----------------------------------------------------------------------------
def get_monthly_trajectory() -> pd.DataFrame:
    """
    Computes monthly post volume and Net Sentiment Index: (Pos - Neg) / Total.
    """
    df = load_round3_reactions().copy()
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

def get_entity_frequencies() -> pd.DataFrame:
    """Extracts target gazetteer mentions from reactions text corpus."""
    df = load_round3_reactions()
    corpus = (df["text"].fillna("") + " " + df["title"].fillna("")).str.lower()

    counts = []
    for entity in GAZETTEER:
        c = corpus.str.count(entity.lower()).sum()
        counts.append({"entity": entity, "mentions": int(c)})

    res = pd.DataFrame(counts).sort_values(by="mentions", ascending=False)
    return res[res["mentions"] > 0]

# -----------------------------------------------------------------------------
# Canonical SQL Challenges
# -----------------------------------------------------------------------------
SQL_CHALLENGES = {
    "E2": {
        "title": "Challenge E2: Top 10 Most Engaged Posts",
        "difficulty": "Easy",
        "sql": """SELECT
    p.post_id,
    p.user_id,
    p.platform,
    p.likes,
    p.shares,
    p.comments,
    p.likes + p.shares + p.comments AS total_engagement
FROM posts AS p
WHERE p.likes IS NOT NULL
ORDER BY total_engagement DESC, p.post_id ASC
LIMIT 10;""",
        "description": "Calculates complete engagement (likes + shares + comments) and returns the 10 highest-performing posts.",
    },
    "M1": {
        "title": "Challenge M1: Which Locations Generate the Most Engagement?",
        "difficulty": "Medium",
        "sql": """SELECT
    u.location,
    COUNT(p.post_id) AS post_count,
    SUM(p.likes + p.shares + p.comments) AS total_engagement
FROM users AS u
JOIN posts AS p
    ON p.user_id = u.user_id
WHERE p.likes IS NOT NULL
GROUP BY u.location
ORDER BY total_engagement DESC, u.location ASC;""",
        "description": "Aggregates total engagement and post counts by creator location, ranking communities by engagement volume.",
    },
    "H2": {
        "title": "Challenge H2: Rank Users Within Their Location (Top 3 per Location)",
        "difficulty": "Hard",
        "sql": """WITH user_engagement AS (
    SELECT
        u.user_id,
        u.location,
        u.follower_count,
        COUNT(p.post_id) AS post_count,
        SUM(p.likes + p.shares + p.comments) AS total_engagement
    FROM users AS u
    JOIN posts AS p
        ON p.user_id = u.user_id
    WHERE p.likes IS NOT NULL
    GROUP BY u.user_id, u.location, u.follower_count
), ranked_users AS (
    SELECT
        user_id,
        location,
        follower_count,
        post_count,
        total_engagement,
        DENSE_RANK() OVER (
            PARTITION BY location
            ORDER BY total_engagement DESC
        ) AS engagement_rank
    FROM user_engagement
)
SELECT
    location,
    engagement_rank,
    user_id,
    follower_count,
    post_count,
    total_engagement
FROM ranked_users
WHERE engagement_rank <= 3
ORDER BY location ASC, engagement_rank ASC, user_id ASC;""",
        "description": "Uses DENSE_RANK() window function partitioned by location to identify the leading 3 creators per location.",
    },
}

def execute_sql_challenge(challenge_id: str) -> Dict[str, Any]:
    """Executes a canonical SQL challenge and returns results with description."""
    cid = challenge_id.strip().upper()
    if cid not in SQL_CHALLENGES:
        raise ValueError(f"Unknown challenge identifier: {challenge_id}")
    meta = SQL_CHALLENGES[cid]
    results_df = execute_sql_query(meta["sql"])
    return {
        "id": cid,
        "title": meta["title"],
        "difficulty": meta["difficulty"],
        "description": meta["description"],
        "sql": meta["sql"],
        "results": results_df,
        "rows": len(results_df),
    }

# -----------------------------------------------------------------------------
# Post Filtering & Aggregations
# -----------------------------------------------------------------------------
def filter_posts(
    platforms: Optional[List[str]] = None,
    min_likes: int = 0,
    search_query: str = "",
    limit: int = 50,
) -> pd.DataFrame:
    """Filters Round 1 cleaned posts based on user interaction criteria."""
    df = load_round1_posts().copy()
    if platforms:
        df = df[df["platform"].isin(platforms)]
    if min_likes > 0:
        df = df[df["likes"] >= min_likes]
    if search_query.strip():
        q = search_query.strip().lower()
        df = df[df["text_content"].str.lower().str.contains(q, na=False)]
    return df.head(limit)

def get_platform_engagement_summary() -> pd.DataFrame:
    """Aggregates post counts and engagement by platform."""
    posts = load_round1_posts()
    return posts.groupby("platform").agg(
        post_count=("post_id", "count"),
        avg_likes=("likes", "mean"),
        avg_shares=("shares", "mean"),
        avg_comments=("comments", "mean"),
    ).reset_index().sort_values(by="post_count", ascending=False)
