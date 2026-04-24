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
                    if _send_email(name, email, subject, message):
                        st.success("✅ Message sent successfully! We'll get back to you soon.")
                        st.balloons()
                    else:
                        st.error("❌ Failed to send message. Please try again later.")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_info:
        st.markdown("""
        <div class="info-card">
            <h3>Contact Info</h3>
            <div style="margin-bottom:16px;">
                <span class="info-label">Email</span>
                <span class="info-value">asthashukla2102@gmail.com</span>
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


def _send_email(name: str, sender_email: str, subject: str, message: str) -> bool:
    """Send contact form email via Gmail SMTP. Returns True on success."""
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    try:
        cfg = st.secrets["email"]
        smtp_user = cfg["sender_email"]
        smtp_pass = cfg["sender_password"]
        receiver  = cfg["receiver_email"]
    except Exception:
        st.warning("⚠️ Email config missing. Please add your Gmail App Password to `.streamlit/secrets.toml`.")
        return False

    # Build a nice HTML email
    html_body = f"""
    <html><body style="font-family:Arial,sans-serif; color:#1e293b;">
      <h2 style="color:#0f172a;">📬 New Contact Form Submission — Talent Map</h2>
      <table style="border-collapse:collapse; width:100%; max-width:600px;">
        <tr>
          <td style="padding:8px 12px; font-weight:bold; background:#f1f5f9; width:120px;">Name</td>
          <td style="padding:8px 12px; border-bottom:1px solid #e2e8f0;">{name}</td>
        </tr>
        <tr>
          <td style="padding:8px 12px; font-weight:bold; background:#f1f5f9;">Email</td>
          <td style="padding:8px 12px; border-bottom:1px solid #e2e8f0;">{sender_email}</td>
        </tr>
        <tr>
          <td style="padding:8px 12px; font-weight:bold; background:#f1f5f9;">Subject</td>
          <td style="padding:8px 12px; border-bottom:1px solid #e2e8f0;">{subject}</td>
        </tr>
        <tr>
          <td style="padding:8px 12px; font-weight:bold; background:#f1f5f9; vertical-align:top;">Message</td>
          <td style="padding:8px 12px; white-space:pre-wrap;">{message}</td>
        </tr>
      </table>
      <hr style="margin-top:24px; border:none; border-top:1px solid #e2e8f0;">
      <p style="font-size:12px; color:#94a3b8;">
        This email was sent automatically from the Talent Map Contact Form.
      </p>
    </body></html>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"]  = f"[Talent Map] {subject} — from {name}"
        msg["From"]     = smtp_user
        msg["To"]       = receiver
        msg["Reply-To"] = sender_email
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, receiver, msg.as_string())
        return True

    except smtplib.SMTPAuthenticationError:
        st.error("🔐 Gmail authentication failed. Check your App Password in secrets.toml.")
        return False
    except Exception as exc:
        st.error(f"Email sending error: {exc}")
        return False
