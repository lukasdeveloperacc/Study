from agents import Agent, Runner, SQLiteSession, WebSearchTool, FileSearchTool
from openai import OpenAI
import dotenv

dotenv.load_dotenv()

import streamlit as st
import asyncio

client = OpenAI()
VECTOR_STORE_ID = (
    "vs_68cec15727b88191a353388e4589d383"  # need to upload in OpenAI Storage
)

if "agent" not in st.session_state:
    st.session_state["agent"] = Agent(
        name="ChatGPTClone",
        instructions="""You are a helpful assistant.
        You have access to the following tools:
            - Web Search Tool: Use this when the user asks a questions that isn't in your training data. Use this tool when the users asks about current or future events, when you think you don't know the answer, try searching for it in the web first.
            - File Search Tool: Use this tool when the user asks a question about facts related to themselves. Or when they ask questions about specific files.""",
        tools=[
            WebSearchTool(),
            FileSearchTool(vector_store_ids=[VECTOR_STORE_ID], max_num_results=3),
        ],
    )

agent: Agent = st.session_state["agent"]

if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession(
        "chat-hostory", "chat-gpt-clone-memory.db"
    )

session: SQLiteSession = st.session_state["session"]


async def paint_history():
    messages = await session.get_items()

    for message in messages:
        if "role" in message:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.write(message["content"])
                else:
                    if message["type"] == "message":
                        st.write(message["content"][0]["text"].replace("$", "\$"))

        if "type" in message:
            if message["type"] == "web_search_call":
                with st.chat_message("ai"):
                    st.write("🔍 Searched the web ...")
            elif message["type"] == "file_search_call":
                with st.chat_message("ai"):
                    st.write("🗂️ Searched your files ...")


asyncio.run(paint_history())


def update_status(status_container, event: str):
    status_messages = {
        "response.web_search_call.completed": ("✅ Web search completed", "complete"),
        "response.web_search_call.in_progress": (
            "🔍 Starting web search...",
            "running",
        ),
        "response.web_search_call.searching": (
            "🔍 Web search in progress...",
            "running",
        ),
        "response.completed": (" ", "complete"),
        "response.file_search_call.completed": ("✅ File search completed", "complete"),
        "response.file_search_call.in_progress": (
            "🔍 Starting file search...",
            "running",
        ),
        "response.file_search_call.searching": (
            "🔍 File search in progress...",
            "running",
        ),
    }

    if event in status_messages:
        label, state = status_messages[event]
        status_container.update(label=label, state=state)


async def run_agent(message):
    with st.chat_message("ai"):
        status_container = st.status("⏳", expanded=False)
        text_placeholder = st.empty()  # container
        response = ""

        stream = Runner.run_streamed(agent, message, session=session)
        async for event in stream.stream_events():
            if event.type == "raw_response_event":
                update_status(status_container, event.data.type)
                if event.data.type == "response.output_text.delta":
                    response += event.data.delta
                    text_placeholder.write(response.replace("$", "\$"))


with st.sidebar:
    reset = st.button("Reset memory")  # if clicked, reset will be True
    if reset:
        asyncio.run(session.clear_session())

    st.write(asyncio.run(session.get_items()))

prompt = st.chat_input(
    "Write a message for your assistant", accept_file=True, file_type=["txt"]
)

if prompt:
    for file in prompt.files:
        if file.type.startswith("text/"):
            with st.chat_message("ai"):
                with st.status("⏳ Uploading file...") as status:
                    uploaded_file = client.files.create(
                        file=(file.name, file.getvalue()), purpose="user_data"
                    )  # upload to storage (bucket), return File Object
                    status.update(label=" Attaching file...")
                    client.vector_stores.files.create(
                        vector_store_id=VECTOR_STORE_ID, file_id=uploaded_file.id
                    )  # Upload to vector store about File Object
                    status.update(label="✅ File uploaded", state="complete")

    if prompt.text:
        with st.chat_message("user"):
            st.write(prompt.text)
        asyncio.run(run_agent(prompt.text))
