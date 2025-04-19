"""Custom ADK tool: convert paper content to PDF."""
import os
import tempfile
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from google.adk.tools import tool

from tools.template_utils import render_template

@tool(name="tex_to_pdf", description="Convert LaTeX content to PDF and return the file URL")
def tex_to_pdf(latex_content: str, output_filename: str = "research_paper.pdf") -> str:
    """
    Converts LaTeX content to PDF using pdflatex.
    
    Args:
        latex_content: String containing valid LaTeX document
        output_filename: Name for the output PDF file
        
    Returns:
        String containing the URL or path to the generated PDF
    """
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write LaTeX content to temporary file
        tex_file = Path(temp_dir) / "paper.tex"
        with open(tex_file, "w") as f:
            f.write(latex_content)
        
        # Run pdflatex
        try:
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", str(tex_file)],
                cwd=temp_dir,
                check=True,
                capture_output=True
            )
            
            # Second run for references
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", str(tex_file)],
                cwd=temp_dir,
                check=True,
                capture_output=True
            )
            
            # Copy output to desired location
            output_path = Path(os.getcwd()) / output_filename
            pdf_path = Path(temp_dir) / "paper.pdf"
            if pdf_path.exists():
                shutil.copy(pdf_path, output_path)
                return str(output_path.absolute())
            else:
                raise FileNotFoundError("PDF generation failed")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # Fallback to reportlab for simple PDF generation if pdflatex fails
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            output_path = Path(os.getcwd()) / output_filename
            c = canvas.Canvas(str(output_path), pagesize=letter)
            c.drawString(100, 750, "LaTeX compilation failed")
            c.drawString(100, 730, "Please ensure LaTeX is installed properly")
            c.drawString(100, 700, "Error: " + str(e))
            c.save()
            
            return str(output_path.absolute())

@tool(name="paper_to_pdf", description="Convert structured paper content to PDF using template")
def paper_to_pdf(
    paper_content: Dict[str, Any],
    template_name: str = "paper_template.tex",
    output_filename: str = "research_paper.pdf"
) -> str:
    """
    Converts structured paper content to PDF using a LaTeX template.
    
    Args:
        paper_content: Dictionary containing paper sections and metadata
        template_name: Name of the template to use
        output_filename: Name for the output PDF file
        
    Returns:
        String containing the URL or path to the generated PDF
    """
    # Render the template with the paper content
    try:
        latex_content = render_template(template_name, paper_content)
        
        # Generate PDF from the rendered LaTeX
        return tex_to_pdf(latex_content, output_filename)
        
    except Exception as e:
        # Fallback to basic PDF if template rendering fails
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        
        output_path = Path(os.getcwd()) / output_filename
        
        # Create the PDF document
        doc = SimpleDocTemplate(str(output_path), pagesize=letter)
        styles = getSampleStyleSheet()
        flowables = []
        
        # Add title
        title = paper_content.get("title", "Research Paper")
        flowables.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
        flowables.append(Spacer(1, 12))
        
        # Add sections
        for section, content in paper_content.items():
            if section not in ["title", "keywords"] and content:
                flowables.append(Paragraph(f"<b>{section.replace('_', ' ').title()}</b>", styles["Heading1"]))
                flowables.append(Spacer(1, 6))
                flowables.append(Paragraph(content, styles["Normal"]))
                flowables.append(Spacer(1, 12))
        
        # Build the PDF
        doc.build(flowables)
        
        return str(output_path.absolute()) 