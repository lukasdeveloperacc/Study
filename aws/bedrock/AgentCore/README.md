# Reference
- [AWS docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-getting-started-toolkit.html)

# Using starter toolkit
## Export requirements.txt
```bash
uv pip compile pyproject.toml -o requirements.txt
```

## Configure
```bash
uv run agentcore configure --entrypoint agent_core_with_starter_toolkit.py --region us-east-1
```
- Need role arn

## Launch
```bash
uv run agentcore launch -l --env OPENAI_API_KEY=...
```
- locally

```bash
uv run agentcore launch --env OPENAI_API_KEY=...
```
- cloud

## Test
```bash
uv run agentcore invoke '{"prompt": "Hello"}'

{"qa": {"answer": "Hello! How can I assist you today?"}}
```
- test

# Not using starter toolkit
## Agent contract requirements
- /invocations Endpoint: POST endpoint for agent interactions (REQUIRED)
- /ping Endpoint: GET endpoint for health checks (REQUIRED)
- Docker Container: ARM64 containerized deployment package

## Local Test
```bash
uv run uvicorn agent_core_without_starter_toolkit:app --port 1234 --reload
```

```bash
curl http://localhost:1234/ping
```

```bash
curl -X POST http://localhost:1234/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "input": {"prompt": "What is artificial intelligence?"}
  }'
```

## Docker
```bash
docker buildx create --use
```

```bash
docker buildx build -f Dockerfile.without_starter_toolkit --platform linux/arm64 -t my-agent:arm64 --load .
```

```bash
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_SESSION_TOKEN=""
export AWS_REGION=""
export OPENAI_API_KEY=""
```

```bash
docker run --platform linux/arm64 -p 8080:1234 \
  -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
  -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
  -e AWS_SESSION_TOKEN="$AWS_SESSION_TOKEN" \
  -e AWS_REGION="$AWS_REGION" \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  my-agent:arm64
```

```bash
curl http://localhost:1234/ping
```

```bash
curl -X POST http://localhost:1234/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "input": {"prompt": "What is artificial intelligence?"}
  }'
```

## ECR
```bash
aws ecr create-repository --repository-name <repo_name> --region us-east-1
```
- create repository in ECR

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account_id>.dkr.ecr.us-east-1.amazonaws.com
```
- login

```bash
docker buildx build -f Dockerfile.without_starter_toolkit --platform linux/arm64 -t <account_id>.dkr.ecr.us-east-1.amazonaws.com/<repo_name>:latest --push .
```
- push

```bash
aws ecr describe-images --repository-name <repo_name> --region us-east-1
```
- validation
