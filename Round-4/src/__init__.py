"""
DATA VORTEX 2026 — Round 4: Source Package.
"""

from src.utils import (
    REPO_ROOT,
    ROUND4_ROOT,
    APP_TITLE,
    APP_SUBTITLE,
    APP_VERSION,
    format_number,
    format_percent,
    format_delta,
    format_date,
    logger,
)
from src.data_loader import (
    load_round1_posts,
    load_round1_users,
    load_round1_corrupted,
    load_round2_training,
    load_round3_reactions,
    execute_sql_query,
    get_sqlite_info,
)
from src.preprocessing import validate_dataframe, clean_social_text
from src.model import (
    load_sentiment_pipeline,
    load_topic_pipeline,
    predict_sentiment,
    predict_topic,
    predict_dual_head,
    PRESET_EXAMPLES,
)
from src.analysis import (
    get_monthly_trajectory,
    get_entity_frequencies,
    execute_sql_challenge,
    filter_posts,
    get_platform_engagement_summary,
    CANDIDATE_SHIFTS,
    ENGAGEMENT_SPIKES,
)
from src.metrics import (
    get_system_scale_metrics,
    get_cross_round_evidence_matrix,
    get_synthesis_pillars,
    FROZEN_SENTIMENT_BENCHMARKS,
    FROZEN_TOPIC_BENCHMARKS,
)
