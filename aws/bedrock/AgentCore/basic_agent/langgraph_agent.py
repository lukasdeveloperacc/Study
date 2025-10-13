from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict

load_dotenv()


class AgentState(TypedDict):
    question: str
    answer: str

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def qa_node(state: AgentState):
    response = llm.invoke(state["question"])
    return {"answer": response.content}

graph_builder = StateGraph(AgentState)
graph_builder.add_node("qa", qa_node)

graph_builder.set_entry_point("qa")
graph_builder.add_edge("qa", END)

graph = graph_builder.compile()
