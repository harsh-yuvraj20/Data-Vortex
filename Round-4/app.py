"""
DATA VORTEX 2026 — ROUND 4: SOCIAL ENGINE REVIVAL
Main Application Landing Page (Executive Home)

Presents executive KPIs, primary visualizations, system-wide scale,
and an orientation roadmap for multi-round exploration in a clean light theme.
"""

from pathlib import Path
import sys
import streamlit as st
import plotly.graph_objects as go

# Ensure Round-4 root is in path
ROUND4_DIR = Path(__file__).resolve().parent
if str(ROUND4_DIR) not in sys.path:
    sys.path.insert(0, str(ROUND4_DIR))

from src.utils import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_VERSION,
    format_number,
    PLOTLY_TEMPLATE,
)
from src.metrics import get_system_scale_metrics
from src.analysis import get_monthly_trajectory
from components.findings import render_limitation_callout
from components.sidebar import render_sidebar
from components.theme import apply_custom_theme
from components.charts import create_data_funnel_chart, create_temporal_trajectory_chart

# -----------------------------------------------------------------------------
# Streamlit Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title=f"{APP_TITLE} | Data Vortex",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply global clean light corporate theme
apply_custom_theme()

# -----------------------------------------------------------------------------
# Main Executive Dashboard
# -----------------------------------------------------------------------------
def render_main():
    render_sidebar()

    # 1. Header Banner
    st.markdown(
        f"""
        <div style="margin-bottom: 1.5rem; padding-bottom: 0.8rem; border-bottom: 1px solid #E2E8F0;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                <span style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B;">
                    DATA VORTEX 2026 &nbsp;>&nbsp; Executive Dashboard
                </span>
                <span style="background-color: #EFF6FF; color: #1E3A8A; font-size: 0.75rem; font-weight: 600; padding: 2px 8px; border-radius: 9999px; border: 1px solid #BFDBFE;">
                    v{APP_VERSION} • Production Validated
                </span>
            </div>
            <h1 style="font-size: 2.2rem; font-weight: 800; color: #0F172A; margin: 0 0 0.3rem 0; line-height: 1.15;">
                {APP_TITLE}
            </h1>
            <p style="font-size: 1.02rem; color: #475569; margin: 0; max-width: 950px; line-height: 1.5;">
                {APP_SUBTITLE}. An offline, multi-round analytical system uniting forensic data recovery,
                dual-head semantic NLP, and longitudinal signal mining into an executive intelligence suite.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Key Validated Metrics / KPIs
    metrics = get_system_scale_metrics()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(
            label="Total Cleaned Posts",
            value=format_number(metrics["total_cleaned_posts"]),
            delta="100% Recovered",
            help="Round 1 Phase 1 forensic cleaning preserved all 12,000 observations.",
        )
    with kpi2:
        st.metric(
            label="Registered Creators",
            value=format_number(metrics["total_registered_users"]),
            delta="0 FK Violations",
            help="Round 1 Phase 2 SQLite core referential integrity verified.",
        )
    with kpi3:
        st.metric(
            label="NLP Training Corpus",
            value=format_number(metrics["total_nlp_training_records"]),
            delta="Exact 1:1:1 Balance",
            help="Round 2 balanced training set across 3 sentiment polarity classes.",
        )
    with kpi4:
        st.metric(
            label="Longitudinal Archive",
            value=format_number(metrics["total_reaction_records"]),
            delta="15-Year Span (2011-2026)",
            help="Round 3 reaction archive tracking algorithmic commentary.",
        )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # 3. Two Primary Visualizations
    col_vis1, col_vis2 = st.columns([5, 5])

    with col_vis1:
        funnel_fig = create_data_funnel_chart(metrics)
        st.plotly_chart(funnel_fig, use_container_width=True)

    with col_vis2:
        traj = get_monthly_trajectory()
        traj_fig = create_temporal_trajectory_chart(traj)
        st.plotly_chart(traj_fig, use_container_width=True)

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # 4. Roadmap & Orientation to Exploration Pages
    st.markdown(
        """
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 18px 20px; margin-bottom: 1.2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
            <h3 style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin: 0 0 0.6rem 0;">
                Application Exploration Roadmap
            </h3>
            <p style="font-size: 0.88rem; color: #475569; margin-bottom: 1rem; line-height: 1.45;">
                Navigate through the sidebar pages to inspect granular multi-round findings and interact with live analytical tools:
            </p>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;">
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 0.72rem; font-weight: 700; color: #1E3A8A; text-transform: uppercase;">Page 01</div>
                    <div style="font-weight: 700; color: #0F172A; margin: 2px 0 4px 0; font-size: 0.9rem;">Overview</div>
                    <p style="font-size: 0.8rem; color: #64748B; margin: 0; line-height: 1.4;">
                        Dataset scale, forensic recovery logs, summary statistics, and the four executive synthesis pillars.
                    </p>
                </div>
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 0.72rem; font-weight: 700; color: #0D9488; text-transform: uppercase;">Page 02</div>
                    <div style="font-weight: 700; color: #0F172A; margin: 2px 0 4px 0; font-size: 0.9rem;">Analysis</div>
                    <p style="font-size: 0.8rem; color: #64748B; margin: 0; line-height: 1.4;">
                        Canonical SQL query outputs (E2, M1, H2), Round 2 NLP held-out benchmarks, candidate shifts (SS1, SS2), and engagement spikes.
                    </p>
                </div>
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 0.72rem; font-weight: 700; color: #2563EB; text-transform: uppercase;">Page 03</div>
                    <div style="font-weight: 700; color: #0F172A; margin: 2px 0 4px 0; font-size: 0.9rem;">Interactive Explorer</div>
                    <p style="font-size: 0.8rem; color: #64748B; margin: 0; line-height: 1.4;">
                        Live interactive post filtering and dual-head NLP classification sandbox with preset domain examples and calibrated probabilities.
                    </p>
                </div>
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 0.72rem; font-weight: 700; color: #D97706; text-transform: uppercase;">Page 04</div>
                    <div style="font-weight: 700; color: #0F172A; margin: 2px 0 4px 0; font-size: 0.9rem;">Methodology</div>
                    <p style="font-size: 0.8rem; color: #64748B; margin: 0; line-height: 1.4;">
                        Four-phase methodology, dataset inventory, model cards, reproducibility guide, and non-causal boundaries.
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 5. Mandatory Limitations Callout
    render_limitation_callout()

if __name__ == "__main__":
    render_main()
