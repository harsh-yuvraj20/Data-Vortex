"""
Sidebar Component for Round 4 Streamlit Application.
"""

from typing import Tuple, Optional
import streamlit as st

from pathlib import Path
import sys

_ROUND4_DIR = str(Path(__file__).resolve().parents[1])
if _ROUND4_DIR not in sys.path:
    sys.path.insert(0, _ROUND4_DIR)

from config.settings import APP_TITLE, APP_SUBTITLE, APP_VERSION
from repositories.sqlite_repository import get_sqlite_repo
from repositories.dataset_repository import DatasetRepository
from repositories.model_repository import ModelRepository

PAGES = [
    "Home",
    "01 Overview",
    "02 Analysis",
    "03 Interactive Explorer",
    "04 Methodology",
]

def render_sidebar() -> None:
    """
    Renders sidebar brand header, system health indicators, and local-first diagnostics
    with clean light corporate styling.
    """
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding: 0.5rem 0 0.8rem 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 0.8rem;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 8px; height: 8px; border-radius: 50%; background-color: #059669;"></div>
                    <span style="font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #1E3A8A;">
                        DATA VORTEX 2026
                    </span>
                </div>
                <h3 style="font-size: 1.1rem; font-weight: 700; color: #0F172A; margin: 0.2rem 0 0.1rem 0;">
                    {APP_TITLE}
                </h3>
                <p style="font-size: 0.78rem; color: #64748B; margin: 0;">
                    Round 4 • Unified Social Engine
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # System Health & Local-First Diagnostics
        st.markdown(
            "<p style='font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #94A3B8; margin-bottom: 0.4rem;'>System Integrity</p>",
            unsafe_allow_html=True,
        )

        try:
            sqlite_status = "Online (Read-Only)"
            get_sqlite_repo().get_database_info()
            sqlite_badge = "🟢"
        except Exception:
            sqlite_status = "Unavailable"
            sqlite_badge = "🔴"

        try:
            ModelRepository.load_sentiment_pipeline()
            ModelRepository.load_topic_pipeline()
            model_status = "Models Loaded"
            model_badge = "🟢"
        except Exception:
            model_status = "Model Missing"
            model_badge = "🔴"

        st.markdown(
            f"""
            <div style="font-size: 0.78rem; color: #475569; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 8px 10px; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>SQLite Core:</span>
                    <span style="font-weight: 600;">{sqlite_badge} {sqlite_status}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>NLP Engine:</span>
                    <span style="font-weight: 600;">{model_badge} {model_status}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Mode:</span>
                    <span style="font-weight: 600; color: #0D9488;">Offline / Local</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("Zero-Duplication Repository Architecture • All Rights Reserved")
