import asyncio
from typing import Optional
import json
from .mcp_server import start_server   # Import your server directly


class MCPClient:
    def __init__(self):
        self.server = None   # This will hold your FastMCP server

    async def connect_to_server(self):
        """Connect directly to the in-process MCP server."""
        try:
            self.server = await start_server()
            tools = await self.server.list_tools()
            print(f"Available tools: {[tool.name for tool in tools]}")
            for tool in tools:
                print(f"- {tool.name}: {tool.description}")
        except Exception as e:
            print(f"Error connecting to server: {e}")
            raise

    async def tools_available(self):
        """List available tools with descriptions and input schemas."""
        tools = await self.server.list_tools()
        tool_descriptions = []
        for tool in tools:
            tool_descriptions.append(
                f"""
                Tool: {tool.name}
                Description: {tool.description.strip()}
                Input Schema: {tool.inputSchema}
                """
            )
        return "\n".join(tool_descriptions)

    def extract_text_content(self, result):
        """Extract text content from MCP TextContent objects or return as-is if already a dict."""
        if hasattr(result, 'text'):
            # It's a TextContent object, extract the text
            try:
                return json.loads(result.text)
            except json.JSONDecodeError:
                return {"result": result.text}
        elif isinstance(result, list) and len(result) > 0 and hasattr(result[0], 'text'):
            # It's a list of TextContent objects, extract the first one
            try:
                return json.loads(result[0].text)
            except json.JSONDecodeError:
                return {"result": result[0].text}
        else:
            # It's already a dict or other format, return as-is
            return result

    async def call_tool_manually(self, tool_name: str, tool_args: dict):
        """Manually call a tool with the given arguments."""
        try:
            result = await self.server.call_tool(tool_name, tool_args)
            
            # Extract clean content from MCP response for all tools
            clean_result = self.extract_text_content(result)
            return clean_result
            
        except Exception as e:
            print(f"\nError calling tool {tool_name}: {str(e)}")
            return {"error": str(e)}

    async def cleanup(self):
        """No-op cleanup for in-process server (kept for compatibility)."""
        pass


async def main():
    """Example usage of the MCP client with fact checking."""
    client = MCPClient()

    try:
        await client.connect_to_server()

        print("\n=== Checking URL Security ===")
        print(await client.call_tool_manually("check_url", {"url": "https://example.com"}))

        print("\n=== Scraping Webpage ===")
        print(await client.call_tool_manually("scrape_webpage", {"url": "https://example.com"}))

        test_statement = "The Earth is round"
        print(f"\n=== Combined Fact Check: '{test_statement}' ===")
        print(await client.call_tool_manually("fact_check", {"statement": test_statement}))

        test_statement2 = "Python is the best programming language"
        print(f"\n=== Combined Fact Check: '{test_statement2}' ===")
        print(await client.call_tool_manually("fact_check", {"statement": test_statement2, "reddit_limit": 5}))

        research_query = "quantum computing applications"
        print(f"\n=== Research: '{research_query}' ===")
        print(await client.call_tool_manually("research", {"query": research_query}))

        research_query2 = "artificial intelligence in medicine"
        print(f"\n=== Research with Custom Limits: '{research_query2}' ===")
        print(await client.call_tool_manually(
            "research",
            {"query": research_query2, "arxiv_max_results": 5, "wikipedia_max_results": 3}
        ))

    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())