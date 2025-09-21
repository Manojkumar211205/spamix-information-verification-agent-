from .prompt import prompt
from .llms import gemini_LLM_interface
import json
import re

prompts = prompt(tools_available=[])

def extract_json_for_orchestrator(text: str):
    """
    Extracts the first JSON block from text (including ```json fences).
    Returns a Python object (list/dict).
    """
    # Try to find fenced JSON block
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # If no fenced block, assume whole text is JSON
        json_str = text.strip()

    # Parse JSON safely
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}\nExtracted: {json_str}")

def parse_links(output):
    """Parse links from LLM output using multiple strategies."""
    
    # 1. Direct JSON parse
    try:
        
        return json.loads(output)
    except json.JSONDecodeError:
        pass

    # 2. Handle code blocks
    try:
        print("second attempt to parse json with code block handling")
        cleaned = output.strip()
        if cleaned.startswith("```") and cleaned.endswith("```"):
            cleaned = "\n".join(cleaned.splitlines()[1:-1])
            return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # 3. Regex: Extract the first JSON-like list from text
    try:
        print("third attempt: regex JSON list")
        match = re.search(r"\[.*\]", output, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass

    # 4. Regex fallback: Extract URLs directly
    print("fourth attempt: regex URLs")
    urls = re.findall(r'(https?://[^\s"\']+|www\.[^\s"\']+)', output)
    if urls:
        return urls

    # 5. Nothing found
    return []    
   

def link_extractor(user_input):
    """extract links from user input using LLM.
    
    Keyword arguments:
    user_input -- the input text from which to extract links
    Return: a list of extracted links
    """
    print(user_input)
    prompt =  prompts.link_checker_prompt(user_input)
    response = gemini_LLM_interface(prompt)
    links = parse_links(response)
    print("Extracted links:", links)
    return links

def input_formator(past_messages,current_message):

    """format the input for fact-checking using LLM."""

    prompt = prompts.input_formator_prompt(past_messages,current_message)
    response =gemini_LLM_interface(prompt)
    return response
    
def link_security_verifyer(verification_results):

    """verify the security of links using LLM."""

    prompt = prompts.link_security_verifyer_prompt(verification_results)
    response = gemini_LLM_interface(prompt)
    return response

def orchestrator(tools,inputmessage):
    """orchestrator for main agent to do tool selection"""
    prompt = prompts.main_orchestration_prompt(tools,inputmessage)
    response = gemini_LLM_interface(prompt=prompt)
    
    return  extract_json_for_orchestrator(response)

input = "Research claims that the Fibonacci sequence appears in pinecone patterns. Let's verify with some math."

