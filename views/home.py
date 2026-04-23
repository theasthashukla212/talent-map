import streamlit as st


def render():
    """Render the Home / Landing page."""

    # ── Hero Section ──
    st.markdown("""
    <div style="text-align:center; padding: 48px 0 24px 0;">
        <div class="badge badge-accent" style="margin-bottom:16px;">AI-Powered Career Guidance</div>
        <h1 class="hero-title">Discover Your<br>Perfect Career Path</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; max-width:650px; margin:0 auto; padding-bottom:36px;">
        <p class="hero-subtitle">
            Talent Map uses machine learning and O*NET occupational data to match your
            unique interests and skills with the careers that suit you best.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA Button ──
    col_l, col_c, col_r = st.columns([1, 1, 1])
    with col_c:
        if st.button("Get Your Career Match", use_container_width=True):
            st.session_state.page = "Recommend"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Stats ──
    s1, s2, s3, s4 = st.columns(4)
    stats = [
        ("900+", "Careers"),
        ("35+", "Skills Analyzed"),
        ("68+", "Knowledge Areas"),
        ("6", "Interest Domains"),
    ]
    for col, (num, label) in zip([s1, s2, s3, s4], stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <span class="stat-number">{num}</span>
                <span class="stat-label">{label}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # ── Features ──
    st.markdown("""
    <div class="section-title">
        <h2>Why Talent Map?</h2>
        <p>Everything you need to find the right career direction.</p>
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    features = [
        ("⚡", "AI-Powered Matching",
         "Cosine similarity algorithms match your profile against hundreds of careers with scientific precision."),
        ("📊", "O*NET Data Driven",
         "Built on the gold-standard O*NET occupational database covering skills, knowledge, and interests."),
        ("→", "Instant Results",
         "Get your top 5 career recommendations in seconds — no sign-up required."),
    ]
    for col, (icon, title, desc) in zip([f1, f2, f3], features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # ── How It Works ──
    st.markdown("""
    <div class="section-title">
        <h2>How It Works</h2>
        <p>Three simple steps to your ideal career.</p>
    </div>
    """, unsafe_allow_html=True)

    h1, h2_, h3_ = st.columns(3)
    steps = [
        ("1", "Select Your Interests",
         "Choose from categories like Technology, Biology, Business, Design, and more."),
        ("2", "Our AI Analyzes",
         "We compare your profile against 900+ occupations using cosine similarity."),
        ("3", "Get Recommendations",
         "Receive your top career matches ranked by compatibility score."),
    ]
    for col, (num, title, desc) in zip([h1, h2_, h3_], steps):
        with col:
            st.markdown(f"""
            <div class="step-card">
                <div class="step-number">{num}</div>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ── Footer CTA ──
    st.markdown("""
    <div class="footer-cta">
        <p>
            Ready to explore your future? Navigate to <strong>Recommend</strong> from the sidebar.
        </p>
    </div>
    """, unsafe_allow_html=True)
