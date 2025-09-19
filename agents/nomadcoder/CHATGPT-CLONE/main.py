from agents import Agent, Runner ,SQLiteSession

import dotenv
dotenv.load_dotenv()

import streamlit as st
import asyncio

if "agent" not in st.session_state:
    st.session_state["agent"] = Agent(name="ChatGPTClone", instructions="""You are a helpful assistant.""")

agent: Agent = st.session_state["agent"]

if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession("chat-history", "chat-gpt-clone-memory.db")

session: SQLiteSession = st.session_state["session"]

async def run_agent(message):
    stream = Runner.run_streamed(agent, message, session)
    async for event in stream.stream_events():
        if event.type == "raw_response_event":
            if event.data.type == "response.output_text.delta":
                with st.chat_message("assistant"):
                    st.write(event.data.delta)

with st.sidebar:
    reset = st.button("Reset memory") # if clicked, reset will be True
    if reset:
        asyncio.run(session.clear_session())

    st.write(asyncio.run(session.get_items()))

prompt = st.chat_input("Write a message for your assistant")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    
    asyncio.run(run_agent(prompt))
    

    

    