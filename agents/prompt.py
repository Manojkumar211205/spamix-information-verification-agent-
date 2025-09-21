

class prompt:
    def __init__(self, tools_available=None):
        self.tools_available = tools_available

    def link_checker_prompt(self, user_input):
     return f"""You are a link extractor. 
            Your job is to analyze the user’s message, find all valid URLs (e.g., starting with http://, https://, or www.), and return them as a JSON list of strings. 
            If no link is found, return an empty list [].
            Do not include any explanation, only return the JSON list.

            User's message: {user_input}"""
    def input_formator_prompt(self,past_messages,current_message):
       return f"""
            You are a News Verification Agent.  
            Your task is to analyze the conversation history and the latest news input, then prepare a clean summarized flow that will be sent for fact-checking.

            ### Inputs:
            - Conversation history:
            {past_messages}

            - Current input (news to verify):
            {current_message}

            ### Task:
            1. Remove any URLs, links, or references to websites from both past messages and the current input.  
            2. Combine the remaining text into a single, coherent summary flow.  
            3. The summary should clearly state the **news claim** and any important context from past messages.  
            4. Do not add opinions. Keep it factual and concise.  
            5. Output only the summarized flow, which will be used in the next LLM call for verification.  

            ### Example:
            Past messages: ["We discussed fake images spreading on X", "Someone shared this link: https://example.com", "Now a claim about floods in Chennai"]  
            Current input: "Breaking: Entire Chennai city is under water after nonstop rain! More here: https://fakeurl.com"  

            Summary flow:  
            'Entire Chennai city is under water after nonstop rain,' in the context of discussions about fake images spreading on X.

            Now generate the summary flow:
            """
    def link_security_verifyer_prompt(self,verification_results):
       return f"""
                You are a strict Security Result Analyzer.

                ### Input:
                The following JSON contains the security results of multiple links:
                {verification_results}

                ### Task:
                1. Check all the links in the JSON.  
                2. If **any link** is marked as malicious, unsafe, or suspicious → output exactly:
                malicious_detected
                3. If **all links** are safe/clean → output exactly:
                all_safe

                ### Output Rules:
                - Return **only one word key**: either malicious_detected OR all_safe.  
                - Do NOT return sentences, JSON, explanations, quotes, or formatting.  
                - Your output must match one of the keys exactly.
                """
    def main_orchestration_prompt(self,tools_description,message):
       return f"""
                You are an AI agent for misinformation verification, processing community inputs in a Python environment. Your task is to analyze a given message and determine if it requires verification. Only verify messages containing public news, factual claims, statistics, research topics, or potential misinformation. Ignore casual messages like greetings, personal opinions without claims, meeting notes, or chit-chat (e.g., "Hi everyone," "Let's meet up," "I like this idea").

                ### Process:
                1. **Analyze the Message**: Read the input message carefully. Classify it:
                - If casual, non-factual, or not verifiable (e.g., social interactions, jokes, personal stories without claims), no tools are needed.
                - If it involves news, facts, statistics, historical events, scientific claims, or potential misinformation, proceed to select tools for verification.

                2. **Select Tools if Needed**: If verification is required, choose the minimal set of relevant tools from the available tools provided below to fact-check or gather evidence. Select tools that directly address the message's claims. For each tool, specify required arguments based on the message content.
                - Avoid unnecessary tool usage—only select tools essential for verification.
                - Tools can be used in parallel if multiple are needed (e.g., web search for facts + X search for real-time discussions).

                3. **Output Format**: 
                - Return ONLY a JSON array of objects, where each object represents a tool call.
                - Structure: [{{"tool": "tool_name", "args": {{"arg1": "value1", "arg2": "value2", ...}}}}, ...]
                - If no tools are needed (casual message or no verification required), return an empty array: []
                - Do not include explanations, reasoning, or text outside the JSON array.

                ### Available Tools for Verification:
                {tools_description}

                ### Input Message:
                {message}

                ### Output:
                - Analyze the message and output ONLY a JSON array as specified, using Python's json module for serialization if needed.
                - Example: `[{{"tool": "web_search", "args": {{"query": "claim to verify", "num_results": 10}}}}]` or `[]`
                """

