import streamlit as st


def get_student_input():
    """
    Collect student profile data through an 8-section questionnaire.
    Returns a dict with all responses keyed by section.
    """

    data = {}

    # ───────────────────────────────────────────────
    # Section 1 — Academic Background
    # ───────────────────────────────────────────────
    st.markdown("""
    <div class="q-section-header">
        <div class="q-section-num">1</div>
        <h3 class="q-section-title">Academic Background</h3>
    </div>
    <p class="q-section-desc">Your basic academic foundation</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        data["stream"] = st.selectbox(
            "What is your stream in class 12?",
            ["PCM", "PCB", "Commerce", "Arts", "Other"],
            key="q_stream",
        )

        data["fav_subjects"] = st.multiselect(
            "What subjects do you enjoy most?",
            ["Mathematics", "Biology", "Computer Science", "Economics",
             "Psychology", "Business Studies"],
            key="q_fav_subjects",
        )

    with col2:
        data["academic_strength"] = st.selectbox(
            "Your academic strength?",
            ["Theory", "Practical", "Problem Solving", "Memorization"],
            key="q_acad_strength",
        )

    st.markdown("<hr class='q-divider'>", unsafe_allow_html=True)

    # ───────────────────────────────────────────────
    # Section 2 — Interest Area
    # ───────────────────────────────────────────────
    st.markdown("""
    <div class="q-section-header">
        <div class="q-section-num">2</div>
        <h3 class="q-section-title">Interest Area</h3>
    </div>
    <p class="q-section-desc">What you like to do</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        data["activities"] = st.multiselect(
            "Which activities do you enjoy?",
            ["Coding", "Drawing / Designing", "Teaching", "Helping People",
             "Business", "Research", "Writing", "Public Speaking"],
            key="q_activities",
        )

        data["work_type"] = st.selectbox(
            "What type of work do you prefer?",
            ["Technical", "Creative", "Analytical", "Social", "Management"],
            key="q_work_type",
        )

    with col2:
        data["work_env"] = st.selectbox(
            "Work environment you like?",
            ["Office", "Field Work", "Remote Work", "Lab Work", "Startup"],
            key="q_work_env",
        )

    st.markdown("<hr class='q-divider'>", unsafe_allow_html=True)

    # ───────────────────────────────────────────────
    # Section 3 — Skills Assessment
    # ───────────────────────────────────────────────
    st.markdown("""
    <div class="q-section-header">
        <div class="q-section-num">3</div>
        <h3 class="q-section-title">Skills Assessment</h3>
    </div>
    <p class="q-section-desc">Your strongest abilities</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        data["strongest_skill"] = st.selectbox(
            "Your strongest skill?",
            ["Logical Thinking", "Communication", "Creativity",
             "Leadership", "Problem Solving", "Analytical Thinking"],
            key="q_strongest_skill",
        )

        data["tech_level"] = st.selectbox(
            "Rate your technical skills",
            ["Beginner", "Intermediate", "Advanced"],
            key="q_tech_level",
        )

    with col2:
        data["comfortable_with"] = st.multiselect(
            "Are you comfortable with:",
            ["Mathematics", "Computers", "Writing", "Public Speaking", "Team Work"],
            key="q_comfortable",
        )

    st.markdown("<hr class='q-divider'>", unsafe_allow_html=True)

    # ───────────────────────────────────────────────
    # Section 4 — Personality Type
    # ───────────────────────────────────────────────
    st.markdown("""
    <div class="q-section-header">
        <div class="q-section-num">4</div>
        <h3 class="q-section-title">Personality Type</h3>
    </div>
    <p class="q-section-desc">Helps improve recommendation accuracy</p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        data["personality"] = st.selectbox(
            "Are you more:",
            ["Introvert", "Extrovert", "Ambivert"],
            key="q_personality",
        )

    with col2:
        data["work_pref"] = st.selectbox(
            "You prefer working:",
            ["Alone", "Team", "Both"],
            key="q_work_pref",
        )

    with col3:
        data["decision_style"] = st.selectbox(
            "Decision making style:",
            ["Fast", "Analytical", "Emotional"],
            key="q_decision",
        )

    st.markdown("<hr class='q-divider'>", unsafe_allow_html=True)

    # ───────────────────────────────────────────────
    # Section 5 — Career Preference
    # ───────────────────────────────────────────────
    st.markdown("""
    <div class="q-section-header">
        <div class="q-section-num">5</div>
        <h3 class="q-section-title">Career Preference</h3>
    </div>
    <p class="q-section-desc">Understanding your direction</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        data["career_type"] = st.selectbox(
            "Preferred career type:",
            ["High Salary", "Work-Life Balance", "Creativity",
             "Stability", "Research"],
            key="q_career_type",
        )

    with col2:
        data["industry"] = st.selectbox(
            "You want to work in:",
            ["Tech Industry", "Healthcare", "Business",
             "Government", "Education"],
            key="q_industry",
        )

    st.markdown("<hr class='q-divider'>", unsafe_allow_html=True)

    # ───────────────────────────────────────────────
    # Section 6 — Knowledge Level
    # ───────────────────────────────────────────────
    st.markdown("""
    <div class="q-section-header">
        <div class="q-section-num">6</div>
        <h3 class="q-section-title">Knowledge Level</h3>
    </div>
    <p class="q-section-desc">Measure your exposure</p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        data["knows_programming"] = st.selectbox(
            "Do you know programming?",
            ["Yes", "No"],
            key="q_programming",
        )

    with col2:
        data["likes_data"] = st.selectbox(
            "Do you like data analysis?",
            ["Yes", "No"],
            key="q_data",
        )

    with col3:
        data["likes_real_problems"] = st.selectbox(
            "Enjoy solving real-world problems?",
            ["Yes", "No"],
            key="q_real_problems",
        )

    st.markdown("<hr class='q-divider'>", unsafe_allow_html=True)

    # ───────────────────────────────────────────────
    # Section 7 — Strengths
    # ───────────────────────────────────────────────
    st.markdown("""
    <div class="q-section-header">
        <div class="q-section-num">7</div>
        <h3 class="q-section-title">Strengths</h3>
    </div>
    <p class="q-section-desc">Self-evaluation of your strengths</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        data["biggest_strength"] = st.selectbox(
            "Your biggest strength:",
            ["Creativity", "Logic", "Communication", "Leadership", "Planning"],
            key="q_strength",
        )

    with col2:
        data["good_at"] = st.multiselect(
            "You are good at:",
            ["Numbers", "People", "Design", "Writing", "Technology"],
            key="q_good_at",
        )

    st.markdown("<hr class='q-divider'>", unsafe_allow_html=True)

    # ───────────────────────────────────────────────
    # Section 8 — Career Goal
    # ───────────────────────────────────────────────
    st.markdown("""
    <div class="q-section-header">
        <div class="q-section-num">8</div>
        <h3 class="q-section-title">Career Goal</h3>
    </div>
    <p class="q-section-desc">Your final direction</p>
    """, unsafe_allow_html=True)

    data["dream_career"] = st.selectbox(
        "Your dream career:",
        ["Software Engineer", "Doctor", "Data Scientist",
         "Business Owner", "Designer", "Teacher"],
        key="q_dream",
    )

    return data