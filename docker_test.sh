#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}AI Research Agent Docker Test${NC}"
echo "==============================="

echo -e "\n${GREEN}Step 1:${NC} Building Docker image..."
docker build -t ai-research-agent -f docker/Dockerfile .

echo -e "\n${GREEN}Step 2:${NC} Verifying Python dependencies..."
docker run --rm ai-research-agent -c "import pkg_resources; print('Installed packages:'); [print(f'{pkg.key}=={pkg.version}') for pkg in sorted(pkg_resources.working_set, key=lambda x: x.key.lower())]"

echo -e "\n${GREEN}Step 3:${NC} Testing arXiv search tool..."
docker run --rm ai-research-agent test_arxiv.py

echo -e "\n${GREEN}Step 4:${NC} Testing with web UI..."
echo -e "${YELLOW}This will start the web UI. Access at http://localhost:7860${NC}"
echo "Press Ctrl+C to stop the container when done testing."
echo

# Check if .env file exists
if [ ! -f .env ]; then
  echo -e "${RED}Warning:${NC} No .env file found. You need to provide GOOGLE_API_KEY."
  echo "Create a .env file with your API key before using the agent."
  echo "Example: echo 'GOOGLE_API_KEY=your_key_here' > .env"
  echo
fi

# Run the container with the web UI
docker run --rm -it \
  -p 7860:7860 \
  -v "$(pwd)/.env:/app/.env:ro" \
  -v "$(pwd)/outputs:/app/outputs" \
  ai-research-agent web_ui.py --host 0.0.0.0

echo -e "\n${GREEN}All tests completed!${NC}" 