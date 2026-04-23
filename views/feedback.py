import streamlit as st
from datetime import datetime


def render():
    """Render the Feedback page."""

    st.markdown("""
    <div class="page-header">
        <div class="badge badge-accent">Your Opinion Matters</div>
        <h1 class="hero-title" style="font-size:2.4rem !important; margin-top:12px;">
            Feedback
        </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; max-width:600px; margin:0 auto 36px auto;">
        <p class="hero-subtitle" style="margin:0 auto;">
            Help us improve Talent Map! Rate your experience and share your thoughts.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Initialize feedback storage ──
    if "feedback_entries" not in st.session_state:
        st.session_state.feedback_entries = []

    # ── Feedback Form ──
    col_form, col_gap, col_history = st.columns([3, 0.3, 2])

    with col_form:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        with st.form("feedback_form", clear_on_submit=True):
            # Star Rating
            st.markdown(
                '<p style="color:#e2e8f0; font-weight:600; margin-bottom:4px;">Rate Your Experience</p>',
                unsafe_allow_html=True,
            )
            rating = st.radio(
                "Rating",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: "★" * x + "☆" * (5 - x),
                horizontal=True,
                label_visibility="collapsed",
            )

            # Category
            category = st.selectbox("Category", [
                "UI / UX Design",
                "Career Recommendations",
                "Data Accuracy",
                "Performance / Speed",
                "Feature Request",
                "Other",
            ])

            # Name (optional)
            name = st.text_input(
                "Your Name (optional)",
                placeholder="Anonymous",
            )

            # Detailed Feedback
            comments = st.text_area(
                "Your Feedback",
                placeholder="Tell us what you liked, disliked, or what we can improve…",
                height=140,
            )

            submitted = st.form_submit_button(
                "Submit Feedback", use_container_width=True
            )

            if submitted:
                if not comments.strip():
                    st.error("Please write some feedback before submitting.")
                else:
                    entry = {
                        "name": name.strip() or "Anonymous",
                        "rating": rating,
                        "category": category,
                        "comments": comments.strip(),
                        "time": datetime.now().strftime("%b %d, %Y — %I:%M %p"),
                    }
                    st.session_state.feedback_entries.insert(0, entry)
                    st.success("Thank you for your feedback!")
                    st.balloons()

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Recent Feedback ──
    with col_history:
        st.markdown("""
        <div class="glass-card" style="margin-bottom:16px;">
            <h3 style="font-size:1.1rem !important; margin-bottom:4px;">Recent Feedback</h3>
            <p style="font-size:0.8rem; color:#64748b;">Showing latest entries</p>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.feedback_entries:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:36px 16px;">
                <div style="width:48px; height:48px; border-radius:14px;
                            background:linear-gradient(135deg, rgba(99,102,241,0.15), rgba(0,212,255,0.1));
                            display:flex; align-items:center; justify-content:center;
                            margin:0 auto 12px auto; font-size:1.2rem;">
                    ◇
                </div>
                <p style="color:#64748b; font-size:0.88rem;">No feedback yet.<br>Be the first!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for entry in st.session_state.feedback_entries[:5]:
                stars = "★" * entry["rating"] + "☆" * (5 - entry["rating"])
                st.markdown(f"""
                <div class="feedback-entry">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <strong style="color:#e2e8f0; font-size:0.92rem;">{entry["name"]}</strong>
                        <span style="font-size:0.75rem; color:#64748b;">{entry["time"]}</span>
                    </div>
                    <div style="margin-bottom:6px; color:#38bdf8; font-size:0.85rem; letter-spacing:2px;">{stars}</div>
                    <span class="badge badge-accent" style="margin-bottom:8px;">{entry["category"]}</span>
                    <p style="font-size:0.85rem; color:#64748b; margin-top:8px; line-height:1.5;">
                        {entry["comments"][:200]}{"…" if len(entry["comments"]) > 200 else ""}
                    </p>
                </div>
                """, unsafe_allow_html=True)
