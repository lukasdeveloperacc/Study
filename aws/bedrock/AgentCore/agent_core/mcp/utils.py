from dotenv import load_dotenv
import boto3, os

load_dotenv()

def get_token(cognito_user_pool_id: str, cognito_user_name: str, cognito_user_password: str, cognito_client_id: str, aws_region: str):
    cognito = boto3.client("cognito-idp", region_name=aws_region)

    try:
        cognito.admin_create_user(
            UserPoolId=cognito_user_pool_id,
            Username=cognito_user_name,
            TemporaryPassword=cognito_user_password,
            MessageAction="SUPPRESS",
        )
        print(f"✅ Created temporary user: {cognito_user_name}")

        cognito.admin_set_user_password(
            UserPoolId=cognito_user_pool_id,
            Username=cognito_user_name,
            Password=cognito_user_password,
            Permanent=True,
        )
        print("✅ Set permanent password")

    except Exception as e:
        print(f"⚠️ Failed to create user: {e}")

    bearer_token = ""
    try:    
        auth_resp = cognito.initiate_auth(
            ClientId=cognito_client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": cognito_user_name,
                "PASSWORD": cognito_user_password,
            },
        )
        bearer_token = auth_resp["AuthenticationResult"]["AccessToken"]
        print(f"✅ Got Access Token: {bearer_token[:30]}...")

    except Exception as e:
        print(f"⚠️ Failed to get token: {e}")

    return bearer_token
    