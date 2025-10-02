from mcp.server.fastmcp import FastMCP
from custom_langgraph import graph

mcp = FastMCP(host="0.0.0.0", port=8000, stateless_http=True)


@mcp.tool()
async def custom_agent(user_message: str) -> str:
    """QA Agent"""
    result = await graph.ainvoke({"question": user_message})
    return result["answer"]


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
