"""Custom ADK tool: search arXiv and return structured metadata."""
from typing import List, Dict
import arxiv
from google.adk import tool

@tool(name="search_arxiv", description="Search arXiv for papers related to a query")
def search_arxiv(query: str, max_results: int = 10) -> List[Dict]:
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