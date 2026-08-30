
import streamlit as st
import random
import re
from difflib import get_close_matches

# =========================================================
# NADER AI
# Simple chatbot - NO API REQUIRED
# =========================================================

BOT_NAME = "Nader AI"

TOPICS = ["technology", "football"]

# =========================================================
# KNOWLEDGE BASE
# =========================================================

KNOWLEDGE = [
    {
        "keywords": ["technology", "tech"],
        "answer": (
            "Technology is about using computers, software, and systems "
            "to solve problems. I know a little about Python, AI, "
            "cybersecurity, cloud, databases, and APIs."
        )
    },

    {
        "keywords": ["python"],
        "answer": (
            "Python is a popular programming language used for web "
            "development, automation, data analysis, AI, and scripting."
        )
    },

    {
        "keywords": ["ai", "artificial intelligence"],
        "answer": (
            "AI means artificial intelligence. It allows software to do "
            "smart tasks like understanding language, recognizing images, "
            "or making predictions."
        )
    },

    {
        "keywords": ["machine learning", "ml"],
        "answer": (
            "Machine learning is a part of AI where a computer learns "
            "patterns from data instead of being given every rule manually."
        )
    },

    {
        "keywords": ["cybersecurity", "security", "hacking"],
        "answer": (
            "Cybersecurity protects systems and data from attacks. "
            "Basic safety steps include strong passwords, two-factor "
            "authentication, updates, and backups."
        )
    },

    {
        "keywords": ["cloud", "cloud computing", "aws", "azure", "google cloud"],
        "answer": (
            "Cloud computing means using remote servers over the internet "
            "for storage, apps, databases, and computing power. "
            "Examples are AWS, Azure, and Google Cloud."
        )
    },

    {
        "keywords": ["database", "sql"],
        "answer": (
            "A database stores organized data. SQL databases like MySQL, "
            "PostgreSQL, and SQLite store data in tables."
        )
    },

    {
        "keywords": ["api"],
        "answer": (
            "An API lets two programs communicate. For example, a weather "
            "app can use an API to get weather data from a server."
        )
    },

    # =====================================================
    # FOOTBALL
    # =====================================================

    {
        "keywords": ["football", "soccer"],
        "answer": (
            "Football, also called soccer in some countries, is a team "
            "game where players try to score goals. A normal match is "
            "90 minutes plus added time."
        )
    },

    {
        "keywords": ["messi", "lionel messi"],
        "answer": (
            "Lionel Messi is an Argentine footballer known for dribbling, "
            "passing, free kicks, and playmaking. He won the FIFA World "
            "Cup with Argentina in 2022."
        )
    },

    {
        "keywords": ["ronaldo", "cristiano ronaldo"],
        "answer": (
            "Cristiano Ronaldo is a Portuguese footballer known for "
            "goal scoring, fitness, and a long career at the top level."
        )
    },

    {
        "keywords": ["world cup", "fifa world cup"],
        "answer": (
            "The FIFA World Cup is the biggest international football "
            "tournament. It is held every four years, and Argentina won "
            "the 2022 World Cup."
        )
    },

    {
        "keywords": ["champions league", "ucl"],
        "answer": (
            "The UEFA Champions League is a top European club football "
            "competition played by the best teams from European leagues."
        )
    },

    {
        "keywords": ["premier league", "epl"],
        "answer": (
            "The Premier League is the top professional football league "
            "in England."
        )
    },

    {
        "keywords": ["offside"],
        "answer": (
            "In football, offside usually means an attacking player is "
            "closer to the opponent's goal than the ball or the second-last "
            "defender when the pass is made."
        )
    },

    {
        "keywords": ["penalty"],
        "answer": (
            "A penalty is a direct kick from the penalty spot, awarded "
            "after a serious foul inside the penalty box."
        )
    },

    {
        "keywords": ["var"],
        "answer": (
            "VAR means Video Assistant Referee. It helps referees review "
            "big decisions like goals, penalties, red cards, and mistaken identity."
        )
    }
]

# =========================================================
# FALLBACK ANSWERS
# =========================================================

FALLBACKS = [
    "I don't know that yet. I only know a little about technology and football.",
    "Please ask me about technology or football.",
    "Try asking: What is Python? What is AI? Who is Messi? What is VAR?"
]

# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def has_word(word, text):
    return re.search(
        r"\b" + re.escape(word) + r"\b",
        text
    ) is not None


# =========================================================
# KEYWORD SCORING
# =========================================================

def score_keywords(text, keywords):

    score = 0

    for keyword in keywords:

        keyword = clean_text(keyword)

        if not keyword:
            continue

        # Multi-word keyword
        if " " in keyword:

            if keyword in text:
                score += 3

        # Single word keyword
        elif has_word(keyword, text):

            score += 2

    return score


# =========================================================
# GENERATE RESPONSE
# =========================================================

def get_reply(user_input):

    text = clean_text(user_input)

    if not text:
        return "Please type something."

    # Greetings
    if any(
        has_word(word, text)
        for word in ["hello", "hi", "hey"]
    ):
        return (
            "Hello! 👋 I'm Nader AI. "
            "Ask me about technology or football."
        )

    # How are you
    if "how are you" in text:

        return (
            "I'm doing great! 🤖 "
            "Ask me a technology or football question."
        )

    # Name
    if "your name" in text or "who are you" in text:

        return (
            f"I am {BOT_NAME}, a simple chatbot "
            "that works without an API."
        )

    # Help
    if "help" in text or "what can you do" in text:

        return (
            "I can chat about technology and football.\n\n"
            "Try asking:\n"
            "• What is Python?\n"
            "• What is AI?\n"
            "• What is machine learning?\n"
            "• Who is Messi?\n"
            "• What is VAR?\n"
            "• What is the Champions League?"
        )

    # Find best knowledge match
    best_entry = None
    best_score = 0

    for entry in KNOWLEDGE:

        score = score_keywords(
            text,
            entry["keywords"]
        )

        if score > best_score:

            best_score = score
            best_entry = entry

    if best_entry:

        return best_entry["answer"]

    # Fuzzy matching
    all_keywords = []
    keyword_to_entry = {}

    for entry in KNOWLEDGE:

        for keyword in entry["keywords"]:

            keyword_clean = clean_text(keyword)

            all_keywords.append(keyword_clean)
            keyword_to_entry[keyword_clean] = entry

    for word in text.split():

        close = get_close_matches(
            word,
            all_keywords,
            n=1,
            cutoff=0.80
        )

        if close:

            return keyword_to_entry[
                close[0]
            ]["answer"]

    # Nothing found
    return random.choice(FALLBACKS)


# =========================================================
# STREAMLIT PAGE
# =========================================================

st.set_page_config(
    page_title="Nader AI",
    page_icon="🤖",
    layout="centered"
)

# =========================================================
# HEADER
# =========================================================

st.title("🤖 Nader AI")

st.caption(
    "A simple AI-style chatbot that works completely without an API."
)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 I'm Nader AI.\n\n"
                "I can answer questions about **technology** "
                "and **football**.\n\n"
                "Try asking me: **What is Python?**"
            )
        }
    ]


# =========================================================
# DISPLAY CHAT
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Ask Nader AI something..."
)

if user_input:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Generate response
    response = get_reply(user_input)

    # Add bot response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    # Refresh page
    st.rerun()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🤖 Nader AI")

    st.write(
        "This chatbot does not use an API. "
        "It uses a local knowledge base and "
        "keyword matching."
    )

    st.divider()

    st.subheader("Topics")

    st.write("💻 Technology")
    st.write("⚽ Football")

    st.divider()

    st.subheader("Try asking")

    st.write("• What is Python?")
    st.write("• What is AI?")
    st.write("• What is machine learning?")
    st.write("• Who is Messi?")
    st.write("• Who is Ronaldo?")
    st.write("• What is VAR?")

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! 👋 I'm Nader AI. "
                    "How can I help you?"
                )
            }
        ]

        st.rerun()

