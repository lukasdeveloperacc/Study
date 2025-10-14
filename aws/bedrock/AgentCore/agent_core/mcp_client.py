from dotenv import load_dotenv

load_dotenv()

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from agent_core.mcp.utils import get_token

import asyncio
import os
import sys


async def remote_main():
    agent_runtime_name = os.getenv("AGENT_NAME")
    region = os.getenv("REGION")

    bearer_token = get_token(
        os.getenv("COGNITO_USER_POOL_ID"),
        os.getenv("COGNITO_USERNAME"),
        os.getenv("COGNITO_PASSWORD"),
        os.getenv("COGNITO_CLIENT_ID"),
        os.getenv("REGION"),
    )
    print(f"✅ Got Access Token: {bearer_token[:30]}...")

    if not agent_runtime_name or not bearer_token:
        print("Error: AGENT_RUNTIME_NAME or BEARER_TOKEN environment variable is not set")
        sys.exit(1)


    agent_arn = os.getenv("AGENT_ARN")
    encoded_arn = agent_arn.replace(":", "%3A").replace("/", "%2F")
    mcp_url = f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{encoded_arn}/invocations?qualifier=DEFAULT"
    headers = {
        "authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }
    print(f"Invoking: {mcp_url}, \nwith headers: {headers}\n")

    async with streamablehttp_client(
        mcp_url, headers, timeout=120, terminate_on_close=False
    ) as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tool_result = await session.list_tools()
            print(tool_result)


if __name__ == "__main__":
    asyncio.run(remote_main())
