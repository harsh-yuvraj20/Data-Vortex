"""
Theme & Visual Design System for DATA VORTEX 2026 — Round 4: Social Engine Revival.

Provides a clean, light, corporate analytical design system:
- Crisp white & light slate background (#F8FAFC / #FFFFFF).
- Clean borders (#E2E8F0) and subtle shadows.
- High-contrast dark typography (#0F172A primary, #475569 secondary).
- Professional navy, royal blue, and restrained teal/amber accents.
- Light Plotly chart integration.
"""

import streamlit as st


def apply_custom_theme(is_landing: bool = False) -> None:
    """
    Injects the clean light corporate design system across all Streamlit pages.
    """
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap');
            
            /* Root & Global App Styling */
            html, body, [class*="css"] {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                color: #0F172A;
            }

            .stApp {
                background-color: #F8FAFC !important;
                color: #0F172A !important;
            }

            /* Container padding */
            .block-container {
                padding-top: 1.8rem !important;
                padding-bottom: 2.5rem !important;
                max-width: 1380px !important;
            }

            /* Headings */
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Outfit', 'Inter', sans-serif !important;
                letter-spacing: -0.015em !important;
                color: #0F172A !important;
            }

            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: #FFFFFF !important;
                border-right: 1px solid #E2E8F0 !important;
            }
            [data-testid="stSidebar"] hr {
                border-color: #E2E8F0 !important;
            }
            [data-testid="stSidebarNav"] {
                padding-top: 0.5rem;
            }
            [data-testid="stSidebarNav"] span {
                color: #334155 !important;
                font-weight: 500 !important;
                font-size: 0.88rem !important;
            }
            [data-testid="stSidebarNav"] a:hover span {
                color: #1E3A8A !important;
            }
            [data-testid="stSidebarNav"] a[aria-current="page"] span {
                color: #1E3A8A !important;
                font-weight: 700 !important;
            }

            /* Metrics */
            [data-testid="stMetric"] {
                background: #FFFFFF !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 8px !important;
                padding: 14px 18px !important;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
            }
            [data-testid="stMetricValue"] {
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.8rem !important;
                font-weight: 700 !important;
                color: #0F172A !important;
                line-height: 1.15 !important;
            }
            [data-testid="stMetricLabel"] {
                color: #64748B !important;
                font-size: 0.76rem !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.04em !important;
                margin-bottom: 2px !important;
            }
            [data-testid="stMetricDelta"] {
                font-size: 0.78rem !important;
                font-weight: 600 !important;
            }

            /* Buttons */
            .stButton button {
                border-radius: 6px !important;
                font-weight: 600 !important;
                border: 1px solid #CBD5E1 !important;
                background-color: #FFFFFF !important;
                color: #0F172A !important;
                transition: all 0.15s ease-in-out !important;
            }
            .stButton button:hover {
                border-color: #1E3A8A !important;
                color: #1E3A8A !important;
                background-color: #F8FAFC !important;
            }

            /* Primary Button */
            .stButton button[kind="primary"] {
                background: #1E3A8A !important;
                color: #FFFFFF !important;
                font-weight: 600 !important;
                border: 1px solid #1E3A8A !important;
                box-shadow: 0 1px 3px rgba(30, 58, 138, 0.25) !important;
            }
            .stButton button[kind="primary"]:hover {
                background: #2563EB !important;
                border-color: #2563EB !important;
                color: #FFFFFF !important;
            }

            /* Tabs */
            [data-baseweb="tab-list"] {
                background: #F1F5F9 !important;
                border-radius: 8px !important;
                border: 1px solid #E2E8F0 !important;
                padding: 4px !important;
                gap: 4px !important;
            }
            [data-baseweb="tab"] {
                color: #64748B !important;
                font-size: 0.88rem !important;
                font-weight: 600 !important;
                padding: 8px 16px !important;
                border-radius: 6px !important;
            }
            [data-baseweb="tab"][aria-selected="true"] {
                background: #FFFFFF !important;
                color: #1E3A8A !important;
                border-bottom: 2px solid #1E3A8A !important;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
            }

            /* Input Controls */
            [data-baseweb="select"] > div,
            [data-testid="stTextInput"] input,
            [data-testid="stTextArea"] textarea,
            [data-testid="stNumberInput"] input {
                background-color: #FFFFFF !important;
                color: #0F172A !important;
                border: 1px solid #CBD5E1 !important;
                border-radius: 6px !important;
            }
            [data-baseweb="select"] > div:hover,
            [data-testid="stTextInput"] input:focus,
            [data-testid="stTextArea"] textarea:focus,
            [data-testid="stNumberInput"] input:focus {
                border-color: #1E3A8A !important;
                box-shadow: 0 0 0 1px #1E3A8A !important;
            }

            /* Dataframes & Tables */
            [data-testid="stDataFrame"] {
                border: 1px solid #E2E8F0 !important;
                border-radius: 8px !important;
                background-color: #FFFFFF !important;
            }

            /* Code block */
            [data-testid="stCodeBlock"] {
                border: 1px solid #E2E8F0 !important;
                border-radius: 8px !important;
            }

            /* Progress Bar */
            .stProgress > div > div > div > div {
                background-color: #2563EB !important;
            }

            /* Alerts & Info Callouts */
            div[data-testid="stAlert"] {
                border-radius: 8px !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_vortex_graphic() -> str:
    """Placeholder returning empty string to preserve compatibility."""
    return ""
