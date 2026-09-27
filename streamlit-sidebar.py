import streamlit as st

st.header("Langchain Chatbox")

with st.sidebar:
    st.header("Chat settings")
    model = st.selectbox("select Model",["gpt-3.5-min","gpt-4.5-mini"])
    temparature = st.slider("temparature",0.0,0.4,1.0)
    max_tokens = st.slider("max tokens",100,400,5000)
