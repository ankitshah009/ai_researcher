"""Custom ADK tool: search Semantic Scholar and return structured metadata."""
from typing import List, Dict
import semanticscholar as sch
from google.adk.tools import FunctionTool

@FunctionTool(name="search_semantic", description="Search Semantic Scholar for papers related to a query")
def search_semantic(query: str, max_results: int = 10) -> List[Dict]:
    """Search Semantic Scholar for papers related to a query."""
    client = sch.SemanticScholar()
    results = client.search_paper(query, limit=max_results)
    
    out = []
    for paper in results:
        # Extract relevant information
        authors = [author.get('name', '') for author in paper.get('authors', [])]
        year = paper.get('year')
        
        out.append({
            "title": paper.get('title', ''),
            "url": paper.get('url', ''),
            "abstract": paper.get('abstract', ''),
            "authors": authors,
            "year": year,
            "citation_count": paper.get('citationCount', 0),
        })
    
    return out 