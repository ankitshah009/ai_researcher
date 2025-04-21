"""Custom ADK tool: convert paper content to PDF."""
import os
import tempfile
import shutil
import subprocess
import traceback
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
            process = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", str(tex_file)],
                cwd=temp_dir,
                check=True,
                capture_output=True,
                text=True
            )
            
            # Print stdout and stderr for debugging
            print(f"pdflatex stdout: {process.stdout[:500]}...")
            if process.stderr:
                print(f"pdflatex stderr: {process.stderr}")
            
            # Second run for references
            process = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", str(tex_file)],
                cwd=temp_dir,
                check=True,
                capture_output=True,
                text=True
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
                # Save the log file for debugging
                log_path = Path(temp_dir) / "paper.log"
                if log_path.exists():
                    shutil.copy(log_path, OUTPUT_DIR / f"{output_filename}.log")
                    print(f"Saved LaTeX log to: {OUTPUT_DIR / f'{output_filename}.log'}")
                raise FileNotFoundError("PDF generation failed")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"× LaTeX error: {e}")
            # Save the log file for debugging if it exists
            log_path = Path(temp_dir) / "paper.log"
            if log_path.exists():
                shutil.copy(log_path, OUTPUT_DIR / f"{output_filename}.log")
                print(f"Saved LaTeX log to: {OUTPUT_DIR / f'{output_filename}.log'}")
            
            # Fallback to reportlab for simple PDF generation if pdflatex fails
            return _generate_fallback_pdf(output_filename, f"LaTeX compilation failed: {e}", paper_content={
                "title": "PDF Generation Error",
                "content": f"Failed to generate PDF with LaTeX: {e}",
                "paper_content": latex_content[:500] + "..." if len(latex_content) > 500 else latex_content
            })

def _generate_fallback_pdf(output_filename: str, error_message: str, paper_content: Dict[str, Any]) -> str:
    """Generate a simple PDF using ReportLab when LaTeX fails"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors
        
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
        
        # Check if we have more structured content
        sections_to_include = [
            "abstract", "introduction", "related_work", "methodology", 
            "experiments", "results", "discussion", "conclusion", "references"
        ]
        
        # Add a note about fallback mode
        flowables.append(Paragraph("<b>Note:</b> This is a fallback PDF generated because the LaTeX template processing failed. The content below may be incomplete.", styles["Normal"]))
        flowables.append(Spacer(1, 12))
        
        # Add sections from paper_content
        for section in sections_to_include:
            content = paper_content.get(section, "")
            if content:
                flowables.append(Paragraph(f"<b>{section.replace('_', ' ').title()}</b>", styles["Heading1"]))
                flowables.append(Spacer(1, 6))
                
                if isinstance(content, dict):
                    for k, v in content.items():
                        flowables.append(Paragraph(f"<b>{k}:</b>", styles["Heading2"]))
                        flowables.append(Paragraph(str(v), styles["Normal"]))
                else:
                    # Split long text into paragraphs
                    paragraphs = str(content).split('\n\n')
                    for para in paragraphs:
                        if para.strip():
                            flowables.append(Paragraph(para, styles["Normal"]))
                            flowables.append(Spacer(1, 6))
                
                flowables.append(Spacer(1, 12))
        
        # Build the PDF
        doc.build(flowables)
        print(f"✓ Generated fallback PDF: {output_path}")
        
        # Save the fallback content for debugging
        with open(OUTPUT_DIR / f"{output_filename}.txt", 'w') as f:
            f.write(f"Fallback PDF content for {title}\n\n")
            f.write(f"Error: {error_message}\n\n")
            for section in sections_to_include:
                content = paper_content.get(section, "")
                if content:
                    f.write(f"## {section.upper()}\n\n")
                    f.write(f"{content}\n\n")
        
        # Return just the filename part
        return output_filename
    except Exception as e:
        print(f"Error in fallback PDF generation: {e}")
        traceback.print_exc()
        # Create an extremely simple text file as absolute last resort
        try:
            with open(OUTPUT_DIR / output_filename, 'w') as f:
                f.write(f"ERROR: Failed to generate PDF\n\n")
                f.write(f"Error message: {error_message}\n\n")
                f.write("Paper content:\n")
                f.write(str(paper_content)[:1000])
            return output_filename
        except:
            # If all else fails, return the error
            return f"Failed to generate PDF: {error_message}"

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
    
    # Save the raw input for debugging
    debug_path = OUTPUT_DIR / f"{output_filename}.input.json"
    try:
        import json
        with open(debug_path, 'w') as f:
            json.dump(paper_content, f, indent=2)
        print(f"Saved input content to: {debug_path}")
    except:
        print("Could not save input JSON for debugging")
    
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
        # Check for the template file
        template_path = ROOT_DIR / "templates" / template_name
        if not os.path.exists(template_path):
            print(f"Template file not found at: {template_path}")
            # Check if we need to generate a simple template
            with open(OUTPUT_DIR / f"{output_filename}.template-missing.log", 'w') as f:
                f.write(f"Template {template_name} not found at {template_path}\n")
            raise FileNotFoundError(f"Template file not found: {template_path}")
            
        # Render the template with the paper content
        print(f"Rendering template {template_path}...")
        latex_content = render_template(template_name, full_paper_content)
        
        # Generate PDF from the rendered LaTeX
        return tex_to_pdf(latex_content, output_filename)
        
    except Exception as e:
        print(f"Error during paper_to_pdf: {e}")
        traceback.print_exc()
        
        # Fallback to basic PDF if template rendering fails
        return _generate_fallback_pdf(
            output_filename, 
            f"Error rendering template: {e}", 
            paper_content=paper_content
        )