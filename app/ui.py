import streamlit as st
import pandas as pd

from .logic import get_ai_response
from .config import APP_NAME, TAGLINE, THEME, GROQ_MODEL_CANDIDATES


def _inject_css():
    st.markdown(
        f"""
        <style>
        .app-bg {{
            background: linear-gradient(180deg, {THEME['bg_light']} 0%, #e3f0ff 100%);
            position: fixed; inset: 0; z-index:-1;
        }}
        .card {{
            background: {THEME['card_bg']};
            border-radius: 16px;
            padding: 16px 18px;
            box-shadow: 0 8px 28px rgba(0,0,0,0.06);
            border: 1px solid rgba(0,0,0,0.04);
        }}
        .muted {{ color: {THEME['text_muted']}; }}
        .title {{ text-align:center; color: {THEME['primary']}; }}
        </style>
        <div class="app-bg"></div>
        """,
        unsafe_allow_html=True,
    )


def _header():
    st.markdown(f"<h1 class='title'>🕊️ {APP_NAME}</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align:center' class='muted'>{TAGLINE}</p>",
        unsafe_allow_html=True,
    )
    st.write("")


def _support_tab():
    st.subheader("Share what's on your mind")

    # Model selector (auto-fallback handled in logic)
    selected_model = st.selectbox(
        "Model (auto-fallback if unavailable):",
        GROQ_MODEL_CANDIDATES,
        index=0,
        help="If this model is unavailable, the app will automatically try other compatible models.",
    )

    # Input state
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    st.session_state.user_input = st.text_area(
        "Your private space (not saved):",
        value=st.session_state.user_input,
        height=180,
        placeholder="Type freely… nothing is stored.",
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        ask = st.button("✨ Get Support", use_container_width=True)
    with col2:
        clear = st.button("🧹 Clear", use_container_width=True)

    if clear:
        st.session_state.user_input = ""
        st.toast("Cleared ✨")  # no manual rerun needed

    if ask and st.session_state.user_input.strip():
        with st.spinner("Thinking…"):
            ok, data = get_ai_response(st.session_state.user_input, model=selected_model)

        if ok:
            st.markdown("#### 🌟 Your Suggestions")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**💡 Practical**")
                st.markdown(f"<div class='card'>{data['suggestion']}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown("**🕉️ Spiritual**")
                st.markdown(f"<div class='card'>{data['spiritual']}</div>", unsafe_allow_html=True)
            with c3:
                st.markdown("**🌱 Action**")
                st.markdown(f"<div class='card'>{data['action']}</div>", unsafe_allow_html=True)

            st.caption(f"Model used: {data.get('_model_used', selected_model)}")
        else:
            st.error(data)


def _trends_tab():
    st.subheader("Trends (Demo)")
    st.caption("Demo only: shows how a future DE pipeline could visualize anonymized themes.")
    demo = pd.DataFrame(
        {
            "theme": ["work", "family", "career", "health", "self-worth", "sleep", "study", "future"],
            "count": [42, 27, 31, 22, 19, 17, 21, 14],
        }
    )
    st.bar_chart(demo.set_index("theme"))
    st.markdown(
        """
        **Future DE idea (with user consent):**
        - Store to S3 → process with Lambda/Glue → query with Athena → visualize in QuickSight/Streamlit.
        """
    )


def render_ui():
    st.set_page_config(page_title=APP_NAME, page_icon="🕊️", layout="centered")
    _inject_css()
    _header()
    tab1, tab2 = st.tabs(["Support", "Trends (Demo)"])
    with tab1:
        _support_tab()
    with tab2:
        _trends_tab()
