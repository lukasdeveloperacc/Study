from dotenv import load_dotenv
from botocore.exceptions import ClientError
import boto3
import os

load_dotenv()

client = boto3.client("bedrock-agentcore-control", region_name="us-east-1")

agent_runtime_name = ""
container_uri = ""
role_arn = ""
openai_api_key = os.getenv("OPENAI_API_KEY")

try:
    response = client.create_agent_runtime(
        agentRuntimeName=agent_runtime_name,
        agentRuntimeArtifact={
            "containerConfiguration": {"containerUri": container_uri}
        },
        networkConfiguration={"networkMode": "PUBLIC"},
        roleArn=role_arn,
        environmentVariables={"OPENAI_API_KEY": openai_api_key},
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
            environmentVariables={"OPENAI_API_KEY": openai_api_key},
        )
    else:
        raise e

except Exception as e:
    print(e)
    raise e

print(f"Agent Runtime created successfully!")
print(f"Agent Runtime ARN: {response['agentRuntimeArn']}")
print(f"Status: {response['status']}")

# update : https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_agent_runtime.html
