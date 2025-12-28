#!/bin/bash
# Docker Quick Start - Checks and starts Docker if needed

echo "🐳 Docker Quick Start Helper"
echo "================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is installed
echo "1️⃣  Checking if Docker is installed..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed!${NC}"
    echo ""
    echo "📥 Install Docker Desktop from:"
    echo "   https://www.docker.com/products/docker-desktop"
    echo ""
    exit 1
fi
echo -e "${GREEN}✅ Docker is installed${NC}"
echo ""

# Check if Docker daemon is running
echo "2️⃣  Checking if Docker daemon is running..."
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker daemon is NOT running!${NC}"
    echo ""
    echo -e "${YELLOW}🔧 Fix:${NC}"
    echo "   1. Open Docker Desktop application"
    echo "   2. Wait for whale icon in menu bar to stop animating"
    echo "   3. Run this script again"
    echo ""

    # Try to open Docker Desktop on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${BLUE}🚀 Attempting to open Docker Desktop...${NC}"
        open -a Docker
        echo ""
        echo "⏳ Waiting for Docker to start (this may take 30-60 seconds)..."

        # Wait for Docker to start (max 60 seconds)
        for i in {1..60}; do
            if docker info &> /dev/null; then
                echo -e "${GREEN}✅ Docker is now running!${NC}"
                break
            fi
            sleep 1
            echo -n "."
        done
        echo ""

        # Check again
        if ! docker info &> /dev/null; then
            echo -e "${RED}❌ Docker failed to start. Please start it manually.${NC}"
            exit 1
        fi
    else
        echo "Please start Docker Desktop manually and run this script again."
        exit 1
    fi
else
    echo -e "${GREEN}✅ Docker daemon is running${NC}"
fi
echo ""

# Show Docker version
echo "3️⃣  Docker version:"
docker --version
echo ""

# Check if models exist
echo "4️⃣  Checking if models are trained..."
if [ -f "models/best_model.pkl" ]; then
    SIZE=$(ls -lh models/best_model.pkl | awk '{print $5}')
    echo -e "${GREEN}✅ Models exist ($SIZE)${NC}"
else
    echo -e "${YELLOW}⚠️  Models not found. Train them first:${NC}"
    echo "   python src/models/train.py"
    echo ""
    read -p "Do you want to train models now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🏋️  Training models..."
        python src/models/train.py
    else
        echo "Skipping model training. Build will use existing models."
    fi
fi
echo ""

# Build Docker image
echo "5️⃣  Building Docker image..."
echo -e "${BLUE}Running: docker build -t heart-disease-api:latest .${NC}"
echo ""

if docker build -t heart-disease-api:latest .; then
    echo ""
    echo -e "${GREEN}✅ Docker image built successfully!${NC}"
    echo ""

    # Ask if user wants to run it
    read -p "Do you want to run the container now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "6️⃣  Starting container..."

        # Clean up existing container
        docker stop heart-disease-api 2>/dev/null
        docker rm heart-disease-api 2>/dev/null

        # Run container
        docker run -d -p 8000:8000 --name heart-disease-api heart-disease-api:latest

        echo ""
        echo "⏳ Waiting for container to start..."
        sleep 5

        # Check container status
        if docker ps | grep -q heart-disease-api; then
            echo -e "${GREEN}✅ Container is running!${NC}"
            echo ""
            echo "🧪 Testing API..."

            # Test health endpoint
            if curl -s http://localhost:8000/health > /dev/null 2>&1; then
                echo -e "${GREEN}✅ API is healthy!${NC}"
                echo ""
                echo "📝 Access the API:"
                echo "   Health: http://localhost:8000/health"
                echo "   Docs: http://localhost:8000/docs"
                echo ""
                echo "📋 Useful commands:"
                echo "   View logs: docker logs -f heart-disease-api"
                echo "   Stop: docker stop heart-disease-api"
                echo "   Remove: docker rm heart-disease-api"
            else
                echo -e "${YELLOW}⚠️  API not responding yet. Check logs:${NC}"
                echo "   docker logs heart-disease-api"
            fi
        else
            echo -e "${RED}❌ Container failed to start. Check logs:${NC}"
            echo "   docker logs heart-disease-api"
        fi
    fi
else
    echo ""
    echo -e "${RED}❌ Docker build failed!${NC}"
    echo ""
    echo "Common issues:"
    echo "  - Missing Dockerfile"
    echo "  - Syntax error in Dockerfile"
    echo "  - Network issues during build"
    exit 1
fi

echo ""
echo "================================"
echo -e "${GREEN}🎉 Done!${NC}"

