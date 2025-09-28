from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

import asyncio
import os
import json

def get_prompt(prompt: str):
    return prompt + """
<canvas_id>
luke@reconlabs.ai-default
</canvas_id>

**Important!!**
1. Don't ask me just answer.
2. On the case that needs json, You must just return only json format. don't use ```json or except sentence.
"""

llm = ChatOpenAI(model="gpt-4o")

async def main():
    client = MultiServerMCPClient(
        {
            "genpresso": {
                "url": os.getenv("MCP_URL"),
                "transport": os.getenv("TRANPORT_TYPE"),
            }
        }
    )
    tools: list = await client.get_tools()
    print(f"Successfully retrieved {len(tools)} tools\n{[tool.name for tool in tools]}")
    
    # message = get_prompt("Please get my canvas JSON Format data using genpresso-canvas-full-info tool.")
    message = get_prompt("Please check my original canvas data and add new text node with '라면 먹는 파이리' using genpresso-add-canvas-object tool.")
    print("message : ", message)

    result = None
    agent = create_react_agent(llm, tools)
    async for chunk in agent.astream({"messages": message}):
        if chunk.get("agent"):
            print(f"Agent Respone: \n{chunk["agent"]["messages"][-1].pretty_print()}")
            result: str = chunk["agent"]["messages"][-1].content
        elif chunk.get("tools"):
            print(f"Tool Respone: \n{chunk["tools"]["messages"][-1].pretty_print()}")
    
    # llm2 = ChatOpenAI(model="gpt-4o").bind_tools(tools, response_format=RootModel, strict=True)
    # result: RootModel = await llm2.ainvoke(message)
    
    if isinstance(result, str):
        result = result.replace("json", "").replace("```", "")
        try:
            result = json.loads(result)
            print("result : ", result)
        except Exception:
            print("result : ", result)
    
    

if __name__ == "__main__":
    asyncio.run(main())

