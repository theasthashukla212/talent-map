import streamlit as st
from pathlib import Path

# ── Page Config (must be first Streamlit call) ──
st.set_page_config(
    page_title="Talent Map — Career Recommendation",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load Custom CSS ──
css_path = Path(__file__).parent / "styles" / "main.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# ── Page Imports ──
from views import home, about, contact, feedback, auth, recommend, chatbot  # noqa: E402

# ── Page Registry ──
PAGES = {
    "Home": home,
    "🤖 AI Assistant": chatbot,
    "Recommend": recommend,
    "About": about,
    "Contact": contact,
    "Feedback": feedback,
    "Account": auth,
}

# ── Sidebar Navigation ──
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:16px 0 24px 0;">
        <div style="width:48px; height:48px; border-radius:14px;
                    background:rgba(56,189,248,0.08);
                    border:1px solid rgba(56,189,248,0.15);
                    display:flex; align-items:center; justify-content:center;
                    margin:0 auto 10px auto;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="3 11 22 2 13 21 11 13 3 11"/>
            </svg>
        </div>
        <h1 style="font-size:1.4rem !important; margin:4px 0 2px 0;
                    background: linear-gradient(135deg, #38bdf8, #60a5fa);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;">Talent Map</h1>
        <p style="font-size:0.78rem; color:#64748b; margin:0;">AI Career Guidance</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Default page
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    st.radio(
        "Navigate",
        options=list(PAGES.keys()),
        key="page",
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Auth status in sidebar footer
    if st.session_state.get("auth_user"):
        user = st.session_state.auth_user
        initials = "".join([w[0].upper() for w in user["name"].split()[:2]])
        st.markdown(f"""
        <div style="text-align:center; padding:8px 0;">
            <div style="width:36px; height:36px; border-radius:10px;
                        background:rgba(56,189,248,0.08);
                        border:1px solid rgba(56,189,248,0.15);
                        display:flex; align-items:center; justify-content:center;
                        margin:0 auto 6px auto; font-size:0.75rem; font-weight:800; color:#38bdf8;">
                {initials}
            </div>
            <p style="color:#e2e8f0; font-size:0.88rem; font-weight:600; margin:4px 0 0 0;">
                {user["name"]}
            </p>
            <p style="color:#64748b; font-size:0.72rem; margin:0;">{user["email"]}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:8px 0;">
            <p style="color:#64748b; font-size:0.78rem;">Not signed in</p>
        </div>
        """, unsafe_allow_html=True)

# ── Render Selected Page ──
PAGES[st.session_state.page].render()