from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

import asyncio
import os

llm = ChatOpenAI(model="gpt-4o")

def get_prompt():
    return """

"""

async def main():

    client = MultiServerMCPClient(
        {
            "genpresso": {
                "url": os.getenv("MCP_URL"),
                "transport": os.getenv("TRANPORT_TYPE"),
            }
        }
    )
    tools = await client.get_tools()
    print(f"Successfully retrieved {len(tools)} tools\n{tools}")
    
    agent = create_react_agent(llm, tools)
    message = get_prompt()
    print("message : ", message)
    async for chunk in agent.astream({"messages": message}):
        if chunk.get("agent"):
            print(chunk["agent"]["messages"][-1].pretty_print())
        elif chunk.get("tool"):
            print(chunk["tool"]["messages"][-1].pretty_print())

if __name__ == "__main__":
    asyncio.run(main())

