from states import ComparisonState
from langgraph.types import Command
from langgraph.graph import END
from langchain_core.messages import AIMessage
from utils import create_strands_agent, create_deep_agent_graph


def intent_classifier_node(state: ComparisonState):
    """자연어에서 사용자 의도 파악"""

    query = state["query"].lower()

    # 키워드 기반 분류
    strands_keywords = [
        "strands",
        "스트랜즈",
    ]
    deepagent_keywords = [
        "deep agent",
        "딥에이전트",
    ]

    # 실제 쿼리 추출 (의도 표현 제거)
    actual_query = query
    intent = "compare_both"  # 기본값

    # 1. Strands 단독 요청 확인
    if any(keyword in query for keyword in strands_keywords):
        intent = "strands_only"
    elif any(keyword in query for keyword in deepagent_keywords):
        intent = "deepagent_only"
    else:
        intent = "deepagent_only"

    # 실제 쿼리 정리
    actual_query = actual_query.strip()
    if not actual_query:
        actual_query = state["query"]  # 원본 유지

    print(f"\n🎯 Intent Analysis")
    print(f"   원본 쿼리: {state['query']}")
    print(f"   감지된 의도: {intent}")
    print(f"   실제 쿼리: {actual_query}")

    return Command(update={"user_intent": intent, "actual_query": actual_query}, goto="router")


def router_node(state: ComparisonState):
    """의도에 따라 라우팅"""

    intent = state["user_intent"]

    print(f"\n🔀 Routing to: {intent}")

    if intent == "strands_only":
        return Command(goto="strands")
    elif intent == "deepagent_only":
        return Command(goto="deepagent")
    else:
        raise ValueError(f"Unknown intent: {intent}")


def strands_node(state: ComparisonState):
    """Strands Agent 실행"""
    import time

    print(f"\n🔵 Strands Agent 실행 중...")
    start = time.time()

    # 실제 쿼리로 실행
    query = state["actual_query"]

    # Strands Agent 생성 및 실행
    strands_agent = create_strands_agent()
    response = strands_agent(query)

    execution_time = time.time() - start
    response = f"Strands 응답: {query}에 대한 빠르고 효율적인 답변"

    print(f"✅ Strands 완료 ({execution_time:.2f}초)")

    return Command(update={"strands_response": response, "strands_time": execution_time}, goto=END)


def deepagent_node(state: ComparisonState):
    """Deep Agent 실행"""
    import time

    print(f"\n🟢 Deep Agent 실행 중...")
    start = time.time()

    # 실제 쿼리로 실행
    query = state["actual_query"]

    deep_agent = create_deep_agent_graph()
    result = deep_agent.invoke({"messages": [{"role": "user", "content": query}]})
    message: AIMessage = result["messages"][-1]
    response = message.content

    execution_time = time.time() - start
    plan = ["1. 계획 수립", "2. 조사", "3. 분석"]

    print(f"✅ Deep Agent 완료 ({execution_time:.2f}초)")

    # Deep Agent만 실행
    return Command(
        update={"deepagent_response": response, "deepagent_time": execution_time, "deepagent_plan": plan}, goto=END
    )
