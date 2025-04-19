from google.adk.agents import Agent
from tools.pdf_export import tex_to_pdf, paper_to_pdf

formatting_agent = Agent(
    name="formatting_agent",
    model="gemini-2.0-flash",
    description="Renders the finished manuscript into PDF via LaTeX template.",
    instruction=(
        "Take the paper content and format it for publication. "
        "Either return clean LaTeX for tex_to_pdf, or organize the content into "
        "a structured dictionary for paper_to_pdf. Use the template-based approach "
        "when possible for better formatting."
    ),
    tools=[tex_to_pdf, paper_to_pdf]
) 