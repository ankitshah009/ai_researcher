# AI Research Agent 🚀

An end-to-end system that transforms a single-line research topic into a full, citation-rich research paper using the Google Agent Development Kit (ADK) and Vertex AI.

## Overview

This project provides:

1. **Multi-Agent Research System**: Specialized agents that collaborate to create comprehensive research papers.

2. **Modern Web Application**:
   - **Flask REST API Backend**: Handles the paper generation process, communicates with Google's ADK, and manages the research job lifecycle.
   - **React Frontend**: A sleek, intuitive UI for submitting research topics, tracking progress, and downloading generated papers.
   - **Gradio UI**: Alternative simple web interface (Legacy)

## Features

- 🤖 **Multi-agent orchestration** - Specialized agents collaborate to create a complete research paper
- 📚 **Literature search** - Automatic discovery of relevant academic papers from arXiv and Semantic Scholar
- 📝 **Structured drafting** - Section-by-section creation of professional academic content
- 🔍 **Citation management** - Generation of properly formatted citations in IEEE format
- 📊 **PDF generation** - Conversion of content to professional-looking PDFs using LaTeX templates
- 🖥️ **Modern React UI** - Beautiful, responsive web interface with real-time progress tracking
- 📱 **RESTful API** - Flexible backend system for integration with other applications
- ⚙️ **Configurable** - Flexible configuration system for customizing the paper generation process

## Project Layout

```
ai_research_agent/
├── README.md
├── requirements.txt
├── config.py               # Central configuration system
├── main.py                 # CLI entry point
├── api.py                  # Flask API backend
├── web_ui.py               # Gradio web interface (Legacy)
├── run_app.sh              # Script to run Flask+React app
├── docker-compose.yml      # Docker deployment for entire stack
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
├── frontend/               # React frontend
│   ├── public/             # Static assets
│   ├── src/                # React components
│   │   ├── components/     # Reusable UI components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── pages/          # Page components
│   │   └── styles/         # CSS and styling
│   └── Dockerfile          # Frontend container build
└── docker/
    └── Dockerfile          # Backend container build
```

## Prerequisites

- Python 3.8+
- Node.js 14+ (for React frontend)
- Google ADK (follow Google's setup instructions)
- An API key for Google Gemini models

## Setup

1. Clone this repository
```bash
git clone https://github.com/yourusername/ai-research-agent.git
cd ai-research-agent
```

2. Set up your API key
```bash
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

3. Choose how to run:

### Option 1: Run with React + Flask (Recommended)
```bash
./run_app.sh
```

This script will:
- Create a Python virtual environment
- Install backend dependencies
- Install frontend dependencies
- Start both the backend API and frontend development server

Once running, you can access:
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:5000](http://localhost:5000)

### Option 2: Run with Gradio UI (Legacy)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python web_ui.py
```

This starts a Gradio web interface at [http://127.0.0.1:7860](http://127.0.0.1:7860).

### Option 3: Run with CLI
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py --topic "Graph Neural Networks for Protein Folding"
```

### Option 4: Run with Docker Compose
```bash
docker-compose up -d
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

4. **Web interfaces** - Both React and Gradio UIs provide access to the same underlying functionality.

## Testing

### Testing the arXiv Integration

You can test the arXiv search functionality by:
1. Opening [http://localhost:3000/test](http://localhost:3000/test)
2. Entering a search query
3. Viewing the results

### Testing the API Directly

You can also test the API endpoints directly:

- Health check:
```bash
curl http://localhost:5000/api/health
```

- Start a research job:
```bash
curl -X POST http://localhost:5000/api/start -H "Content-Type: application/json" -d '{"topic":"Impact of quantum computing on cryptography"}'
```

### Run the test suite
```bash
python -m pytest
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

MIT License 