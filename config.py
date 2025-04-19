"""Configuration settings for the AI Research Agent."""
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Base directory for the application
BASE_DIR = Path(__file__).parent.absolute()

# Default configuration
DEFAULT_CONFIG: Dict[str, Any] = {
    # API settings
    "api_key_env_var": "GOOGLE_API_KEY",
    
    # Model settings
    "models": {
        "coordinator": "gemini-2.0-flash",
        "outline": "gemini-2.5-pro",
        "literature": "gemini-2.0-flash",
        "drafting": "gemini-2.5-pro",
        "citation": "gemini-2.0-flash",
        "formatting": "gemini-2.0-flash"
    },
    
    # Output settings
    "output": {
        "default_pdf_name": "research_paper.pdf",
        "output_dir": str(BASE_DIR / "outputs"),
        "create_output_dir": True
    },
    
    # Tool settings
    "tools": {
        "arxiv": {
            "max_results_default": 10,
            "max_results_limit": 50
        },
        "semantic_scholar": {
            "max_results_default": 10,
            "max_results_limit": 50
        }
    },
    
    # Paper settings
    "paper": {
        "citation_style": "IEEE",  # IEEE, APA, MLA, etc.
        "min_references": 8,
        "max_references": 30,
        "section_order": [
            "Abstract",
            "Introduction",
            "Related Work",
            "Methodology",
            "Experiments",
            "Results",
            "Discussion",
            "Conclusion",
            "References"
        ]
    },
    
    # Logging settings
    "logging": {
        "log_file": "ai_research_agent.log",
        "log_level": "INFO",
        "console_output": True
    }
}

# Runtime configuration (can be modified programmatically)
config = DEFAULT_CONFIG.copy()

def get_config() -> Dict[str, Any]:
    """Get the current configuration."""
    return config

def update_config(updates: Dict[str, Any]) -> None:
    """Update the configuration with new values."""
    global config
    
    # Recursive dictionary update
    def update_dict(d, u):
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                update_dict(d[k], v)
            else:
                d[k] = v
    
    update_dict(config, updates)

def load_config_from_file(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from a file."""
    if config_path is None:
        config_path = os.path.join(BASE_DIR, "config.json")
    
    if not os.path.exists(config_path):
        return config
    
    import json
    try:
        with open(config_path, 'r') as f:
            file_config = json.load(f)
        update_config(file_config)
    except Exception as e:
        print(f"Error loading config from {config_path}: {e}")
    
    return config

# Create output directory if it doesn't exist
if config["output"]["create_output_dir"]:
    output_dir = Path(config["output"]["output_dir"])
    output_dir.mkdir(exist_ok=True, parents=True) 