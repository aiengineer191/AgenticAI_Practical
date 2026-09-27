import streamlit as st

st.title("welcome to langchain chatbox")
st.write("Welcome to LangChain Chatbox")

if "count" not in st.session_state:
     st.session_state.count = 0 

if st.button("click me"):
    st.session_state.count += 1

if "count" in st.session_state:    
    st.write(f"the count is {st.session_state.count}")      


     