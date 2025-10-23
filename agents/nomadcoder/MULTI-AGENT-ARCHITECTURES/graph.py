from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.prebuilt import InjectedState
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from pydantic import BaseModel

llm = init_chat_model("openai:gpt-4o")

class SupervisorOutput(BaseModel):
    next_agent: Literal["korean_agent", "greek_agent", "spanish_agent", "__end__"]
    reasoning: str

class AgentsState(MessagesState):
    current_agent: str
    transfered_by: str
    reasoning: str

def make_agent_tool(tool_name, tool_description, system_prompt, tools):
    # return graph
    
    def agent_node(state: AgentsState):
        llm_with_tools = llm.bind_tools(tools)
        response = llm_with_tools.invoke(f"""{system_prompt}

Conversation history:
{state["messages"]}""")
        
        return { "messages": [response] }
    
    agent_builder = StateGraph(AgentsState)
    agent_builder.add_node("agent", agent_node)
    agent_builder.add_node("tools", ToolNode(tools=tools))
    
    agent_builder.add_edge(START, "agent")
    agent_builder.add_conditional_edges("agent", tools_condition)
    agent_builder.add_edge("tools", "agent")
    agent_builder.add_edge("agent", END)
    
    agent = agent_builder.compile()
    
    # How to inject state into tool
    @tool(name_or_callable=tool_name, description=tool_description)
    def agent_tool(state: Annotated[dict, InjectedState]): # Tool로 State를 주입
        result = agent.invoke(state)
        return result["messages"][-1].content

    return agent_tool

tools = [
    make_agent_tool(
        tool_name="korean_agent",
        tool_description="Use this when the user is speaking korean.",
        system_prompt="You're a korean customer support agent you speak in korean.",
        tools=[],
    ),
    make_agent_tool(
        tool_name="greek_agent",
        tool_description="Use this when the user is speaking greek.",
        system_prompt="You're a greek customer support agent you speak in greek.",
        tools=[],
    ),
    make_agent_tool(
        tool_name="spanish_agent",
        tool_description="Use this when the user is speaking spanish.",
        system_prompt="You're a spanish customer support agent you speak in spanish.",
        tools=[],
    ),
]
def supervisor(state: AgentState):
    llm_with_tools = llm.bind_tools(tools=tools)
    result = llm_with_tools.invoke(state["messages"])

    return {"messages": [result]}

graph_builder = StateGraph(AgentsState)

graph_builder.add_node(supervisor.__name__, supervisor)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.add_edge(START, supervisor.__name__)
graph_builder.add_conditional_edges(supervisor.__name__, tools_condition)
graph_builder.add_edge("tools", supervisor.__name__)
graph_builder.add_edge(supervisor.__name__, END)

graph = graph_builder.compile()
