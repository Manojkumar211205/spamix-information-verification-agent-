from groq import Groq # Make sure you have the Groq SDK installed
from .config.settings import LLM_API_KEY, LLM_MODEL
from .tools.tools_registry import TOOLS
import json
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import time
from typing import Dict, Any

# Initialize Groq client
client = Groq(api_key=LLM_API_KEY)

class WebScraper500Words:
    """
    A simple web scraper that extracts the first 500 words from any given URL.
    """
    
    def __init__(self, timeout: int = 10, delay: float = 1.0):
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        
        # Set user agent to avoid being blocked
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def is_valid_url(self, url: str) -> bool:
        """Validate if the URL is properly formatted."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that aren't letters, numbers, or basic punctuation
        text = re.sub(r'[^\w\s.,!?;:\-\'"()]', ' ', text)
        # Remove extra spaces
        text = ' '.join(text.split())
        return text.strip()
    
    def extract_text_from_html(self, html_content: str, url: str) -> str:
        """Extract meaningful text content from HTML."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script, style, nav, footer, and other non-content elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'noscript']):
            element.decompose()
        
        # Try to find main content areas first
        content_selectors = [
            'article', 
            '[role="main"]', 
            'main', 
            '.content', 
            '#content', 
            '.post-content',
            '.entry-content',
            '.article-content',
            '.blog-post',
            'div[class*="content"]'
        ]
        
        main_content = None
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        # If no main content found, use body
        if not main_content:
            main_content = soup.find('body') or soup
        
        # Extract text from paragraphs, headings, and lists primarily
        text_elements = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'div'])
        
        extracted_text = ""
        for element in text_elements:
            text = element.get_text(strip=True)
            if text and len(text) > 20:  # Only include substantial text blocks
                extracted_text += text + " "
        
        # If still no good content, get all text
        if len(extracted_text.strip()) < 100:
            extracted_text = main_content.get_text(separator=' ', strip=True)
      
        return self.clean_text(extracted_text)
    
    def get_first_500_words(self, text: str) -> Dict[str, Any]:
        """Extract first 500 words from text and return metadata."""
        words = text.split()
        
        if len(words) <= 200:
            return {
                'text': text,
                'word_count': len(words),
                'is_truncated': False,
                'total_characters': len(text)
            }
        
        first_500_words = ' '.join(words[:200])
        return {
            'text': first_500_words,
            'word_count': 200,
            'is_truncated': True,
            'total_words_available': len(words),
            'total_characters': len(first_500_words)
        }
    
    def scrape_url(self, url: str) -> Dict[str, Any]:
        """
        Main method to scrae URL and extract first 500 words.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        result = {
            'url': url,
            'success': False,
            'error': None,
            'text': '',
            'word_count': 0
        }
        
        # Validate URL
        if not self.is_valid_url(url):
            result['error'] = 'Invalid URL format'
            return result
        
        try:
            # Add delay to be respectful to servers
            time.sleep(self.delay)
            
            # Make request
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
           
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if 'html' not in content_type:
                result['error'] = f'Unsupported content type: {content_type}'
                return result
            
            # Extract text from HTML
            extracted_text = self.extract_text_from_html(response.text, url)


            
            if not extracted_text:
                result['error'] = 'No readable text content found'
                return result
            
            # Get first 500 words
            word_data = self.get_first_500_words(extracted_text)
            
            result.update({
                'success': True,
                'text': word_data['text'],
                'word_count': word_data['word_count']
            })
            
        except requests.exceptions.RequestException as e:
            result['error'] = f'Request failed: {str(e)}'
        except Exception as e:
            result['error'] = f'Unexpected error: {str(e)}'
        
        return result


def agent_decide_and_run(url: str):
    """
    Agent uses Groq LLaMA 3.3 to decide which tools to run for the given URL,
    executes them, and returns results.
    """
    tool_list = ", ".join(TOOLS.keys())

    prompt = f"""
    You are a security agent. 
    Available tools: {tool_list}.
    A user gives you the URL: {url}.
    Decide which ONE or TWO tools are most useful to check if it is malicious. 
    Reply with a JSON list of tool names only.
    Example: ["google_safe_browsing", "virustotal"]
    """

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )

    # Groq returns a string
    tool_selection_text = response.choices[0].message.content.strip()

    # Parse JSON safely
    try:
        selected_tools = json.loads(tool_selection_text)
        if not isinstance(selected_tools, list):
            raise ValueError("Not a list")
    except:
        selected_tools = ["google_safe_browsing"]  # fallback

    # Execute selected tools
    results = {}
    for tool_name in selected_tools:
        if tool_name in TOOLS:
            try:
                results[tool_name] = TOOLS[tool_name](url)
            except Exception as e:
                results[tool_name] = {"status": "error", "details": str(e)}

    return {
        "url": url,
        "tools_used": selected_tools,
        "results": results,
    }

