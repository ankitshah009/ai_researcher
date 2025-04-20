#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_section() {
    echo -e "\n${BLUE}=== $1 ===${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}! $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_section "AI Research Agent - Docker Test Suite"

# Step 1: Ensure we have an API key
if [ ! -f .env ] || ! grep -q "GOOGLE_API_KEY" .env; then
    print_warning "No API key found in .env file."
    read -p "Enter your Google API key: " API_KEY
    echo "GOOGLE_API_KEY=${API_KEY}" > .env
    print_success "API key saved to .env file"
else
    print_success "API key found in .env file"
fi

# Step 2: Build and start the containers
print_section "Starting Docker Containers"
echo "This may take a while for the first build..."

if [ "$1" == "--rebuild" ]; then
    docker compose down
    docker compose build --no-cache
    BUILD_RESULT=$?
else
    docker compose build
    BUILD_RESULT=$?
fi

if [ $BUILD_RESULT -ne 0 ]; then
    print_error "Failed to build Docker images"
    exit 1
fi

print_success "Docker images built successfully"

docker compose up -d
if [ $? -ne 0 ]; then
    print_error "Failed to start Docker containers"
    exit 1
fi

print_success "Docker containers started successfully"

# Step 3: Wait for backend to be ready
print_section "Checking Backend Health"
echo "Waiting for backend to be ready..."

for i in {1..30}; do
    if curl -s http://localhost:5001/api/health > /dev/null; then
        print_success "Backend is ready"
        break
    fi
    
    if [ $i -eq 30 ]; then
        print_error "Backend failed to start within timeout period"
        echo "Logs from backend container:"
        docker compose logs backend
        exit 1
    fi
    
    echo -n "."
    sleep 2
done

# Step 4: Test arXiv search functionality
print_section "Testing arXiv Search Functionality"
echo "Sending test query to arXiv search endpoint..."

QUERY="Transformer Neural Networks"
RESULT=$(curl -s "http://localhost:5001/api/test/arxiv?query=${QUERY}&limit=1")

if echo "$RESULT" | grep -q "success"; then
    print_success "arXiv search test successful"
    echo "Sample result:"
    echo "$RESULT" | grep -o '"title":"[^"]*"' | head -1
else
    print_error "arXiv search test failed"
    echo "Response: $RESULT"
    exit 1
fi

# Step 5: Check frontend accessibility
print_section "Checking Frontend Accessibility"
echo "Checking if frontend is accessible..."

if curl -s http://localhost:3000 | grep -q "React App"; then
    print_success "Frontend is accessible"
else
    print_warning "Frontend may not be ready yet. Please check http://localhost:3000 manually."
fi

# Final confirmation
print_section "Test Results"
print_success "All tests completed successfully"
echo ""
echo -e "You can access the application at ${GREEN}http://localhost:3000${NC}"
echo -e "API is available at ${GREEN}http://localhost:5001${NC}"
echo ""
echo "To stop the containers, run: docker compose down" 