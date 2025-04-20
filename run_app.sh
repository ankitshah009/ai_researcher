#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting AI Research Agent...${NC}"

# Check if python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${YELLOW}npm is not installed. Please install Node.js first.${NC}"
    exit 1
fi

# Check if the virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate the virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Install backend dependencies
echo -e "${GREEN}Installing backend dependencies...${NC}"
pip install -r requirements.txt

# Install frontend dependencies
echo -e "${GREEN}Installing frontend dependencies...${NC}"
cd frontend
npm install
cd ..

# Start backend in the background
echo -e "${GREEN}Starting backend API...${NC}"
python api.py &
BACKEND_PID=$!

# Start frontend in the background
echo -e "${GREEN}Starting frontend...${NC}"
cd frontend
npm start &
FRONTEND_PID=$!

# Function to handle cleanup
cleanup() {
    echo -e "${YELLOW}Shutting down...${NC}"
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}

# Set up the trap to catch signals
trap cleanup SIGINT SIGTERM

echo -e "${GREEN}AI Research Agent is running!${NC}"
echo -e "${GREEN}Backend API: http://localhost:5000${NC}"
echo -e "${GREEN}Frontend: http://localhost:3000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"

# Wait forever (or until Ctrl+C)
wait 