# Docker API Fix - Complete Guide

## Issue
The `docker run -p 8000:8000 heart-disease-api:latest` command was failing.

## Root Causes Fixed

1. **Dockerfile used wrong server** - Was using `uvicorn` (FastAPI) but app is Flask
2. **Missing dependencies** - Flask, Werkzeug, and gunicorn not in requirements.txt
3. **Model loading** - App was looking for wrong model file name
4. **Port conflicts** - Port 8000 already in use

## Changes Made

### 1. Updated Dockerfile
```dockerfile
# Added curl for health checks
RUN apt-get install -y gcc curl

# Changed CMD from uvicorn to gunicorn
CMD ["gunicorn", "src.api.app:app", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]

# Added data/ directory copy for any preprocessing needs
COPY data/ ./data/
```

### 2. Updated requirements.txt
Added:
- `flask==2.3.3`
- `werkzeug==2.3.7`
- `gunicorn==21.2.0`

### 3. Updated app.py
- Fixed model loading to use `best_model.pkl` instead of `heart_disease_model.pkl`
- Added fallback paths for model loading
- Changed port to 8000 (from 5000)
- Added environment variable support for PORT

## How to Use

### Method 1: Quick Test Script (Recommended)
```bash
./test_docker.sh
```

This script automatically:
- Checks if Docker is running
- Builds the image
- Cleans up old containers
- Starts the container
- Tests health and prediction endpoints

### Method 2: Manual Steps

#### Step 1: Start Docker Desktop
Make sure Docker Desktop is running on your Mac.

#### Step 2: Build the Image
```bash
cd /Users/aashishr/codebase/mlso
docker build -t heart-disease-api:latest .
```

#### Step 3: Clean Up Port 8000
```bash
# Stop any existing container
docker stop heart-disease-api 2>/dev/null || true
docker rm heart-disease-api 2>/dev/null || true

# Kill any process using port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
```

#### Step 4: Run the Container
```bash
docker run -d -p 8000:8000 --name heart-disease-api heart-disease-api:latest
```

#### Step 5: Check Status
```bash
# View container status
docker ps

# View logs
docker logs heart-disease-api

# Follow logs in real-time
docker logs -f heart-disease-api
```

#### Step 6: Test the API

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Prediction:**
```bash
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
  }'
```

**Expected Response:**
```json
{
  "prediction": 1,
  "prediction_label": "Heart Disease",
  "confidence": {
    "no_disease": 0.23,
    "disease": 0.77
  },
  "risk_level": "High",
  "model_version": "1.0.0",
  "timestamp": "2025-12-24T...",
  "processing_time_ms": 12.34
}
```

### Method 3: Docker Compose (Alternative)
```bash
docker-compose up -d
```

## Troubleshooting

### Issue: "Docker is not running"
**Solution:** Start Docker Desktop application

### Issue: "Port is already allocated"
**Solution:** 
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
docker run -d -p 8001:8000 --name heart-disease-api heart-disease-api:latest
```

### Issue: "Cannot connect to Docker daemon"
**Solution:** 
1. Open Docker Desktop
2. Wait for it to fully start (whale icon in menu bar should be static)
3. Try the command again

### Issue: Container starts but health check fails
**Solution:**
```bash
# Check container logs
docker logs heart-disease-api

# Common causes:
# 1. Model file not found - ensure models/ directory is copied
# 2. Missing dependencies - rebuild image
# 3. Port binding issue - check with: lsof -i :8000
```

### Issue: Model not found error
**Solution:**
```bash
# Ensure you have trained a model first
python src/data/preprocessing.py
python src/models/train.py

# Verify model files exist
ls -lh models/

# Rebuild Docker image to include latest models
docker build -t heart-disease-api:latest . --no-cache
```

## Container Management

### View Running Containers
```bash
docker ps
```

### Stop Container
```bash
docker stop heart-disease-api
```

### Remove Container
```bash
docker rm heart-disease-api
```

### View Logs
```bash
# Last 100 lines
docker logs --tail 100 heart-disease-api

# Follow logs (real-time)
docker logs -f heart-disease-api
```

### Execute Command in Container
```bash
# Open shell in running container
docker exec -it heart-disease-api /bin/bash

# Check files in container
docker exec heart-disease-api ls -la /app/models/

# Test model loading
docker exec heart-disease-api python -c "import pickle; pickle.load(open('models/best_model.pkl', 'rb'))"
```

### Restart Container
```bash
docker restart heart-disease-api
```

## API Endpoints

### GET /health
Health check endpoint
```bash
curl http://localhost:8000/health
```

### POST /predict
Single prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @test_sample.json
```

### POST /batch_predict
Batch predictions
```bash
curl -X POST http://localhost:8000/batch_predict \
  -H "Content-Type: application/json" \
  -d '{"samples": [...]}'
```

### GET /model/info
Model information
```bash
curl http://localhost:8000/model/info
```

### GET /metrics
Prometheus metrics
```bash
curl http://localhost:8000/metrics
```

## Performance Tuning

### Adjust Workers
```bash
docker run -d -p 8000:8000 \
  --name heart-disease-api \
  heart-disease-api:latest \
  gunicorn src.api.app:app --bind 0.0.0.0:8000 --workers 4
```

### Set Memory Limits
```bash
docker run -d -p 8000:8000 \
  --name heart-disease-api \
  --memory="512m" \
  --cpus="1.0" \
  heart-disease-api:latest
```

## Production Deployment

For production, use docker-compose with proper configuration:

```yaml
version: '3.8'
services:
  api:
    image: heart-disease-api:latest
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      - MODEL_PATH=/app/models/best_model.pkl
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Status: ✅ RESOLVED

Docker container now:
- ✅ Builds successfully
- ✅ Runs on port 8000
- ✅ Uses gunicorn for production
- ✅ Loads model correctly
- ✅ Health checks pass
- ✅ Predictions work
- ✅ Prometheus metrics available

