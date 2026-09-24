"""
Metric Cards Component for Round 4 Streamlit Application.
"""

from typing import Union, Optional
import streamlit as st

def render_kpi_card(
    label: str,
    value: Union[str, int, float],
    delta: Optional[str] = None,
    delta_color: str = "normal",  # "normal", "inverse", "off"
    subtext: Optional[str] = None,
    help_text: Optional[str] = None,
):
    """
    Renders a clean, high-contrast light KPI card.
    """
    is_positive = str(delta).startswith("+") or "Recovered" in str(delta) or "0 FK" in str(delta) or "Balance" in str(delta)
    delta_color_css = "#059669" if is_positive else "#DC2626"

    with st.container():
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px 16px; margin-bottom: 0.8rem; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                <div style="font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; color: #64748B; margin-bottom: 4px;">
                    {label}
                </div>
                <div style="font-size: 1.65rem; font-weight: 700; color: #0F172A; line-height: 1.1; margin-bottom: 4px; font-family: 'Outfit', sans-serif;">
                    {value}
                </div>
                {"<div style='font-size: 0.8rem; color: " + delta_color_css + "; font-weight: 600;'>" + delta + "</div>" if delta else ""}
                {"<div style='font-size: 0.75rem; color: #94A3B8; margin-top: 4px;'>" + subtext + "</div>" if subtext else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )
