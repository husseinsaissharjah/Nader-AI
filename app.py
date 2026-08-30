import streamlit as st
from openai import OpenAI

st.set_page_config(
page_title="Nader AI",
page_icon="🤖",
layout="wide",
initial_sidebar_state="expanded"
)

st.markdown("""

<style>
.stApp {
    background-color: #f7f9fc;
}

.nader-header {
    text-align: center;
    padding: 30px 10px 20px 10px;
}

.nader-title {
    font-size: 44px;
    font-weight: 800;
}

.nader-subtitle {
    font-size: 17px;
    color: #667085;
}

.footer {
    text-align: center;
    color: #98a2b3;
    font-size: 13px;
    margin-top: 40px;
    padding-bottom: 20px;
}

</style>

""", unsafe_allow_html=True)

# =========================================================

# OPENAI API KEY

# =========================================================

try:
api_key = st.secrets["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"]
except Exception:
api_key = ""

if not api_key:
st.error("⚠️ Nader AI is not connected to OpenAI yet.")
st.info(
"Go to your Streamlit app settings → Secrets and add:\n\n"
"OPENAI_API_KEY = "your-api-key""
)
st.stop()

client = OpenAI(api_key=api_key)

# =========================================================

# MODEL

# =========================================================

MODEL = "gpt-5.6"

# =========================================================

# NADER AI INSTRUCTIONS

# =========================================================

SYSTEM_PROMPT = """
You are Nader AI, a friendly and intelligent general-purpose AI assistant.

Your name is Nader AI.

You can help with:

* General knowledge
* Current events
* News
* Football and sports
* Mathematics
* Education
* Science
* Technology
* Programming
* History
* Geography
* Business
* Travel
* Writing
* Everyday life questions

Rules:

1. Answer naturally and conversationally.
2. Be accurate and useful.
3. Never invent facts.
4. For current or recent information, use web search when available.
5. This includes today's news, football results, transfers, fixtures,
   standings, injuries, current events, weather and current prices.
6. Explain mathematics step by step when appropriate.
7. Adapt explanations to the user's level.
8. Keep simple answers concise.
9. Give more detail when the question requires it.
10. If you don't know something, say so.
11. Answer in English or Arabic according to the user's language.
12. Lebanese Arabic can be answered naturally in Lebanese Arabic.
13. Be friendly and professional.
14. Clearly identify opinions as opinions.
15. Do not pretend old information is current.
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

```
st.markdown("## 🤖 Nader AI")

st.write(
    "Your AI assistant for knowledge, education, "
    "football, news and everyday questions."
)

st.divider()

st.markdown("### ⚙️ Settings")

st.session_state.web_enabled = st.toggle(
    "🌐 Web Search",
    value=st.session_state.web_enabled
)

st.divider()

if st.button("🗑️ New Conversation", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

st.divider()

st.markdown("### 💡 Try asking")

st.caption("⚽ What is the latest football news?")
st.caption("📰 What are today's biggest news stories?")
st.caption("📐 Explain derivatives simply.")
st.caption("💻 Help me write Python code.")
st.caption("🌍 What is happening in the world today?")
st.caption("🧠 Give me a challenging math problem.")

st.divider()

st.caption("Nader AI")
```

# =========================================================

# HEADER

# =========================================================

st.markdown("""

<div class="nader-header">

<div class="nader-title">
🤖 Nader AI
</div>

<div class="nader-subtitle">
Ask me anything — news, football, education, technology and more.
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================

# WELCOME SCREEN

# =========================================================

if len(st.session_state.messages) == 0:

```
st.markdown("### 👋 Hello!")

st.write(
    "I'm Nader AI. Ask me anything about knowledge, "
    "education, football, news, technology or everyday life."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        "⚽ Football\n\n"
        "Results, fixtures, transfers, players and teams."
    )

with col2:
    st.info(
        "📰 Current News\n\n"
        "Recent events and what is happening now."
    )

with col3:
    st.info(
        "📚 Learning\n\n"
        "Math, science, programming and explanations."
    )
```

# =========================================================

# SHOW CHAT HISTORY

# =========================================================

for message in st.session_state.messages:

```
with st.chat_message(message["role"]):
    st.markdown(message["content"])
```

# =========================================================

# CHAT INPUT

# =========================================================

user_input = st.chat_input("Message Nader AI...")

# =========================================================

# PROCESS USER QUESTION

# =========================================================

if user_input:

```
st.session_state.messages.append(
    {
        "role": "user",
        "content": user_input
    }
)

with st.chat_message("user"):
    st.markdown(user_input)

with st.chat_message("assistant"):

    try:

        with st.spinner("Nader is thinking..."):

            if st.session_state.web_enabled:

                response = client.responses.create(
                    model=MODEL,
                    instructions=SYSTEM_PROMPT,
                    input=st.session_state.messages,
                    tools=[
                        {
                            "type": "web_search"
                        }
                    ]
                )

            else:

                response = client.responses.create(
                    model=MODEL,
                    instructions=SYSTEM_PROMPT,
                    input=st.session_state.messages
                )

            answer = response.output_text

            if not answer:
                answer = "I couldn't generate an answer. Please try again."

    except Exception as e:

        answer = (
            "⚠️ Nader AI encountered an error.\n\n"
            "Please check your API key and settings.\n\n"
            "Error: " + str(e)
        )

    st.markdown(answer)

st.session_state.messages.append(
    {
        "role": "assistant",
        "content": answer
    }
)
```

# =========================================================

# FOOTER

# =========================================================

st.markdown(
""" <div class="footer">
Nader AI • Your intelligent AI assistant </div>
""",
unsafe_allow_html=True
)
