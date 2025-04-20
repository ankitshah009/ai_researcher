#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_header() {
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

# Check for Docker and Docker Compose
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! docker compose version &> /dev/null; then
    print_warning "Docker Compose V2 not found. Falling back to 'docker-compose'."
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating a template .env file..."
    echo "GOOGLE_API_KEY=your_api_key_here" > .env
    print_warning "Please edit .env file and add your Google API key"
fi

# Command-line argument parsing
BUILD_FLAG=""
case "$1" in
    --rebuild)
        BUILD_FLAG="--build"
        ;;
    --clean)
        print_header "Cleaning up Docker resources"
        $COMPOSE_CMD down -v
        docker system prune -f
        print_success "Cleanup complete"
        exit 0
        ;;
    --help)
        echo "Usage: ./deploy.sh [OPTION]"
        echo "Options:"
        echo "  --rebuild    Force rebuild of Docker images"
        echo "  --clean      Remove containers, networks, and unused images"
        echo "  --help       Display this help message"
        exit 0
        ;;
esac

print_header "Deploying AI Research Agent"

# Build and start containers
print_header "Starting containers"
$COMPOSE_CMD up -d $BUILD_FLAG

if [ $? -ne 0 ]; then
    print_error "Failed to start containers. Check the logs above."
    exit 1
fi

print_success "Containers started successfully!"

# Display URLs
print_header "Access Information"
echo -e "Backend API:  ${GREEN}http://localhost:5001${NC}"
echo -e "Frontend UI:  ${GREEN}http://localhost:3000${NC}"
echo ""
echo -e "You can view logs with: ${YELLOW}docker compose logs -f${NC}"
echo -e "Stop the system with:   ${YELLOW}docker compose down${NC}"

# Check if services are up
print_header "Health Check"
sleep 5
if curl -s http://localhost:5001/api/health > /dev/null; then
    print_success "Backend API is running"
else
    print_warning "Backend API is not responding yet. Check logs with 'docker compose logs -f backend'"
fi

print_success "Deployment complete!" 