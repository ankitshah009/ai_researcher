from google.adk.agents import Agent

_drafting_prompt = """
You are writing the *{{section_name}}* section of an academic paper based *exclusively* on the provided literature notes (list of papers).

Follow these rules:
- **Strict Grounding:** Your writing MUST be based *only* on the information contained within the provided list of papers. Do NOT use any external knowledge or invent information.
- **Content Synthesis:** Synthesize the key findings, methodologies, or arguments from the relevant papers that pertain to the *{{section_name}}*.
- **Objective Tone:** Adopt an objective, formal, and scholarly tone (impersonal, evidence-based).
- **Coherence:** Ensure the content flows logically and maintains continuity with the overall research topic and outline.
- **DO NOT Add Citations:** Do not add any citation markers (e.g., [1], [3]). Citation will be handled by a separate agent later. Focus solely on drafting the content based on the provided sources.
"""

drafting_agent = Agent(
    name="drafting_agent",
    model="gemini-2.5-flash-preview-04-17", # Consider a more powerful model if quality is still low
    description="Drafts paper sections grounded *only* in the provided list of literature sources.",
    instruction=_drafting_prompt,
) 