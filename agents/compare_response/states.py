from typing import TypedDict, Literal


class ComparisonState(TypedDict):
    query: str
    user_intent: Literal["strands_only", "deepagent_only", "compare_both"] | None
    actual_query: str | None  # 의도 제거한 실제 쿼리

    strands_response: str | None
    strands_time: float | None

    deepagent_response: str | None
    deepagent_time: float | None
    deepagent_plan: list | None

    comparison_report: dict | None
