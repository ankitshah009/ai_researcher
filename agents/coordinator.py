from google.adk.agents import Agent
from agents.outline_agent import outline_agent
from agents.literature_agent import literature_agent
from agents.drafting_agent import drafting_agent
from agents.citation_agent import citation_agent
from agents.formatting_agent import formatting_agent

_coordinator_prompt = """
You are the Research Coordinator, orchestrating the creation of an academic paper.

**Workflow & Data Flow:**
1.  **Outline:** On receiving the research topic, delegate to `outline_agent` to get the paper outline.
2.  **Literature Review:** Pass the outline to `literature_agent`. It will return a JSON list of 50 relevant source papers.
3.  **Drafting (Iterative):** For each section in the outline:
    *   Pass the specific outline section AND the **full list of 50 source papers** to `drafting_agent`.
    *   Receive the drafted text for that section (which should be grounded ONLY in the sources).
4.  **Citation:** Once all sections are drafted:
    *   Assemble the complete drafted text.
    *   Pass the **complete drafted text** AND the **original list of 50 source papers** to `citation_agent`.
    *   Receive the text back with inline citations added AND a formatted reference list.
5.  **Formatting & PDF Generation:**
    *   Structure the final, cited paper content (including title, abstract, all sections, and the reference list from `citation_agent`) into a dictionary with expected keys (title, abstract, introduction, related_work, etc.).
    *   Pass this **structured dictionary** AND a specific **output filename** (e.g., 'research_paper.pdf') to `formatting_agent`.
    *   **Crucially, explicitly instruct `formatting_agent` to call the `paper_to_pdf` tool** with the provided dictionary and filename.
6.  **Completion:** Once `formatting_agent` confirms PDF generation (returning the filename), respond to the user confirming completion and stating the output filename.

**Important:** Ensure the list of 50 source papers is consistently passed between relevant stages (literature -> drafting -> citation).
"""

coordinator_agent = Agent(
    name="research_coordinator",
    model="gemini-2.5-flash-preview-04-17",
    description="Top‑level orchestrator that delegates stages and manages data flow for research paper generation.",
    instruction=_coordinator_prompt,
    sub_agents=[outline_agent, literature_agent, drafting_agent, citation_agent, formatting_agent],
)