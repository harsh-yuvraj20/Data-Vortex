"""
Header Component for Round 4 Streamlit Application.
"""

import streamlit as st
from pathlib import Path
import sys

_ROUND4_DIR = str(Path(__file__).resolve().parents[1])
if _ROUND4_DIR not in sys.path:
    sys.path.insert(0, _ROUND4_DIR)

from config.settings import APP_TITLE, APP_SUBTITLE, APP_VERSION

def render_header(page_title: str, page_description: str, breadcrumb: str = "Social Engine"):
    """
    Renders a unified top header with breadcrumbs, title, description, and status tag
    with clean light corporate styling.
    """
    st.markdown(
        f"""
        <div style="margin-bottom: 1.5rem; padding-bottom: 0.8rem; border-bottom: 1px solid #E2E8F0;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                <span style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B;">
                    DATA VORTEX 2026 &nbsp;>&nbsp; {breadcrumb} &nbsp;>&nbsp; <span style="color: #1E3A8A;">{page_title}</span>
                </span>
                <span style="background-color: #EFF6FF; color: #1E3A8A; font-size: 0.75rem; font-weight: 600; padding: 2px 8px; border-radius: 9999px; border: 1px solid #BFDBFE;">
                    v{APP_VERSION} • Production Validated
                </span>
            </div>
            <h1 style="font-size: 1.85rem; font-weight: 700; color: #0F172A; margin: 0 0 0.4rem 0; line-height: 1.2;">
                {page_title}
            </h1>
            <p style="font-size: 0.95rem; color: #475569; margin: 0; max-width: 900px; line-height: 1.45;">
                {page_description}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
