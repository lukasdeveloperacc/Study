from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import StateGraph, END, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from basic_agent.tools import get_mcp_tools

import asyncio

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent_core_tools = get_mcp_tools()
tools = []
tools += agent_core_tools
print("Tools : ", tools)

tool_node = ToolNode(tools=tools)
llm_with_tools = llm.bind_tools(tools)

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
