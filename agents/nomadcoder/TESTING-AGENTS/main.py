from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()


class EmailState(TypedDict):
    email: str
    category: Literal["spam", "normal", "urgent"]
    priority_score: int
    response: str


def categorize_email(state: EmailState) -> EmailState:
    email = state.get("email", "").lower()

    if "urgent" in email or "asap" in email:
        category = "urgent"
    elif "offer" in email or "discount" in email:
        category = "spam"
    else:
        category = "normal"

    return {"category": category}


def assign_priority(state: EmailState) -> EmailState:
    scores = {"urgent": 10, "spam": 1, "normal": 5}

    return {"priority_score": scores[state["category"]]}


def draft_response(state: EmailState) -> EmailState:
    responses = {
        "urgent": "I will answer you as fast as i can",
        "normal": "I'll get back to you soon",
        "spam": "Go away!",
    }

    return {"response": responses[state["category"]]}


graph_builder = StateGraph(EmailState)

graph_builder.add_node(categorize_email.__name__, categorize_email)
graph_builder.add_node(assign_priority.__name__, assign_priority)
graph_builder.add_node(draft_response.__name__, draft_response)

graph_builder.add_edge(START, categorize_email.__name__)
graph_builder.add_edge(categorize_email.__name__, assign_priority.__name__)
graph_builder.add_edge(assign_priority.__name__, draft_response.__name__)
graph_builder.add_edge(draft_response.__name__, END)

graph = graph_builder.compile(checkpointer=checkpointer)
