# Docker Quick Reference

## 🚀 Quick Start
```bash
./test_docker.sh
```

## 🔨 Build
```bash
docker build -t heart-disease-api:latest .
```

## ▶️ Run
```bash
docker run -d -p 8000:8000 --name heart-disease-api heart-disease-api:latest
```

## 🧹 Clean Up
```bash
docker stop heart-disease-api && docker rm heart-disease-api
```

## 📋 View Logs
```bash
docker logs -f heart-disease-api
```

## 🏥 Test Health
```bash
curl http://localhost:8000/health
```

## 🔮 Test Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @test_sample.json
```

## 🐛 Troubleshoot
```bash
# Check container status
docker ps -a | grep heart-disease

# View last 50 log lines
docker logs --tail 50 heart-disease-api

# Execute shell in container
docker exec -it heart-disease-api /bin/bash

# Check model file
docker exec heart-disease-api ls -lh /app/models/

# Kill port 8000
lsof -ti:8000 | xargs kill -9
```

## 📊 Monitor
```bash
# Container stats
docker stats heart-disease-api

# Container inspect
docker inspect heart-disease-api

# Prometheus metrics
curl http://localhost:8000/metrics
```

