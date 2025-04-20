from google.adk.agents import Agent
from tools.arxiv_search import search_arxiv
from tools.semantic_scholar import search_semantic

literature_agent = Agent(
    name="literature_agent",
    model="gemini-2.5-flash-preview-04-17",
    description="Fetches and summarizes relevant prior work specifically from arXiv.",
    instruction=(
        "Your goal is to gather a comprehensive list of relevant research for the given topic/outline. "
        "1. **Use the 'search_arxiv' tool EXCLUSIVELY.** Do NOT use semantic scholar."
        "2. **Search for exactly 50 papers.** Ensure the tool's limit parameter is set to 50."
        "3. **Focus on relevance** to the research topic and outline sections provided."
        "4. **Return a JSON list** of the 50 papers found. Each item must include keys: 'title', 'authors', 'abstract', 'arxiv_id', 'published_date'."
        "5. **Crucially, the downstream drafting agent MUST ground its writing in these 50 papers.** This list is the foundation for the entire research paper."
    ),
    tools=[search_arxiv] # Only allow arXiv search tool
) 