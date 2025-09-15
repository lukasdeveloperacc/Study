from crewai.tools import tool
from firecrawl import FirecrawlApp, ScrapeOptions

import os, re

@tool
def web_search_tool(query: str) -> str:
    """
    Web Search Tool.
    Args:
        query (str): The query to search the web for.
    Returns:
        A list of search results with the website content in Markdown format..
    """
    app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    response = app.search(
        query=query, 
        scrape_options=ScrapeOptions(formats=["markdown"]), 
        limit=5
    )

    if not response.success:
        return "Error using tool."
    
    cleaned_chunks = []
    for result in response.data:
        title = result["title"]
        url = result["url"]
        markdown = result["markdown"]

        cleaned = re.sub(r'\\+|\n+', '', markdown).strip() # decrease tokens
        cleaned = re.sub(r"\[[^\]]+\]\([^\)]+\)|https?://[^\s]+", "", cleaned) # remove links

        cleaned_result = {
            "title": title,
            "url": url,
            "markdown": cleaned
        }
        cleaned_chunks.append(cleaned_result)
    
    return cleaned_chunks
