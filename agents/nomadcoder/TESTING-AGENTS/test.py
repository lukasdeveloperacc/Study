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
    result = graph.invoke({"email": email})

    assert result["category"] == expected_category
    assert result["priority_score"] == expected_score
