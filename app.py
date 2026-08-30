import streamlit as st
import random
import re
import math
from difflib import SequenceMatcher, get_close_matches

BOT_NAME = "Nader AI"
VERSION = "2.0"

st.set_page_config(page_title="Nader AI", page_icon="🤖", layout="centered")

st.markdown("""
<style>
.main-title{text-align:center;font-size:42px;font-weight:700;margin-bottom:0}
.subtitle{text-align:center;color:#777;margin-bottom:25px}
.status-box{padding:10px;border-radius:10px;background:#f4f4f4;text-align:center;margin-bottom:15px}
</style>
""", unsafe_allow_html=True)

KNOWLEDGE = [
    {"topic":"technology","keywords":["technology","tech"],"answer":"Technology is the use of scientific knowledge, tools, software, machines, and systems to solve problems and make tasks easier."},
    {"topic":"python","keywords":["python","python programming","programming language"],"answer":"Python is a popular programming language known for its simple syntax. It is widely used for web development, automation, data analysis, artificial intelligence, machine learning, and scripting."},
    {"topic":"ai","keywords":["ai","artificial intelligence","what is ai"],"answer":"AI stands for Artificial Intelligence. It refers to computer systems that can perform tasks that normally require human intelligence, such as understanding language, recognizing images, learning patterns, and making predictions."},
    {"topic":"machine learning","keywords":["machine learning","ml"],"answer":"Machine learning is a branch of AI where computers learn patterns from data and use those patterns to make predictions or decisions."},
    {"topic":"cybersecurity","keywords":["cybersecurity","cyber security","security","hacking"],"answer":"Cybersecurity is the practice of protecting computers, networks, applications, and data from unauthorized access and attacks. Good practices include strong passwords, two-factor authentication, software updates, and backups."},
    {"topic":"cloud","keywords":["cloud","cloud computing","aws","azure","google cloud"],"answer":"Cloud computing means using remote servers over a network to store data, run applications, and provide computing resources. AWS, Microsoft Azure, and Google Cloud are major cloud platforms."},
    {"topic":"database","keywords":["database","databases","sql","mysql","postgresql","sqlite"],"answer":"A database is a system for storing and organizing data. SQL databases such as MySQL, PostgreSQL, and SQLite store structured information, often in tables."},
    {"topic":"api","keywords":["api","apis","application programming interface"],"answer":"An API, or Application Programming Interface, allows different software programs to communicate with each other."},
    {"topic":"streamlit","keywords":["streamlit","stream lit"],"answer":"Streamlit is a Python framework that makes it easy to build interactive web applications, especially for data science, machine learning, dashboards, and Python projects."},
    {"topic":"football","keywords":["football","soccer"],"answer":"Football, also called soccer in many countries, is a team sport where two teams try to score by putting the ball into the opponent's goal. A normal match lasts 90 minutes plus added time."},
    {"topic":"messi","keywords":["messi","lionel messi","leo messi"],"answer":"Lionel Messi is an Argentine footballer widely regarded as one of the greatest players in football history. He is known for his dribbling, passing, vision, finishing, and playmaking. He won the FIFA World Cup with Argentina in 2022."},
    {"topic":"ronaldo","keywords":["ronaldo","cristiano ronaldo","cr7"],"answer":"Cristiano Ronaldo is a Portuguese footballer known for his goal scoring, athleticism, heading, finishing, and long career at the highest level of football."},
    {"topic":"world cup","keywords":["world cup","fifa world cup"],"answer":"The FIFA World Cup is the world's biggest international football tournament. It is normally held every four years. Argentina won the 2022 World Cup in Qatar."},
    {"topic":"champions league","keywords":["champions league","ucl","uefa champions league"],"answer":"The UEFA Champions League is one of the most prestigious club football competitions in the world. It features top European clubs competing against each other."},
    {"topic":"premier league","keywords":["premier league","epl","english premier league"],"answer":"The Premier League is the highest level of professional football in England. It is one of the most popular football leagues in the world."},
    {"topic":"offside","keywords":["offside","off side"],"answer":"In simple terms, an attacking player is generally in an offside position if, when a teammate plays the ball, the player is nearer to the opponent's goal line than both the ball and the second-last opponent, subject to the official rules and exceptions."},
    {"topic":"penalty","keywords":["penalty","penalty kick"],"answer":"A penalty kick is awarded when a team commits a direct-free-kick offence inside its own penalty area. The kick is taken from the penalty mark."},
    {"topic":"var","keywords":["var","video assistant referee"],"answer":"VAR stands for Video Assistant Referee. It helps referees review important incidents involving goals, penalties, direct red cards, and mistaken identity."},
    {"topic":"calculus","keywords":["calculus","differentiation"],"answer":"Calculus is a branch of mathematics dealing mainly with change and accumulation. Its two major areas are differential calculus and integral calculus."},
    {"topic":"optimization","keywords":["optimization","maximize","minimize","maximum","minimum"],"answer":"Optimization is the process of finding the largest or smallest possible value of a quantity. In calculus, we usually define a function, find critical points using the derivative, and determine which point gives the maximum or minimum."},
    {"topic":"derivative","keywords":["derivative","derivatives","find derivative"],"answer":"A derivative measures the instantaneous rate of change of a function. Geometrically, it represents the slope of the tangent line to a curve."},
    {"topic":"integral","keywords":["integral","integration","integrals"],"answer":"An integral can represent accumulation or area. Definite integrals calculate accumulated quantities over an interval, while indefinite integrals represent families of antiderivatives."},
    {"topic":"pythagorean theorem","keywords":["pythagorean theorem","pythagoras","pythagorean"],"answer":"The Pythagorean theorem states that for a right triangle, a² + b² = c², where c is the hypotenuse."},
    {"topic":"computer","keywords":["computer","computers"],"answer":"A computer is an electronic device that processes data according to instructions called programs. Modern computers can perform calculations, store information, communicate, and run complex applications."},
    {"topic":"internet","keywords":["internet","the internet","web"],"answer":"The Internet is a worldwide network of connected computer systems that communicate using standardized protocols."},
]

ARABIC_KNOWLEDGE = [
    {"keywords":["مرحبا","اهلا","أهلا","هاي","سلام"],"answer":"أهلا وسهلا! 👋 أنا Nader AI. فيني ساعدك بأسئلة عن التكنولوجيا، كرة القدم، والرياضيات."},
    {"keywords":["مين ميسي","من هو ميسي","ميسي مين"],"answer":"ليونيل ميسي لاعب كرة قدم أرجنتيني ومن أشهر لاعبي كرة القدم في التاريخ. فاز مع الأرجنتين بكأس العالم سنة 2022."},
    {"keywords":["شو يعني ai","ما هو ai","شو هو ai","شو يعني الذكاء الاصطناعي"],"answer":"AI يعني الذكاء الاصطناعي. هو مجال بيخلي الكمبيوتر يعمل مهام عادةً بتحتاج ذكاء بشري، مثل فهم اللغة والتعرف على الصور والتعلم من البيانات."},
    {"keywords":["شو يعني بايثون","ما هي بايثون","شو هي python","بايثون"],"answer":"Python هي لغة برمجة مشهورة وسهلة نسبياً، وبتستخدم بالـ AI، تحليل البيانات، تطوير المواقع، والأتمتة."},
    {"keywords":["كيفك","كيف حالك","شو اخبارك"],"answer":"منيح كتير 😄 شكراً لسؤالك! شو بتحب تسألني؟"},
    {"keywords":["شكرا","شكراً","مرسي","يسلمو"],"answer":"العفو! 😊 أنا جاهز إذا بدك تسأل عن أي شيء بعرفه."},
]

FALLBACKS = [
    "I'm not sure about that yet. Try asking me about technology, football, mathematics, or Python.",
    "I don't have enough information to answer that. Try rephrasing your question.",
    "I'm still learning. You can ask me about Python, AI, Messi, Ronaldo, football, calculus, or mathematics."
]

def normalize_text(text):
    if not text:
        return ""
    text = text.lower().strip()
    replacements = {"what's":"what is","who's":"who is","whats":"what is","whos":"who is","cant":"can not","dont":"do not","doesnt":"does not","isnt":"is not"}
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[^\w\s\u0600-\u06FF]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def keyword_score(text, keyword):
    keyword = normalize_text(keyword)
    if not keyword:
        return 0
    if keyword in text:
        return 5 if " " in keyword else 4
    score = 0
    for kw in keyword.split():
        for tw in text.split():
            if len(kw) >= 3 and SequenceMatcher(None, kw, tw).ratio() >= 0.88:
                score += 2
    return score

def contains_arabic(text):
    return bool(re.search(r"[\u0600-\u06FF]", text))

def calculate_expression(user_input):
    text = user_input.lower()
    for old, new in {"×":"*","÷":"/","^":"**"}.items():
        text = text.replace(old, new)
    text = re.sub(r"[^0-9+\-*/().%\s]", "", text).strip()
    if not text or not re.search(r"\d", text) or len(text) > 100:
        return None
    try:
        result = eval(text, {"__builtins__": {}}, {})
        if isinstance(result, (int, float)) and math.isfinite(float(result)):
            return str(int(result)) if float(result).is_integer() else f"{result:.10g}"
    except Exception:
        pass
    return None

def get_reply(user_input):
    original = user_input.strip()
    text = normalize_text(original)
    if not text:
        return "Please type something.", 0

    if contains_arabic(original):
        best = None
        best_score = 0
        for entry in ARABIC_KNOWLEDGE:
            score = max(keyword_score(text, k) for k in entry["keywords"])
            if score > best_score:
                best_score = score
                best = entry
        if best and best_score >= 3:
            return best["answer"], best_score

    if any(x in text.split() for x in ["hello", "hi", "hey"]):
        return "Hello! 👋 I'm Nader AI. What would you like to talk about?", 10
    if "how are you" in text:
        return "I'm doing great! 🤖 Thanks for asking. What can I help you with?", 10
    if "your name" in text or "who are you" in text:
        return f"I'm {BOT_NAME} V{VERSION}. 🤖 I'm a local chatbot that works without an API key.", 10
    if text == "help" or "what can you do" in text:
        return "I can help with 💻 technology, ⚽ football, ➗ mathematics, 🐍 Python, 🤖 AI, and 🧮 calculations.", 10
    if any(x in text for x in ["thanks", "thank you"]):
        return "You're welcome! 😊", 10
    if any(x in text for x in ["goodbye", "bye"]):
        return "Goodbye! 👋 Come back anytime.", 10

    if re.search(r"\d", text) and (re.search(r"[+\-*/×÷^]", text) or any(x in text for x in ["calculate", "solve", "equals"])):
        result = calculate_expression(original)
        if result is not None:
            return f"🧮 The answer is **{result}**.", 10

    best_entry = None
    best_score = 0
    for entry in KNOWLEDGE:
        score = sum(keyword_score(text, k) for k in entry["keywords"])
        if score > best_score:
            best_score = score
            best_entry = entry
    if best_entry and best_score >= 3:
        return best_entry["answer"], best_score

    keywords = [(normalize_text(k), e["answer"]) for e in KNOWLEDGE for k in e["keywords"] if " " not in normalize_text(k)]
    keyword_list = [k for k, _ in keywords]
    for word in text.split():
        if len(word) < 3:
            continue
        matches = get_close_matches(word, keyword_list, n=1, cutoff=0.78)
        if matches:
            return next(answer for k, answer in keywords if k == matches[0]), 2

    return random.choice(FALLBACKS), 0

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"Hello! 👋 I'm **Nader AI V2**.\n\nI work without an API key. Ask me about technology, football, mathematics, Python, AI, or try a calculation."}]
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

st.markdown('<div class="main-title">🤖 Nader AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Version 2.0 • No API Key Required</div>', unsafe_allow_html=True)
st.markdown('<div class="status-box">🟢 Online • Local Knowledge Engine • No API</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🤖 Nader AI")
    st.write("A lightweight chatbot that runs without an API key.")
    st.divider()
    st.subheader("📚 Knowledge")
    for item in ["💻 Technology","⚽ Football","➗ Mathematics","🐍 Python","🤖 AI","🧮 Calculator","🇱🇧 Basic Arabic"]:
        st.write(item)
    st.divider()
    st.subheader("💡 Try these")
    for suggestion in ["What is Python?","What is AI?","Who is Messi?","What is VAR?","What is calculus?","25 × 17"]:
        if st.button(suggestion, use_container_width=True):
            st.session_state.messages.append({"role":"user","content":suggestion})
            answer, _ = get_reply(suggestion)
            st.session_state.messages.append({"role":"assistant","content":answer})
            st.session_state.question_count += 1
            st.rerun()
    st.divider()
    st.write(f"💬 Questions asked: **{st.session_state.question_count}**")
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = [{"role":"assistant","content":"Conversation cleared. 👋 How can I help you?"}]
        st.session_state.question_count = 0
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask Nader AI something...")
if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    answer, _ = get_reply(user_input)
    st.session_state.messages.append({"role":"assistant","content":answer})
    st.session_state.question_count += 1
    st.rerun()
