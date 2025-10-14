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

    cognito = boto3.client("cognito-idp", region_name=region)
    print(os.getenv("COGNITO_USER_POOL_ID"))
    print(os.getenv("COGNITO_CLIENT_ID"))
    print(os.getenv("COGNITO_USERNAME"))
    print(os.getenv("COGNITO_PASSWORD"))
    try:
        # 3️⃣ 유저 생성 (임시 비밀번호)
        cognito.admin_create_user(
            UserPoolId=os.getenv("COGNITO_USER_POOL_ID"),
            Username=os.getenv("COGNITO_USERNAME", "luke"),
            TemporaryPassword=os.getenv("COGNITO_PASSWORD", "1234"),
            MessageAction="SUPPRESS",
        )
        print(f"✅ Created temporary user: {os.getenv("COGNITO_USERNAME", "luke")}")

        # 4️⃣ 비밀번호를 영구 비밀번호로 변경
        cognito.admin_set_user_password(
            UserPoolId=os.getenv("COGNITO_USER_POOL_ID"),
            Username=os.getenv("COGNITO_USERNAME", "luke"),
            Password=os.getenv("COGNITO_PASSWORD", "1234"),
            Permanent=True,
        )
        print("✅ Set permanent password")

    except Exception as e:
        print(f"⚠️ Failed to create user: {e}")

    auth_resp = cognito.initiate_auth(
        ClientId=os.getenv("COGNITO_CLIENT_ID"),
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": os.getenv("COGNITO_USERNAME", "luke"),
            "PASSWORD": os.getenv("COGNITO_PASSWORD", "1234"),
        },
    )
    bearer_token = auth_resp["AuthenticationResult"]["AccessToken"]
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
