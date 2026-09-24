"""
PAGE 4 — METHODOLOGY
DATA VORTEX 2026 — Round 4: Social Engine Revival

Presents concise technical documentation in clean light styling:
1. Four-phase analytical methodology (Round 1 through Round 4)
2. Canonical dataset provenance & zero-duplication architecture
3. Model cards & calibration protocols
4. Reproducibility instructions & offline local-first execution
5. Mandatory research boundaries & non-causality disclosure
"""

from pathlib import Path
import sys
import streamlit as st

ROUND4_DIR = Path(__file__).resolve().parent.parent
if str(ROUND4_DIR) not in sys.path:
    sys.path.insert(0, str(ROUND4_DIR))

from src.utils import APP_TITLE
from src.metrics import get_cross_round_evidence_matrix
from components.findings import render_limitation_callout
from components.sidebar import render_sidebar
from components.header import render_header
from components.theme import apply_custom_theme

st.set_page_config(
    page_title=f"Methodology | {APP_TITLE}",
    page_icon="📖",
    layout="wide",
)

# Apply global clean light corporate theme
apply_custom_theme()


def render():
    render_sidebar()
    render_header(
        page_title="Methodology, Architecture & Provenance",
        page_description="Comprehensive guide to the four-phase analytical lifecycle, zero-duplication repository architecture, calibration standards, and local reproducibility.",
        breadcrumb="04 Methodology",
    )

    # 1. Four-Phase Lifecycle Grid
    st.markdown(
        """
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 18px 20px; margin-bottom: 1.2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
            <h3 style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin: 0 0 0.8rem 0;">
                Four-Phase Analytical Lifecycle
            </h3>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;">
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 0.72rem; font-weight: 700; color: #1E3A8A; text-transform: uppercase;">Phase 1 • Round 1</div>
                    <div style="font-weight: 700; color: #0F172A; margin: 2px 0 4px 0; font-size: 0.88rem;">Recovery & Relational SQL</div>
                    <p style="font-size: 0.78rem; color: #64748B; margin: 0; line-height: 1.4;">
                        Forensic cleaning of 12,000 corrupted posts across 1,500 users. Relational SQLite engineering and challenges E2, M1, and H2.
                    </p>
                </div>
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 0.72rem; font-weight: 700; color: #0D9488; text-transform: uppercase;">Phase 2 • Round 2</div>
                    <div style="font-weight: 700; color: #0F172A; margin: 2px 0 4px 0; font-size: 0.88rem;">NLP Semantic Models</div>
                    <p style="font-size: 0.78rem; color: #64748B; margin: 0; line-height: 1.4;">
                        Dual-head classification pipelines: Logistic Regression (Sentiment) and Linear SVM (Topic Intent) on 9,000 balanced items.
                    </p>
                </div>
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 0.72rem; font-weight: 700; color: #D97706; text-transform: uppercase;">Phase 3 • Round 3</div>
                    <div style="font-weight: 700; color: #0F172A; margin: 2px 0 4px 0; font-size: 0.88rem;">Longitudinal Signals</div>
                    <p style="font-size: 0.78rem; color: #64748B; margin: 0; line-height: 1.4;">
                        Mined 204 reaction items across a 15-year window. Identified candidate shifts SS1 & SS2 and engagement spikes ES1–ES3.
                    </p>
                </div>
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px;">
                    <div style="font-size: 0.72rem; font-weight: 700; color: #2563EB; text-transform: uppercase;">Phase 4 • Round 4</div>
                    <div style="font-weight: 700; color: #0F172A; margin: 2px 0 4px 0; font-size: 0.88rem;">Streamlit-First System</div>
                    <p style="font-size: 0.78rem; color: #64748B; margin: 0; line-height: 1.4;">
                        Modular, local-first Streamlit application integrating data loading, SQLite execution, live inference, and synthesis offline.
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Cross-Round Verification Matrix
    st.markdown("<h4 style='font-size: 1.05rem; font-weight: 700; color: #0F172A; margin: 0 0 0.5rem 0;'>Cross-Round Verification Matrix</h4>", unsafe_allow_html=True)
    evidence_df = get_cross_round_evidence_matrix()
    st.dataframe(evidence_df, height=210)

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # 3. Model Cards & Calibration Protocols
    m_col1, m_col2 = st.columns([5, 5])

    with m_col1:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; height: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                <h4 style="font-size: 0.98rem; font-weight: 700; color: #0F172A; margin: 0 0 0.5rem 0;">
                    Model Cards & Calibration Standards
                </h4>
                <div style="font-size: 0.82rem; color: #334155; line-height: 1.5;">
                    <div style="margin-bottom: 8px;">
                        <strong>Sentiment Classifier:</strong><br>
                        • Model: TF-IDF Unigrams/Bigrams + Logistic Regression (C=1.0)<br>
                        • Calibration: Posterior probabilities via <code>predict_proba</code>. Sums strictly to 1.0 across classes.
                    </div>
                    <div>
                        <strong>Topic Category Classifier:</strong><br>
                        • Model: TF-IDF Word N-grams + Linear Support Vector Machine (LinearSVC)<br>
                        • Calibration: Signed margin distance via <code>decision_function</code>. Explicitly labeled softmax approximation displayed in UI without claiming true posterior probability.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m_col2:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; height: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                <h4 style="font-size: 0.98rem; font-weight: 700; color: #0F172A; margin: 0 0 0.5rem 0;">
                    Local-First Architecture & Reproducibility
                </h4>
                <p style="font-size: 0.82rem; color: #475569; margin-bottom: 8px;">
                    The application operates entirely offline on a local machine without external API keys or remote dependencies:
                </p>
                <pre style="background: #0F172A; color: #F8FAFC; padding: 10px; border-radius: 6px; font-size: 0.78rem;">pip install -r requirements.txt\nstreamlit run app.py</pre>
                <div style="font-size: 0.78rem; color: #64748B; margin-top: 6px;">
                    All canonical artifacts are loaded via deterministic repository-relative paths without duplicating binary files.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 4. Mandatory Limitations
    render_limitation_callout()


if __name__ == "__main__":
    render()
