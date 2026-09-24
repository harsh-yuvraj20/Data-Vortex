"""
Data loader module for DATA VORTEX 2026 — Round 4.

Loads canonical datasets across Rounds 1, 2, and 3 via relative paths with
Streamlit caching and provides immutable read-only SQLite connectivity.
"""

from typing import Dict, Any, Optional
import sqlite3
import pandas as pd
import streamlit as st

try:
    from src.utils import (
        ROUND1_POSTS_CSV,
        ROUND1_USERS_CSV,
        ROUND1_RAW_POSTS_CSV,
        ROUND1_DB_PATH,
        ROUND2_TRAIN_CSV,
        ROUND3_REACTIONS_CSV,
        logger,
    )
    from src.preprocessing import validate_dataframe
except ImportError:
    from utils import (
        ROUND1_POSTS_CSV,
        ROUND1_USERS_CSV,
        ROUND1_RAW_POSTS_CSV,
        ROUND1_DB_PATH,
        ROUND2_TRAIN_CSV,
        ROUND3_REACTIONS_CSV,
        logger,
    )
    from preprocessing import validate_dataframe

# -----------------------------------------------------------------------------
# Tabular Dataset Loaders
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_round1_posts() -> pd.DataFrame:
    """Loads canonical cleaned posts dataset (12,000 records)."""
    if not ROUND1_POSTS_CSV.exists():
        raise FileNotFoundError(f"Cleaned posts not found at: {ROUND1_POSTS_CSV}")
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

@st.cache_data(show_spinner=False)
def load_round1_users() -> pd.DataFrame:
    """Loads canonical cleaned users dataset (1,500 records)."""
    if not ROUND1_USERS_CSV.exists():
        raise FileNotFoundError(f"Cleaned users not found at: {ROUND1_USERS_CSV}")
    df = pd.read_csv(ROUND1_USERS_CSV)
    validate_dataframe(
        df,
        required_columns=["user_id", "location", "language", "account_created", "follower_count"],
        min_rows=1500,
        name="Round-1 Cleaned Users",
    )
    df["account_created"] = pd.to_datetime(df["account_created"])
    return df

@st.cache_data(show_spinner=False)
def load_round1_corrupted() -> pd.DataFrame:
    """Loads raw corrupted posts (for forensic comparison)."""
    if not ROUND1_RAW_POSTS_CSV.exists():
        raise FileNotFoundError(f"Raw corrupted posts not found at: {ROUND1_RAW_POSTS_CSV}")
    return pd.read_csv(ROUND1_RAW_POSTS_CSV)

@st.cache_data(show_spinner=False)
def load_round2_training() -> pd.DataFrame:
    """Loads canonical NLP training dataset (9,000 records, balanced 1:1:1)."""
    if not ROUND2_TRAIN_CSV.exists():
        raise FileNotFoundError(f"NLP training dataset not found at: {ROUND2_TRAIN_CSV}")
    df = pd.read_csv(ROUND2_TRAIN_CSV)
    validate_dataframe(
        df,
        required_columns=["post_text", "sentiment_label", "topic_category"],
        min_rows=9000,
        name="Round-2 NLP Training Data",
    )
    return df

@st.cache_data(show_spinner=False)
def load_round3_reactions() -> pd.DataFrame:
    """Loads canonical reaction archive dataset (204 records)."""
    if not ROUND3_REACTIONS_CSV.exists():
        raise FileNotFoundError(f"Reaction dataset not found at: {ROUND3_REACTIONS_CSV}")
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

# -----------------------------------------------------------------------------
# SQLite Read-Only Database Interface
# -----------------------------------------------------------------------------
def get_sqlite_connection() -> sqlite3.Connection:
    """Opens an immutable read-only connection to data_vortex.db."""
    if not ROUND1_DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at: {ROUND1_DB_PATH}")
    uri = f"file:{ROUND1_DB_PATH.resolve()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def execute_sql_query(sql: str, params: tuple = ()) -> pd.DataFrame:
    """Executes a read-only SQL query and returns a pandas DataFrame."""
    cleaned_sql = sql.strip().upper()
    if not cleaned_sql.startswith("SELECT") and not cleaned_sql.startswith("WITH") and not cleaned_sql.startswith("EXPLAIN"):
        raise ValueError("Security Violation: Only read-only SELECT or WITH statements are permitted.")
    
    conn = get_sqlite_connection()
    try:
        return pd.read_sql_query(sql, conn, params=params)
    finally:
        conn.close()

def get_sqlite_info() -> Dict[str, Any]:
    """Inspects table names, row counts, and database integrity."""
    conn = get_sqlite_connection()
    try:
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        foreign_keys = conn.execute("PRAGMA foreign_key_check").fetchall()
        tables = [
            row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            ).fetchall()
        ]
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tables}
        return {
            "integrity": integrity,
            "foreign_key_violations": len(foreign_keys),
            "tables": tables,
            "row_counts": counts,
        }
    finally:
        conn.close()
