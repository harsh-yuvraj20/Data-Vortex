"""
Configuration and settings for DATA VORTEX 2026 — Round 4: Social Engine Revival.

Provides deterministic, machine-independent path resolution, canonical artifact
pointers, UI style constants, and application metadata.
"""

from pathlib import Path
import os

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
    # Fallback to parent of Round-4 if installed inside workspace
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
# Application Metadata
# -----------------------------------------------------------------------------
APP_TITLE = "Social Engine Revival"
APP_SUBTITLE = "DATA VORTEX 2026 — Round 4 Integrated Intelligence Dashboard"
APP_VERSION = "4.0.0"
APP_DESCRIPTION = (
    "Executive-grade multi-round synthesis uniting forensic data recovery (Round 1), "
    "dual-head NLP semantic intelligence (Round 2), and temporal shift mining (Round 3)."
)

# -----------------------------------------------------------------------------
# Color Palette & Visual System
# -----------------------------------------------------------------------------
COLOR_PRIMARY = "#1E3A8A"      # Deep Navy
COLOR_SECONDARY = "#0D9488"    # Restrained Teal
COLOR_ACCENT = "#2563EB"       # Royal Blue
COLOR_SLATE_DARK = "#0F172A"   # Slate 900
COLOR_SLATE_CARD = "#1E293B"   # Slate 800
COLOR_SLATE_LIGHT = "#F8FAFC"  # Slate 50
COLOR_TEXT_PRIMARY = "#0F172A" # Dark Charcoal for light surfaces
COLOR_TEXT_MUTED = "#64748B"   # Slate 500
COLOR_SUCCESS = "#059669"      # Emerald 600
COLOR_WARNING = "#D97706"      # Amber 600
COLOR_DANGER = "#DC2626"       # Crimson 600

# Sentiment Colors
SENTIMENT_COLORS = {
    "Positive": "#059669",
    "Neutral": "#64748B",
    "Negative": "#DC2626",
}

# Topic Category Colors
TOPIC_COLORS = {
    "Feature_Feedback": "#2563EB",
    "Technical_Issues": "#D97706",
    "Community_Discussion": "#0D9488",
    "Account_Security": "#DC2626",
}

# Plotly Research Theme Layout
PLOTLY_TEMPLATE = {
    "layout": {
        "font": {"family": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif", "size": 12, "color": "#1E293B"},
        "title": {"font": {"family": "Outfit, Inter, sans-serif", "size": 15, "color": "#0F172A"}, "x": 0.02, "xanchor": "left"},
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(248,250,252,0.6)",
        "margin": {"l": 50, "r": 30, "t": 45, "b": 45},
        "xaxis": {"gridcolor": "#E2E8F0", "linecolor": "#CBD5E1", "zerolinecolor": "#CBD5E1"},
        "yaxis": {"gridcolor": "#E2E8F0", "linecolor": "#CBD5E1", "zerolinecolor": "#CBD5E1"},
    }
}

# -----------------------------------------------------------------------------
# Authoritative Benchmark Constants (Held-Out Test Set from Round 2)
# -----------------------------------------------------------------------------
FROZEN_SENTIMENT_METRICS = {
    "accuracy": 0.5786,
    "macro_f1": 0.5795,
    "weighted_f1": 0.5800,
    "model_type": "TF-IDF + Logistic Regression",
    "calibration": "Calibrated Posterior Probabilities (predict_proba)",
}

FROZEN_TOPIC_METRICS = {
    "accuracy": 0.9264,
    "macro_f1": 0.5805,
    "weighted_f1": 0.9110,
    "model_type": "TF-IDF + Linear SVM (LinearSVC)",
    "calibration": "Hyperplane Margin Distance (decision_function) with Softmax Approximation",
}
