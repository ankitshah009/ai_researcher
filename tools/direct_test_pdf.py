"""Direct test for PDF generation with better error reporting"""
import os
import sys
from pathlib import Path
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.pdf_export import paper_to_pdf

def generate_test_pdf():
    """Generate a test PDF with sample content"""
    print("\n===== TESTING PDF GENERATION =====")
    
    # Sample paper content
    sample_content = {
        "title": "Test Research Paper - Generated on Request",
        "abstract": "This is a test paper to verify PDF generation is working correctly.",
        "keywords": "testing, pdf, generation",
        "introduction": "This test paper was created to debug PDF generation issues.",
        "related_work": "No related work section for this test.",
        "methodology": "We created a test paper with minimal content.",
        "experiments": "No experiments were conducted for this test.",
        "results": "PDF generation should result in a file in the outputs directory.",
        "discussion": "If this test works, it confirms PDF generation is functional.",
        "conclusion": "This test helps identify issues in the PDF generation process."
    }
    
    try:
        # Generate PDF with debugging
        print(f"Attempting to generate PDF with sample content...")
        print(f"Current working directory: {os.getcwd()}")
        
        # Generate the PDF file
        output_filename = "direct_test_output.pdf"
        result = paper_to_pdf(sample_content, output_filename=output_filename)
        
        # Verify the file exists
        output_dir = Path(os.getcwd()) / "outputs"
        pdf_path = output_dir / output_filename
        
        print(f"\nGeneration result: {result}")
        print(f"Expected PDF location: {pdf_path}")
        print(f"File exists: {pdf_path.exists()}")
        
        if pdf_path.exists():
            print(f"\n✅ SUCCESS: PDF was generated at {pdf_path}")
            print(f"File size: {pdf_path.stat().st_size} bytes")
            return True
        else:
            print(f"\n❌ ERROR: PDF file was not found at expected location")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: PDF generation failed with exception:")
        print(f"  {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generate_test_pdf()
    sys.exit(0 if success else 1)