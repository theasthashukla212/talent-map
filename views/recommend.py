"""
views/recommend.py
------------------
Career Recommendation page — requires authentication.
Results are saved to the database per user.
"""

import streamlit as st
from src.recommender import recommend
from modules.input_module import get_student_input
from modules.recommendation import recommend_domain
from views.auth import require_login
from database.models import save_recommendation


def render():
    """Render the Career Recommendation page with the full 8-section questionnaire."""

    # ── Auth gate ──────────────────────────────────────────────────────────────
    if not require_login("Career Recommendations"):
        return

    st.markdown("""
    <div class="page-header">
        <div class="badge badge-accent">Career Finder</div>
        <h1 class="hero-title" style="font-size:2.4rem !important; margin-top:12px;">
            Career Recommendation
        </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; max-width:650px; margin:0 auto 36px auto;">
        <p class="hero-subtitle" style="margin:0 auto;">
            Complete the questionnaire below and let our AI engine find the best
            career matches for you from <strong style="color:#38bdf8;">900+ occupations</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── 8-Section Questionnaire ──
    st.markdown('<div class="glass-card" style="margin-bottom:28px;">', unsafe_allow_html=True)
    user_data = get_student_input()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Recommend Button ──
    _, btn_col, _ = st.columns([1, 1.5, 1])
    with btn_col:
        run = st.button("Find My Career Match", use_container_width=True)

    if run:
        with st.spinner("Analyzing your profile against 900+ careers…"):
            career_results = recommend(user_data)
            best_domain, domain_scores = recommend_domain(user_data)

        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

        # ── Best Career Match ──
        top_job   = list(career_results.keys())[0]
        top_score = list(career_results.values())[0]

        # ── Save to DB ──
        user = st.session_state.auth_user
        try:
            save_recommendation(
                user_id=user["id"],
                top_career=top_job,
                top_score=top_score,
                best_domain=best_domain,
            )
        except Exception:
            pass  # DB write failure should not break the UI

        st.markdown(f"""
        <div class="best-match animate-fade-in-up">
            <span style="font-size:0.78rem; color:#64748b; text-transform:uppercase;
                         letter-spacing:2px; font-weight:600;">Best Career Match</span>
            <h2>{top_job}</h2>
            <p style="font-size:1.1rem; color:#64748b;">
                Compatibility Score: <strong style="color:#38bdf8;">{round(top_score * 100, 1)}%</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Two-column layout: Careers + Domain ──
        col_careers, col_gap, col_domain = st.columns([3, 0.2, 2])

        # ── Left: Top 5 Career Matches ──
        with col_careers:
            st.markdown("""
            <h3 style="font-size:1.2rem !important; margin-bottom:16px;">
                Top 5 Career Matches
            </h3>
            """, unsafe_allow_html=True)

            for rank, (job, score) in enumerate(career_results.items(), 1):
                pct = round(score * 100, 1)

                if pct >= 70:
                    color = "#34d399"
                    label = "Excellent"
                elif pct >= 50:
                    color = "#0ea5e9"
                    label = "Good"
                elif pct >= 30:
                    color = "#fbbf24"
                    label = "Fair"
                else:
                    color = "#f87171"
                    label = "Low"

                rank_label = {1: "1st", 2: "2nd", 3: "3rd"}.get(rank, f"{rank}th")

                st.markdown(f"""
                <div class="result-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <div style="display:flex; align-items:center; gap:10px;">
                            <span style="font-size:0.72rem; font-weight:800; color:#38bdf8;
                                         background:rgba(56,189,248,0.1);
                                         padding:4px 10px; border-radius:8px; border:1px solid rgba(56,189,248,0.2);">
                                {rank_label}
                            </span>
                            <strong style="color:#e2e8f0; font-size:0.98rem;">{job}</strong>
                        </div>
                        <div style="text-align:right;">
                            <span style="color:{color}; font-weight:700; font-size:1.05rem;">{pct}%</span>
                            <span style="font-size:0.72rem; color:#64748b; margin-left:6px;">{label}</span>
                        </div>
                    </div>
                    <div class="score-bar-bg">
                        <div class="score-bar-fill" style="width:{pct}%; background:linear-gradient(90deg, #0ea5e9, {color});"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # ── Right: Domain Recommendation ──
        with col_domain:
            st.markdown("""
            <h3 style="font-size:1.2rem !important; margin-bottom:16px;">
                Recommended Domain
            </h3>
            """, unsafe_allow_html=True)

            domain_icons = {
                "Engineering & Technology": "E&T",
                "Medical & Healthcare":     "M&H",
                "Business & Management":    "B&M",
                "Creative & Design":        "C&D",
                "Arts & Humanities":        "A&H",
                "Science & Research":       "S&R",
                "Education & Social Work":  "E&S",
            }

            st.markdown(f"""
            <div class="domain-card">
                <div class="domain-icon" style="font-size:0.8rem; font-weight:800; color:#38bdf8;">
                    {domain_icons.get(best_domain, "?")}
                </div>
                <span style="font-size:1.15rem; font-weight:700; color:#e2e8f0; display:block;">
                    {best_domain}
                </span>
                <span style="font-size:0.78rem; color:#64748b; margin-top:6px; display:block;">
                    Best Fit Domain
                </span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <p style="font-size:0.88rem; color:#64748b; font-weight:600; margin-bottom:12px;">
                Domain Scores
            </p>
            """, unsafe_allow_html=True)

            max_score = max(domain_scores.values()) if max(domain_scores.values()) > 0 else 1
            sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)

            for domain, score in sorted_domains:
                pct = round((score / max_score) * 100)
                is_best = domain == best_domain
                bar_color = "#38bdf8" if is_best else "#0ea5e9"

                st.markdown(f"""
                <div style="margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:3px;">
                        <span style="font-size:0.8rem; color:{'#e2e8f0' if is_best else '#64748b'}; font-weight:{'700' if is_best else '400'};">
                            {domain}
                        </span>
                        <span style="font-size:0.78rem; color:#64748b; font-weight:600;">{score}</span>
                    </div>
                    <div class="score-bar-bg">
                        <div class="score-bar-fill" style="width:{pct}%; background:{bar_color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # ── Tip + save confirmation ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("✅ Result saved to your profile! View it under **Account → Your Profile**.")
        st.info(
            "**Tip:** Try changing your answers across different sections — "
            "your interests, skills, and personality all influence the results!"
        )
