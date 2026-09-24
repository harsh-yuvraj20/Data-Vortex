"""
Metrics and evaluation module for DATA VORTEX 2026 — Round 4.

Calculates executive KPIs, cross-round scale metrics, held-out model benchmarks,
and the synthesis evidence matrix.
"""

from typing import Dict, Any, List
import pandas as pd

try:
    from src.data_loader import (
        load_round1_posts,
        load_round1_users,
        load_round2_training,
        load_round3_reactions,
    )
except ImportError:
    from data_loader import (
        load_round1_posts,
        load_round1_users,
        load_round2_training,
        load_round3_reactions,
    )

# -----------------------------------------------------------------------------
# Frozen Canonical Benchmarks (Round 2 Held-Out Test Set)
# -----------------------------------------------------------------------------
FROZEN_SENTIMENT_BENCHMARKS = {
    "accuracy": 0.5786,
    "macro_f1": 0.5795,
    "weighted_f1": 0.5800,
    "model_type": "TF-IDF + Logistic Regression (C=1.0)",
    "calibration": "Calibrated Posterior Probabilities (predict_proba)",
}

FROZEN_TOPIC_BENCHMARKS = {
    "accuracy": 0.9264,
    "macro_f1": 0.5805,
    "weighted_f1": 0.9110,
    "model_type": "TF-IDF + Linear SVM (LinearSVC)",
    "calibration": "Signed Decision Margin Distance (decision_function) with Labeled Softmax Approximation",
}

# -----------------------------------------------------------------------------
# System Scale & Cross-Round Metrics
# -----------------------------------------------------------------------------
def get_system_scale_metrics() -> Dict[str, Any]:
    """Calculates verified system scale counts across all rounds."""
    posts = load_round1_posts()
    users = load_round1_users()
    train = load_round2_training()
    reactions = load_round3_reactions()

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

def get_cross_round_evidence_matrix() -> pd.DataFrame:
    """Returns the authoritative cross-round verification matrix."""
    return pd.DataFrame([
        {
            "Round": "Round 1 Phase 1",
            "Domain": "Forensic EDA",
            "Authoritative Artifact": "Social_Engine_Posts_Cleaned.csv",
            "Verified Metric": "12,000 posts / 1,500 users",
            "Validation Status": "PASS",
        },
        {
            "Round": "Round 1 Phase 2",
            "Domain": "SQLite Database",
            "Authoritative Artifact": "data_vortex.db",
            "Verified Metric": "13,500 records (Integrity: OK)",
            "Validation Status": "PASS",
        },
        {
            "Round": "Round 2",
            "Domain": "Sentiment Model",
            "Authoritative Artifact": "sentiment_label_pipeline.pkl",
            "Verified Metric": "Accuracy: 0.5786 | Macro F1: 0.5795",
            "Validation Status": "PASS",
        },
        {
            "Round": "Round 2",
            "Domain": "Topic Model",
            "Authoritative Artifact": "topic_category_pipeline.pkl",
            "Verified Metric": "Accuracy: 0.9264 | Weighted F1: 0.9110",
            "Validation Status": "PASS",
        },
        {
            "Round": "Round 3",
            "Domain": "Temporal Mining",
            "Authoritative Artifact": "round3_recommendation_algorithm_reactions.csv",
            "Verified Metric": "204 items (Window: 2011–2026)",
            "Validation Status": "PASS",
        },
        {
            "Round": "Round 4",
            "Domain": "Unified App",
            "Authoritative Artifact": "app.py",
            "Verified Metric": "Streamlit 5-page modular architecture",
            "Validation Status": "PASS",
        },
    ])

def get_synthesis_pillars() -> List[Dict[str, Any]]:
    """Returns the four core executive narrative synthesis pillars."""
    return [
        {
            "title": "Pillar 1: Forensic Recovery & Zero Fabrication",
            "tag": "Round 1 Foundation",
            "color": "#1E3A8A",
            "summary": (
                "Reconstructed 100% of 12,000 corrupted posts across 1,500 registered users. "
                "Restored relational integrity in SQLite with 0 foreign key violations without "
                "synthetically generating data points."
            ),
            "metric_label": "Recovery Rate",
            "metric_value": "100.0%",
        },
        {
            "title": "Pillar 2: Calibrated Semantic Understanding",
            "tag": "Round 2 NLP",
            "color": "#0D9488",
            "summary": (
                "Deployed dual-head NLP pipelines separating subjective sentiment from functional topic. "
                "Maintains strict calibration honesty by reporting true probabilities for Logistic Regression "
                "and margin distances for Linear SVM."
            ),
            "metric_label": "Topic Weighted F1",
            "metric_value": "0.9110",
        },
        {
            "title": "Pillar 3: Temporal Trajectory & Candidate Shifts",
            "tag": "Round 3 Dynamics",
            "color": "#D97706",
            "summary": (
                "Mined 204 longitudinal reaction records from 2011 to 2026. Identified candidate shifts "
                "SS1 (Sep-Oct 2025, Δ = -0.80) and SS2 (Oct-Nov 2024, Δ = +0.80), tracking algorithmic changes "
                "without unwarranted causal assertions."
            ),
            "metric_label": "Peak Spike Ratio",
            "metric_value": "284.0×",
        },
        {
            "title": "Pillar 4: Systemic Cohesion & Offline Portability",
            "tag": "Round 4 Synthesis",
            "color": "#2563EB",
            "summary": (
                "Unified the social engine into a local-first Streamlit application. Employs a layered "
                "service pattern with zero data duplication, zero cloud dependencies, and dynamic root path resolution."
            ),
            "metric_label": "Total Artifacts",
            "metric_value": "22,704 Rows",
        },
    ]
