#!/usr/bin/env python3
"""Simple test for the arXiv search functionality."""
import os
import sys
import json
import arxiv

def search_arxiv_direct(query: str, max_results: int = 10):
    """Search arXiv directly without using the ADK tool."""
    print(f"Searching arXiv for: {query}")
    search = arxiv.Search(query=query, max_results=max_results)
    out = []
    for result in search.results():
        out.append({
            "title": result.title,
            "url": result.pdf_url,
            "summary": result.summary[:200] + "..." if len(result.summary) > 200 else result.summary,
            "authors": [a.name for a in result.authors],
            "published": result.published.strftime("%Y-%m-%d"),
        })
    return out

def main():
    """Test the arXiv search with a simple query."""
    print("Testing arXiv search functionality...")
    
    try:
        # Run a simple search
        results = search_arxiv_direct("Transfer learning in computer vision", max_results=3)
        
        # Display the results
        print(f"Found {len(results)} papers:")
        print(json.dumps(results, indent=2))
        print("\nTest successful!")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 