from google.adk.agents import Agent

citation_agent = Agent(
    name="citation_agent",
    model="gemini-2.0-flash",
    description="Formats reference list in IEEE style and ensures every in‑text citation is matched.",
    instruction="Return the final reference list sorted numerically. Do not invent DOIs or authors.",
) 