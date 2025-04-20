from google.adk.agents import Agent
from tools.pdf_export import tex_to_pdf, paper_to_pdf

formatting_agent = Agent(
    name="formatting_agent",
    model="gemini-2.5-flash-preview-04-17",
    description="Renders the finished manuscript into PDF via LaTeX template.",
    instruction=(
        "Your job is to receive the completed paper content and generate a PDF document. "
        "When you receive a paper with content for various sections, you MUST: "
        "1. Organize the content into a structured dictionary with keys matching the template: "
        "   title, abstract, keywords, introduction, related_work, methodology, experiments, results, discussion, "
        "   limitations, future_work, conclusion, acknowledgment, references, appendix. "
        "2. Call paper_to_pdf with this dictionary and the specified output filename. "
        "3. Report back with the filename of the generated PDF. "
        "ALWAYS use the paper_to_pdf function to generate the final document. "
        "Do not simply return the content without calling the PDF generation function."
    ),
    tools=[tex_to_pdf, paper_to_pdf]
)