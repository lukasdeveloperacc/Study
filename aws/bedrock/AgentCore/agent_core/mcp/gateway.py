import boto3

def create_gateway():
    agent_core_client = boto3.client("bedrock-agentcore-control", region_name="us-east-1")
    gateway = agent_core_client.create_gateway(
        name="test-mcp-gateway",
        roleArn="arn:aws:iam::123456789012:role/MyAgentCoreServiceRole",
        protocolType="MCP",
        authorizerType="AWS_IAM"
    )
    
    return gateway

if __name__ == "__main__":
    gateway = create_gateway()
    print(gateway)
    
