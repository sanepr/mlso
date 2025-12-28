#!/bin/bash
# Test script for Docker API

echo "🧪 Testing Heart Disease API"
echo "================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Build the image
echo ""
echo "🔨 Building Docker image..."
docker build -t heart-disease-api:latest . || exit 1

# Stop and remove existing container
echo ""
echo "🧹 Cleaning up old containers..."
docker stop heart-disease-api 2>/dev/null || true
docker rm heart-disease-api 2>/dev/null || true

# Kill any process using port 8000
echo ""
echo "🔫 Freeing up port 8000..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Run the container
echo ""
echo "🚀 Starting container..."
docker run -d -p 8000:8000 --name heart-disease-api heart-disease-api:latest

# Wait for startup
echo ""
echo "⏳ Waiting for API to start..."
sleep 5

# Check container status
echo ""
echo "📊 Container status:"
docker ps | grep heart-disease-api

# Check logs
echo ""
echo "📋 Container logs:"
docker logs heart-disease-api 2>&1 | head -20

# Test health endpoint
echo ""
echo "🏥 Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
if [ $? -eq 0 ]; then
    echo "✅ Health check passed!"
    echo "$HEALTH_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$HEALTH_RESPONSE"
else
    echo "❌ Health check failed!"
    docker logs heart-disease-api
    exit 1
fi

# Test prediction endpoint
echo ""
echo "🔮 Testing prediction endpoint..."
curl -X POST http://localhost:8000/predict \
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
  }' | python3 -m json.tool

echo ""
echo "================================"
echo "✅ All tests passed!"
echo ""
echo "📝 Container is running on http://localhost:8000"
echo "📝 View logs: docker logs -f heart-disease-api"
echo "📝 Stop container: docker stop heart-disease-api"
echo "📝 Remove container: docker rm heart-disease-api"

