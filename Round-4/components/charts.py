"""
Chart Components for Round 4 Streamlit Application.

Provides clean, uniform Plotly visualizations strictly complying with research
aesthetics: light corporate theme, no misleading axes, restrained palettes, and clear labels.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from pathlib import Path
import sys

_ROUND4_DIR = str(Path(__file__).resolve().parents[1])
if _ROUND4_DIR not in sys.path:
    sys.path.insert(0, _ROUND4_DIR)

from config.settings import (
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_ACCENT,
    SENTIMENT_COLORS,
    TOPIC_COLORS,
    PLOTLY_TEMPLATE,
)

def create_data_funnel_chart(metrics: Dict[str, Any]) -> go.Figure:
    """Creates a clean horizontal funnel showing data volume across rounds in light theme."""
    stages = [
        "Round 1: Cleaned Posts",
        "Round 2: NLP Training Corpus",
        "Round 1: Registered Users",
        "Round 3: Reaction Archive",
    ]
    values = [
        metrics["total_cleaned_posts"],
        metrics["total_nlp_training_records"],
        metrics["total_registered_users"],
        metrics["total_reaction_records"],
    ]

    fig = go.Figure(
        go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial",
            marker={
                "color": ["#1E3A8A", "#2563EB", "#0D9488", "#D97706"],
                "line": {"width": 1, "color": "#CBD5E1"},
            },
        )
    )
    fig.update_layout(
        title="Cross-Round Data Scale & Architecture Flow",
        height=280,
        margin={"l": 160, "r": 20, "t": 40, "b": 20},
        font=PLOTLY_TEMPLATE["layout"]["font"],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig

def create_temporal_trajectory_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders dual-axis monthly volume and Net Sentiment Index line with clean light styling.
    """
    fig = go.Figure()

    # Bar: Monthly Volume
    fig.add_trace(
        go.Bar(
            x=df["year_month"],
            y=df["total"],
            name="Monthly Reaction Volume",
            marker_color="#CBD5E1",
            opacity=0.7,
            yaxis="y1",
        )
    )

    # Line: Net Sentiment Index
    fig.add_trace(
        go.Scatter(
            x=df["year_month"],
            y=df["net_sentiment_index"],
            name="Net Sentiment Index (Pos - Neg)/Total",
            mode="lines+markers",
            line={"color": "#1E3A8A", "width": 2.5},
            marker={"size": 6, "color": "#1E3A8A"},
            yaxis="y2",
        )
    )

    fig.update_layout(
        title="Longitudinal Sentiment Trajectory & Archive Activity (2011–2026)",
        height=360,
        margin={"l": 40, "r": 40, "t": 50, "b": 40},
        font=PLOTLY_TEMPLATE["layout"]["font"],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,250,252,0.6)",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
        xaxis={"title": "Observation Month", "tickangle": -45, "gridcolor": "#E2E8F0"},
        yaxis={
            "title": "Post Volume",
            "side": "left",
            "gridcolor": "#E2E8F0",
            "showgrid": True,
        },
        yaxis2={
            "title": "Net Sentiment Index",
            "side": "right",
            "overlaying": "y",
            "range": [-1.1, 1.1],
            "zeroline": True,
            "zerolinecolor": "#94A3B8",
            "zerolinewidth": 1.5,
            "showgrid": False,
        },
    )
    return fig

def create_platform_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """Bar chart of platform post volumes and engagement in light theme."""
    fig = go.Figure(
        go.Bar(
            x=df["platform"],
            y=df["post_count"],
            marker_color=["#1E3A8A", "#2563EB", "#0D9488", "#059669"],
            text=[f"{v:,} posts" for v in df["post_count"]],
            textposition="auto",
        )
    )
    fig.update_layout(
        title="Post Volume by Origin Platform (Round 1)",
        height=310,
        margin={"l": 40, "r": 20, "t": 40, "b": 40},
        font=PLOTLY_TEMPLATE["layout"]["font"],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,250,252,0.6)",
        xaxis={"title": "Platform", "gridcolor": "#E2E8F0"},
        yaxis={"title": "Total Cleaned Posts", "gridcolor": "#E2E8F0"},
    )
    return fig

def create_distribution_pie_or_bar(df: pd.DataFrame, category_col: str, count_col: str, title: str, color_map: dict) -> go.Figure:
    """Renders a clean horizontal bar chart for category distributions in light theme."""
    colors = [color_map.get(cat, "#64748B") for cat in df[category_col]]
    
    fig = go.Figure(
        go.Bar(
            y=df[category_col],
            x=df[count_col],
            orientation="h",
            marker_color=colors,
            text=[f"{v:,} ({p}%)" for v, p in zip(df[count_col], df["percentage"])],
            textposition="auto",
        )
    )
    fig.update_layout(
        title=title,
        height=260,
        margin={"l": 140, "r": 20, "t": 40, "b": 30},
        font=PLOTLY_TEMPLATE["layout"]["font"],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,250,252,0.6)",
        xaxis={"title": "Record Count", "gridcolor": "#E2E8F0"},
        yaxis={"autorange": "reversed"},
    )
    return fig

def create_entity_frequency_chart(df: pd.DataFrame) -> go.Figure:
    """Renders horizontal bar chart of entity mentions in light theme."""
    fig = go.Figure(
        go.Bar(
            y=df["entity"],
            x=df["mentions"],
            orientation="h",
            marker_color="#0D9488",
            text=df["mentions"],
            textposition="auto",
        )
    )
    fig.update_layout(
        title="Target Gazetteer Entity Mentions in Reactions (Round 3)",
        height=300,
        margin={"l": 100, "r": 20, "t": 40, "b": 30},
        font=PLOTLY_TEMPLATE["layout"]["font"],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,250,252,0.6)",
        xaxis={"title": "Mention Count", "gridcolor": "#E2E8F0"},
        yaxis={"autorange": "reversed"},
    )
    return fig
