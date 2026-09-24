"""
PAGE 1 — OVERVIEW
DATA VORTEX 2026 — Round 4: Social Engine Revival

Presents dataset scale, summary statistics, platform post volume distribution,
four executive synthesis pillars, and data recovery audit logs in clean light styling.
"""

from pathlib import Path
import sys
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

ROUND4_DIR = Path(__file__).resolve().parent.parent
if str(ROUND4_DIR) not in sys.path:
    sys.path.insert(0, str(ROUND4_DIR))

from src.utils import APP_TITLE, format_number
from src.metrics import get_system_scale_metrics, get_synthesis_pillars
from src.analysis import get_platform_engagement_summary
from components.findings import render_limitation_callout
from components.sidebar import render_sidebar
from components.header import render_header
from components.theme import apply_custom_theme
from components.charts import create_platform_distribution_chart

st.set_page_config(
    page_title=f"Overview | {APP_TITLE}",
    page_icon="📊",
    layout="wide",
)

# Apply global clean light corporate theme
apply_custom_theme()


def render():
    render_sidebar()
    render_header(
        page_title="Dataset Overview & Executive Summary",
        page_description="High-level synthesis of the recovered social ecosystem, platform-level engagement distributions, and the four analytical pillars established across Rounds 1 through 3.",
        breadcrumb="01 Overview",
    )

    # 1. Scale & Summary Statistics
    metrics = get_system_scale_metrics()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(
            label="Cleaned Posts Corpus",
            value=format_number(metrics["total_cleaned_posts"]),
            delta="100% Recovered",
            help="12,000 posts across 4 platforms (Round 1 Phase 1)",
        )
    with c2:
        st.metric(
            label="Registered Creators",
            value=format_number(metrics["total_registered_users"]),
            delta="1,500 Creators",
            help="Relational user registry in SQLite core (Round 1 Phase 2)",
        )
    with c3:
        st.metric(
            label="Average Engagement / Post",
            value=str(metrics["avg_engagement_per_post"]),
            help=f"Total Likes: {format_number(metrics['total_likes'])}",
        )
    with c4:
        st.metric(
            label="Algorithmic Reactions",
            value=format_number(metrics["total_reaction_records"]),
            delta="15-Year Archive",
            help="Hacker News discussion archive (Round 3)",
        )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # 2. Main Visualizations & Platform Breakdown
    col_plat, col_forensic = st.columns([5, 5])

    with col_plat:
        plat_df = get_platform_engagement_summary()
        fig_plat = create_platform_distribution_chart(plat_df)
        st.plotly_chart(fig_plat, use_container_width=True)

    with col_forensic:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 18px 20px; height: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                <h4 style="font-size: 1.05rem; font-weight: 700; color: #0F172A; margin: 0 0 0.5rem 0;">
                    Forensic Restoration & Integrity Audit
                </h4>
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.5; margin-bottom: 0.8rem;">
                    Key data quality anomalies remediated systematically without altering analytical ground truth:
                </p>
                <div style="font-size: 0.82rem; color: #334155; line-height: 1.55;">
                    <div style="margin-bottom: 6px;">• <strong>Timestamp Repair:</strong> Standardized epoch, ISO 8601, and shifted year strings to canonical UTC datetime.</div>
                    <div style="margin-bottom: 6px;">• <strong>Text Escaping:</strong> Repaired unescaped quotes and embedded delimiters that corrupted CSV column bounds.</div>
                    <div style="margin-bottom: 6px;">• <strong>Zero Fabrication:</strong> No missing values or synthetic records were generated. 100% genuine data recovery.</div>
                    <div>• <strong>Referential Linkage:</strong> All 12,000 posts link to verified creator IDs in the SQLite core (0 foreign-key violations).</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # 3. Four Executive Synthesis Pillars
    st.markdown("<h3 style='font-size: 1.15rem; font-weight: 700; color: #0F172A; margin: 0 0 0.6rem 0;'>Executive Synthesis Pillars</h3>", unsafe_allow_html=True)
    pillars = get_synthesis_pillars()

    p_col1, p_col2 = st.columns(2)
    for i, p in enumerate(pillars):
        target_col = p_col1 if i % 2 == 0 else p_col2
        with target_col:
            st.markdown(
                f"""
                <div style="background: #FFFFFF; border-left: 4px solid {p['color']}; border-top: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0; border-radius: 6px; padding: 14px 16px; margin-bottom: 0.8rem; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                        <span style="font-size: 0.92rem; font-weight: 700; color: #0F172A;">{p['title']}</span>
                        <span style="font-size: 0.72rem; font-weight: 600; background: #F1F5F9; color: {p['color']}; padding: 2px 6px; border-radius: 4px;">
                            {p['tag']}
                        </span>
                    </div>
                    <p style="font-size: 0.83rem; color: #475569; margin: 0 0 6px 0; line-height: 1.45;">
                        {p['summary']}
                    </p>
                    <div style="font-size: 0.78rem; font-weight: 600; color: #1E3A8A;">
                        Key Metric: <span style="color: #0F172A;">{p['metric_label']} = {p['metric_value']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # 4. Limitations Callout
    render_limitation_callout()


if __name__ == "__main__":
    render()
