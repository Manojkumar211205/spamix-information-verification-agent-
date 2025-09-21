from mcp.server.fastmcp import FastMCP
from .agent import *
from tools.tools.fact_checker import fact_checker
from tools.tools.research_tool import research_tool

# Initialize FastMCP server
mcp = FastMCP("custom_server")


async def start_server():
    """Start MCP server for in-process usage."""
    return mcp
@mcp.tool()
async def check_url(url: str) -> dict:
    """Check the status or content of a given URL.

    Args:
        url: The URL to check (e.g., https://example.com)
    """
    try:
        if not url:
            return {"error": "URL is required"}
        result =  agent_decide_and_run(url)
        return  result
    except Exception as e:
        return {"error": f"Failed to check URL: {str(e)}"}

@mcp.tool(name="scrape_webpage",description="gives the first 500 words of a webpage of the given url which we can what type of content the wepage has.")
async def scrape_url(url: str) :
    """Scrape a URL for content.

    Args:
        url: The URL to scrape (e.g., https://example.com)
    """
    try:
        if not url:
            return {"error": "URL is required"}
        result = WebScraper500Words().scrape_url(url)
        return result
    except Exception as e:
        return {"error": f"Failed to scrape URL: {str(e)}"}

@mcp.tool(name="fact_check", description="Check the veracity of a statement using both Google Fact Check Tools and Reddit content")
async def fact_check_statement(statement: str, reddit_limit: int = 10) -> dict:
    """Fact-check a statement using both Google Fact Check Tools and Reddit content.

    Args:
        statement: The statement to fact-check (e.g., "The Earth is flat")
        reddit_limit: Number of Reddit posts to search (default: 10)
    """
    try:
        if not statement:
            return {"error": "Statement is required"}
        result = fact_checker(statement, reddit_limit)
        return result
    except Exception as e:
        return {"error": f"Failed to fact-check statement: {str(e)}"}

@mcp.tool(name="research", description="Research a topic using ArXiv academic papers and Wikipedia articles")
async def research_topic(query: str, arxiv_max_results: int = 10, wikipedia_max_results: int = 5) -> dict:
    """Research a topic using both ArXiv and Wikipedia sources.

    Args:
        query: The research query (e.g., "machine learning in healthcare")
        arxiv_max_results: Maximum number of ArXiv papers to fetch (default: 10)
        wikipedia_max_results: Maximum number of Wikipedia articles to fetch (default: 5)
    """
    try:
        if not query:
            return {"error": "Query is required"}
        result = research_tool(query, arxiv_max_results, wikipedia_max_results)
        
        return result
    except Exception as e:
        return {"error": f"Failed to research topic: {str(e)}"}





