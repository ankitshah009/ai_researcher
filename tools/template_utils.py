"""Utilities for working with LaTeX templates for paper generation."""
import os
from pathlib import Path
from typing import Dict, Any, Optional
import jinja2

# Get the base directory
BASE_DIR = Path(__file__).parent.parent.absolute()
TEMPLATES_DIR = BASE_DIR / "templates"

def get_template(template_name: str = "paper_template.tex") -> jinja2.Template:
    """
    Load a LaTeX template by name.
    
    Args:
        template_name: Name of the template file
        
    Returns:
        Jinja2 Template object
    """
    template_path = TEMPLATES_DIR / template_name
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template {template_name} not found at {template_path}")
    
    # Create Jinja2 environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
        block_start_string='\\BLOCK{',
        block_end_string='}',
        variable_start_string='{{',
        variable_end_string='}}',
        comment_start_string='\\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
    )
    
    return env.get_template(template_name)

def render_template(template_name: str, context: Dict[str, Any]) -> str:
    """
    Render a template with the given context.
    
    Args:
        template_name: Name of the template file
        context: Dictionary of variables to render in the template
        
    Returns:
        Rendered template as a string
    """
    template = get_template(template_name)
    return template.render(**context) 