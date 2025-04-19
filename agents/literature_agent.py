from google.adk.agents import Agent
from tools.arxiv_search import search_arxiv
from tools.semantic_scholar import search_semantic

literature_agent = Agent(
    name="literature_agent",
    model="gemini-2.0-flash",
    description="Fetches and summarizes relevant prior work.",
    instruction=(
        "Use the provided search tools to gather at least 8 high‑quality papers "
        "published after 2020 that are most relevant to the outline. Return a JSON "
        "list with keys: title, key_takeaway, citation."),
    tools=[search_arxiv, search_semantic]
) 