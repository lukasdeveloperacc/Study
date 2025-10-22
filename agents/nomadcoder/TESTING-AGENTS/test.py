from main import graph

import pytest


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
    # result = graph.nodes["draft_response"].invoke(
    #     {"category": "spam"}, config={"configurable": {"thread_id": "1"}}
    # )
    # assert "Go away!" in result["response"]


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

    assert 1 <= result["priority_score"] <= 3
