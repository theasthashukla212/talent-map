import streamlit as st


def render():
    """Render the About page."""

    st.markdown("""
    <div class="page-header">
        <div class="badge badge-accent">About Us</div>
        <h1 class="hero-title" style="font-size:2.6rem !important; margin-top:12px;">
            About Talent Map
        </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; max-width:700px; margin:0 auto 40px auto;">
        <p class="hero-subtitle" style="margin:0 auto;">
            Talent Map is a career recommendation system that helps students and
            individuals discover suitable career paths based on their interests,
            skills, and academic background.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Mission ──
    st.markdown("""
    <div class="glass-card animate-fade-in-up" style="margin-bottom:32px;">
        <h2 style="font-size:1.4rem !important; margin-bottom:12px;">Our Mission</h2>
        <p style="font-size:1rem; line-height:1.8; color:#64748b;">
            Choosing a career can be overwhelming. With hundreds of possible paths and
            constantly evolving industries, students often feel lost. Talent Map bridges
            this gap by leveraging data science and occupational research to provide
            <strong style="color:#38bdf8;">personalized, evidence-based career recommendations</strong>
            — making career exploration accessible, fast, and fun.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── How It Works ──
    st.markdown("""
    <div class="section-title" style="margin-top:40px;">
        <h2>How It Works</h2>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    steps = [
        ("1", "Profile Input",
         "You select your interests, skills, and academic background through an intuitive interface."),
        ("2", "Cosine Similarity",
         "Your profile is converted into a feature vector and compared against 900+ occupation vectors."),
        ("3", "Ranked Results",
         "The top matching careers are returned, ranked by their similarity score to your profile."),
    ]
    for col, (num, title, desc) in zip([c1, c2, c3], steps):
        with col:
            st.markdown(f"""
            <div class="step-card">
                <div class="step-number">{num}</div>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # ── Technology Stack ──
    st.markdown("""
    <div class="section-title">
        <h2>Technology Stack</h2>
    </div>
    """, unsafe_allow_html=True)

    t1, t2, t3, t4 = st.columns(4)
    tech = [
        ("Py", "Python", "Core language"),
        ("Pd", "Pandas & NumPy", "Data processing"),
        ("SK", "Scikit-learn", "ML algorithms"),
        ("St", "Streamlit", "Web framework"),
    ]
    for col, (icon, name, desc) in zip([t1, t2, t3, t4], tech):
        with col:
            st.markdown(f"""
            <div class="tech-card">
                <div class="tech-icon" style="font-size:0.85rem; font-weight:800; color:#38bdf8;">{icon}</div>
                <span style="font-size:0.95rem; font-weight:700; color:#e2e8f0; display:block;">{name}</span>
                <span style="font-size:0.78rem; color:#64748b; margin-top:4px;">{desc}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # ── Data Source ──
    st.markdown("""
    <div class="glass-card" style="margin-bottom:32px;">
        <h2 style="font-size:1.4rem !important; margin-bottom:12px;">Data Source — O*NET</h2>
        <p style="font-size:0.95rem; line-height:1.8; color:#64748b;">
            Our recommendation engine is powered by the
            <strong style="color:#38bdf8;">O*NET (Occupational Information Network)</strong>
            database — the nation's primary source of occupational information.
            It provides comprehensive data on skills, knowledge areas, interests,
            and work activities for over 900 occupations.
        </p>
        <div style="margin-top:16px; display:flex; gap:10px; flex-wrap:wrap;">
            <span class="badge badge-accent">Skills Matrix</span>
            <span class="badge badge-accent">Knowledge Matrix</span>
            <span class="badge badge-accent">Interest Matrix (RIASEC)</span>
            <span class="badge badge-accent">Occupation Titles</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

   
