from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from firecrawl import Firecrawl
from env import FIRECRAWL_API_KEY


def _web_search(query: str):
    firecrawl = Firecrawl(api_key=FIRECRAWL_API_KEY)

    response = firecrawl.search(
        query, limit=5, integration="crewai"
    )  # integration : 통합할 플랫폼 지정해주면 잘 맞춰서 출력해줌.

    if not response:
        return f"No search results found for query: {query}"

    search_results = []

    if response.web:
        for result in response.web:
            title = getattr(result, "title", "No Title")
            url = getattr(result, "url", "")
            description = getattr(result, "description", "")

            search_results.append(
                {
                    "title": title,
                    "url": url,
                    "content": (
                        description[:500] + "..."
                        if len(description) > 500
                        else description
                    ),
                }
            )
        search_result = {
            "query": query,
            "results_count": len(search_results),
            "results": search_results,
        }
        return search_result


class WebSearchToolInput(BaseModel):
    """Input schema for WebSearchTool."""

    query: str = Field(..., description="The search query to look for.")


class WebSearchTool(BaseTool):
    name: str = "web_search_tool"
    description: str = (
        "Searches the web for information based on a query and returns relevant results with titles, URLs, and content snippets."
    )
    args_schema: Type[BaseModel] = WebSearchToolInput

    def _run(self, query: str):
        return _web_search(query)


web_search_tool = WebSearchTool()
