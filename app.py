```python
import streamlit as st
from openai import OpenAI

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Nader AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main page */
    .stApp {
        background: #f7f9fc;
    }

    /* Header */
    .nader-header {
        text-align: center;
        padding: 25px 10px 10px 10px;
    }

    .nader-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .nader-subtitle {
        font-size: 17px;
        color: #667085;
    }

    /* Chat messages */
    .user-message {
        background: #e8f0fe;
        padding: 14px 18px;
        border-radius: 18px;
        margin: 10px 0;
        margin-left: 10%;
    }

    .ai-message {
        background: white;
        padding: 16px 20px;
        border-radius: 18px;
        margin: 10px 0;
        margin-right: 10%;
        border: 1px solid #e6e9ef;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #ffffff;
    }

    /* Buttons */
    .stButton button {
        border-radius: 10px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #98a2b3;
        font-size: 13px;
        margin-top: 30px;
        padding-bottom: 20px;
    }

</style>
""", unsafe_allow_html=True)

# =========================================================
# API CONFIGURATION
# =========================================================

# Streamlit Cloud:
# Add your key under:
#
# Settings → Secrets
#
# OPENAI_API_KEY = "your-api-key"

api_key = st.secrets.get("OPENAI_API_KEY", "")

if not api_key:
    st.error(
        "⚠️ OpenAI API key is missing.\n\n"
        "Add OPENAI_API_KEY to your Streamlit Secrets."
    )
    st.stop()

client = OpenAI(api_key=api_key)

# =========================================================
# MODEL
# =========================================================

MODEL = "gpt-5.6-luna"

# =========================================================
# NADER AI SYSTEM INSTRUCTIONS
# =========================================================

SYSTEM_PROMPT = """
You are Nader AI, a helpful, intelligent and friendly general-purpose AI assistant.

Your name is Nader AI.

You can help users with:

• General knowledge
• Mathematics
• Science
• Education
• Technology
• Programming
• History
• Geography
• Business
• Current events
• News
• Football and other sports
• Travel
• Everyday life questions
• Writing and rewriting
• Explanations and tutoring

IMPORTANT:

1. Answer naturally and conversationally.
2. Be accurate and honest.
3. Never invent facts.
4. If the user asks about current, recent, today's, latest, live, or changing information, use web search.
5. Use web search for current football news, results, fixtures, standings, transfers, injuries, current players, current political/news events, prices, weather, and other time-sensitive information.
6. When using current information, clearly distinguish current facts from general knowledge.
7. When appropriate, mention the source of important current information.
8. If the user asks a mathematical or educational question, explain it clearly step by step.
9. Adapt your explanation to the user's level.
10. Do not unnecessarily make answers complicated.
11. If the user asks for an opinion, clearly indicate that it is an opinion.
12. If you are unsure, say so instead of making something up.
13. You can answer in English or Arabic depending on the language used by the user.
14. For Lebanese Arabic questions, you may respond naturally in Lebanese Arabic when appropriate.
15. Be concise for simple questions and more detailed for complex questions.

You are not a replacement for a doctor, lawyer or financial professional. For high-stakes matters, provide general information and encourage professional advice.
"""

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "web_enabled" not in st.session_state:
    st.session_state.web_enabled = True

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🤖 Nader AI")

    st.markdown(
        "Your personal AI assistant for questions, "
        "learning, news, football and everyday life."
    )

    st.divider()

    st.markdown("### ⚙️ Settings")

    st.session_state.web_enabled = st.toggle(
        "🌐 Web Search",
        value=st.session_state.web_enabled,
        help="Use current internet information for recent questions."
    )

    st.divider()

    if st.button(
        "🗑️ New Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### 💡 Try asking")

    examples = [
        "⚽ What is the latest football news?",
        "📰 What are today's biggest news stories?",
        "📐 Explain derivatives simply.",
        "💻 Help me write Python code.",
        "🌍 What is happening in the world today?",
        "🧠 Give me a challenging math problem."
    ]

    for example in examples:
        st.caption(example)

    st.divider()

    st.caption("Nader AI")
    st.caption("Powered by OpenAI")

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="nader-header">

<div class="nader-title">
🤖 Nader AI
</div>

<div class="nader-subtitle">
Ask me anything — knowledge, education, football, news, technology and more.
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# WELCOME SCREEN
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown("### 👋 Hello!")

    st.markdown(
        """
        I'm **Nader AI**.

        You can ask me about almost anything.

        **For example:**
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "⚽ **Football**\n\n"
            "Latest news, results, transfers, players and teams."
        )

    with col2:
        st.info(
            "📰 **Current Events**\n\n"
            "Ask about recent news and what is happening now."
        )

    with col3:
        st.info(
            "📚 **Learning**\n\n"
            "Math, science, programming and explanations."
        )

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    role = message["role"]
    content = message["content"]

    if role == "user":

        st.markdown(
            f"""
            <div class="user-message">
                <strong>👤 You</strong><br><br>
                {content}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="ai-message">
                <strong>🤖 Nader AI</strong><br><br>
            """,
            unsafe_allow_html=True
        )

        st.markdown(content)

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Message Nader AI..."
)

# =========================================================
# PROCESS USER QUESTION
# =========================================================

if user_input:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare conversation
    conversation = []

    for message in st.session_state.messages:
        conversation.append(
            {
                "role": message["role"],
                "content": message["content"]
            }
        )

    # -----------------------------------------------------
    # ASK NADER AI
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Nader is thinking..."):

            try:

                # Use web search when enabled
                tools = []

                if st.session_state.web_enabled:
                    tools.append(
                        {
                            "type": "web_search"
                        }
                    )

                response = client.responses.create(
                    model=MODEL,
                    instructions=SYSTEM_PROMPT,
                    input=conversation,
                    tools=tools
                )

                answer = response.output_text

                if not answer:
                    answer = (
                        "I'm sorry, I couldn't generate an answer "
                        "right now. Please try again."
                    )

            except Exception as e:

                answer = (
                    "⚠️ I couldn't connect to the AI service.\n\n"
                    "Please check your OpenAI API key and try again.\n\n"
                    f"Technical information: `{str(e)}`"
                )

            st.markdown(answer)

    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Nader AI • AI assistant for learning, information and everyday questions
    </div>
    """,
    unsafe_allow_html=True
)
```
