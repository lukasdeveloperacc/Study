from bedrock_agentcore.runtime import BedrockAgentCoreApp
from custom_langgraph import graph


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
