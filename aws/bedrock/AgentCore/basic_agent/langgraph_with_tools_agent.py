from dotenv import load_dotenv

load_dotenv()


from langgraph.graph import StateGraph, END, START
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState
from agent_core.mcp.utils import get_token

import asyncio, os

token = get_token(
    os.getenv("COGNITO_USER_POOL_ID"),
    os.getenv("COGNITO_USERNAME"),
    os.getenv("COGNITO_PASSWORD"),
    os.getenv("COGNITO_CLIENT_ID"),
    os.getenv("REGION"),
)
client = MultiServerMCPClient(
        {
            "genpresso": {
                "url": os.getenv("MCP_URL"),
                "transport": "streamable_http",
                "headers": {
                    "authorization": f"Bearer {token}"
                }
            }
        }
    )

tools = asyncio.run(client.get_tools())
print(f"Tools: {tools}")

llm_with_tools = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)
tool_node = ToolNode(tools)

def qa_node(state: MessagesState):
    message = state["messages"]
    response = llm_with_tools.invoke(message)
    return {"messages": [response]}

graph_builder = StateGraph(MessagesState)
graph_builder.add_node("qa", qa_node)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "qa")
graph_builder.add_conditional_edges("qa", tools_condition)
graph_builder.add_edge("tools", "qa")
graph_builder.add_edge("qa", END)


graph = graph_builder.compile()

async def test():
    while True:
        user_input = await asyncio.to_thread(input, "User: ")
        if user_input == "exit":
            break

        async for chunk in graph.astream({"messages": [HumanMessage(content=user_input)]}, stream_mode="values"):
            chunk["messages"][-1].pretty_print()
        
        
if __name__ == "__main__":
    asyncio.run(test())
