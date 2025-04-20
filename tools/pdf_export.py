"""Custom ADK tool: convert paper content to PDF."""
import os
import tempfile
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from google.adk.tools import FunctionTool

# Import the template rendering function
from tools.template_utils import render_template

# Define the outputs directory - make this an absolute path
ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Project root
OUTPUT_DIR = ROOT_DIR / "outputs"
print(f"PDF export module loaded. Output directory: {OUTPUT_DIR}")

# Ensure outputs directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def tex_to_pdf(latex_content: str, output_filename: str = "research_paper.pdf") -> str:
    """
    Converts LaTeX content to PDF using pdflatex, saving it to the outputs directory.
    
    Args:
        latex_content: String containing valid LaTeX document
        output_filename: Name for the output PDF file
        
    Returns:
        String containing the filename of the generated PDF if successful
    """
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / output_filename
    print(f"Will save PDF to: {output_path}")
    
    # Save the LaTeX source for debugging
    latex_path = OUTPUT_DIR / f"{output_filename}.tex"
    with open(latex_path, 'w') as f:
        f.write(latex_content)
    print(f"Saved LaTeX source to: {latex_path}")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write LaTeX content to temporary file
        tex_file = Path(temp_dir) / "paper.tex"
        with open(tex_file, "w") as f:
            f.write(latex_content)
        
        # Run pdflatex
        try:
            print(f"Running pdflatex in {temp_dir}")
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
            pdf_path = Path(temp_dir) / "paper.pdf"
            if pdf_path.exists():
                shutil.copy(pdf_path, output_path)
                print(f"✓ Successfully generated PDF: {output_path}")
                # Just return the filename part, not the full path
                return output_filename
            else:
                print(f"× No PDF file found at {pdf_path}")
                raise FileNotFoundError("PDF generation failed")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"× LaTeX error: {e}")
            
            # Fallback to reportlab for simple PDF generation if pdflatex fails
            return _generate_fallback_pdf(output_filename, f"LaTeX compilation failed: {e}", paper_content={
                "title": "PDF Generation Error",
                "content": f"Failed to generate PDF with LaTeX: {e}",
            })

def _generate_fallback_pdf(output_filename: str, error_message: str, paper_content: Dict[str, Any]) -> str:
    """Generate a simple PDF using ReportLab when LaTeX fails"""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    
    output_path = OUTPUT_DIR / output_filename
    print(f"Generating fallback PDF at {output_path}")
    
    # Create the PDF document
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    flowables = []
    
    # Add title
    title = paper_content.get("title", "Research Paper")
    flowables.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    flowables.append(Spacer(1, 12))
    
    # Add error message
    flowables.append(Paragraph("<b>Error:</b>", styles["Heading1"]))
    flowables.append(Paragraph(error_message, styles["Normal"]))
    flowables.append(Spacer(1, 12))
    
    # Add sections
    for section, content in paper_content.items():
        if section not in ["title"] and content:
            flowables.append(Paragraph(f"<b>{section.replace('_', ' ').title()}</b>", styles["Heading1"]))
            flowables.append(Spacer(1, 6))
            
            # Handle both string and dict content types
            if isinstance(content, dict):
                for k, v in content.items():
                    flowables.append(Paragraph(f"<b>{k}:</b> {v}", styles["Normal"]))
            else:
                flowables.append(Paragraph(str(content), styles["Normal"]))
                
            flowables.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(flowables)
    print(f"✓ Generated fallback PDF: {output_path}")
    
    # Return just the filename part
    return output_filename

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
        String containing the filename of the generated PDF
    """
    print(f"Starting paper_to_pdf generation for {output_filename}")
    print(f"Template: {template_name}")
    print(f"Content keys: {', '.join(paper_content.keys())}")
    
    # Ensure all expected keys have at least default values if not provided
    default_content = {
        "title": "Untitled Research Paper",
        "abstract": "",
        "keywords": "",
        "introduction": "",
        "related_work": "",
        "methodology": "",
        "experiments": "",
        "results": "",
        "discussion": "",
        "limitations": "",
        "future_work": "",
        "conclusion": "",
        "acknowledgment": "",
        "references": "",
        "appendix": None
    }
    
    # Merge provided content with defaults
    full_paper_content = {**default_content, **paper_content}
    
    try:
        # Render the template with the paper content
        print("Rendering template...")
        latex_content = render_template(template_name, full_paper_content)
        
        # Generate PDF from the rendered LaTeX
        return tex_to_pdf(latex_content, output_filename)
        
    except Exception as e:
        print(f"Error during paper_to_pdf: {e}")
        
        # Fallback to basic PDF if template rendering fails
        return _generate_fallback_pdf(
            output_filename, 
            f"Error rendering template: {e}", 
            paper_content=paper_content
        )