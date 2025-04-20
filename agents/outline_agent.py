from google.adk.agents import Agent

outline_agent = Agent(
    name="outline_agent",
    model="gemini-2.5-flash-preview-04-17",  # higher‑quality model for planning
    description="Drafts a detailed section‑by‑section outline for an academic research paper.",
    instruction=(
        "You are a senior researcher. Given a topic, produce a structured outline "
        "with Title, Abstract, Introduction, Related Work, Methodology, Experiments, "
        "Results, Discussion, Conclusion, and References placeholder. Each heading "
        "should include bullet‑level talking points to guide subsequent drafting."
    ),
) 