"""Tests for the research agent tools."""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.arxiv_search import search_arxiv
from tools.semantic_scholar import search_semantic
from tools.pdf_export import tex_to_pdf


class TestArxivSearch(unittest.TestCase):
    """Tests for the arXiv search tool."""
    
    @patch('arxiv.Search')
    def test_search_arxiv(self, mock_search):
        """Test the arXiv search functionality."""
        # Mock the Search class and its results
        mock_result = MagicMock()
        mock_result.title = "Test Paper"
        mock_result.pdf_url = "https://arxiv.org/pdf/1234.5678"
        mock_result.summary = "This is a test paper summary."
        mock_result.authors = [MagicMock(name="Test Author")]
        mock_result.published.strftime.return_value = "2023-01-01"
        
        mock_search.return_value.results.return_value = [mock_result]
        
        # Test the search function
        results = search_arxiv("test query", max_results=1)
        
        # Verify the results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Test Paper")
        self.assertEqual(results[0]["url"], "https://arxiv.org/pdf/1234.5678")
        self.assertEqual(results[0]["summary"], "This is a test paper summary.")
        self.assertEqual(results[0]["authors"], ["Test Author"])
        self.assertEqual(results[0]["published"], "2023-01-01")


class TestSemanticScholarSearch(unittest.TestCase):
    """Tests for the Semantic Scholar search tool."""
    
    @patch('semanticscholar.SemanticScholar')
    def test_search_semantic(self, mock_semantic_scholar):
        """Test the Semantic Scholar search functionality."""
        # Mock the Semantic Scholar client
        mock_client = MagicMock()
        mock_client.search_paper.return_value = [{
            'title': 'Test Paper',
            'url': 'https://semanticscholar.org/paper/123',
            'abstract': 'This is a test abstract.',
            'authors': [{'name': 'Test Author'}],
            'year': 2023,
            'citationCount': 42
        }]
        
        mock_semantic_scholar.return_value = mock_client
        
        # Test the search function
        results = search_semantic("test query", max_results=1)
        
        # Verify the results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Test Paper")
        self.assertEqual(results[0]["url"], "https://semanticscholar.org/paper/123")
        self.assertEqual(results[0]["abstract"], "This is a test abstract.")
        self.assertEqual(results[0]["authors"], ["Test Author"])
        self.assertEqual(results[0]["year"], 2023)
        self.assertEqual(results[0]["citation_count"], 42)


class TestPdfExport(unittest.TestCase):
    """Tests for the PDF export tool."""
    
    @patch('subprocess.run')
    def test_tex_to_pdf_success(self, mock_run):
        """Test successful PDF generation."""
        # Set up the mock subprocess.run
        mock_run.return_value = MagicMock(returncode=0)
        
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save current working directory
            old_cwd = os.getcwd()
            try:
                # Change to the temp directory
                os.chdir(temp_dir)
                
                # Create mock PDF file (since subprocess is mocked)
                Path(temp_dir).joinpath("paper.pdf").touch()
                
                # Test the PDF generation
                output_path = tex_to_pdf("\\documentclass{article}\\begin{document}Test\\end{document}", "test.pdf")
                
                # Verify the output path
                self.assertTrue(output_path.endswith("test.pdf"))
                
            finally:
                # Restore working directory
                os.chdir(old_cwd)
    
    @patch('subprocess.run')
    @patch('reportlab.pdfgen.canvas.Canvas')
    def test_tex_to_pdf_fallback(self, mock_canvas, mock_run):
        """Test fallback to reportlab when pdflatex fails."""
        # Set up the mock subprocess.run to fail
        mock_run.side_effect = Exception("pdflatex not found")
        
        # Set up the mock Canvas
        mock_canvas_instance = MagicMock()
        mock_canvas.return_value = mock_canvas_instance
        
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save current working directory
            old_cwd = os.getcwd()
            try:
                # Change to the temp directory
                os.chdir(temp_dir)
                
                # Test the PDF generation with fallback
                output_path = tex_to_pdf("\\documentclass{article}\\begin{document}Test\\end{document}", "test.pdf")
                
                # Verify the output path
                self.assertTrue(output_path.endswith("test.pdf"))
                
                # Verify that reportlab was used
                mock_canvas_instance.drawString.assert_called()
                mock_canvas_instance.save.assert_called_once()
                
            finally:
                # Restore working directory
                os.chdir(old_cwd)


if __name__ == '__main__':
    unittest.main() 