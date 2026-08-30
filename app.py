import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Nader AI", page_icon="🤖")
st.title("🤖 Nader AI")
st.caption("Your personal AI assistant")

# Load API key from Streamlit secrets or environment variable
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

if not api_key:
    st.error("Please add your OpenAI API key to Streamlit secrets or environment variables.")
    st.stop()

client = OpenAI(api_key=api_key)

# Important: Tell the AI who it is
SYSTEM_PROMPT = "You are Nader AI, a helpful, friendly, and concise assistant."

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hello! I'm Nader AI. How can I help you today?"}
    ]

# Show previous messages, but skip the system message
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Message Nader AI..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate assistant reply with streaming
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        full_reply = ""

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            full_reply += delta
            placeholder.markdown(full_reply + "▌")

        placeholder.markdown(full_reply)

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": full_reply})
