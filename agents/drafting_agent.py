from google.adk.agents import Agent

_drafting_prompt = """
You are writing the *{{section_name}}* section of an academic paper.
Follow these rules:
- Adopt an objective, scholarly tone (APA style).
- Cite sources in IEEE numeric format (e.g. [3]).
- Maintain continuity with the provided outline and literature notes.
"""

drafting_agent = Agent(
    name="drafting_agent",
    model="gemini-2.5-pro",
    description="Converts the outline and literature summaries into fully‑written prose, section by section.",
    instruction=_drafting_prompt,
) 