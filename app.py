import random
import re
from difflib import get_close_matches

BOT_NAME = "MiniChat"
TOPICS = ["technology", "football"]

KNOWLEDGE = [
    {
        "keywords": ["technology", "tech"],
        "answer": "Technology is about using computers, software, and systems to solve problems. I know a little about Python, AI, cybersecurity, cloud, databases, and APIs."
    },
    {
        "keywords": ["python"],
        "answer": "Python is a popular programming language used for web development, automation, data analysis, AI, and scripting."
    },
    {
        "keywords": ["ai", "artificial intelligence"],
        "answer": "AI means artificial intelligence. It allows software to do smart tasks like understanding language, recognizing images, or making predictions."
    },
    {
        "keywords": ["machine learning", "ml"],
        "answer": "Machine learning is a part of AI where a computer learns patterns from data instead of being given every rule manually."
    },
    {
        "keywords": ["cybersecurity", "security", "hacking"],
        "answer": "Cybersecurity protects systems and data from attacks. Basic safety steps include strong passwords, two-factor authentication, updates, and backups."
    },
    {
        "keywords": ["cloud", "cloud computing", "aws", "azure", "google cloud"],
        "answer": "Cloud computing means using remote servers over the internet for storage, apps, databases, and computing power. Examples are AWS, Azure, and Google Cloud."
    },
    {
        "keywords": ["database", "sql"],
        "answer": "A database stores organized data. SQL databases like MySQL, PostgreSQL, and SQLite store data in tables."
    },
    {
        "keywords": ["api"],
        "answer": "An API lets two programs communicate. For example, a weather app can use an API to get weather data from a server."
    },

    {
        "keywords": ["football", "soccer"],
        "answer": "Football, also called soccer in some countries, is a team game where players try to score goals. A normal match is 90 minutes plus added time."
    },
    {
        "keywords": ["messi", "lionel messi"],
        "answer": "Lionel Messi is an Argentine footballer known for dribbling, passing, free kicks, and playmaking. He won the FIFA World Cup with Argentina in 2022."
    },
    {
        "keywords": ["ronaldo", "cristiano ronaldo"],
        "answer": "Cristiano Ronaldo is a Portuguese footballer known for goal scoring, fitness, and a long career at the top level."
    },
    {
        "keywords": ["world cup", "fifa world cup"],
        "answer": "The FIFA World Cup is the biggest international football tournament. It is held every four years, and Argentina won the 2022 World Cup."
    },
    {
        "keywords": ["champions league", "ucl"],
        "answer": "The UEFA Champions League is a top European club football competition played by the best teams from European leagues."
    },
    {
        "keywords": ["premier league", "epl"],
        "answer": "The Premier League is the top professional football league in England."
    },
    {
        "keywords": ["offside"],
        "answer": "In football, offside usually means an attacking player is closer to the opponent's goal than the ball or the second-last defender when the pass is made."
    },
    {
        "keywords": ["penalty"],
        "answer": "A penalty is a direct kick from the penalty spot, awarded after a serious foul inside the penalty box."
    },
    {
        "keywords": ["var"],
        "answer": "VAR means Video Assistant Referee. It helps referees review big decisions like goals, penalties, red cards, and mistaken identity."
    }
]

FALLBACKS = [
    "I don't know that yet. I only know a little about technology and football.",
    "Please ask me about technology or football.",
    "Try asking: What is Python? What is AI? Who is Messi? What is VAR?"
]

def clean_text(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def has_word(word, text):
    return re.search(r"\b" + re.escape(word) + r"\b", text) is not None

def score_keywords(text, keywords):
    score = 0

    for keyword in keywords:
        keyword = clean_text(keyword)

        if not keyword:
            continue

        if " " in keyword:
            if keyword in text:
                score += 3
        elif has_word(keyword, text):
            score += 2

    return score

def get_reply(user_input):
    text = clean_text(user_input)

    if not text:
        return "Please type something."

    if any(has_word(word, text) for word in ["hello", "hi", "hey"]):
        return "Hello! Ask me about technology or football."

    if "how are you" in text:
        return "I'm good. Ask me a technology or football question."

    if "your name" in text:
        return f"I am {BOT_NAME}, a simple chat-only bot."

    if "help" in text or "what can you do" in text:
        return f"I can chat about {', '.join(TOPICS)}. Try: What is Python? What is AI? Who is Messi? What is VAR?"

    best_entry = None
    best_score = 0

    for entry in KNOWLEDGE:
        score = score_keywords(text, entry["keywords"])

        if score > best_score:
            best_score = score
            best_entry = entry

    if best_entry:
        return best_entry["answer"]

    all_keywords = []
    keyword_to_entry = {}

    for entry in KNOWLEDGE:
        for keyword in entry["keywords"]:
            keyword_clean = clean_text(keyword)
            all_keywords.append(keyword_clean)
            keyword_to_entry[keyword_clean] = entry

    for word in text.split():
        close = get_close_matches(word, all_keywords, n=1, cutoff=0.85)

        if close:
            return keyword_to_entry[close[0]]["answer"]

    return random.choice(FALLBACKS)

def main():
    print(f"{BOT_NAME}: Hello! I only chat about {', '.join(TOPICS)}.")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")

        if user_input.lower().strip() in ["exit", "quit", "bye"]:
            print(f"{BOT_NAME}: Goodbye!")
            break

        print(f"{BOT_NAME}: {get_reply(user_input)}")

if __name__ == "__main__":
    main()
