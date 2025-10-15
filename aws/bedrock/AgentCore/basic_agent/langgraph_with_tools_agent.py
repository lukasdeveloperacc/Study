from dotenv import load_dotenv

load_dotenv()


from langgraph.graph import StateGraph, END, START
from langgraph.graph import MessagesState
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

import asyncio

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def qa_node(state: MessagesState):
    message = state["messages"]
    response = llm.invoke(message)
    return {"messages": [response]}

graph_builder = StateGraph(MessagesState)
graph_builder.add_node("qa", qa_node)

graph_builder.add_edge(START, "qa")
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
