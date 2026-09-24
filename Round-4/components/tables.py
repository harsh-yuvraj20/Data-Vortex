"""
Table Component for Round 4 Streamlit Application.
"""

from typing import Optional
import pandas as pd
import streamlit as st

def render_interactive_table(
    df: pd.DataFrame,
    title: Optional[str] = None,
    caption: Optional[str] = None,
    height: int = 320,
):
    """
    Renders a styled Streamlit dataframe in clean light styling.
    """
    if title:
        st.markdown(f"<p style='font-size: 0.95rem; font-weight: 600; color: #0F172A; margin: 0.5rem 0 0.2rem 0;'>{title}</p>", unsafe_allow_html=True)
    if caption:
        st.caption(caption)
    
    st.dataframe(df, height=height)
