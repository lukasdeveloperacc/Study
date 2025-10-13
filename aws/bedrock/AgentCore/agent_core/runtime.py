from fastapi import FastAPI, HTTPException
from basic_agent.langgraph_agent import graph
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime, timezone


app = FastAPI()


class InvocationRequest(BaseModel):
    input: Dict[str, Any]


class InvocationResponse(BaseModel):
    output: Dict[str, Any]


@app.post("/invocations", response_model=InvocationResponse)
async def agent_invocation(request: InvocationRequest):
    """Handler for agent invocation"""
    try:
        user_message = request.input.get("prompt", "Hello Let's test AgentCore")
        if not user_message:
            raise HTTPException(
                status_code=400,
                detail="No prompt found in input. Please provide a 'prompt' key in the input.",
            )

        result = await graph.ainvoke({"question": user_message})
        answer = result["answer"]

        return InvocationResponse(
            output={
                "message": answer,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Agent processing failed: {str(e)}"
        )


@app.get("/ping")
async def ping():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
