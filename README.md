# AI Research Scientist Agent (Google ADK)

An end-to-end code-base that transforms a single-line research topic into a full, citation-rich research paper using the Google Agent Development Kit (ADK) and Vertex AI.

## Features

- 🤖 **Multi-agent orchestration** - Specialized agents collaborate to create a complete research paper
- 📚 **Literature search** - Automatic discovery of relevant academic papers from arXiv and Semantic Scholar
- 📝 **Structured drafting** - Section-by-section creation of professional academic content
- 🔍 **Citation management** - Generation of properly formatted citations in IEEE format
- 📊 **PDF generation** - Conversion of content to professional-looking PDFs using LaTeX templates
- 🖥️ **Web interface** - Easy-to-use Gradio UI for interactive paper generation
- ⚙️ **Configurable** - Flexible configuration system for customizing the paper generation process

## Project Layout

```
ai_research_agent/
├── README.md
├── requirements.txt
├── config.py               # Central configuration system
├── main.py                 # CLI entry point
├── web_ui.py               # Gradio web interface
├── test_agent.py           # Script for testing the agent
├── run_tests.py            # Test runner for unit tests
├── agents/
│   ├── __init__.py
│   ├── coordinator.py      # Orchestrates the research workflow
│   ├── outline_agent.py    # Creates paper structure
│   ├── literature_agent.py # Finds relevant papers
│   ├── drafting_agent.py   # Writes sections
│   ├── citation_agent.py   # Handles citations
│   └── formatting_agent.py # Creates PDF output
├── tools/
│   ├── __init__.py
│   ├── arxiv_search.py     # Search arXiv papers
│   ├── semantic_scholar.py # Search Semantic Scholar
│   ├── pdf_export.py       # Convert to PDF
│   └── template_utils.py   # LaTeX template utilities
├── templates/
│   └── paper_template.tex  # LaTeX template for papers
├── callbacks/
│   └── logging_callback.py # Track agent progress
├── tests/
│   ├── __init__.py
│   └── test_tools.py       # Unit tests for tools
├── evaluation/
│   └── eval_suite.py       # Quality metrics
└── docker/
    └── Dockerfile          # Container deployment
```

## Setup and Installation

### Prerequisites

- Python 3.9+
- [Google API Key](https://ai.google.dev/) for Gemini models access

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai_research_agent.git
   cd ai_research_agent
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Google API key:
   ```bash
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

## Usage

### Command Line Interface

Generate a research paper from the command line:

```bash
python main.py --topic "Graph Neural Networks for Protein Folding"
```

Additional options:
```bash
python main.py --topic "Your Research Topic" --output "custom_filename.pdf" --verbose
```

### Web Interface

Launch the web UI for a user-friendly interface:

```bash
python web_ui.py
```

This starts a Gradio web interface at http://127.0.0.1:7860 where you can:
- Enter your research topic
- Monitor progress in real-time
- Download the generated PDF

### Testing

Run the test suite to verify everything is working:

```bash
python run_tests.py
```

Test with a sample topic:

```bash
python test_agent.py --topic "Reinforcement Learning for Autonomous Vehicles"
```

## How It Works

1. **Hierarchical delegation** - The `coordinator_agent` orchestrates the entire workflow, delegating tasks to specialized sub-agents.

2. **Staged workflow**:
   - `outline_agent` creates the paper structure
   - `literature_agent` searches for relevant papers using arXiv and Semantic Scholar
   - `drafting_agent` writes each section with proper citations
   - `citation_agent` formats the references in IEEE style
   - `formatting_agent` generates the final PDF using LaTeX templates

3. **Custom tools** - External API integration with arXiv and Semantic Scholar provides access to real research papers.

4. **Templating system** - LaTeX templates ensure professional formatting with fallback to ReportLab for environments without LaTeX.

5. **Configuration** - Centralized configuration in `config.py` allows customization of models, output formats, and agent behavior.

## Customization

You can create a `config.json` file to override default settings:

```json
{
  "models": {
    "coordinator": "gemini-2.5-pro"
  },
  "paper": {
    "citation_style": "APA"
  }
}
```

Or modify programmatically:

```python
from config import update_config
update_config({"output": {"default_pdf_name": "my_paper.pdf"}})
```

## Deployment Options

### Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GOOGLE_API_KEY=your_api_key_here
python main.py --topic "Your Topic"
```

### Docker Deployment

#### Quick Start

The easiest way to run the AI Research Agent is using Docker with our helper scripts:

```bash
# Run the Web UI
./run_web_ui.sh

# Run tests and validation
./docker_test.sh
```

#### Manual Docker Commands

Build the Docker image:
```bash
docker build -t ai-research-agent -f docker/Dockerfile .
```

Run the agent with CLI:
```bash
docker run --rm -it \
  -v "$(pwd)/.env:/app/.env:ro" \
  -v "$(pwd)/outputs:/app/outputs" \
  ai-research-agent main.py --topic "Your Research Topic"
```

Run the web UI:
```bash
docker run --rm -it \
  -p 7860:7860 \
  -v "$(pwd)/.env:/app/.env:ro" \
  -v "$(pwd)/outputs:/app/outputs" \
  ai-research-agent web_ui.py --host 0.0.0.0
```

### Cloud Deployment

Enable Vertex AI and Agent Engine APIs in your GCP project:

```bash
gcloud beta agentlifecycle deploy --image=gcr.io/your-project/ai-research-agent --project=$PROJECT_ID
```

## Next Steps

- Swap Gemini for Gemma or Llama-3 by changing the `model` field in config
- Add a plagiarism-checker tool during drafting
- Fine-tune templates for specific conference formats (e.g., ICML, NeurIPS)
- Implement citation style switching (IEEE, APA, MLA)

## License

MIT

✨ Happy researching! 