from google.adk.agents import Agent
from agents.outline_agent import outline_agent
from agents.literature_agent import literature_agent
from agents.drafting_agent import drafting_agent
from agents.citation_agent import citation_agent
from agents.formatting_agent import formatting_agent

coordinator_agent = Agent(
    name="research_coordinator",
    model="gemini-2.0-flash",
    description="Top‑level orchestrator that delegates stages of the research‑paper workflow.",
    instruction=(
        "On first user message (a research topic), delegate to outline_agent. "
        "Then iterate outline→literature→drafting (per section)→citation→formatting. "
        "After PDF is produced, respond with the download link."
    ),
    sub_agents=[outline_agent, literature_agent, drafting_agent, citation_agent, formatting_agent],
) 