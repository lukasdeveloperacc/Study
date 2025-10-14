# AgentCore Runtime
## Docker Image Push
```bash
REPO_NAME=luke_basic_agent
REGION=us-east-1
aws ecr create-repository --repository-name ${REPO_NAME} --region ${REGION}
```
- create repository in ECR

```bash
ACCOUNT_ID=207637378596
REGION=us-east-1
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com
```
- login

```bash
ACCOUNT_ID=207637378596
REGION=us-east-1
DOCKER_IMAGE_NAME=luke_basic_agent

docker build --platform linux/arm64 -f agent_core/Dockerfile.runtime -t ${DOCKER_IMAGE_NAME}:latest .
docker tag ${DOCKER_IMAGE_NAME}:latest ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${DOCKER_IMAGE_NAME}:latest
docker push ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${DOCKER_IMAGE_NAME}:latest
```

### Deploy
```bash
uv run agent_core/runtime_deploy.py
```

## AgentCore MCP
### Docker Image Push
```bash
REPO_NAME=luke_mcp
REGION=us-east-1
aws ecr create-repository --repository-name ${REPO_NAME} --region ${REGION}
```
- create repository in ECR

```bash
ACCOUNT_ID=207637378596
REGION=us-east-1
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com
```
- login

```bash
ACCOUNT_ID=207637378596
REGION=us-east-1
DOCKER_IMAGE_NAME=luke_mcp

docker build --platform linux/arm64 -f agent_core/Dockerfile.mcp -t ${DOCKER_IMAGE_NAME}:latest .
docker tag ${DOCKER_IMAGE_NAME}:latest ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${DOCKER_IMAGE_NAME}:latest
docker push ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${DOCKER_IMAGE_NAME}:latest
```

### Deploy
```bash
uv run agent_core/mcp_deploy.py
```

### Test
```bash
uv run agent_core/mcp_client.py
```
