from dotenv import load_dotenv

load_dotenv()

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.a2a.utils.agent_to_a2a import to_a2a


def dummy_tool(hello: str):
    """Dummy Tool. Helps the agent"""
    return "world"


agent = Agent(
    name="HistoryHelperAgent",
    description="An agent that can help students with their history homework",
    model=LiteLlm("openai/gpt-4o"),
    tools=[dummy_tool],
    sub_agents=[],
)


app = to_a2a(agent, port=8001)  # create server
# uv run uvicorn agent:app --port 8001
