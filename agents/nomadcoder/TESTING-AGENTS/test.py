from main import graph

import pytest


@pytest.mark.parametrize(
    "email, expected_category, expected_score",
    [
        ("This is urgent!", "urgent", 10),
        ("I wanna talk to you", "normal", 5),
        ("I have an offer for you", "spam", 1),
    ],
)
def test_full_graph(email, expected_category, expected_score):
    result = graph.invoke({"email": email}, config={"configurable": {"thread_id": "1"}})

    assert result["category"] == expected_category
    assert result["priority_score"] == expected_score


# only one node test
def test_individual_nodes():
    # categorize_email
    result = graph.nodes["categorize_email"].invoke(
        {"email": "Check out this offer"}, config={"configurable": {"thread_id": "1"}}
    )
    assert result["category"] == "spam"

    # assign_priority
    result = graph.nodes["assign_priority"].invoke(
        {"category": "spam"}, config={"configurable": {"thread_id": "1"}}
    )
    assert result["priority_score"] == 1

    # draft_response
    result = graph.nodes["draft_response"].invoke(
        {"category": "spam"}, config={"configurable": {"thread_id": "1"}}
    )
    assert "Go away!" in result["response"]


# Partial graph test
def test_partial_execution():
    from main import categorize_email, draft_response

    graph.update_state(
        config={"configurable": {"thread_id": "1"}},
        values={
            "email": "Please check out this offer",
            "category": "spam",
        },  # 이미 값이 주어져서 진행된 것처럼 가장할 수 있다.
        as_node=categorize_email.__name__,  # categorize_email 노드인 척하기
    )

    result = graph.invoke(
        None,
        config={"configurable": {"thread_id": "1"}},
        interrupt_after=draft_response.__name__,  # 테스트에서 유용한 인터럽트
    )

    assert result["priority_score"] == 1
