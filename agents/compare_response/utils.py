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
