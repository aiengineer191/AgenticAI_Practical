import streamlit as st

st.title("welcome to langchain chatbox")
st.write("Welcome to LangChain Chatbox")

name = st.text_input("what is your name")

if st.button("say hello"):
    st.write(f"hello {name}")
else:
    st.write("Pls enter your name")    