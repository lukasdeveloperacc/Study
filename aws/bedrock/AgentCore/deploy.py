import boto3

# Create the client
client = boto3.client('bedrock-agentcore-control', region_name="us-east-1")

# Call the CreateAgentRuntime operation
response = client.create_agent_runtime(
    agentRuntimeName='hello_agent',
    agentRuntimeArtifact={
        'containerConfiguration': {
            'containerUri': '129231402580.dkr.ecr.us-east-1.amazonaws.com/agents:test'
        }
    },
    networkConfiguration={"networkMode":"PUBLIC"},
    roleArn='arn:aws:iam::129231402580:role/bedrock-role'
)
