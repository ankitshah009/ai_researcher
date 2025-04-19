"""Custom ADK tool: search arXiv and return structured metadata."""
from typing import List, Dict
import arxiv
from google.adk.tools import FunctionTool

@FunctionTool(name="search_arxiv", description="Search arXiv for papers related to a query")
def search_arxiv(query: str, max_results: int = 10) -> List[Dict]:
    """Search arXiv for papers related to a query.
    
    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 10)
        
    Returns:
        List of dictionaries containing paper metadata
    """
    search = arxiv.Search(query=query, max_results=max_results)
    out = []
    for result in search.results():
        out.append({
            "title": result.title,
            "url": result.pdf_url,
            "summary": result.summary,
            "authors": [a.name for a in result.authors],
            "published": result.published.strftime("%Y-%m-%d"),
        })
    return out

# Create the FunctionTool from the function
arxiv_search_tool = FunctionTool(func=search_arxiv)