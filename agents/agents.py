from .processor import *
import os
import sys
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcp_server.client import MCPClient

mcp_client = MCPClient()

async def init_mcp_connection():
    await mcp_client.connect_to_server(r"mcp_server\mcp_server.py")

async def close_mcp_connection():
    await mcp_client.cleanup()

async def link_verifier(user_input):
    print("Starting link verification...")
    
    links = link_extractor(user_input)
    print("Extracted links:", links)
    if not links:
        print("No links found in the input.")
        return

    tool_results = []
    for link in links:
        tool_args = {"url": link}
        verification = await mcp_client.call_tool_manually("check_url", tool_args)
        print("Result from check_url:", verification)
        tool_results.append(verification)
            
    verification_results = link_security_verifyer(tool_results)
    if verification_results == "malicious_detected":
        print("⚠️ Warning: Malicious link detected!")
        return
    elif verification_results == "all_safe":
        print("✅ All links are safe.")
        scraped_data = []
        for link in links:
            tool_args = {"url": link}
            scrape_result = await mcp_client.call_tool_manually("scrape_webpage", tool_args)
            print("Result from scrape_webpage:", scrape_result)
            if scrape_result.get("text"):
                scrape_result= scrape_result['text']
            scraped_data.append(scrape_result)
        print("Final scraped data:", scraped_data)

        return "\n\n\n".join(scraped_data)
    else:
        print("Unexpected verification result.")
        return
    

async def misinformation_checker(user_input):
    print("starting misinformation check ...")
    formated_input =  input_formator([],user_input)
    tools = await mcp_client.tools_available()
    orchestration = orchestrator(tools,formated_input)
    print("Orchestrator decision:", orchestration)
    tool_results = []
    for tool_call in orchestration:
        tool_name = tool_call.get("tool")
        tool_args = tool_call.get("args", {})
        result = await mcp_client.call_tool_manually(tool_name, tool_args)
        print(result)
        tool_results.append(result)
    
    miss_informations = []
    is_miss_info = True
    for results in tool_results:
        if not results["status"]:
            miss_informations.append(results['reason'])
        else:
            is_miss_info = False
            break
    if not is_miss_info:
        return "everything is correct or it is a normal conversational message"
    else:
        return "\n\n\n".join(miss_informations)

async def agent_handler(user_input):
    await init_mcp_connection()
    link_results = await link_verifier(user_input)
    print("Link verifier results:", link_results)

    misinformation_results = await misinformation_checker(user_input)
    print("Misinformation checker results:", misinformation_results)
    await close_mcp_connection()
    return misinformation_results



