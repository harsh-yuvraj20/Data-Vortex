"""
PAGE 2 — ANALYSIS
DATA VORTEX 2026 — Round 4: Social Engine Revival

Presents authoritative analytical results across all rounds:
1. Canonical SQL challenges (E2, M1, H2) against 'data_vortex.db'
2. NLP semantic training distributions and held-out test benchmarks
3. Longitudinal Net Sentiment Index trajectory, candidate shifts (SS1, SS2), and spikes (ES1–ES3)
in clean light styling.
"""

from pathlib import Path
import sys
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

ROUND4_DIR = Path(__file__).resolve().parent.parent
if str(ROUND4_DIR) not in sys.path:
    sys.path.insert(0, str(ROUND4_DIR))

from src.utils import APP_TITLE, format_percent, SENTIMENT_COLORS, TOPIC_COLORS
from src.data_loader import load_round2_training
from src.analysis import (
    execute_sql_challenge,
    get_monthly_trajectory,
    get_entity_frequencies,
    CANDIDATE_SHIFTS,
    ENGAGEMENT_SPIKES,
)
from src.metrics import FROZEN_SENTIMENT_BENCHMARKS, FROZEN_TOPIC_BENCHMARKS
from components.findings import render_limitation_callout
from components.sidebar import render_sidebar
from components.header import render_header
from components.theme import apply_custom_theme
from components.charts import create_distribution_pie_or_bar, create_entity_frequency_chart

st.set_page_config(
    page_title=f"Analysis | {APP_TITLE}",
    page_icon="🔬",
    layout="wide",
)

# Apply global clean light corporate theme
apply_custom_theme()


def render():
    render_sidebar()
    render_header(
        page_title="Core Multi-Round Analytical Results",
        page_description="Audited empirical findings derived directly from canonical repository artifacts: production SQL challenges, NLP test set evaluations, and longitudinal reaction dynamics.",
        breadcrumb="02 Analysis",
    )

    tab_sql, tab_nlp, tab_signals = st.tabs([
        "1. Relational SQL Core (Round 1)",
        "2. Semantic NLP Intelligence (Round 2)",
        "3. Temporal Signals & Shifts (Round 3)",
    ])

    # -------------------------------------------------------------------------
    # TAB 1: RELATIONAL SQL CHALLENGES
    # -------------------------------------------------------------------------
    with tab_sql:
        st.markdown(
            """
            <div style="margin: 0.5rem 0 1rem 0;">
                <h3 style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin: 0;">
                    Canonical SQLite Challenge Execution
                </h3>
                <p style="font-size: 0.84rem; color: #64748B; margin: 0.2rem 0 0 0;">
                    Live query execution directly against 'data/data_vortex.db' opened in read-only mode.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        challenge_choice = st.selectbox(
            "Select Challenge Query:",
            options=[
                "E2 - Most Engaged Posts (Easy)",
                "M1 - Which Locations Generate the Most Engagement? (Medium)",
                "H2 - Rank Users Within Their Location (Hard)",
            ],
            index=0,
            key="page2_sql_selector",
        )
        cid = challenge_choice.split(" ")[0]

        try:
            ch_data = execute_sql_challenge(cid)
            col_sql_code, col_sql_res = st.columns([5, 5])
            with col_sql_code:
                st.caption(f"SQL Definition: {ch_data['title']}")
                st.code(ch_data["sql"], language="sql")
                st.info(ch_data["description"])
            with col_sql_res:
                st.caption(f"Executed Table ({ch_data['rows']} rows from data_vortex.db)")
                st.dataframe(ch_data["results"], height=260)
        except Exception as e:
            st.error(f"SQL query error: {str(e)}")

    # -------------------------------------------------------------------------
    # TAB 2: SEMANTIC NLP INTELLIGENCE
    # -------------------------------------------------------------------------
    with tab_nlp:
        st.markdown(
            """
            <div style="margin: 0.5rem 0 1rem 0;">
                <h3 style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin: 0;">
                    Dual-Head Classification Benchmarks
                </h3>
                <p style="font-size: 0.84rem; color: #64748B; margin: 0.2rem 0 0 0;">
                    Held-out test set evaluation metrics and training class distributions from Round 2.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Benchmark KPI Cards
        b_col1, b_col2, b_col3, b_col4 = st.columns(4)
        with b_col1:
            st.metric(
                label="Sentiment Accuracy",
                value=format_percent(FROZEN_SENTIMENT_BENCHMARKS["accuracy"]),
                help="Logistic Regression (C=1.0)",
            )
        with b_col2:
            st.metric(
                label="Sentiment Macro F1",
                value=format_percent(FROZEN_SENTIMENT_BENCHMARKS["macro_f1"]),
                help="Balanced 3-Class Test",
            )
        with b_col3:
            st.metric(
                label="Topic Accuracy",
                value=format_percent(FROZEN_TOPIC_BENCHMARKS["accuracy"]),
                help="Linear SVM (LinearSVC)",
            )
        with b_col4:
            st.metric(
                label="Topic Weighted F1",
                value=format_percent(FROZEN_TOPIC_BENCHMARKS["weighted_f1"]),
                help="4-Class Intent Test",
            )

        st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

        # Training Class Distributions
        train_df = load_round2_training()
        col_s_dist, col_t_dist = st.columns(2)

        with col_s_dist:
            s_counts = train_df["sentiment_label"].value_counts().reset_index()
            s_counts.columns = ["sentiment", "count"]
            s_counts["percentage"] = (s_counts["count"] / len(train_df) * 100).round(1)
            fig_s = create_distribution_pie_or_bar(
                s_counts,
                category_col="sentiment",
                count_col="count",
                title="Sentiment Training Balance (9,000 Records)",
                color_map=SENTIMENT_COLORS,
            )
            st.plotly_chart(fig_s, use_container_width=True)

        with col_t_dist:
            t_counts = train_df["topic_category"].value_counts().reset_index()
            t_counts.columns = ["topic", "count"]
            t_counts["percentage"] = (t_counts["count"] / len(train_df) * 100).round(1)
            fig_t = create_distribution_pie_or_bar(
                t_counts,
                category_col="topic",
                count_col="count",
                title="Topic Intent Distribution (9,000 Records)",
                color_map=TOPIC_COLORS,
            )
            st.plotly_chart(fig_t, use_container_width=True)

    # -------------------------------------------------------------------------
    # TAB 3: TEMPORAL SIGNALS & SHIFTS
    # -------------------------------------------------------------------------
    with tab_signals:
        st.markdown(
            """
            <div style="margin: 0.5rem 0 1rem 0;">
                <h3 style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin: 0;">
                    Temporal Trajectory, Candidate Shifts & Spikes
                </h3>
                <p style="font-size: 0.84rem; color: #64748B; margin: 0.2rem 0 0 0;">
                    Longitudinal reaction tracking across the 15-year observation window (2011–2026).
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_sig_l, col_sig_r = st.columns([5, 5])

        with col_sig_l:
            st.markdown("<p style='font-size: 0.95rem; font-weight: 700; color: #0F172A;'>Audited Candidate Shifts (SS1 & SS2)</p>", unsafe_allow_html=True)
            for s in CANDIDATE_SHIFTS:
                delta_val = float(s["delta"])
                is_neg = delta_val < 0
                badge_bg = "#FEE2E2" if is_neg else "#DCFCE7"
                badge_color = "#DC2626" if is_neg else "#16A34A"
                border_color = "#DC2626" if is_neg else "#16A34A"
                delta_str = f"{delta_val:+.2f}"
                st.markdown(
                    f"""
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid {border_color}; border-radius: 6px; padding: 12px 14px; margin-bottom: 0.8rem; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <span style="font-weight: 700; color: #0F172A; font-size: 0.9rem;">{s['id']}: {s['period']}</span>
                            <span style="font-size: 0.75rem; font-weight: 700; color: {badge_color}; background: {badge_bg}; padding: 2px 6px; border-radius: 4px;">
                                Δ {delta_str}
                            </span>
                        </div>
                        <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 4px;">
                            Sample: {s['sample_size']} • Focus: <strong>{s['primary_topic']}</strong>
                        </div>
                        <p style="font-size: 0.82rem; color: #334155; margin: 0; line-height: 1.4;">
                            {s['finding']}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with col_sig_r:
            st.markdown("<p style='font-size: 0.95rem; font-weight: 700; color: #0F172A;'>Target Gazetteer Entity Mentions</p>", unsafe_allow_html=True)
            ent_df = get_entity_frequencies()
            fig_ent = create_entity_frequency_chart(ent_df)
            st.plotly_chart(fig_ent, use_container_width=True)

        st.markdown("<p style='font-size: 0.95rem; font-weight: 700; color: #0F172A; margin-top: 0.5rem;'>Extreme Engagement Spike Anomalies (Baseline: 6.00)</p>", unsafe_allow_html=True)
        spikes_df = pd.DataFrame(ENGAGEMENT_SPIKES)
        disp_spikes = spikes_df[["id", "date", "observed_score", "ratio", "title", "sentiment", "topic"]].copy()
        disp_spikes.columns = ["Spike ID", "Event Date", "Observed Score", "Baseline Multiple", "Discussion Title", "Sentiment", "Topic Intent"]
        st.dataframe(disp_spikes, height=160)

    # Limitations Callout
    render_limitation_callout()


if __name__ == "__main__":
    render()
