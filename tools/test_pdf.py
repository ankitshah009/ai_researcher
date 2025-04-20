"""Simple test script to verify PDF generation works"""
import os
from pathlib import Path
from tools.pdf_export import paper_to_pdf

def test_pdf_generation():
    """Test the PDF generation function with simple content"""
    print("Testing PDF generation...")
    
    # Simple test content for PDF
    paper_content = {
        "title": "Test Research Paper",
        "abstract": "This is a simple test abstract to verify PDF generation is working.",
        "keywords": "testing, pdf, generation",
        "introduction": "This is an introduction section for the test paper.",
        "related_work": "This would typically contain a review of related work.",
        "methodology": "The methodology section describes how the research was conducted.",
        "experiments": "Experiments section describes what tests were performed.",
        "results": "Results of the experiments would be described here.",
        "discussion": "A discussion of the findings would be included here.",
        "limitations": "This section describes the limitations of the research.",
        "future_work": "Future work that could be done to extend this research.",
        "conclusion": "This is the conclusion of the test paper.",
        "acknowledgment": "Thanks to everyone who helped with this test.",
        "references": "\\bibitem{test} Test Reference, 2023"
    }
    
    try:
        # Generate the PDF
        output_file = paper_to_pdf(paper_content, output_filename="test_output.pdf")
        print(f"Success! PDF generated at: {output_file}")
        full_path = Path(os.getcwd()) / "outputs" / output_file
        print(f"Full path: {full_path}")
        print(f"File exists: {full_path.exists()}")
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False

if __name__ == "__main__":
    test_pdf_generation()