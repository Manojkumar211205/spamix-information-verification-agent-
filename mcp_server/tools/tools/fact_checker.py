import requests
import google.generativeai as genai
import json
import praw
from ...config.settings import GOOGLE_API_KEY, GEMINI_API_KEY, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_REFRESH_TOKEN, REDDIT_USER_AGENT, TAVILY_API_KEY


# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Base endpoint for Google Fact Check Tools API
BASE_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

# Reddit client will be initialized lazily when needed
reddit = None

def get_reddit_client():
    """Initialize Reddit client lazily with proper error handling"""
    global reddit
    if reddit is None:
        if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_REFRESH_TOKEN, REDDIT_USER_AGENT]):
            raise Exception("Reddit credentials not configured. Please set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_REFRESH_TOKEN, and REDDIT_USER_AGENT environment variables.")
        
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            refresh_token=REDDIT_REFRESH_TOKEN,
            user_agent=REDDIT_USER_AGENT
        )
    return reddit

def fact_check_search(query, page_size=10):
    """Search for fact-checks using Google's Fact Check Tools API"""
    params = {
        "query": query,
        "pageSize": page_size,
        "key": GOOGLE_API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("claims", [])
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Request error: {e}"}

def search_reddit(query, limit=10):
    """Search Reddit for relevant content"""
    content_list = []
    try:
        reddit_client = get_reddit_client()
        for submission in reddit_client.subreddit("all").search(query, limit=limit):
            content_list.append({
                'title': submission.title,
                'content': submission.selftext,
                'subreddit': str(submission.subreddit),
                'score': submission.score,
                'url': submission.url
            })
    except Exception as e:
        return {"error": f"Reddit search error: {e}"}
    return content_list

def tavily_search(query, max_results=10, topic="news"):
    """Search using Tavily API for web content"""
    url = "https://api.tavily.com/search"
    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "max_results": max_results,
        "topic": topic,
        "search_depth": "advanced",
        "include_answer": True,
        "include_raw_content": True
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.RequestException as e:
        return {"error": f"Tavily search request error: {e}"}
    except ValueError:
        return {"error": "Tavily returned invalid JSON"}

def fact_check_with_gemini_google(user_prompt, fact_check_data):
    """Use Gemini to compare user prompt against Google Fact Check data"""
    
    # Prepare fact-check content
    content_text = ""
    for claim in fact_check_data:
        content_text += f"Claim: {claim.get('text', 'No claim text')}\n"
        content_text += f"Claimant: {claim.get('claimant', 'Unknown')}\n"
        
        # Get review information
        reviews = claim.get('claimReview', [])
        for review in reviews:
            publisher = review.get('publisher', {}).get('name', 'Unknown')
            rating = review.get('textualRating', 'No rating')
            url = review.get('url', 'No URL')
            content_text += f"Publisher: {publisher}\n"
            content_text += f"Rating: {rating}\n"
            content_text += f"Review URL: {url}\n"
        content_text += "\n" + "-"*50 + "\n\n"
    
    prompt = f"""
    You are a fact-checking AI. Compare the user's statement with the provided fact-check data from Google's Fact Check Tools API.

    User's Statement: "{user_prompt}"

    Fact-Check Data:
    {content_text}

    Based on the comparison, determine if the user's statement aligns with or is supported by the fact-check data.

    Respond ONLY in JSON format with exactly these two keys:
    {{
        "status": true or false,
        "reason": "detailed explanation of why the statement is true or false based on the fact-check data"
    }}

    Rules:
    - Return true if the statement is supported by credible fact-checkers
    - Return false if the statement is disputed or contradicted by fact-checkers
    - Consider the ratings from multiple fact-checking organizations
    - Provide a clear reason explaining your decision based on the fact-check results
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return json.dumps({
            "status": False,
            "reason": f"Error in fact-checking analysis: {str(e)}"
        })

def fact_check_with_gemini_reddit(user_prompt, reddit_data):
    """Use Gemini to compare user prompt against Reddit content"""
    
    # Prepare Reddit content
    content_text = ""
    for item in reddit_data:
        content_text += f"Title: {item['title']}\n"
        content_text += f"Content: {item['content']}\n"
        content_text += f"Subreddit: {item['subreddit']}\n"
        content_text += f"Score: {item['score']}\n\n"
    
    prompt = f"""
    You are a fact-checking AI. Compare the user's statement with the provided content from Reddit discussions.

    User's Statement: "{user_prompt}"

    Reddit Content:
    {content_text}

    Based on the comparison, determine if the user's statement aligns with or is supported by the Reddit content.

    Respond ONLY in JSON format with exactly these two keys:
    {{
        "status": true or false,
        "reason": "detailed explanation of why the statement is true or false based on the Reddit content"
    }}

    Rules:
    - Return true if the statement is supported by the Reddit content
    - Return false if the statement contradicts or is not supported by the Reddit content
    - Consider the credibility and consensus of the sources
    - Provide a clear reason explaining your decision
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return json.dumps({
            "status": False,
            "reason": f"Error in Reddit fact-checking analysis: {str(e)}"
        })

def fact_check_with_gemini_tavily(user_prompt, tavily_data):
    """Use Gemini to compare user prompt against Tavily search results"""
    
    # Prepare Tavily content
    content_text = ""
    for item in tavily_data:
        content_text += f"Title: {item.get('title', 'No title')}\n"
        content_text += f"URL: {item.get('url', 'No URL')}\n"
        content_text += f"Content: {item.get('content', item.get('snippet', 'No content'))}\n"
        content_text += f"Score: {item.get('score', 'No score')}\n"
        content_text += f"Published Date: {item.get('published_date', 'Unknown date')}\n\n"
        content_text += "-"*50 + "\n\n"
    
    prompt = f"""
    You are a fact-checking AI. Compare the user's statement with the provided web content from Tavily search results.

    User's Statement: "{user_prompt}"

    Web Content from Tavily Search:
    {content_text}

    Based on the comparison, determine if the user's statement aligns with or is supported by the web content.

    Respond ONLY in JSON format with exactly these two keys:
    {{
        "status": true or false,
        "reason": "detailed explanation of why the statement is true or false based on the web content"
    }}

    Rules:
    - Return true if the statement is supported by credible web sources
    - Return false if the statement contradicts or is not supported by the web content
    - Consider the credibility, recency, and consensus of the sources
    - Provide a clear reason explaining your decision
    - Take into account the publication dates and source reliability
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return json.dumps({
            "status": False,
            "reason": f"Error in Tavily fact-checking analysis: {str(e)}"
        })

def fact_checker(statement: str, reddit_limit: int = 10, tavily_max_results: int = 10, tavily_topic: str = "news"):
    """Check the veracity of a statement using Google Fact Check Tools, Reddit content, and Tavily web search.
    
    Args:
        statement: The statement to fact-check (e.g., "The Earth is flat")
        reddit_limit: Number of Reddit posts to search (default: 10)
        tavily_max_results: Maximum number of Tavily search results (default: 10)
        tavily_topic: Tavily search topic category (default: "news")
    
    Returns:
        Dictionary containing combined fact-check results from all three sources
    """
    try:
        if not statement:
            return {"error": "Statement is required"}
        
        # Search Google Fact Check Tools
        google_results = fact_check_search(statement)
        google_error = None
        if isinstance(google_results, dict) and "error" in google_results:
            google_error = google_results["error"]
            google_results = []
        
        # Search Reddit
        reddit_results = search_reddit(statement, reddit_limit)
        reddit_error = None
        if isinstance(reddit_results, dict) and "error" in reddit_results:
            reddit_error = reddit_results["error"]
            reddit_results = []
        
        # Search Tavily
        tavily_results = tavily_search(statement, tavily_max_results, tavily_topic)
        tavily_error = None
        if isinstance(tavily_results, dict) and "error" in tavily_results:
            tavily_error = tavily_results["error"]
            tavily_results = []
        
        # Process Google Fact Check results
        google_analysis = None
        if google_results and not google_error:
            google_fact_check_result = fact_check_with_gemini_google(statement, google_results)
            try:
                # Clean the response by removing markdown code blocks if present
                cleaned_result = google_fact_check_result.strip()
                if cleaned_result.startswith('json'):
                    cleaned_result = cleaned_result[7:]  # Remove json
                if cleaned_result.endswith(''):
                    cleaned_result = cleaned_result[:-3]  # Remove 
                cleaned_result = cleaned_result.strip()
                
                google_analysis = json.loads(cleaned_result)
            except json.JSONDecodeError:
                google_analysis = {
                    "status": False,
                    "reason": f"Could not parse Google fact-check response: {google_fact_check_result}"
                }
        else:
            google_analysis = {
                "status": False,
                "reason": google_error or "No fact-check data found in Google's database"
            }
        
        # Process Reddit results
        reddit_analysis = None
        if reddit_results and not reddit_error:
            reddit_fact_check_result = fact_check_with_gemini_reddit(statement, reddit_results)
            try:
                # Clean the response by removing markdown code blocks if present
                cleaned_result = reddit_fact_check_result.strip()
                if cleaned_result.startswith('json'):
                    cleaned_result = cleaned_result[7:]  # Remove json
                if cleaned_result.endswith(''):
                    cleaned_result = cleaned_result[:-3]  # Remove 
                cleaned_result = cleaned_result.strip()
                
                reddit_analysis = json.loads(cleaned_result)
            except json.JSONDecodeError:
                reddit_analysis = {
                    "status": False,
                    "reason": f"Could not parse Reddit fact-check response: {reddit_fact_check_result}"
                }
        else:
            reddit_analysis = {
                "status": False,
                "reason": reddit_error or "No relevant content found on Reddit"
            }
        
        # Process Tavily results
        tavily_analysis = None
        if tavily_results and not tavily_error:
            tavily_fact_check_result = fact_check_with_gemini_tavily(statement, tavily_results)
            try:
                # Clean the response by removing markdown code blocks if present
                cleaned_result = tavily_fact_check_result.strip()
                if cleaned_result.startswith('json'):
                    cleaned_result = cleaned_result[7:]  # Remove json
                if cleaned_result.endswith(''):
                    cleaned_result = cleaned_result[:-3]  # Remove 
                cleaned_result = cleaned_result.strip()
                
                tavily_analysis = json.loads(cleaned_result)
            except json.JSONDecodeError:
                tavily_analysis = {
                    "status": False,
                    "reason": f"Could not parse Tavily fact-check response: {tavily_fact_check_result}"
                }
        else:
            tavily_analysis = {
                "status": False,
                "reason": tavily_error or "No relevant web content found through Tavily search"
            }
        
        # Determine overall status based on all three sources
        google_supports = google_analysis.get("status", False)
        reddit_supports = reddit_analysis.get("status", False)
        tavily_supports = tavily_analysis.get("status", False)
        overall_status = google_supports or reddit_supports or tavily_supports
        
        # Create comprehensive reason
        reason_parts = []
        
        if google_error:
            reason_parts.append(f"Google Fact Check: Error - {google_error}")
        else:
            google_verdict = "SUPPORTS" if google_supports else "DOES NOT SUPPORT"
            google_sources = len(google_results) if google_results else 0
            reason_parts.append(f"Google Fact Check ({google_sources} sources): {google_verdict} - {google_analysis.get('reason', 'No analysis available')}")
        
        if reddit_error:
            reason_parts.append(f"Reddit Community: Error - {reddit_error}")
        else:
            reddit_verdict = "SUPPORTS" if reddit_supports else "DOES NOT SUPPORT"
            reddit_sources = len(reddit_results) if reddit_results else 0
            reason_parts.append(f"Reddit Community ({reddit_sources} sources): {reddit_verdict} - {reddit_analysis.get('reason', 'No analysis available')}")
        
        if tavily_error:
            reason_parts.append(f"Tavily Web Search: Error - {tavily_error}")
        else:
            tavily_verdict = "SUPPORTS" if tavily_supports else "DOES NOT SUPPORT"
            tavily_sources = len(tavily_results) if tavily_results else 0
            reason_parts.append(f"Tavily Web Search ({tavily_sources} sources): {tavily_verdict} - {tavily_analysis.get('reason', 'No analysis available')}")
        
        # Combine results into simplified JSON format
        combined_result = {
            "status": overall_status,
            "reason": " | ".join(reason_parts)
        }
        
        return combined_result
            
    except Exception as e:
        return {"error": f"Failed to fact-check statement: {str(e)}"}