from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.types import Command
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

def make_agent(prompt, tools):
    # return graph
    
    def agent_node(state: AgentsState):
        llm_with_tools = llm.bind_tools(tools)
        response = llm_with_tools.invoke(f"""{prompt}

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
    
    return agent

def supervisor(state: AgentState):
    structured_llm = llm.with_structured_output(SupervisorOutput)
    response: SupervisorOutput = structured_llm.invoke(f"""
    You are a supervisor that routes conversations to the appropriate language agent.

        Analyse the customers request and the conversation history and decide which agent should handle the conversation.

        The options for the next agent are:
        - greek_agent
        - spanish_agent
        - korean_agent      
        - __end__
        
        <CONVERSATION_HISTORY>
        {state.get("messages", [])}
        </CONVERSATION_HISTORY>

        IMPORTANT:
        
        Never transfer to the same agent twice in a row.

        If an agent has replied end the conversation by returning __end__
    """)

    return Command(goto=response.next_agent, update={"reasoning": response.reasoning})

graph_builder = StateGraph(AgentsState)

graph_builder.add_node(supervisor.__name__, supervisor, destinations=("korean_agent", "spanish_agent", "greek_agent", "__end__"))
graph_builder.add_node(
    "korean_agent",
    make_agent(
        prompt="You're a Korean customer support agent. You only speak and understand Korean.",
        tools=[],
    ),
)
graph_builder.add_node(
    "greek_agent",
    make_agent(
        prompt="You're a Greek customer support agent. You only speak and understand Greek.",
        tools=[],
    ),
)
graph_builder.add_node(
    "spanish_agent",
    make_agent(
        prompt="You're a Spanish customer support agent. You only speak and understand Spanish.",
        tools=[],
    ),
)


graph_builder.add_edge(START, supervisor.__name__)

# Connections For sure back to supervisor
graph_builder.add_edge("korean_agent", supervisor.__name__)
graph_builder.add_edge("spanish_agent", supervisor.__name__)
graph_builder.add_edge("greek_agent", supervisor.__name__)

graph = graph_builder.compile()
