"""
views/auth.py
-------------
Sign-In / Sign-Up page backed by SQLite + bcrypt.
Users are persisted across sessions and server restarts.
"""

import streamlit as st
import re
from database.models import (
    create_user,
    get_user_by_email,
    verify_password,
    get_user_recommendations,
)


# ── Helper: lock banner shown on protected pages ────────────────────────────
def require_login(feature_name: str = "this feature") -> bool:
    """
    Call at the top of any protected page.
    Returns True if logged in, False (and renders a redirect banner) if not.
    """
    if st.session_state.get("auth_user"):
        return True

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(239,68,68,0.06));
        border: 1px solid rgba(239,68,68,0.3);
        border-radius: 16px;
        padding: 40px 32px;
        text-align: center;
        margin: 48px auto;
        max-width: 520px;
    ">
        <div style="font-size:2.5rem; margin-bottom:12px;">🔒</div>
        <h2 style="color:#f87171; font-size:1.6rem; margin-bottom:8px;">Sign In Required</h2>
        <p style="color:#94a3b8; font-size:1rem; line-height:1.6; margin-bottom:24px;">
            You need to be signed in to access <strong style="color:#e2e8f0;">{feature_name}</strong>.
            <br>Create a free account — it takes less than a minute!
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Go to Sign In / Sign Up", use_container_width=True, key="auth_redirect_btn"):
            st.session_state.page = "Account"
            st.rerun()

    return False


# ── Main render ─────────────────────────────────────────────────────────────
def render():
    """Render the Sign In / Sign Up page."""

    if "auth_user" not in st.session_state:
        st.session_state.auth_user = None

    if st.session_state.auth_user:
        _render_profile()
        return

    # ── Header ──
    st.markdown("""
    <div class="page-header">
        <div class="badge badge-accent">Account</div>
        <h1 class="hero-title" style="font-size:2.4rem !important; margin-top:12px;">
            Welcome to Talent Map
        </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; max-width:500px; margin:0 auto 32px auto;">
        <p class="hero-subtitle" style="margin:0 auto;">
            Sign in to save your career recommendations and access all features,
            or create a free account in seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Centered container ──
    _, center, _ = st.columns([1, 2, 1])

    with center:
        tab_signin, tab_signup = st.tabs(["🔑  Sign In", "✨  Sign Up"])

        # ──────── SIGN IN ────────
        with tab_signin:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            with st.form("signin_form"):
                email = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")

                if st.form_submit_button("Sign In →", use_container_width=True):
                    if not email.strip() or not password.strip():
                        st.error("Please fill in all fields.")
                    else:
                        user = get_user_by_email(email.strip())
                        if user is None:
                            st.error("No account found with this email. Please sign up first.")
                        elif not verify_password(password, user["password_hash"]):
                            st.error("Incorrect password. Please try again.")
                        else:
                            st.session_state.auth_user = {
                                "id":    user["id"],
                                "name":  user["name"],
                                "email": user["email"],
                            }
                            st.success(f"Welcome back, {user['name']}! 🎉")
                            st.balloons()
                            st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        # ──────── SIGN UP ────────
        with tab_signup:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            with st.form("signup_form"):
                full_name  = st.text_input("Full Name", placeholder="Jane Doe")
                email_su   = st.text_input("Email", placeholder="you@example.com", key="signup_email")
                password_su = st.text_input("Password", type="password",
                                            placeholder="Min. 6 characters", key="signup_pass")
                confirm_pw  = st.text_input("Confirm Password", type="password",
                                            placeholder="Repeat password")

                if st.form_submit_button("Create Account →", use_container_width=True):
                    errors = []
                    if not full_name.strip():
                        errors.append("Full name is required.")
                    if not email_su.strip():
                        errors.append("Email is required.")
                    elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email_su):
                        errors.append("Please enter a valid email address.")
                    if len(password_su) < 6:
                        errors.append("Password must be at least 6 characters.")
                    if password_su != confirm_pw:
                        errors.append("Passwords do not match.")

                    if errors:
                        for e in errors:
                            st.error(e)
                    else:
                        new_user = create_user(full_name.strip(), email_su.strip(), password_su)
                        if new_user is None:
                            st.error("An account with this email already exists. Please sign in.")
                        else:
                            st.session_state.auth_user = new_user
                            st.success("Account created successfully! Welcome aboard 🚀")
                            st.balloons()
                            st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)


# ── Profile page ─────────────────────────────────────────────────────────────
def _render_profile():
    """Show the profile card and recent recommendations for logged-in users."""

    user = st.session_state.auth_user

    st.markdown("""
    <div class="page-header">
        <div class="badge badge-accent">Signed In</div>
        <h1 class="hero-title" style="font-size:2.4rem !important; margin-top:12px;">
            Your Profile
        </h1>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_gap, col_right = st.columns([2, 0.2, 3])

    with col_left:
        initials = "".join([w[0].upper() for w in user["name"].split()[:2]])
        st.markdown(f"""
        <div class="best-match" style="margin-top:20px; text-align:center;">
            <div style="width:72px; height:72px; border-radius:20px;
                        background:linear-gradient(135deg,rgba(56,189,248,0.15),rgba(96,165,250,0.1));
                        border:2px solid rgba(56,189,248,0.25);
                        display:flex; align-items:center; justify-content:center;
                        margin:0 auto 16px auto; font-size:1.4rem; font-weight:800; color:#38bdf8;">
                {initials}
            </div>
            <h2 style="margin-bottom:4px;">{user["name"]}</h2>
            <p style="color:#64748b; font-size:0.95rem; margin:0 0 20px 0;">{user["email"]}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Sign Out", use_container_width=True):
            st.session_state.auth_user = None
            st.rerun()

    with col_right:
        st.markdown("""
        <h3 style="font-size:1.1rem !important; margin-bottom:16px;">
            Recent Career Recommendations
        </h3>
        """, unsafe_allow_html=True)

        history = get_user_recommendations(user["id"], limit=5)

        if not history:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:28px 16px;">
                <p style="color:#64748b; font-size:0.9rem;">
                    No recommendations yet.<br>
                    Head to <strong>Recommend</strong> to get started!
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for rec in history:
                pct = round(rec["top_score"] * 100, 1)
                st.markdown(f"""
                <div class="result-card" style="margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <strong style="color:#e2e8f0; font-size:0.95rem;">{rec["top_career"]}</strong>
                        <span style="color:#38bdf8; font-weight:700;">{pct}%</span>
                    </div>
                    <div style="display:flex; justify-content:space-between;">
                        <span style="font-size:0.78rem; color:#64748b;">{rec["best_domain"]}</span>
                        <span style="font-size:0.75rem; color:#64748b;">{rec["created_at"][:10]}</span>
                    </div>
                    <div class="score-bar-bg" style="margin-top:8px;">
                        <div class="score-bar-fill" style="width:{pct}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
