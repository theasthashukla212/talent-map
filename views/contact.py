import streamlit as st
import re


def render():
    """Render the Contact page."""

    st.markdown("""
    <div class="page-header">
        <div class="badge badge-accent">Get In Touch</div>
        <h1 class="hero-title" style="font-size:2.4rem !important; margin-top:12px;">
            Contact Us
        </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; max-width:600px; margin:0 auto 36px auto;">
        <p class="hero-subtitle" style="margin:0 auto;">
            Have a question, suggestion, or just want to say hello? Fill out the form
            below and we'll get back to you.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Layout: Form + Info ──
    col_form, col_gap, col_info = st.columns([3, 0.3, 1.5])

    with col_form:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Full Name", placeholder="Enter your name")
            email = st.text_input("Email Address", placeholder="you@example.com")
            subject = st.selectbox("Subject", [
                "General Inquiry",
                "Career Recommendation Issue",
                "Feature Request",
                "Bug Report",
                "Partnership / Collaboration",
                "Other",
            ])
            message = st.text_area(
                "Message",
                placeholder="Type your message here…",
                height=150,
            )

            submitted = st.form_submit_button(
                "Send Message", use_container_width=True
            )

            if submitted:
                errors = []
                if not name.strip():
                    errors.append("Name is required.")
                if not email.strip():
                    errors.append("Email is required.")
                elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                    errors.append("Please enter a valid email address.")
                if not message.strip():
                    errors.append("Message cannot be empty.")

                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    # Store in session_state for demo purposes
                    if "contact_messages" not in st.session_state:
                        st.session_state.contact_messages = []
                    st.session_state.contact_messages.append({
                        "name": name,
                        "email": email,
                        "subject": subject,
                        "message": message,
                    })
                    st.success("Message sent successfully! We'll get back to you soon.")
                    st.balloons()

        st.markdown('</div>', unsafe_allow_html=True)

    with col_info:
        st.markdown("""
        <div class="info-card">
            <h3>Contact Info</h3>
            <div style="margin-bottom:16px;">
                <span class="info-label">Email</span>
                <span class="info-value">talentmap@university.edu</span>
            </div>
            <div style="margin-bottom:16px;">
                <span class="info-label">Location</span>
                <span class="info-value">MCA Department<br>University Campus</span>
            </div>
            <div>
                <span class="info-label">Hours</span>
                <span class="info-value">Mon – Fri: 9 AM – 5 PM</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card">
            <h3>Useful Links</h3>
            <p style="font-size:0.9rem; line-height:2.2;">
                <a href="https://www.onetonline.org/" target="_blank"
                   style="color:#38bdf8; text-decoration:none; font-weight:500;">O*NET Online →</a><br>
                <a href="https://github.com" target="_blank"
                   style="color:#38bdf8; text-decoration:none; font-weight:500;">GitHub Repo →</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
