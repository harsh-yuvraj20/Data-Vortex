"""
Findings Component for Round 4 Streamlit Application.
"""

import streamlit as st

def render_finding_card(title: str, text: str, tag: str = "Empirical Finding", tag_color: str = "#1E3A8A"):
    """
    Renders an analytical takeaway card in clean light styling.
    """
    st.markdown(
        f"""
        <div style="background: #FFFFFF; border-left: 4px solid {tag_color}; border-top: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0; border-radius: 6px; padding: 12px 16px; margin-bottom: 0.8rem; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <span style="font-size: 0.9rem; font-weight: 700; color: #0F172A;">{title}</span>
                <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; background: #F1F5F9; color: {tag_color}; padding: 2px 6px; border-radius: 4px;">
                    {tag}
                </span>
            </div>
            <p style="font-size: 0.85rem; color: #475569; margin: 0; line-height: 1.45;">
                {text}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_limitation_callout():
    """
    Renders the mandatory research boundaries and non-causality callout in clean light styling.
    """
    st.markdown(
        """
        <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-left: 4px solid #D97706; border-radius: 6px; padding: 12px 16px; margin: 1rem 0;">
            <div style="font-size: 0.85rem; font-weight: 700; color: #92400E; margin-bottom: 4px;">
                ⚠️ Methodological Boundaries & Non-Causality Disclosure
            </div>
            <div style="font-size: 0.82rem; color: #78350F; line-height: 1.45;">
                <strong>1. Historical Archive Sampling:</strong> Round 3 data originates from a bounded historical Hacker News archive sample (2011–2026), reflecting technical platform users rather than a continuous real-time public stream.<br>
                <strong>2. Non-Causality Principle:</strong> Identified candidate shifts (SS1, SS2) and engagement spikes (ES1, ES2, ES3) are empirical temporal associations. Causality is strictly disclaimed due to unobserved confounders.<br>
                <strong>3. Missing Attributes:</strong> Comment scores are omitted by API design and excluded from aggregate scores rather than synthetically imputed.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
