from main import graph
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

import pytest

load_dotenv()
llm = init_chat_model("openai:gpt-4o-mini")


class SimilarityScoreOutput(BaseModel):
    similarity_score: int = Field(
        description="How similar is the response to the examples?", gt=0, lt=100
    )


RESPONSE_EXAMPLES = {
    "urgent": [
        "Thank you for your urgent message. We are addressing this immediately and will respond as soon as possible.",
        "We've received your urgent request and are prioritizing it. Our team is on it right away.",
        "This urgent matter has our immediate attention. We'll respond promptly.",
    ],
    "normal": [
        "Thank you for your email. We'll review it and get back to you within 24-48 hours.",
        "We've received your message and will respond soon. Thank you for reaching out.",
        "Thank you for contacting us. We'll process your request and respond shortly.",
        "Thank you for the update. I will review the information and follow up as needed.",
        "Thank you for the update on the project status. I will review and follow up by the end of the week.",
        "Thanks for sharing this update. We'll review and respond accordingly.",
    ],
    "spam": [
        "This message has been flagged as spam and filtered.",
        "This email has been identified as promotional content.",
        "This message has been marked as spam.",
    ],
}


def judge_response(response: str, category: str):
    # Similarity judge method
    structured_llm = llm.with_structured_output(SimilarityScoreOutput)
    examples = RESPONSE_EXAMPLES[category]
    result: SimilarityScoreOutput = structured_llm.invoke(
        f"""
        Score how similar this response is to the examples.

        Category: {category}

        Examples:
        {"\n".join(examples)}

        Response to evaluate:
        {response}

        Scoring criteria:
        - 90-100: Very similar in tone, content, and intent
        - 70-89: Similar with minor differences
        - 50-69: Moderately similar, captures main idea
        - 30-49: Some similarity but missing key elements
        - 0-29: Very different or inappropriate
        """
    )

    return result.similarity_score


@pytest.mark.parametrize(
    "email, expected_category, min_score, max_score",
    [
        ("This is urgent!", "urgent", 8, 10),
        ("I wanna talk to you", "normal", 4, 7),
        ("I have an offer for you", "spam", 1, 3),
    ],
)
def test_full_graph(email, expected_category, min_score, max_score):
    result = graph.invoke({"email": email}, config={"configurable": {"thread_id": "1"}})

    assert result["category"] == expected_category
    assert min_score <= result["priority_score"] <= max_score


# only one node test
def test_individual_nodes():
    # categorize_email
    result = graph.nodes["categorize_email"].invoke(
        {"email": "Check out this offer"}, config={"configurable": {"thread_id": "1"}}
    )
    assert result["category"] == "spam"

    # assign_priority
    result = graph.nodes["assign_priority"].invoke(
        {"category": "spam", "email": "buy this pot."},
        config={"configurable": {"thread_id": "1"}},
    )
    assert 1 <= result["priority_score"] <= 3

    # draft_response
    result = graph.nodes["draft_response"].invoke(
        {
            "category": "spam",
            "email": "I have a great offer for you!",
            "priority_score": 1,
        },
        config={"configurable": {"thread_id": "1"}},
    )

    similarity_score = judge_response(result["response"], "spam")
    assert similarity_score >= 80


# Partial graph test
def test_partial_execution():
    from main import categorize_email, draft_response

    graph.update_state(
        config={"configurable": {"thread_id": "1"}},
        values={
            "email": "Get rich quick!!! I have a pyramid scheme for you!",
            "category": "spam",
        },  # 이미 값이 주어져서 진행된 것처럼 가장할 수 있다.
        as_node=categorize_email.__name__,  # categorize_email 노드인 척하기
    )

    result = graph.invoke(
        None,
        config={"configurable": {"thread_id": "1"}},
        interrupt_after=draft_response.__name__,  # 테스트에서 유용한 인터럽트
    )

    assert 1 <= result["priority_score"] <= 3
