from langchain_mcp_adapters.client import MultiServerMCPClient
from agent_core.mcp.utils import get_token

import os
import sys
import asyncio

region = os.getenv("REGION")
agent_arn = os.getenv("AGENT_ARN")
encoded_arn = agent_arn.replace(":", "%3A").replace("/", "%2F")
agent_core_url = f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{encoded_arn}/invocations?qualifier=DEFAULT"

bearer_token = get_token(
        os.getenv("COGNITO_USER_POOL_ID"),
        os.getenv("COGNITO_USERNAME"),
        os.getenv("COGNITO_PASSWORD"),
        os.getenv("COGNITO_CLIENT_ID"),
        os.getenv("REGION"),
    )
print(f"✅ Got Access Token: {bearer_token[:30]}...")

if not bearer_token:
    print("Error: BEARER_TOKEN environment variable is not set")
    sys.exit(1)

headers = {
    "authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json",
}

client = MultiServerMCPClient(
    {
        "agent_core": {
            "url": agent_core_url,
            "transport": "streamable_http",
            "headers": headers,
        }
    }
)

def get_mcp_tools():
    return asyncio.run(client.get_tools())

