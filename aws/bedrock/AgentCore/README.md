# Reference
- [AWS docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-getting-started-toolkit.html)

# Export requirements.txt
```bash
uv pip compile pyproject.toml -o requirements.txt
```

# Configure
```bash
uv run agentcore configure --entrypoint agent_core.py --region us-east-1
```

# Launch
```bash
uv run agentcore launch
```

# Test
```bash
uv run agentcore invoke '{"prompt": "Hello"}'
```
