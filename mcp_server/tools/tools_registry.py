from .tools.google_safe_browsing import google_safe_browsing
from .tools.virustotal import virustotal
from .tools.urlscan import urlscan
from .tools.fact_checker import fact_checker
from .tools.research_tool import research_tool

TOOLS = {
    "google_safe_browsing": google_safe_browsing,
    "virustotal": virustotal,
    "urlscan": urlscan,
    "fact_checker": fact_checker,
    "research_tool": research_tool,
}
