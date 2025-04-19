#!/usr/bin/env python3
"""Simple test for the arXiv search tool."""
import os
import sys
import json
from tools.arxiv_search import search_arxiv

def main():
    """Test the arXiv search tool with a simple query."""
    print("Testing arXiv search...")
    
    try:
        # Run a simple search
        results = search_arxiv("Transfer learning in computer vision", max_results=3)
        
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