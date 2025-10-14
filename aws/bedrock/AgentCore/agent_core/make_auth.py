from dotenv import load_dotenv

load_dotenv()

import boto3
import os


REGION = os.getenv("REGION", "us-east-1")


def create_cognito_for_agent(agent_name: str):
    """
    Cognito User Pool + Client 생성 후 discovery_url과 client_id 반환
    """
    cognito = boto3.client("cognito-idp", region_name=REGION)

    # 1️⃣ User Pool 생성
    user_pool_name = f"{agent_name}-test-pool"
    pool_resp = cognito.create_user_pool(
            PoolName=user_pool_name,
            Policies={
                "PasswordPolicy": {
                    "MinimumLength": 8,
                    "RequireUppercase": True,
                    "RequireNumbers": True,
                "RequireSymbols": False,
            }
        },
    )
    user_pool_id = pool_resp["UserPool"]["Id"]
    print(f"✅ Created User Pool: {user_pool_id}")

    # 2️⃣ User Pool Client 생성
    client_name = f"{agent_name}-client"
    client_resp = cognito.create_user_pool_client(
        UserPoolId=user_pool_id,
        ClientName=client_name,
        GenerateSecret=False,
        ExplicitAuthFlows=["ALLOW_USER_PASSWORD_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"],
    )
    client_id = client_resp["UserPoolClient"]["ClientId"]

    # 3️⃣ Discovery URL
    discovery_url = f"https://cognito-idp.{REGION}.amazonaws.com/{user_pool_id}/.well-known/openid-configuration"

    print(f"✅ Cognito User Pool ID: {user_pool_id}")
    print(f"✅ Cognito Client ID: {client_id}")
    print(f"✅ Discovery URL: {discovery_url}")

    return user_pool_id, discovery_url, client_id


if __name__ == "__main__":
    # 테스트 실행
    agent_name = os.getenv("AGENT_NAME", "luke_mcp")
    create_cognito_for_agent(agent_name)
