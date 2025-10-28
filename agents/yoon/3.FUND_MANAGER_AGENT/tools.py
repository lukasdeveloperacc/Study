import yfinance as yf
from typing import Type
from crewai.tools import BaseTool
from firecrawl import Firecrawl
from pydantic import BaseModel, Field
from env import FIRECRAWL_API_KEY


def _yahoo_finance(ticker: str, period: str = "1y"):

    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)
        info = stock.info

        if history.empty:
            return f"No historical data found for ticker: {ticker}"

        current_price = history["Close"].iloc[-1] if not history.empty else None
        year_high = history["High"].max()
        year_low = history["Low"].min()

        revenue_growth = "N/A"
        try:
            financials = stock.financials
            if not financials.empty and "Total Revenue" in financials.index:
                revenues = financials.loc["Total Revenue"].dropna()
                if len(revenues) >= 2:
                    latest_revenue = revenues.iloc[0]
                    prev_revenue = revenues.iloc[1]
                    revenue_growth = (
                        f"{((latest_revenue - prev_revenue) / prev_revenue * 100):.2f}%"
                    )
        except Exception:
            pass

        company_data = {
            "ticker": ticker,
            "company_name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "current_price": float(current_price) if current_price else None,
            "52_week_high": float(year_high),
            "52_week_low": float(year_low),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "forward_pe": info.get("forwardPE", "N/A"),
            "price_to_book": info.get("priceToBook", "N/A"),
            "revenue_growth": revenue_growth,
            "profit_margin": info.get("profitMargins", "N/A"),
            "operating_margin": info.get("operatingMargins", "N/A"),
            "debt_to_equity": info.get("debtToEquity", "N/A"),
            "return_on_equity": info.get("returnOnEquity", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "business_summary": (
                info.get("longBusinessSummary", "N/A")[:500] + "..."
                if info.get("longBusinessSummary")
                and len(info.get("longBusinessSummary", "")) > 500
                else info.get("longBusinessSummary", "N/A")
            ),
        }

        return company_data

    except Exception as e:
        return f"Error retrieving data for {ticker}: {e}"


class YahooFinanceInput(BaseModel):
    ticker: str = Field(
        ...,
        description="The stock ticker symbol for the company to look up. For example, 'AAPL' for Apple or '005930.KS' for Samsung Electronics.",
    )
    period: str = Field(
        "1y",
        description="The time period for historical data, used to calculate highs and lows. Defaults to '1y'. Valid formats: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'.",
    )


class YahooFinanceTool(BaseTool):
    name: str = "yahoo_finance_tool"
    description: str = """
    Use this tool to get comprehensive financial data and company information for a specific stock ticker from Yahoo Finance.
    It provides a full snapshot including current price, historical high/low for the period, valuation metrics (P/E, P/B), dividend yield, market cap, and a business summary.
    This is extremely useful for fundamental analysis or when a user asks for detailed information about a company, not just its stock price.
    """
    args_schema: Type[BaseModel] = YahooFinanceInput

    def _run(self, ticker: str, period: str = "1y"):
        return _yahoo_finance(ticker, period)


def _web_search(query: str):
    firecrawl = Firecrawl(api_key=FIRECRAWL_API_KEY)

    response = firecrawl.search(query, limit=5, integration="crewai")

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
                    "content": description,
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
yahoo_finance_tool = YahooFinanceTool()


if __name__ == "__main__":
    test_tickers = ["NVDA", "GOOGL", "TSLA"]
    for ticker in test_tickers:
        print(f"{ticker}")
        print("\n")
        result = _yahoo_finance(ticker)
        print(result)
        print("\n")
