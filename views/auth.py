import streamlit as st
import re


def render():
    """Render the Sign In / Sign Up page."""

    # ── Init session state ──
    if "auth_user" not in st.session_state:
        st.session_state.auth_user = None
    if "registered_users" not in st.session_state:
        st.session_state.registered_users = {}  # email -> {name, password}

    # ── If already logged in ──
    if st.session_state.auth_user:
        _render_profile()
        return

    # ── Header ──
    st.markdown("""
    <div class="page-header">
        <div class="badge badge-accent">Account</div>
        <h1 class="hero-title" style="font-size:2.4rem !important; margin-top:12px;">
            Welcome Back
        </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; max-width:500px; margin:0 auto 32px auto;">
        <p class="hero-subtitle" style="margin:0 auto;">
            Sign in to save your career recommendations or create a new account.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Centered container ──
    _, center, _ = st.columns([1, 2, 1])

    with center:
        tab_signin, tab_signup = st.tabs(["Sign In", "Sign Up"])

        # ──────── SIGN IN ────────
        with tab_signin:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            with st.form("signin_form"):
                email = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                remember = st.checkbox("Remember me")

                if st.form_submit_button("Sign In", use_container_width=True):
                    if not email.strip() or not password.strip():
                        st.error("Please fill in all fields.")
                    elif email not in st.session_state.registered_users:
                        st.error("No account found with this email. Please sign up first.")
                    elif st.session_state.registered_users[email]["password"] != password:
                        st.error("Incorrect password. Please try again.")
                    else:
                        user_data = st.session_state.registered_users[email]
                        st.session_state.auth_user = {
                            "name": user_data["name"],
                            "email": email,
                        }
                        st.success(f"Welcome back, {user_data['name']}!")
                        st.balloons()
                        st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        # ──────── SIGN UP ────────
        with tab_signup:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            with st.form("signup_form"):
                full_name = st.text_input("Full Name", placeholder="John Doe")
                email_su = st.text_input("Email", placeholder="you@example.com", key="signup_email")
                password_su = st.text_input("Password", type="password", placeholder="••••••••", key="signup_pass")
                confirm_pw = st.text_input("Confirm Password", type="password", placeholder="••••••••")

                if st.form_submit_button("Create Account", use_container_width=True):
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
                    if email_su in st.session_state.registered_users:
                        errors.append("An account with this email already exists.")

                    if errors:
                        for e in errors:
                            st.error(e)
                    else:
                        st.session_state.registered_users[email_su] = {
                            "name": full_name.strip(),
                            "password": password_su,
                        }
                        st.session_state.auth_user = {
                            "name": full_name.strip(),
                            "email": email_su,
                        }
                        st.success("Account created successfully!")
                        st.balloons()
                        st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)


def _render_profile():
    """Show a simple profile card for logged-in users."""

    user = st.session_state.auth_user

    st.markdown("""
    <div class="page-header">
        <div class="badge badge-accent">Signed In</div>
        <h1 class="hero-title" style="font-size:2.4rem !important; margin-top:12px;">
            Your Profile
        </h1>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 2, 1])
    with center:
        initials = "".join([w[0].upper() for w in user["name"].split()[:2]])
        st.markdown(f"""
        <div class="best-match" style="margin-top:20px;">
            <div class="team-avatar" style="width:72px; height:72px; border-radius:20px;
                        font-size:1.4rem; font-weight:800; color:#38bdf8;
                        margin:0 auto 16px auto;">
                {initials}
            </div>
            <h2 style="margin-bottom:4px;">{user["name"]}</h2>
            <p style="color:#64748b; font-size:0.95rem;">{user["email"]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Sign Out", use_container_width=True):
            st.session_state.auth_user = None
            st.rerun()
