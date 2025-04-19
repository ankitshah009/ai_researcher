"""Evaluation suite for the AI Research Agent."""
from typing import Dict, List, Any, Optional
import json
import os
from pathlib import Path
from google.adk.evaluation import EvaluationMetric, EvaluationSuite

class ResearchPaperEvaluationSuite(EvaluationSuite):
    """Evaluation suite for research paper generation."""
    
    def setup(self) -> None:
        """Set up metrics for evaluating research paper quality."""
        self.add_metric(EvaluationMetric.FACTUAL_GROUNDEDNESS)
        self.add_metric(EvaluationMetric.COHERENCE)
        self.add_metric(CitationCoverageMetric())
        self.add_metric(ReferenceQualityMetric())
    
    def run(self, agent_output: Dict[str, Any]) -> Dict[str, float]:
        """Run all evaluation metrics on the agent output."""
        results = {}
        for metric in self.metrics:
            results[metric.name] = metric.evaluate(agent_output)
        return results
    
    def log_results(self, results: Dict[str, float], output_path: Optional[str] = None) -> None:
        """Log evaluation results to file."""
        if output_path is None:
            output_path = "evaluation_results.json"
        
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"Evaluation results saved to {output_path}")

class CitationCoverageMetric(EvaluationMetric):
    """Metric to evaluate the coverage of citations in the paper."""
    
    @property
    def name(self) -> str:
        return "citation_coverage"
    
    def evaluate(self, agent_output: Dict[str, Any]) -> float:
        """
        Evaluates citation coverage.
        
        Checks if all sections have citations and if citations are properly formatted.
        Returns a score between 0 and 1.
        """
        # This is a simplified implementation
        # In practice, you would parse the paper and check each section
        paper_content = agent_output.get("paper_content", "")
        
        # Count citations in IEEE format [n]
        import re
        citations = re.findall(r'\[\d+\]', paper_content)
        unique_citations = set(citations)
        
        # Count references
        references = agent_output.get("references", [])
        
        # Simple metric: ratio of unique citations to references
        if not references:
            return 0.0
            
        return min(1.0, len(unique_citations) / len(references))

class ReferenceQualityMetric(EvaluationMetric):
    """Metric to evaluate the quality of references."""
    
    @property
    def name(self) -> str:
        return "reference_quality"
    
    def evaluate(self, agent_output: Dict[str, Any]) -> float:
        """
        Evaluates reference quality.
        
        Checks if references are recent, relevant, and from reputable sources.
        Returns a score between 0 and 1.
        """
        # This is a simplified implementation
        references = agent_output.get("references", [])
        
        if not references:
            return 0.0
        
        # Count references with publication year >= 2020
        recent_count = 0
        for ref in references:
            year = ref.get("year")
            if year and int(year) >= 2020:
                recent_count += 1
        
        # Score based on percentage of recent references
        return recent_count / len(references)

# Usage example:
# suite = ResearchPaperEvaluationSuite()
# results = suite.run(agent_output)
# suite.log_results(results) 