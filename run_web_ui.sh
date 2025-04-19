#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error:${NC} Docker is not installed or not in PATH."
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if the image exists, build if not
if ! docker image inspect ai-research-agent &> /dev/null; then
    echo -e "${YELLOW}Docker image not found. Building it now...${NC}"
    docker build -t ai-research-agent -f docker/Dockerfile .
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Warning:${NC} No .env file found. You need to provide GOOGLE_API_KEY."
    echo "Create a .env file with your API key before using the agent."
    echo "Example: echo 'GOOGLE_API_KEY=your_key_here' > .env"
    read -p "Do you want to create .env file now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your Google API key: " API_KEY
        echo "GOOGLE_API_KEY=${API_KEY}" > .env
        echo -e "${GREEN}Created .env file with your API key.${NC}"
    fi
fi

# Create outputs directory if it doesn't exist
mkdir -p outputs

echo -e "${GREEN}Starting AI Research Agent Web UI${NC}"
echo -e "${YELLOW}Access at http://localhost:7860${NC}"
echo "Press Ctrl+C to stop the container when done."
echo

# Run the container with the web UI
docker run --rm -it \
  -p 7860:7860 \
  -v "$(pwd)/.env:/app/.env:ro" \
  -v "$(pwd)/outputs:/app/outputs" \
  ai-research-agent python web_ui.py --host 0.0.0.0 