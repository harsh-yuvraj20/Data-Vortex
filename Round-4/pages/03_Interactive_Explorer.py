"""
PAGE 3 — INTERACTIVE EXPLORER
DATA VORTEX 2026 — Round 4: Social Engine Revival

Provides two interactive tools in clean light styling:
1. Dynamic Post Explorer with multi-attribute filtering (Platform, Likes, Keyword Search, Ordering)
2. Live Dual-Head NLP Inference Sandbox with domain presets, calibrated posterior probabilities, and signed margin scores
"""

from pathlib import Path
import sys
import streamlit as st
import pandas as pd

ROUND4_DIR = Path(__file__).resolve().parent.parent
if str(ROUND4_DIR) not in sys.path:
    sys.path.insert(0, str(ROUND4_DIR))

from src.utils import APP_TITLE, format_number, format_percent, SENTIMENT_COLORS, TOPIC_COLORS
from src.analysis import filter_posts
from src.model import predict_dual_head, PRESET_EXAMPLES
from src.data_loader import load_round1_posts
from components.sidebar import render_sidebar
from components.header import render_header
from components.theme import apply_custom_theme

st.set_page_config(
    page_title=f"Interactive Explorer | {APP_TITLE}",
    page_icon="🔍",
    layout="wide",
)

# Apply global clean light corporate theme
apply_custom_theme()


def render():
    render_sidebar()
    render_header(
        page_title="Interactive Data & Model Explorer",
        page_description="Engage directly with the social dataset through parameterized filters, and evaluate live NLP model predictions with verified calibration protocols.",
        breadcrumb="03 Interactive Explorer",
    )

    tab_explore, tab_inference = st.tabs([
        "1. Dynamic Post Record Explorer",
        "2. Live NLP Semantic Prediction Sandbox",
    ])

    # -------------------------------------------------------------------------
    # TAB 1: DYNAMIC POST EXPLORER
    # -------------------------------------------------------------------------
    with tab_explore:
        st.markdown(
            """
            <div style="margin: 0.5rem 0 0.8rem 0;">
                <h3 style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin: 0;">
                    Multi-Attribute Social Post Filter
                </h3>
                <p style="font-size: 0.84rem; color: #64748B; margin: 0.2rem 0 0 0;">
                    Every control dynamically queries the underlying 12,000 post corpus in memory.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        f_col1, f_col2, f_col3, f_col4 = st.columns([2, 2, 2, 3])
        with f_col1:
            all_plats = ["Twitter", "Instagram", "Reddit", "Facebook"]
            selected_plats = st.multiselect(
                "Filter Platforms",
                options=all_plats,
                default=all_plats,
                key="p3_plat_filter",
            )
        with f_col2:
            min_likes = st.number_input(
                "Min Likes Threshold",
                min_value=0,
                max_value=10000,
                value=0,
                step=50,
                key="p3_likes_filter",
            )
        with f_col3:
            sort_order = st.selectbox(
                "Order Records By",
                options=["Highest Likes", "Highest Shares", "Highest Comments", "Default"],
                index=0,
                key="p3_sort_filter",
            )
        with f_col4:
            search_query = st.text_input(
                "Search Text Content",
                placeholder="e.g. security, algorithm, update...",
                key="p3_search_filter",
            )

        # Execute dynamic filtering
        posts_df = load_round1_posts().copy()
        if selected_plats:
            posts_df = posts_df[posts_df["platform"].isin(selected_plats)]
        else:
            posts_df = posts_df.iloc[0:0]
        if min_likes > 0 and not posts_df.empty:
            posts_df = posts_df[posts_df["likes"] >= min_likes]
        if search_query.strip() and not posts_df.empty:
            posts_df = posts_df[posts_df["text_content"].str.lower().str.contains(search_query.strip().lower(), na=False)]

        if not posts_df.empty:
            if sort_order == "Highest Likes":
                posts_df = posts_df.sort_values(by="likes", ascending=False)
            elif sort_order == "Highest Shares":
                posts_df = posts_df.sort_values(by="shares", ascending=False)
            elif sort_order == "Highest Comments":
                posts_df = posts_df.sort_values(by="comments", ascending=False)

        # Dynamic Summary Bar
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric("Matching Observations", format_number(len(posts_df)))
        with m_col2:
            st.metric("Filtered Likes Total", format_number(posts_df["likes"].sum()) if not posts_df.empty else "0")
        with m_col3:
            avg_eng = round((posts_df["likes"] + posts_df["shares"] + posts_df["comments"]).mean(), 1) if not posts_df.empty else 0.0
            st.metric("Avg Engagement in Selection", str(avg_eng))

        if not selected_plats:
            st.info("No platforms selected. Please select one or more platforms above to display posts.")
        elif posts_df.empty:
            st.warning("No records matched your filter criteria. Try adjusting the search query or minimum likes.")
        else:
            display_cols = ["post_id", "user_id", "platform", "timestamp", "likes", "shares", "comments", "text_content"]
            st.dataframe(posts_df[display_cols].head(100), height=300)
            st.caption(f"Displaying top {min(100, len(posts_df))} of {len(posts_df):,} matching observations.")

    # -------------------------------------------------------------------------
    # TAB 2: LIVE NLP INFERENCE SANDBOX
    # -------------------------------------------------------------------------
    with tab_inference:
        st.markdown(
            """
            <div style="margin: 0.5rem 0 0.8rem 0;">
                <h3 style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin: 0;">
                    Dual-Head NLP Semantic Prediction Sandbox
                </h3>
                <p style="font-size: 0.84rem; color: #64748B; margin: 0.2rem 0 0 0;">
                    Evaluate arbitrary text against canonical Round 2 models. Features true calibrated probabilities for Logistic Regression and signed margin distances for Linear SVM.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        def set_preset_text(t: str):
            st.session_state["p3_nlp_input"] = t

        if "p3_nlp_input" not in st.session_state:
            st.session_state["p3_nlp_input"] = PRESET_EXAMPLES[0]["text"]

        st.markdown("<p style='font-size: 0.78rem; font-weight: 600; text-transform: uppercase; color: #64748B; margin-bottom: 0.3rem;'>Quick Domain Presets:</p>", unsafe_allow_html=True)
        preset_cols = st.columns(4)
        for i, p in enumerate(PRESET_EXAMPLES):
            with preset_cols[i]:
                st.button(
                    p["name"],
                    key=f"p3_preset_{i}",
                    on_click=set_preset_text,
                    args=(p["text"],),
                    use_container_width=True,
                )

        input_text = st.text_area(
            "Input text for real-time semantic analysis:",
            height=90,
            key="p3_nlp_input",
            help="Type custom text or click any domain preset above to analyze sentiment and topic intent.",
        )

        if input_text.strip():
            try:
                res = predict_dual_head(input_text)
                sent_res = res["sentiment"]
                topic_res = res["topic"]

                res1, res2 = st.columns(2)
                with res1:
                    s_color = SENTIMENT_COLORS.get(sent_res["label"], "#1E3A8A")
                    st.markdown(
                        f"""
                        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 3px solid {s_color}; border-radius: 6px; padding: 14px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                            <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #64748B;">Predicted Sentiment</div>
                            <div style="font-size: 1.45rem; font-weight: 700; color: {s_color}; margin: 2px 0 6px 0; font-family: 'Outfit', sans-serif;">
                                {sent_res["label"]}
                            </div>
                            <div style="font-size: 0.8rem; color: #475569; margin-bottom: 8px;">
                                Posterior Probability: <strong>{format_percent(sent_res["confidence"])}</strong>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.caption("Calibrated Posterior Probabilities (Sums to 1.0):")
                    for cls_name, prob in sent_res["probabilities"].items():
                        st.progress(prob, text=f"{cls_name}: {format_percent(prob)}")

                with res2:
                    t_color = TOPIC_COLORS.get(topic_res["label"], "#0D9488")
                    winning_margin = topic_res["margins"].get(topic_res["label"], 0.0)
                    winning_softmax = topic_res["softmax_scores"].get(topic_res["label"], topic_res["confidence"])
                    st.markdown(
                        f"""
                        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 3px solid {t_color}; border-radius: 6px; padding: 14px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                            <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #64748B;">Predicted Topic Category</div>
                            <div style="font-size: 1.45rem; font-weight: 700; color: {t_color}; margin: 2px 0 6px 0; font-family: 'Outfit', sans-serif;">
                                {topic_res["label"]}
                            </div>
                            <div style="font-size: 0.8rem; color: #475569; margin-bottom: 8px;">
                                Winning Margin: <strong>{winning_margin:+.3f}</strong> • Softmax Score: <strong>{winning_softmax:.1%}</strong>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.caption("Linear SVM Signed Margin Distances (decision_function):")
                    for cls_name, margin in topic_res["margins"].items():
                        sign = "+" if margin > 0 else ""
                        st.text(f"• {cls_name}: {sign}{margin:.3f}")

                st.caption(f"ℹ️ {res['disclaimer']}")

            except Exception as e:
                st.error(f"Inference execution failed: {str(e)}")
        else:
            st.info("Enter text above or click a domain preset to generate real-time sentiment and topic predictions.")


if __name__ == "__main__":
    render()
