from tools.tools.google_safe_browsing import google_safe_browsing
from tools.tools.virustotal import virustotal
from tools.tools.urlscan import urlscan
from tools.tools.fact_checker import fact_checker
from tools.tools.research_tool import research_tool

TOOLS = {
    "google_safe_browsing": google_safe_browsing,
    "virustotal": virustotal,
    "urlscan": urlscan,
    "fact_checker": fact_checker,
    "research_tool": research_tool,
}
