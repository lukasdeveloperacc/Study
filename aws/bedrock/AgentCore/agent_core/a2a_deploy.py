from dotenv import load_dotenv

load_dotenv()

from botocore.exceptions import ClientError

import boto3
import os


client = boto3.client("bedrock-agentcore-control", region_name="us-east-1")

agent_runtime_name = os.getenv("AGENT_NAME")
container_uri = os.getenv("CONTAINER_URI")
role_arn = os.getenv("ROLE_ARN")
server_protocol = "MCP"  # MCP | HTTP

# Auth of Cognito
discovery_url = os.getenv("COGNITO_DISCOVERY_URL")
client_id = os.getenv("COGNITO_CLIENT_ID")

try:
    response = client.create_agent_runtime(
        agentRuntimeName=agent_runtime_name,
        agentRuntimeArtifact={
            "containerConfiguration": {"containerUri": container_uri}
        },
        networkConfiguration={"networkMode": "PUBLIC"},
        roleArn=role_arn,
        protocolConfiguration={"serverProtocol": server_protocol},
        authorizerConfiguration={
            "customJWTAuthorizer": {
                "discoveryUrl": discovery_url,
                "allowedClients": [client_id],
            }
        },
    )

except ClientError as e:
    if e.response["Error"]["Code"] == "ConflictException":
        print("Agent Runtime already exists")
        response = client.list_agent_runtimes()
        runtime_id = [
            runtime["agentRuntimeId"]
            for runtime in response["agentRuntimes"]
            if runtime["agentRuntimeName"] == agent_runtime_name
        ][0]
        response = client.update_agent_runtime(
            agentRuntimeId=runtime_id,
            agentRuntimeArtifact={
                "containerConfiguration": {"containerUri": container_uri}
            },
            networkConfiguration={"networkMode": "PUBLIC"},
            roleArn=role_arn,
            protocolConfiguration={"serverProtocol": server_protocol},
            authorizerConfiguration={
                "customJWTAuthorizer": {
                    "discoveryUrl": discovery_url,
                    "allowedClients": [client_id],
                }
            },
        )
    else:
        raise e

except Exception as e:
    print(e)
    raise e

print(f"Agent Runtime created successfully!")
print(f"Agent Runtime ARN: {response['agentRuntimeArn']}")
print(f"Status: {response['status']}")
