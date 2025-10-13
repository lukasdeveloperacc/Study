from dotenv import load_dotenv

load_dotenv()

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

import asyncio
import os
import sys
import boto3


async def remote_main():
    role_arn = os.getenv("ROLE_ARN")
    agent_runtime_name = os.getenv("AGENT_NAME")
    region = os.getenv("REGION")

    sts = boto3.client("sts")
    resp = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName="AgentCoreSession"
    )
    agentcore = boto3.client(
        "bedrock-agentcore", 
        region_name=region, 
        aws_access_key_id=resp["Credentials"]["AccessKeyId"], 
        aws_secret_access_key=resp["Credentials"]["SecretAccessKey"], 
        aws_session_token=resp["Credentials"]["SessionToken"]
    )
    
    token_resp = agentcore.get_workload_access_token(
        workloadName=agent_runtime_name
    )
    bearer_token = token_resp["accessToken"]
    expires_at = token_resp["expirationTime"]

    print("BEARER_TOKEN:", bearer_token)
    print("Expires at:", expires_at)

    # if not agent_arn or not bearer_token:
    #     print("Error: AGENT_ARN or BEARER_TOKEN environment variable is not set")
    #     sys.exit(1)

    # encoded_arn = agent_arn.replace(":", "%3A").replace("/", "%2F")
    # mcp_url = f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{encoded_arn}/invocations?qualifier=DEFAULT"
    # headers = {
    #     "authorization": f"Bearer {bearer_token}",
    #     "Content-Type": "application/json",
    # }
    # print(f"Invoking: {mcp_url}, \nwith headers: {headers}\n")

    # async with streamablehttp_client(
    #     mcp_url, headers, timeout=120, terminate_on_close=False
    # ) as (
    #     read_stream,
    #     write_stream,
    #     _,
    # ):
    #     async with ClientSession(read_stream, write_stream) as session:
    #         await session.initialize()
    #         tool_result = await session.list_tools()
    #         print(tool_result)


if __name__ == "__main__":
    asyncio.run(remote_main())
