def create_strands_agent():
    """
    Strands Agent: Model-driven approach
    - LLM이 자율적으로 추론하고 도구 선택
    - 가벼운 에이전트 루프
    - 최소한의 추상화
    """
    from strands import Agent
    from strands.models.openai import OpenAIModel

    model = OpenAIModel(model_id="gpt-5.1-2025-11-13", region="ap-northeast-2")

    agent = Agent(
        model=model,
        system_prompt="""You are an efficient AI assistant.        
Analyze the query and use the available tools as needed to provide 
a clear, direct answer. Be practical and efficient.""",
    )

    return agent


def create_deep_agent_graph():
    """
    Deep Agent: Planning + Sub-agents + File System
    """
    from deepagents import create_deep_agent
    from langchain.chat_models import init_chat_model

    model = init_chat_model(model="gpt-5.1-2025-11-13")

    # Research sub-agent
    research_subagent = {
        "name": "research-specialist",
        "description": "Deep research and comprehensive analysis",
        "system_prompt": "You are a research specialist. Conduct thorough analysis.",
    }

    # Deep Agent 생성
    agent = create_deep_agent(
        model=model,
        subagents=[research_subagent],
        system_prompt="""You are a Deep Agent - systematic and thorough.

Your workflow:
1. PLAN: Use write_todos to create a structured plan
2. RESEARCH: Investigate systematically using available tools
3. DELEGATE: Use research-specialist for deep analysis when needed
4. DOCUMENT: Store findings in files for reference
5. SYNTHESIZE: Create comprehensive, well-researched responses

Take time to think deeply and provide thorough answers.""",
    )

    return agent


def extract_reasoning_from_strands(response):
    """Strands의 추론 과정 추출"""
    if hasattr(response, "reasoning_trace"):
        return response.reasoning_trace
    return "LLM autonomous reasoning"


def extract_plan_from_deep(result):
    """Deep Agent의 todo list 추출"""
    for msg in result.get("messages", []):
        if isinstance(msg, dict) and "tool_calls" in msg:
            for call in msg["tool_calls"]:
                if call.get("name") == "write_todos":
                    return call.get("arguments", {}).get("todos", [])
    return []


def extract_subagent_calls_from_deep(result):
    """서브에이전트 호출 추출"""
    calls = []
    for msg in result.get("messages", []):
        if isinstance(msg, dict) and "tool_calls" in msg:
            for call in msg["tool_calls"]:
                if "subagent" in call.get("name", "").lower():
                    calls.append({"name": call.get("name"), "purpose": call.get("arguments", {})})
    return calls


def extract_file_operations_from_deep(result):
    """파일 작업 추출"""
    ops = []
    for msg in result.get("messages", []):
        if isinstance(msg, dict) and "tool_calls" in msg:
            for call in msg["tool_calls"]:
                tool_name = call.get("name", "")
                if any(x in tool_name for x in ["write_file", "read_file", "edit_file"]):
                    ops.append({"operation": tool_name, "details": call.get("arguments", {})})
    return ops
