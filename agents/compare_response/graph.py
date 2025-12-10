from langgraph.graph import StateGraph, START
from states import ComparisonState
from nodes import intent_classifier_node, router_node, strands_node, deepagent_node


def create_smart_routing_graph():
    """스마트 라우팅 그래프 생성"""

    workflow = StateGraph(ComparisonState)

    # 노드 추가
    workflow.add_node("intent_classifier", intent_classifier_node)

    workflow.add_node("router", router_node)
    workflow.add_node("strands", strands_node)
    workflow.add_node("deepagent", deepagent_node)

    # 엣지 구성
    workflow.add_edge(START, "intent_classifier")
    workflow.add_edge("intent_classifier", "router")

    # Router에서 조건부 분기
    workflow.add_conditional_edges(
        "router",
        lambda s: s["user_intent"],
        {"strands_only": "strands", "deepagent_only": "deepagent", "compare_both": "strands"},
    )

    return workflow.compile()


if __name__ == "__main__":

    async def run_with_natural_language(query: str):
        """자연어 쿼리로 실행"""

        app = create_smart_routing_graph()

        print(f"\n{'='*70}")
        print(f"💬 사용자 쿼리: {query}")
        print(f"{'='*70}")

        result = await app.ainvoke(
            {
                "query": query,
                "user_intent": None,
                "actual_query": None,
                "strands_response": None,
                "strands_time": None,
                "strands_tool_calls": None,
                "deepagent_response": None,
                "deepagent_time": None,
                "deepagent_plan": None,
                "comparison_report": None,
            }
        )

        # 결과 출력
        print(f"\n{'='*70}")
        print(f"📝 실행 결과")
        print(f"{'='*70}")

        if result["strands_response"]:
            print(f"\n🔵 Strands 응답:")
            print(f"   {result['strands_response']}")
            print(f"   실행 시간: {result['strands_time']:.2f}초")

        if result["deepagent_response"]:
            print(f"\n🟢 Deep Agent 응답:")
            print(f"   {result['deepagent_response']}")
            print(f"   실행 시간: {result['deepagent_time']:.2f}초")

    import asyncio

    test_queries = ["Strands Agent로 최근 강남구청 맛집 스케줄 만들어줘", "Deep Agent로 강남구청 맛집 스케줄 만들어줘"]

    print("=" * 70)
    print("Strands Agent")
    print("=" * 70)
    asyncio.run(run_with_natural_language(test_queries[0]))

    print("\n\n" + "=" * 70)
    print("Deep Agent")
    print("=" * 70)
    asyncio.run(run_with_natural_language(test_queries[1]))
