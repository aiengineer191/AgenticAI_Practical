from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
import streamlit as st
import sqlite3
from langchain_tavily import TavilyResearch

load_dotenv()

DATABASE = "SQL3-CHECKPOINTER"

@st.cache_resource #run one time and return many times using decorator
def getagent(): 

    #create the connection and save
    #checkpointer used to save the user input state in the form of json
    con = sqlite3.connect(database=DATABASE,check_same_thread=False)
    checkpointer = SqliteSaver(con)
    checkpointer.setup()

    #create LLM 
    llm = ChatOpenAI(model="gpt-4.1-min",temperature=0.6)
    search = TavilyResearch()

    return create_agent(
        model=llm,
        tools=[search],
        system_prompt="you are a helpful AI chat assistant respond user questions" \
        "use web search tool or external search tool whenever required" \
        "dont hallusination",
        checkpointer=checkpointer

    )

agent = getagent()
THREAD_ID = "sample_demo_thread"
config = {"configurable":{"thread_id":THREAD_ID}}

st.caption(f"using thread : {THREAD_ID}") #sample harcoded thread

state = agent.get_state(config)
saved_messaged = state.values.get("messages","")
for msg in saved_messaged:
    if msg.role == "user":
        with st.chat_message("user"):
            st.markdown(msg.content)

    elif  msg.role == "ai":       
        with st.chat_message("assistant"):
            st.markdown(msg.content) 

prompt = st.text_input("Prompt",placeholder="Enter Your Prompt ...")

if prompt:
    with st.spinner("In Progress..."):
        response = agent.invoke({
                "messages":[
                    {"role":"user","content":prompt}
                ]
        },config=config)

    st.rerun()   

