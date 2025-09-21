import requests
import google.generativeai as genai
import json
import arxiv
import wikipedia
from config.settings import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

def search_arxiv(query, max_results=10):
    """Search ArXiv for academic papers related to the query"""
    try:
        # Create ArXiv client
        client = arxiv.Client()
        
        # Search for papers
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        papers = []
        for paper in client.results(search):
            papers.append({
                'title': paper.title,
                'abstract': paper.summary
            })
        
        return papers
    except Exception as e:
        return {"error": f"ArXiv search error: {e}"}

def search_wikipedia(query, max_results=5):
    """Search Wikipedia for articles related to the query"""
    try:
        # Search for Wikipedia pages
        search_results = wikipedia.search(query, results=max_results)
        
        articles = []
        for title in search_results:
            try:
                # Get the full article
                page = wikipedia.page(title)
                articles.append({
                    'title': page.title,
                    'summary': page.summary
                })
            except wikipedia.exceptions.DisambiguationError as e:
                # Handle disambiguation pages
                articles.append({
                    'title': title,
                    'summary': f"Disambiguation page with options: {', '.join(e.options[:5])}"
                })
            except Exception as e:
                # Skip problematic pages
                continue
        
        return articles
    except Exception as e:
        return {"error": f"Wikipedia search error: {e}"}

def analyze_with_gemini_arxiv(query, arxiv_data):
    """Use Gemini to analyze ArXiv papers for the query"""
    
    # Prepare ArXiv content
    content_text = ""
    for paper in arxiv_data:
        content_text += f"Title: {paper['title']}\n"
        content_text += f"Abstract: {paper['abstract']}\n\n"
    
    prompt = f"""
    You are a research analysis AI. Analyze the provided academic papers from ArXiv in relation to the user's query.

    User's Query: "{query}"

    ArXiv Papers:
    {content_text}

    Based on the analysis, provide insights about the research landscape for this query.

    Respond ONLY in JSON format with exactly these keys:
    {{
        "key_findings": ["list of main findings from the papers"],
        "research_trends": ["list of research trends observed"],
        "gaps": ["list of research gaps or areas needing more work"],
        "recommendations": ["list of recommendations for further research"]
    }}

    Rules:
    - Extract key findings from the abstracts
    - Identify patterns and trends across papers
    - Note any gaps in the research
    - Provide actionable recommendations
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return json.dumps({
            "key_findings": [],
            "research_trends": [],
            "gaps": [],
            "recommendations": [f"Error in analysis: {str(e)}"]
        })

def analyze_with_gemini_wikipedia(query, wikipedia_data):
    """Use Gemini to analyze Wikipedia articles for the query"""
    
    # Prepare Wikipedia content
    content_text = ""
    for article in wikipedia_data:
        content_text += f"Title: {article['title']}\n"
        content_text += f"Summary: {article['summary']}\n\n"
    
    prompt = f"""
    You are a knowledge analysis AI. Analyze the provided Wikipedia articles in relation to the user's query.

    User's Query: "{query}"

    Wikipedia Articles:
    {content_text}

    Based on the analysis, provide insights about the knowledge available for this query.

    Respond ONLY in JSON format with exactly these keys:
    {{
        "key_concepts": ["list of key concepts covered"],
        "knowledge_areas": ["list of knowledge areas represented"],
        "completeness": "assessment of how complete the information is",
        "credibility": "assessment of the credibility of sources"
    }}

    Rules:
    - Extract key concepts from the summaries
    - Identify knowledge areas covered
    - Assess completeness of information
    - Evaluate credibility of Wikipedia sources
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return json.dumps({
            "key_concepts": [],
            "knowledge_areas": [],
            "completeness": "Error in analysis",
            "credibility": "Unable to assess"
        })

def research_tool(query: str, arxiv_max_results: int = 10, wikipedia_max_results: int = 5):
    """Research a topic using both ArXiv and Wikipedia sources.
    
    Args:
        query: The research query (e.g., "machine learning in healthcare")
        arxiv_max_results: Maximum number of ArXiv papers to fetch (default: 10)
        wikipedia_max_results: Maximum number of Wikipedia articles to fetch (default: 5)
    
    Returns:
        Dictionary containing combined research results from both sources
    """
    try:
        if not query:
            return {"error": "Query is required"}
        
        # Search ArXiv
        arxiv_results = search_arxiv(query, arxiv_max_results)
        arxiv_error = None
        if isinstance(arxiv_results, dict) and "error" in arxiv_results:
            arxiv_error = arxiv_results["error"]
            arxiv_results = []
        
        # Search Wikipedia
        wikipedia_results = search_wikipedia(query, wikipedia_max_results)
        wikipedia_error = None
        if isinstance(wikipedia_results, dict) and "error" in wikipedia_results:
            wikipedia_error = wikipedia_results["error"]
            wikipedia_results = []
        
        # Process ArXiv results
        arxiv_analysis = None
        if arxiv_results and not arxiv_error:
            arxiv_analysis_result = analyze_with_gemini_arxiv(query, arxiv_results)
            try:
                # Clean the response by removing markdown code blocks if present
                cleaned_result = arxiv_analysis_result.strip()
                if cleaned_result.startswith('json'):
                    cleaned_result = cleaned_result[7:]  # Remove json
                if cleaned_result.endswith(''):
                    cleaned_result = cleaned_result[:-3]  # Remove 
                cleaned_result = cleaned_result.strip()
                
                arxiv_analysis = json.loads(cleaned_result)
            except json.JSONDecodeError:
                arxiv_analysis = {
                    "key_findings": [],
                    "research_trends": [],
                    "gaps": [],
                    "recommendations": [f"Could not parse ArXiv analysis: {arxiv_analysis_result}"]
                }
        else:
            arxiv_analysis = {
                "key_findings": [],
                "research_trends": [],
                "gaps": [],
                "recommendations": [arxiv_error or "No ArXiv papers found"]
            }
        
        # Process Wikipedia results
        wikipedia_analysis = None
        if wikipedia_results and not wikipedia_error:
            wikipedia_analysis_result = analyze_with_gemini_wikipedia(query, wikipedia_results)
            try:
                # Clean the response by removing markdown code blocks if present
                cleaned_result = wikipedia_analysis_result.strip()
                if cleaned_result.startswith('json'):
                    cleaned_result = cleaned_result[7:]  # Remove json
                if cleaned_result.endswith(''):
                    cleaned_result = cleaned_result[:-3]  # Remove 
                cleaned_result = cleaned_result.strip()
                
                wikipedia_analysis = json.loads(cleaned_result)
            except json.JSONDecodeError:
                wikipedia_analysis = {
                    "key_concepts": [],
                    "knowledge_areas": [],
                    "completeness": "Error in analysis",
                    "credibility": "Unable to assess"
                }
        else:
            wikipedia_analysis = {
                "key_concepts": [],
                "knowledge_areas": [],
                "completeness": "No information found",
                "credibility": "Unable to assess"
            }
        
        # Determine overall status - true if we found any results
        arxiv_papers = len(arxiv_results) if arxiv_results else 0
        wikipedia_articles = len(wikipedia_results) if wikipedia_results else 0
        overall_status = (arxiv_papers > 0) or (wikipedia_articles > 0)
        
        # Create comprehensive reason as single string
        reason_parts = []
        
        # ArXiv section
        if arxiv_error:
            reason_parts.append(f"ArXiv research error: {arxiv_error}")
        else:
            if arxiv_papers > 0:
                arxiv_text = f"ArXiv research supports the query with {arxiv_papers} papers"
                
                # Add key findings if available
                if arxiv_analysis.get('key_findings'):
                    arxiv_text += f", including findings about {', '.join(arxiv_analysis['key_findings'])}"
                
                # Add research trends if available
                if arxiv_analysis.get('research_trends'):
                    arxiv_text += f", and research trends in {', '.join(arxiv_analysis['research_trends'])}"
                
                reason_parts.append(arxiv_text)
            else:
                reason_parts.append("ArXiv research does not support the query - no relevant papers found")
        
        # Wikipedia section
        if wikipedia_error:
            reason_parts.append(f"Wikipedia knowledge error: {wikipedia_error}")
        else:
            if wikipedia_articles > 0:
                wikipedia_text = f"Wikipedia knowledge supports the query with {wikipedia_articles} articles"
                
                # Add key concepts if available
                if wikipedia_analysis.get('key_concepts'):
                    wikipedia_text += f", covering concepts like {', '.join(wikipedia_analysis['key_concepts'])}"
                
                # Add knowledge areas if available
                if wikipedia_analysis.get('knowledge_areas'):
                    wikipedia_text += f", and knowledge areas including {', '.join(wikipedia_analysis['knowledge_areas'])}"
                
                reason_parts.append(wikipedia_text)
            else:
                reason_parts.append("Wikipedia knowledge does not support the query - no relevant articles found")
        
        # Add research gaps if available
        if arxiv_analysis.get("gaps"):
            reason_parts.append(f"Research gaps remain in {', '.join(arxiv_analysis['gaps'])}")
        
        # Add recommendations if available
        if arxiv_analysis.get("recommendations"):
            reason_parts.append(f"Recommendations include {', '.join(arxiv_analysis['recommendations'])}")
        
        # Combine results into simplified JSON format
        combined_result = {
            "status": overall_status,
            "reason": ". ".join(reason_parts) + "."
        }
        
        return combined_result
            
    except Exception as e:
        return {"error": f"Failed to research query: {str(e)}"}
    