from typing import Literal
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain.chat_models import init_chat_model

llm = init_chat_model("openai:gpt-4o-mini")

checkpointer = MemorySaver()


class EmailState(TypedDict):
    email: str
    category: Literal["spam", "normal", "urgent"]
    priority_score: int
    response: str


class EmailClassificationOutput(BaseModel):
    category: Literal["spam", "normal", "urgent"] = Field(
        description="Category of the email"
    )


class PriorityScoreOutput(BaseModel):
    priority_score: int = Field(description="Priority score from 1 to 10", ge=1, le=10)


def categorize_email(state: EmailState) -> EmailState:
    structured_llm = llm.with_structured_output(EmailClassificationOutput)
    result: EmailClassificationOutput = structured_llm.invoke(
        f"""Classify this email into one of three categories:
        - urgent: time-sensitive, requires immediate attention
        - normal: regular business communication
        - spam: promotional, marketing, or unwanted content

        Email: {state['email']}"""
    )

    return {"category": result.category}


def assign_priority(state: EmailState) -> EmailState:
    s_llm = llm.with_structured_output(PriorityScoreOutput)

    result: PriorityScoreOutput = s_llm.invoke(
        f"""Assign a priority score from 1-10 for this {state['category']} email.
        Consider:
        - Category: {state['category']}
        - Email content: {state['email']}

        Guidelines:
        - Urgent emails: usually 8-10
        - Normal emails: usually 4-7
        - Spam emails: usually 1-3"""
    )

    return {"priority_score": result.priority_score}


def draft_response(state: EmailState) -> EmailState:
    result = llm.invoke(
        f"""Draft a brief, professional response for this {state['category']} email.

        Original email: {state['email']}
        Category: {state['category']}
        Priority: {state['priority_score']}/10

        Guidelines:
        - Urgent: Acknowledge urgency, promise immediate attention
        - Normal: Professional acknowledgment, standard timeline
        - Spam: Brief notice that message was filtered

        Keep response under 2 sentences."""
    )

    return {"response": result.content}


graph_builder = StateGraph(EmailState)

graph_builder.add_node(categorize_email.__name__, categorize_email)
graph_builder.add_node(assign_priority.__name__, assign_priority)
graph_builder.add_node(draft_response.__name__, draft_response)

graph_builder.add_edge(START, categorize_email.__name__)
graph_builder.add_edge(categorize_email.__name__, assign_priority.__name__)
graph_builder.add_edge(assign_priority.__name__, draft_response.__name__)
graph_builder.add_edge(draft_response.__name__, END)

graph = graph_builder.compile(checkpointer=checkpointer)
