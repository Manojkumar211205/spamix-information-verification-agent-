import asyncio
from typing import Optional
from contextlib import AsyncExitStack
import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
    async def connect_to_server(self, server_script_path: str = r"mcp_server/mcp_server.py"):
        """Connect to an MCP server over stdio."""
        try:
            if not os.path.isfile(server_script_path):
                raise FileNotFoundError(f"Server script not found: {server_script_path}")

            server_params = StdioServerParameters(
                command="python",
                args=[server_script_path],
                env=None,
            )

            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            self.stdio, self.protocol = stdio_transport
            self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.protocol))
            await self.session.initialize()

            # List available tools
            response = await self.session.list_tools()
            tools = response.tools
            print(f"Available tools: {[tool.name for tool in tools]}")
            for tool in tools:
                print(f"- {tool.name}: {tool.description}")

        except Exception as e:
            print(f"Error connecting to server: {e}")
            raise
    async def tools_available(self):
        # List available tools
            response = await self.session.list_tools()
            tools = response.tools
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
    async def call_tool_manually(self, tool_name: str, tool_args: dict):
        """Manually call a tool with the given arguments.

        Args:
            tool_name: Name of the tool to call (e.g., 'check_url')
            tool_args: Dictionary of arguments for the tool (e.g., {'url': 'https://example.com'})
        """
        try:
            result = await self.session.call_tool(tool_name, tool_args)
            
            # Parse the result content to get the actual JSON
            if result.content and len(result.content) > 0:
                content = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                try:
                    # Try to parse as JSON for better formatting
                    import json
                    parsed_result = json.loads(content)
                  
                    return parsed_result
                except json.JSONDecodeError:
                    # If not JSON, print as is
                    print(f"\nResult from {tool_name}: {content}")
            else:
                print(f"\nResult from {tool_name}: No content returned")
        except Exception as e:
            
            print(f"\nError calling tool {tool_name}: {str(e)}")

    async def cleanup(self):
        """Clean up resources."""
        try:
            await self.exit_stack.aclose()
        except Exception as e:
          pass

async def main():
    """Example usage of the MCP client with fact checking."""
    client = MCPClient()
    
    try:
        # Connect to the MCP server
        await client.connect_to_server()
        
        # Example 1: Check a URL for security threats
        print("\n=== Checking URL Security ===")
        await client.call_tool_manually("check_url", {"url": "https://example.com"})
        
        # Example 2: Scrape a webpage
        print("\n=== Scraping Webpage ===")
        await client.call_tool_manually("scrape_webpage", {"url": "https://example.com"})
        
        # Example 3: Combined fact-check (Google + Reddit in single JSON)
        test_statement = "The Earth is round"
        print(f"\n=== Combined Fact Check: '{test_statement}' ===")
        await client.call_tool_manually("fact_check", {"statement": test_statement})
        
        # Example 4: Combined fact-check for another statement
        test_statement2 = "Python is the best programming language"
        print(f"\n=== Combined Fact Check: '{test_statement2}' ===")
        await client.call_tool_manually("fact_check", {"statement": test_statement2, "reddit_limit": 5})
        
        # Example 5: Research a topic using ArXiv and Wikipedia
        research_query = "quantum computing applications"
        print(f"\n=== Research: '{research_query}' ===")
        await client.call_tool_manually("research", {"query": research_query})
        
        # Example 6: Research with custom limits
        research_query2 = "artificial intelligence in medicine"
        print(f"\n=== Research with Custom Limits: '{research_query2}' ===")
        await client.call_tool_manually("research", {"query": research_query2, "arxiv_max_results": 5, "wikipedia_max_results": 3})
        
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())

