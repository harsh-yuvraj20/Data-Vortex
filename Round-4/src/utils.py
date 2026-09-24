"""
Utility functions and configuration for DATA VORTEX 2026 — Round 4.

Provides dynamic, machine-independent path resolution, UI design tokens,
formatting utilities, and structured logging.
"""

from pathlib import Path
from typing import Union, Optional
import os
import logging
import sys
import pandas as pd

# -----------------------------------------------------------------------------
# Dynamic Repository Root Detection
# -----------------------------------------------------------------------------
def get_repo_root() -> Path:
    """
    Locates the repository root dynamically by inspecting parent directories
    for the canonical Round-1, Round-2, and Round-3 folders.
    """
    current = Path(__file__).resolve().parent
    for candidate in [current, current.parent, current.parent.parent]:
        if (candidate / "Round-1").exists() and (candidate / "Round-2").exists():
            return candidate
    return Path(__file__).resolve().parent.parent.parent

REPO_ROOT = get_repo_root()
ROUND4_ROOT = REPO_ROOT / "Round-4"

# -----------------------------------------------------------------------------
# Canonical Previous-Round Artifact Paths (Zero-Duplication Architecture)
# -----------------------------------------------------------------------------
ROUND1_POSTS_CSV = REPO_ROOT / "Round-1" / "Phase-1" / "data" / "cleaned" / "Social_Engine_Posts_Cleaned.csv"
ROUND1_USERS_CSV = REPO_ROOT / "Round-1" / "Phase-1" / "data" / "cleaned" / "Social_Engine_Users_Cleaned.csv"
ROUND1_RAW_POSTS_CSV = REPO_ROOT / "Round-1" / "Phase-1" / "data" / "raw" / "Social_Engine_Posts_Corrupted.csv"
ROUND1_DB_PATH = REPO_ROOT / "Round-1" / "Phase-2" / "data" / "data_vortex.db"

ROUND2_TRAIN_CSV = REPO_ROOT / "Round-2" / "data" / "Labeled_Social_NLP_Training_Data.csv"
ROUND2_SENTIMENT_MODEL = REPO_ROOT / "Round-2" / "models" / "sentiment_label_pipeline.pkl"
ROUND2_TOPIC_MODEL = REPO_ROOT / "Round-2" / "models" / "topic_category_pipeline.pkl"

ROUND3_REACTIONS_CSV = REPO_ROOT / "Round-3" / "data" / "processed" / "round3_recommendation_algorithm_reactions.csv"

# -----------------------------------------------------------------------------
# Application Metadata & Visual System
# -----------------------------------------------------------------------------
APP_TITLE = "Social Engine Revival"
APP_SUBTITLE = "DATA VORTEX 2026 — Round 4 Integrated Intelligence Dashboard"
APP_VERSION = "4.0.0"

# Color Palette
COLOR_PRIMARY = "#1E3A8A"      # Deep Navy
COLOR_SECONDARY = "#0D9488"    # Restrained Teal
COLOR_ACCENT = "#2563EB"       # Royal Blue
COLOR_SLATE_DARK = "#0F172A"   # Slate 900
COLOR_SLATE_LIGHT = "#F8FAFC"  # Slate 50
COLOR_SUCCESS = "#059669"      # Emerald 600
COLOR_WARNING = "#D97706"      # Amber 600
COLOR_DANGER = "#DC2626"       # Crimson 600

SENTIMENT_COLORS = {
    "Positive": "#059669",
    "Neutral": "#64748B",
    "Negative": "#DC2626",
}

TOPIC_COLORS = {
    "Feature_Feedback": "#2563EB",
    "Technical_Issues": "#D97706",
    "Community_Discussion": "#0D9488",
    "Account_Security": "#DC2626",
}

PLOTLY_TEMPLATE = {
    "layout": {
        "font": {"family": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif", "size": 12, "color": "#1E293B"},
        "title": {"font": {"family": "Outfit, Inter, sans-serif", "size": 15, "color": "#0F172A"}, "x": 0.02, "xanchor": "left"},
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(248,250,252,0.6)",
        "margin": {"l": 50, "r": 30, "t": 45, "b": 45},
        "xaxis": {"gridcolor": "#E2E8F0", "linecolor": "#CBD5E1"},
        "yaxis": {"gridcolor": "#E2E8F0", "linecolor": "#CBD5E1"},
    }
}

# -----------------------------------------------------------------------------
# Formatting Helpers
# -----------------------------------------------------------------------------
def format_number(val: Union[int, float, None], precision: int = 0) -> str:
    """Formats an integer or float with comma separators."""
    if val is None or pd.isna(val):
        return "N/A"
    if precision == 0:
        return f"{int(round(val)):,}"
    return f"{val:,.{precision}f}"

def format_percent(val: Union[int, float, None], precision: int = 1) -> str:
    """Formats a decimal float as a percentage string."""
    if val is None or pd.isna(val):
        return "N/A"
    return f"{val * 100:.{precision}f}%"

def format_delta(val: Union[int, float, None], precision: int = 4) -> str:
    """Formats a delta with explicit + or - sign."""
    if val is None or pd.isna(val):
        return "N/A"
    sign = "+" if val > 0 else ""
    return f"{sign}{val:.{precision}f}"

def format_date(val: Union[str, pd.Timestamp], fmt: str = "%b %d, %Y") -> str:
    """Formats a date or timestamp string."""
    if val is None or pd.isna(val):
        return "N/A"
    try:
        ts = pd.to_datetime(val)
        return ts.strftime(fmt)
    except Exception:
        return str(val)

# -----------------------------------------------------------------------------
# Structured Logger
# -----------------------------------------------------------------------------
def get_logger(name: str = "round4") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"))
        logger.addHandler(handler)
    return logger

logger = get_logger()
