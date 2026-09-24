"""
SQLite Repository for Round 1 Phase 2 Database Access.

Provides strictly read-only access to 'data_vortex.db' with parameterized queries,
schema inspection, and canonical competition SQL challenges (E2, M1, H2).
"""

import sqlite3
from typing import Dict, Any, List
import pandas as pd
import streamlit as st

from pathlib import Path
import sys

_ROUND4_DIR = str(Path(__file__).resolve().parents[1])
if _ROUND4_DIR not in sys.path:
    sys.path.insert(0, _ROUND4_DIR)

from config.settings import ROUND1_DB_PATH
from utils.logging_config import logger

class SQLiteRepository:
    """Manages read-only interaction with the canonical SQLite database."""

    def __init__(self, db_path=None):
        self.db_path = db_path or ROUND1_DB_PATH

    def get_connection(self) -> sqlite3.Connection:
        """Establishes an immutable read-only connection."""
        if not self.db_path.exists():
            raise FileNotFoundError(f"Canonical database not found at: {self.db_path}")
        uri = f"file:{self.db_path.resolve()}?mode=ro"
        conn = sqlite3.connect(uri, uri=True, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def get_database_info(self) -> Dict[str, Any]:
        """Inspects table names, row counts, and integrity status."""
        with self.get_connection() as conn:
            integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
            foreign_keys = conn.execute("PRAGMA foreign_key_check").fetchall()
            
            tables = [
                row[0] for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                ).fetchall()
            ]
            
            table_counts = {}
            for t in tables:
                cnt = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                table_counts[t] = cnt

        return {
            "integrity": integrity,
            "foreign_key_violations": len(foreign_keys),
            "tables": tables,
            "row_counts": table_counts,
        }

    def execute_query(self, sql: str, params: tuple = ()) -> pd.DataFrame:
        """Executes an arbitrary read-only SQL SELECT query."""
        cleaned_sql = sql.strip().upper()
        if not cleaned_sql.startswith("SELECT") and not cleaned_sql.startswith("WITH") and not cleaned_sql.startswith("EXPLAIN"):
            raise ValueError("Only read-only SELECT or WITH statements are permitted.")
        
        conn = self.get_connection()
        try:
            return pd.read_sql_query(sql, conn, params=params)
        finally:
            conn.close()

    # -------------------------------------------------------------------------
    # Canonical SQL Challenges (E2, M1, H2)
    # -------------------------------------------------------------------------
    @staticmethod
    def get_challenge_e2_sql() -> str:
        """Challenge E2: Top 10 Most Engaged Posts (likes + shares + comments)."""
        return """SELECT
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
LIMIT 10;"""

    @staticmethod
    def get_challenge_m1_sql() -> str:
        """Challenge M1: Which Locations Generate the Most Engagement?"""
        return """SELECT
    u.location,
    COUNT(p.post_id) AS post_count,
    SUM(p.likes + p.shares + p.comments) AS total_engagement
FROM users AS u
JOIN posts AS p
    ON p.user_id = u.user_id
WHERE p.likes IS NOT NULL
GROUP BY u.location
ORDER BY total_engagement DESC, u.location ASC;"""

    @staticmethod
    def get_challenge_h2_sql() -> str:
        """Challenge H2: Rank Users Within Their Location (Top 3 per location)."""
        return """WITH user_engagement AS (
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
ORDER BY location ASC, engagement_rank ASC, user_id ASC;"""

@st.cache_resource
def get_sqlite_repo() -> SQLiteRepository:
    """Returns a cached SQLiteRepository instance."""
    return SQLiteRepository()

@st.cache_data
def run_cached_query(sql: str) -> pd.DataFrame:
    """Runs and caches a SQL query."""
    repo = get_sqlite_repo()
    return repo.execute_query(sql)
