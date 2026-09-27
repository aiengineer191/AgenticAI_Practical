import streamlit as st

st.header("welcome to Chatbot")

with st.sidebar:
    if st.button("clear"):
        st.session_state.messaage = []
        st.rerun()

if "messaage" not in st.session_state:
    st.session_state.messaage = []

for msg in st.session_state.messaage:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Enter your prompt") 

if prompt:
    st.session_state.messaage.append({"role":"user","content":prompt})
    st.session_state.messaage.append({"role":"system","content":f"you said {prompt}"})
    st.rerun()