#!/bin/bash
# Kubernetes Deployment Script for Heart Disease API

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🚀 Kubernetes Deployment for Heart Disease API"
echo "=============================================="

# Check if Docker daemon is running
echo ""
echo "🐳 Checking Docker daemon..."
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker daemon is not running!${NC}"
    echo ""
    echo -e "${YELLOW}📋 Docker Desktop is REQUIRED for Kubernetes deployment.${NC}"
    echo ""
    echo "Quick fix:"
    echo "  1. Open Docker Desktop application"
    echo "  2. Wait for whale icon to stop animating (30-60 seconds)"
    echo "  3. Run this script again"
    echo ""

    # Try to start Docker Desktop automatically on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${BLUE}🚀 Attempting to open Docker Desktop...${NC}"
        open -a Docker 2>/dev/null

        if [ $? -eq 0 ]; then
            echo ""
            echo "⏳ Docker Desktop is starting. This may take 30-60 seconds..."
            echo "   Waiting for Docker to be ready..."

            # Wait up to 60 seconds for Docker to start
            for i in {1..60}; do
                if docker info > /dev/null 2>&1; then
                    echo ""
                    echo -e "${GREEN}✅ Docker is now running!${NC}"
                    echo "   Continuing with deployment..."
                    sleep 2
                    break
                fi
                sleep 1
                echo -n "."
            done
            echo ""

            # Check again
            if ! docker info > /dev/null 2>&1; then
                echo -e "${RED}❌ Docker failed to start within 60 seconds.${NC}"
                echo ""
                echo "Please:"
                echo "  1. Check Docker Desktop is installed"
                echo "  2. Open Docker Desktop manually"
                echo "  3. Wait for it to fully start"
                echo "  4. Run this script again"
                echo ""
                echo "📚 See detailed guide: K8S_DOCKER_NOT_RUNNING.md"
                exit 1
            fi
        else
            echo -e "${RED}❌ Could not open Docker Desktop automatically.${NC}"
            echo ""
            echo "Please open Docker Desktop manually:"
            echo "  • Press Cmd+Space and type 'Docker'"
            echo "  • Or find Docker in Applications folder"
            echo ""
            echo "Then run this script again."
            echo ""
            echo "📚 See detailed guide: K8S_DOCKER_NOT_RUNNING.md"
            exit 1
        fi
    else
        echo "Please start Docker Desktop manually and run this script again."
        echo ""
        echo "📚 See detailed guide: K8S_DOCKER_NOT_RUNNING.md"
        exit 1
    fi
fi
echo -e "${GREEN}✅ Docker is running${NC}"

# Use local minikube binary
MINIKUBE="./minikube-darwin-arm64"

# Check if minikube binary exists
if [ ! -f "$MINIKUBE" ]; then
    echo -e "${RED}❌ Minikube binary not found at $MINIKUBE${NC}"
    echo "Please download minikube for your platform from https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

# Make sure it's executable
chmod +x "$MINIKUBE"

# Check if minikube is running
echo ""
echo "📊 Checking minikube status..."
if ! $MINIKUBE status > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Minikube is not running. Starting minikube...${NC}"
    $MINIKUBE start --driver=docker --cpus=2 --memory=4096
    echo -e "${GREEN}✅ Minikube started successfully${NC}"
else
    echo -e "${GREEN}✅ Minikube is already running${NC}"
fi

# Check Docker image exists
echo ""
echo "🐳 Checking Docker image..."
if ! docker images | grep -q "heart-disease-api"; then
    echo -e "${YELLOW}⚠️  Docker image not found. Building...${NC}"
    docker build -t heart-disease-api:latest .
    echo -e "${GREEN}✅ Docker image built${NC}"
else
    echo -e "${GREEN}✅ Docker image exists${NC}"
fi

# Load image into minikube
echo ""
echo "📦 Loading image into minikube..."
$MINIKUBE image load heart-disease-api:latest
echo -e "${GREEN}✅ Image loaded into minikube${NC}"

# Delete existing deployment if any
echo ""
echo "🧹 Cleaning up existing deployment..."
$MINIKUBE kubectl -- delete -f deployment/kubernetes/ --ignore-not-found=true
sleep 5

# Deploy to Kubernetes
echo ""
echo "🚢 Deploying to Kubernetes..."
$MINIKUBE kubectl -- apply -f deployment/kubernetes/deployment.yaml
$MINIKUBE kubectl -- apply -f deployment/kubernetes/service.yaml

# Wait for deployment to be ready
echo ""
echo "⏳ Waiting for deployment to be ready..."
$MINIKUBE kubectl -- wait --for=condition=available --timeout=300s deployment/heart-disease-api

# Get deployment status
echo ""
echo "📊 Deployment Status:"
$MINIKUBE kubectl -- get deployments
echo ""
$MINIKUBE kubectl -- get pods
echo ""
$MINIKUBE kubectl -- get services

# Get the service URL
echo ""
echo "🌐 Getting service URL..."
SERVICE_URL=$($MINIKUBE service heart-disease-api --url)
echo -e "${GREEN}✅ Service URL: $SERVICE_URL${NC}"

# Test the health endpoint
echo ""
echo "🏥 Testing health endpoint..."
sleep 5
if curl -s "$SERVICE_URL/health" > /dev/null; then
    echo -e "${GREEN}✅ Health check passed!${NC}"
    curl -s "$SERVICE_URL/health" | python3 -m json.tool
else
    echo -e "${RED}❌ Health check failed${NC}"
    echo "Check logs with: $MINIKUBE kubectl -- logs -l app=heart-disease-api"
fi

# Test prediction endpoint
echo ""
echo "🔮 Testing prediction endpoint..."
PREDICTION=$(curl -s -X POST "$SERVICE_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63,
    "sex": 1,
    "cp": 3,
    "trestbps": 145,
    "chol": 233,
    "fbs": 1,
    "restecg": 0,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 2.3,
    "slope": 0,
    "ca": 0,
    "thal": 1
  }')

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Prediction test passed!${NC}"
    echo "$PREDICTION" | python3 -m json.tool
else
    echo -e "${RED}❌ Prediction test failed${NC}"
fi

echo ""
echo "=============================================="
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "=============================================="
echo ""
echo "📝 Useful Commands:"
echo "  View pods:         $MINIKUBE kubectl -- get pods"
echo "  View services:     $MINIKUBE kubectl -- get services"
echo "  View logs:         $MINIKUBE kubectl -- logs -l app=heart-disease-api -f"
echo "  Get service URL:   $MINIKUBE service heart-disease-api --url"
echo "  Delete deployment: $MINIKUBE kubectl -- delete -f deployment/kubernetes/"
echo "  Stop minikube:     $MINIKUBE stop"
echo ""
echo "🌐 Access the API at: $SERVICE_URL"
echo ""

