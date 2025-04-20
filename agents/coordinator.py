from google.adk.agents import Agent
from agents.outline_agent import outline_agent
from agents.literature_agent import literature_agent
from agents.drafting_agent import drafting_agent
from agents.citation_agent import citation_agent
from agents.formatting_agent import formatting_agent

coordinator_agent = Agent(
    name="research_coordinator",
    model="gemini-2.5-flash-preview-04-17",
    description="Top‑level orchestrator that delegates stages of the research‑paper workflow.",
    instruction=(
        "On first user message (a research topic), delegate to outline_agent. "
        "Then iterate outline→literature→drafting (per section)→citation→formatting. "
        "When passing content to formatting_agent, provide the COMPLETE paper content as a structured dictionary "
        "with keys for each section (title, abstract, introduction, related_work, methodology, experiments, "
        "results, discussion, conclusion, references). "
        "IMPORTANT: Make sure to explicitly ask formatting_agent to generate the PDF using paper_to_pdf and provide "
        "a specific output filename. "
        "After PDF is produced, respond with the output filename and tell the user they can download it "
        "from the /outputs directory."
    ),
    sub_agents=[outline_agent, literature_agent, drafting_agent, citation_agent, formatting_agent],
)