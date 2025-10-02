from bedrock_agentcore.runtime import BedrockAgentCoreApp
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict

load_dotenv()

# 상태 정의
class AgentState(TypedDict):
    question: str
    answer: str

# LLM 준비
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 노드 정의: LLM에게 질의응답 시키기
def qa_node(state: AgentState):
    response = llm.invoke(state["question"])
    return {"answer": response.content}

# 그래프 구성
graph_builder = StateGraph(AgentState)
graph_builder.add_node("qa", qa_node)

graph_builder.set_entry_point("qa")
graph_builder.add_edge("qa", END)

graph = graph_builder.compile()

app = BedrockAgentCoreApp()

@app.entrypoint
async def agent_invocation(payload):
    """Handler for agent invocation"""
    user_message = payload.get("prompt", "Hello Let's test AgentCore")

    async for chunk in graph.astream({"question": user_message}):
        print(chunk)
        yield (chunk)

if __name__ == "__main__":
    app.run()
