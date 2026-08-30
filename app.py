import streamlit as st

st.set_page_config(page_title="My Streamlit App", page_icon="🚀")

st.title("Hello Streamlit 👋")

name = st.text_input("What is your name?")

if name:
    st.success(f"Welcome, {name}!")

number = st.slider("Pick a number", 0, 100, 25)
st.write("You selected:", number)