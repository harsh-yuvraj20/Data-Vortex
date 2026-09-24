"""
Filters Component for Round 4 Streamlit Application.
"""

from typing import List, Tuple, Optional
import streamlit as st
import pandas as pd

def render_post_filters(available_platforms: List[str]) -> Tuple[List[str], Optional[tuple], int, str]:
    """
    Renders filter controls for post exploration.
    """
    col1, col2, col3, col4 = st.columns([2, 2, 2, 3])

    with col1:
        platforms = st.multiselect(
            "Platform",
            options=available_platforms,
            default=available_platforms,
            key="filter_platforms",
        )

    with col2:
        min_likes = st.number_input(
            "Min Likes",
            min_value=0,
            max_value=10000,
            value=0,
            step=50,
            key="filter_min_likes",
        )

    with col3:
        sort_by = st.selectbox(
            "Order By",
            options=["Newest", "Most Likes", "Most Shares", "Most Comments"],
            index=0,
            key="filter_sort",
        )

    with col4:
        query = st.text_input(
            "Search Text",
            placeholder="e.g. login, update, performance...",
            key="filter_search_query",
        )

    return platforms, None, min_likes, query
