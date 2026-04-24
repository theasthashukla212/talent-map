import streamlit as st
from views.auth import require_login

# ── System prompt that defines the chatbot personality ──
SYSTEM_PROMPT = """You are an Intelligent Career Guidance Assistant inside a web app called "Talent Map".

Your personality is:
- Friendly, supportive, and motivating
- Clear and simple (avoid complex jargon)
- Slightly futuristic and uplifting (anti-gravity vibe — light, positive, forward-thinking)
- Never robotic or overly formal

Your role is to:
- Help users explore career options
- Suggest skills, tools, and learning paths
- Explain career roles in simple language
- Guide users based on their interests, strengths, and goals
- Encourage confidence and growth

Behavior rules:
- Always give structured answers (use bullet points when helpful)
- Keep responses concise but useful
- If the user is confused, guide them step-by-step
- If unsure, ask clarifying questions instead of guessing
- Do NOT give irrelevant or off-topic answers
- Stay STRICTLY focused on career guidance only

If a user asks about a career, always explain:
  - What the role is (1–2 lines)
  - Required skills
  - Tools/technologies to learn
  - How to start (step-by-step roadmap)

If a user asks "what should I do?":
  → Ask 2–3 quick questions about their interests, skills, and goals, then suggest options.

Tone examples to use naturally:
- "Let's map this out 🚀"
- "You're closer than you think"
- "Here's your launch plan"
- "Great question! Let's explore this together."

You are part of a student career app, so keep guidance practical and realistic for beginners.

Avoid:
- Negative or discouraging language
- Overly long paragraphs
- Complex technical explanations unless asked
- Off-topic or unrelated responses

End responses with a short motivating line when appropriate."""


def _get_gemini_client():
    """Initialize and return a Gemini GenerativeModel."""
    try:
        import google.generativeai as genai

        # Try multiple ways to read the key
        api_key = ""
        try:
            api_key = st.secrets["gemini"]["api_key"]
        except Exception:
            pass
        if not api_key:
            try:
                api_key = st.secrets["GEMINI_API_KEY"]
            except Exception:
                pass

        if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
            return None, "no_key"

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT,
        )
        return model, "ok"
    except ImportError:
        return None, "no_lib"
    except Exception as e:
        return None, str(e)



def _chat_with_gemini(model, history: list, user_message: str) -> str:
    """Send a message and get a response using Gemini's multi-turn chat."""
    try:
        # Build history in Gemini format
        gemini_history = []
        for msg in history[:-1]:  # exclude the latest user message
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})

        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        return f"⚠️ Something went wrong: {str(e)}"


def render():
    """Render the AI Career Chatbot page."""

    # ── Auth gate ──────────────────────────────────────────────────────────────
    if not require_login("AI Career Assistant"):
        return

    # ── Page Header ──
    st.markdown("""
    <div class="page-header">
        <div class="badge badge-accent">AI-Powered</div>
        <h1 class="hero-title" style="font-size:2.4rem !important; margin-top:12px;">
            Career Guidance Assistant
        </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; max-width:600px; margin:0 auto 28px auto;">
        <p class="hero-subtitle" style="margin:0 auto; font-size:1rem !important;">
            Ask me anything about careers, skills, roadmaps, and your future 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Chat Custom CSS ──
    st.markdown("""
    <style>
    /* Chat container */
    .chat-wrapper {
        max-width: 820px;
        margin: 0 auto;
    }

    /* Message bubbles */
    .msg-row {
        display: flex;
        align-items: flex-start;
        margin-bottom: 18px;
        animation: fadeInUp 0.35s ease-out;
    }
    .msg-row.user { flex-direction: row-reverse; }

    .avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        font-weight: 800;
        flex-shrink: 0;
    }
    .avatar-bot {
        background: rgba(56,189,248,0.15);
        border: 1px solid rgba(56,189,248,0.25);
        color: #38bdf8;
        margin-right: 12px;
    }
    .avatar-user {
        background: rgba(56,189,248,0.08);
        border: 1px solid rgba(56,189,248,0.12);
        color: #94a3b8;
        margin-left: 12px;
    }

    .bubble {
        max-width: 72%;
        padding: 14px 18px;
        border-radius: 16px;
        font-size: 0.93rem;
        line-height: 1.65;
    }
    .bubble-bot {
        background: rgba(16,24,48,0.7);
        border: 1px solid rgba(56,189,248,0.12);
        color: #e2e8f0;
        border-top-left-radius: 4px;
    }
    .bubble-user {
        background: rgba(56,189,248,0.10);
        border: 1px solid rgba(56,189,248,0.18);
        color: #e2e8f0;
        border-top-right-radius: 4px;
        text-align: right;
    }

    /* Typing indicator */
    .typing-dot {
        display: inline-block;
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #38bdf8;
        animation: typing 1.2s infinite ease-in-out;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes typing {
        0%, 80%, 100% { transform: scale(0.7); opacity: 0.4; }
        40%            { transform: scale(1.1); opacity: 1;   }
    }

    /* Suggestion chips */
    .chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 auto 20px auto; max-width: 820px; }
    .chip {
        background: rgba(56,189,248,0.07);
        border: 1px solid rgba(56,189,248,0.18);
        border-radius: 20px;
        padding: 6px 16px;
        font-size: 0.8rem;
        color: #38bdf8;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .chip:hover { background: rgba(56,189,248,0.14); }

    /* Chat area background */
    .chat-area {
        background: rgba(11,17,32,0.5);
        border: 1px solid rgba(56,189,248,0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        min-height: 380px;
        max-height: 520px;
        overflow-y: auto;
        backdrop-filter: blur(8px);
    }

    /* Fix Streamlit's chat input styling */
    .stChatInput textarea {
        background: rgba(11,17,32,0.7) !important;
        border: 1px solid rgba(56,189,248,0.2) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stChatInput textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 3px rgba(56,189,248,0.1) !important;
    }
    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] li,
    [data-testid="stChatMessageContent"] span {
        color: #e2e8f0 !important;
    }
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Initialize model ──
    model, status = _get_gemini_client()

    # ── Init session state ──
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "chat_initialized" not in st.session_state:
        st.session_state.chat_initialized = False

    # ── Welcome message (shown once) ──
    if not st.session_state.chat_initialized:
        welcome = (
            "Hey there! 👋 I'm your **Intelligent Career Guidance Assistant** — "
            "here to help you navigate your future with confidence.\n\n"
            "You can ask me things like:\n"
            "- *\"What careers suit someone who loves coding?\"*\n"
            "- *\"How do I become a Data Scientist?\"*\n"
            "- *\"I like art and technology — what should I do?\"*\n\n"
            "Let's map this out 🚀 — what's on your mind?"
        )
        st.session_state.chat_history.append({"role": "assistant", "content": welcome})
        st.session_state.chat_initialized = True

    # ── API key warning ──
    if status == "no_key":
        st.info(
            "💡 **AI not connected yet.** Add your Gemini API key to `.streamlit/secrets.toml`:\n"
            "```toml\n[gemini]\napi_key = \"YOUR_GEMINI_API_KEY\"\n```\n"
            "Get a free key at [aistudio.google.com](https://aistudio.google.com/app/apikey) — it's free!",
            icon="🔑"
        )
    elif status == "no_lib":
        st.warning("⚠️ `google-generativeai` not installed. Run: `pip install google-generativeai`")

    # ── Quick suggestion chips ──
    suggestions = [
        "💻 Careers in Tech",
        "📊 Become a Data Scientist",
        "🎨 Creative career paths",
        "💰 Highest paying jobs",
        "🚀 I don't know what to do",
        "🧠 AI & Machine Learning",
    ]

    st.markdown('<div class="chip-row">', unsafe_allow_html=True)
    chip_cols = st.columns(len(suggestions))
    for i, (col, chip) in enumerate(zip(chip_cols, suggestions)):
        with col:
            if st.button(chip, key=f"chip_{i}", use_container_width=True):
                # Extract clean text from chip (remove emoji prefix)
                clean = chip.split(" ", 1)[1] if " " in chip else chip
                st.session_state.chat_history.append({"role": "user", "content": clean})
                if model:
                    with st.spinner("Thinking..."):
                        reply = _chat_with_gemini(model, st.session_state.chat_history, clean)
                else:
                    reply = _demo_response(clean)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Chat Messages Display ──
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "assistant":
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("user", avatar="👤"):
                    st.markdown(msg["content"])

    # ── Chat Input ──
    user_input = st.chat_input("Ask me about any career, skill, or your future... 🚀")

    if user_input and user_input.strip():
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Get AI response
        if model:
            with st.spinner(""):
                reply = _chat_with_gemini(model, st.session_state.chat_history, user_input)
        else:
            reply = _demo_response(user_input)

        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    # ── Bottom toolbar (Clear + Stats) ──
    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_l:
        msg_count = len([m for m in st.session_state.chat_history if m["role"] == "user"])
        st.markdown(
            f'<p style="color:#64748b; font-size:0.8rem; margin:8px 0 0 0;">💬 {msg_count} message{"s" if msg_count != 1 else ""}</p>',
            unsafe_allow_html=True
        )
    with col_r:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.chat_initialized = False
            st.rerun()


def _demo_response(user_input: str) -> str:
    """Fallback demo response when Gemini API is not configured."""
    user_lower = user_input.lower()

    if any(w in user_lower for w in ["data", "data science", "analyst"]):
        return (
            "**Data Science** is a fantastic path! 📊\n\n"
            "**What the role is:**\nData Scientists extract insights from large datasets to help organizations make smarter decisions.\n\n"
            "**Skills Required:**\n"
            "- Statistics & Mathematics\n- Python or R programming\n- Data visualization\n- Machine Learning basics\n\n"
            "**Tools to Learn:**\n"
            "- Python (pandas, NumPy, matplotlib)\n- Jupyter Notebooks\n- SQL\n- Tableau / Power BI\n\n"
            "**Your Roadmap:**\n"
            "1. Learn Python basics (2–3 months)\n"
            "2. Study statistics & probability\n"
            "3. Practice on Kaggle datasets\n"
            "4. Build 2–3 portfolio projects\n"
            "5. Apply for internships!\n\n"
            "You're closer than you think — every expert started exactly where you are now. 🚀"
        )
    elif any(w in user_lower for w in ["web", "developer", "frontend", "backend", "coding", "tech"]):
        return (
            "**Web Development** is one of the most in-demand careers right now! 💻\n\n"
            "**What the role is:**\nWeb Developers build websites and web applications that people use every day.\n\n"
            "**Skills Required:**\n"
            "- HTML, CSS, JavaScript (Frontend)\n- Python/Node.js (Backend)\n- Database basics (SQL)\n- Version control (Git)\n\n"
            "**Tools to Learn:**\n"
            "- VS Code, GitHub\n- React.js or Vue.js (frontend)\n- Django or Node.js (backend)\n\n"
            "**Your Roadmap:**\n"
            "1. Master HTML + CSS (1 month)\n"
            "2. Learn JavaScript deeply\n"
            "3. Pick one framework (React recommended)\n"
            "4. Build 3 real projects\n"
            "5. Deploy them on GitHub Pages / Vercel\n\n"
            "Here's your launch plan — the web is waiting for YOU! 🌐"
        )
    elif any(w in user_lower for w in ["ai", "machine learning", "ml", "artificial"]):
        return (
            "**AI & Machine Learning** — the future is literally here! 🧠\n\n"
            "**What the role is:**\nML Engineers build systems that can learn from data and make predictions or decisions automatically.\n\n"
            "**Skills Required:**\n"
            "- Python (must!)\n- Linear Algebra & Statistics\n- Machine Learning algorithms\n- Deep Learning fundamentals\n\n"
            "**Tools to Learn:**\n"
            "- scikit-learn, TensorFlow, PyTorch\n- Jupyter Notebooks\n- Hugging Face (for NLP)\n\n"
            "**Your Roadmap:**\n"
            "1. Get comfortable with Python\n"
            "2. Learn ML basics with scikit-learn\n"
            "3. Study Andrew Ng's ML course (free on Coursera)\n"
            "4. Build a cool ML project\n"
            "5. Share it on GitHub + LinkedIn\n\n"
            "You're already asking the right questions. Let's map this out! 🚀"
        )
    elif any(w in user_lower for w in ["creative", "art", "design", "ui", "ux"]):
        return (
            "**UI/UX Design** is where creativity meets technology! 🎨\n\n"
            "**What the role is:**\nUI/UX Designers craft beautiful, user-friendly digital experiences for apps and websites.\n\n"
            "**Skills Required:**\n"
            "- Visual design principles\n- User research & empathy\n- Prototyping\n- Basic HTML/CSS knowledge\n\n"
            "**Tools to Learn:**\n"
            "- Figma (essential!)\n- Adobe XD\n- Canva (beginner friendly)\n\n"
            "**Your Roadmap:**\n"
            "1. Learn Figma — it's free and powerful\n"
            "2. Study UI/UX principles on YouTube\n"
            "3. Redesign 2–3 existing apps (great practice!)\n"
            "4. Build a portfolio on Behance / Dribbble\n"
            "5. Apply for freelance gigs or internships\n\n"
            "Creativity is your superpower — now let's give it direction! ✨"
        )
    elif any(w in user_lower for w in ["don't know", "confused", "help", "what should", "not sure", "lost"]):
        return (
            "No worries at all — that's exactly why I'm here! 😊\n\n"
            "Let me help you find the right direction. Just answer these 3 quick questions:\n\n"
            "1. **What do you enjoy doing?** *(e.g., coding, designing, helping people, analyzing numbers, creating content)*\n"
            "2. **What are you good at?** *(e.g., problem-solving, communication, art, math)*\n"
            "3. **What's your goal?** *(e.g., high salary, creative work, working from home, helping others)*\n\n"
            "Once I know these, I'll suggest the **perfect career paths** just for you!\n\n"
            "You're closer than you think — one answer at a time. 🚀"
        )
    elif any(w in user_lower for w in ["salary", "highest paying", "money", "pay", "earn"]):
        return (
            "Let's talk **high-paying careers**! 💰\n\n"
            "**Top paying fields right now:**\n\n"
            "| Career | Avg. Salary (Global) |\n"
            "|---|---|\n"
            "| Machine Learning Engineer | ₹12–30 LPA |\n"
            "| Data Scientist | ₹8–25 LPA |\n"
            "| Cloud Architect | ₹15–35 LPA |\n"
            "| Full Stack Developer | ₹6–20 LPA |\n"
            "| Cybersecurity Analyst | ₹8–22 LPA |\n\n"
            "**The key to high pay:**\n"
            "- Build strong practical skills (not just theory)\n"
            "- Get certified (AWS, Google, etc.)\n"
            "- Build a solid portfolio\n"
            "- Network actively on LinkedIn\n\n"
            "Which of these excites you most? I'll give you a full roadmap! 🚀"
        )
    else:
        return (
            "Great question! I'd love to help you explore that. 🌟\n\n"
            "To give you the **best career guidance**, could you tell me:\n\n"
            "1. **What topics or activities do you enjoy?**\n"
            "2. **What skills do you already have?**\n"
            "3. **What kind of work environment do you prefer?**\n\n"
            "With these answers, I can map out the perfect career path for you!\n\n"
            "*(Tip: Add your Gemini API key in `.streamlit/secrets.toml` to unlock full AI-powered responses!)* 🔑\n\n"
            "You've got this — let's figure it out together! 🚀"
        )
