from dotenv import load_dotenv
import boto3, json, os
from botocore.exceptions import ClientError

load_dotenv()

account_id = os.getenv("ACCOUNT_ID")
region = os.getenv("REGION", "us-east-1")
agent_name = os.getenv("AGENT_NAME")
role_name = f"AgentCoreRuntimeRole-{agent_name}"

iam = boto3.client("iam", region_name=region)

trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowAgentCoreAssumeRole",
            "Effect": "Allow",
            "Principal": {"Service": "bedrock-agentcore.amazonaws.com"},
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {"aws:SourceAccount": account_id},
                "ArnLike": {
                    "aws:SourceArn": f"arn:aws:bedrock-agentcore:{region}:{account_id}:*"
                },
            },
        }
    ],
}

def ensure_role():
    try:
        iam.get_role(RoleName=role_name)
        print(f"✅ Role {role_name} already exists, updating trust policy...")
        iam.update_assume_role_policy(
            RoleName=role_name, PolicyDocument=json.dumps(trust_policy)
        )
    except iam.exceptions.NoSuchEntityException:
        print(f"🚀 Creating new IAM Role: {role_name}")
        iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="AgentCore Runtime execution role",
        )

    base_policies = [
        "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess",
        "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess",
        "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
        "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
    ]
    for policy_arn in base_policies:
        try:
            iam.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        except ClientError as e:
            if e.response["Error"]["Code"] != "EntityAlreadyExists":
                print(f"⚠️ Failed to attach policy {policy_arn}: {e}")

    print(f"🎯 IAM Role ready: arn:aws:iam::{account_id}:role/{role_name}")
    return f"arn:aws:iam::{account_id}:role/{role_name}"

if __name__ == "__main__":
    role_arn = ensure_role()
    print("✅ Final Role ARN:", role_arn)
