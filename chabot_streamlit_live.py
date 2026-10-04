import streamlit as st
import sqlite3
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.checkpoint.sqlite import SqliteSaver
load_dotenv()
st.title("Streamlit chatbot")


CHECKPOINT_DB = "checkpoints.sqlite"

@st.cache_resource
def get_agent():
    conn = sqlite3.connect(CHECKPOINT_DB,check_same_thread= False)
    checkpointer = SqliteSaver(conn)
    checkpointer.setup()
    llm = ChatOpenAI(model="gpt-4.1-mini",temperature=0.6)
    search = TavilySearch()
    

    return create_agent(
        model=llm,
        tools=[search],
        system_prompt=("you are a helpful assistant that can answer questions about the world and provide information based on the user's queries. "
        "You have access to a search tool that can retrieve relevant information from the web. "
        "Use this tool to provide accurate and up-to-date answers to the user's questions."),checkpointer=checkpointer
    )

agent = get_agent()
THREAD_ID = "demo_thread"
thread_config = {"configurable":{"thread_id": THREAD_ID}}
st.caption(f"using Thread ID: {THREAD_ID}")

snapshot = agent.get_state(thread_config)
stored_messages = snapshot.values.get("messages","")

for msg in stored_messages:
    if msg.type == "user":
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif msg.type == "ai":
        with st.chat_message("assistant"):
            st.markdown(msg.content)        

prompt = st.text_input("Prompt:",placeholder="Enter your prompt here",key="input")

if prompt:
    with st.spinner("Loading...."):
        response = agent.invoke({
            "messages":[
                {"role":"user","content":prompt}
            ]
        },config=thread_config)

    st.rerun()    

