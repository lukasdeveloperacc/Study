import dotenv

dotenv.load_dotenv()
import asyncio
import streamlit as st
import numpy as np
import wave, io

from agents import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered, Runner, SQLiteSession, function_tool, RunContextWrapper, Agent
from agents.voice import AudioInput
from models import UserAccountContext
from my_agents.triage_agent import triage_agent
from openai import OpenAI



client = OpenAI()

user_account_ctx = UserAccountContext(
    customer_id=1,
    name="nico",
    tier="basic",
)


if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession(
        "chat-history",
        "customer-support-memory.db",
    )
session = st.session_state["session"]

if "agent" not in st.session_state:
    st.session_state["agent"] = triage_agent

def convert_audio(audio_input):
     audio_data = audio_input.getvalue()

     with wave.open(io.BytesIO(audio_data), "rb") as wav_file:
        audio_frames = wav_file.readframes(-1)

        return np.frombuffer(audio_frames, dtype=np.int16)

async def run_agent(audio_input):
    status_container = st.status("Processing voice message ...")
    try:
        # turn audio into a numpy array
        audio_array = convert_audio(audio_input)
        audio = AudioInput(buffer=audio_array)
        # create custom workflow
        # create the pipeline

        stream = Runner.run_streamed(
            st.session_state["agent"],
            audio_input,
            session=session,
                context=user_account_ctx, # It doesn't transfer the context to the agent
            )   

    except InputGuardrailTripwireTriggered:
        st.write("I can't help you that.")

    except OutputGuardrailTripwireTriggered:
        st.write("Can't show you that answer.")


audio_input = st.audio_input(
    "Record your message",
)

if audio_input:

    if "text_placeholder" in st.session_state:
        st.session_state["text_placeholder"].empty()

    if audio_input:
        with st.chat_message("human"):
            st.audio(audio_input)
        asyncio.run(run_agent(audio_input))


with st.sidebar:
    reset = st.button("Reset memory")
    if reset:
        asyncio.run(session.clear_session())
    st.write(asyncio.run(session.get_items()))
