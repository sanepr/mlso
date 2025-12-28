# 🎉 Docker Fix - Complete Summary

## Issue Resolved
Fixed `docker run -p 8000:8000 heart-disease-api:latest` command that was failing.

---

## 🔧 Problems Fixed

### 1. Wrong Application Server ❌ → ✅
- **Before:** Dockerfile used `uvicorn` (for FastAPI)
- **After:** Changed to `gunicorn` (for Flask)
- **Why:** The app.py is a Flask application, not FastAPI

### 2. Missing Dependencies ❌ → ✅
- **Added to requirements.txt:**
  - `flask==2.3.3`
  - `werkzeug==2.3.7`
  - `gunicorn==21.2.0`

### 3. Wrong Model Path ❌ → ✅
- **Before:** Looking for `models/heart_disease_model.pkl`
- **After:** Uses `models/best_model.pkl` with fallback paths

### 4. Missing Health Check Tool ❌ → ✅
- **Added:** `curl` to Dockerfile for health checks

### 5. Port Configuration ❌ → ✅
- **Before:** Flask running on port 5000
- **After:** Configured to run on port 8000

---

## 📁 Files Created/Modified

### New Files Created:
1. ✅ `test_docker.sh` - Automated test script
2. ✅ `DOCKER_FIX.md` - Complete troubleshooting guide
3. ✅ `test_sample.json` - Sample data for testing

### Files Modified:
1. ✅ `Dockerfile` - Fixed CMD, added curl, added data/ copy
2. ✅ `requirements.txt` - Added Flask and gunicorn
3. ✅ `src/api/app.py` - Fixed model loading and port
4. ✅ `README.md` - Updated Docker instructions

---

## 🚀 How to Use

### Option 1: Quick Test (Recommended)
```bash
./test_docker.sh
```

### Option 2: Manual Steps
```bash
# 1. Ensure Docker Desktop is running

# 2. Build the image
docker build -t heart-disease-api:latest .

# 3. Clean up
docker stop heart-disease-api 2>/dev/null || true
docker rm heart-disease-api 2>/dev/null || true

# 4. Run the container
docker run -d -p 8000:8000 --name heart-disease-api heart-disease-api:latest

# 5. Test it
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d @test_sample.json
```

---

## 🧪 Testing Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-24T...",
  "service": "heart-disease-prediction",
  "version": "1.0.0",
  "model_loaded": true
}
```

### Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63, "sex": 1, "cp": 3, "trestbps": 145,
    "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150,
    "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
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
  "processing_time_ms": 12.34
}
```

### Model Info
```bash
curl http://localhost:8000/model/info
```

### Prometheus Metrics
```bash
curl http://localhost:8000/metrics
```

---

## 📊 Technical Details

### Dockerfile Configuration
```dockerfile
FROM python:3.9-slim
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y gcc curl

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application files
COPY src/ ./src/
COPY models/ ./models/
COPY data/ ./data/

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8000/health || exit 1

# Production server
CMD ["gunicorn", "src.api.app:app", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]
```

### Gunicorn Configuration
- **Workers:** 2 (adjust based on CPU cores: 2-4 × CPU cores)
- **Timeout:** 120 seconds
- **Bind:** 0.0.0.0:8000 (all interfaces)

---

## 🔍 Verification Checklist

Before running Docker:
- ✅ Docker Desktop is installed and running
- ✅ Models are trained (`python src/models/train.py`)
- ✅ `models/best_model.pkl` exists
- ✅ No process using port 8000

After running Docker:
- ✅ Container status is "Up"
- ✅ Health endpoint returns 200
- ✅ Prediction endpoint works
- ✅ No errors in logs

---

## 🐛 Common Issues & Solutions

### Issue: Docker daemon not running
**Solution:** Start Docker Desktop application

### Issue: Port 8000 already in use
**Solution:**
```bash
lsof -ti:8000 | xargs kill -9
```

### Issue: Model file not found
**Solution:**
```bash
# Train models first
python src/data/preprocessing.py
python src/models/train.py

# Verify
ls -lh models/best_model.pkl

# Rebuild image
docker build -t heart-disease-api:latest . --no-cache
```

### Issue: Container starts but exits immediately
**Solution:**
```bash
# Check logs
docker logs heart-disease-api

# Common causes:
# 1. Model loading failed
# 2. Port conflict
# 3. Missing dependencies
```

---

## 📈 Performance Tuning

### Adjust Workers
```bash
docker run -d -p 8000:8000 \
  --name heart-disease-api \
  heart-disease-api:latest \
  gunicorn src.api.app:app --bind 0.0.0.0:8000 --workers 4 --threads 2
```

### Set Resource Limits
```bash
docker run -d -p 8000:8000 \
  --name heart-disease-api \
  --memory="512m" \
  --cpus="1.0" \
  heart-disease-api:latest
```

---

## 📦 Container Management

### View Logs
```bash
# Last 100 lines
docker logs --tail 100 heart-disease-api

# Follow in real-time
docker logs -f heart-disease-api
```

### Execute Commands
```bash
# Open shell
docker exec -it heart-disease-api /bin/bash

# Check files
docker exec heart-disease-api ls -la /app/models/

# Test Python imports
docker exec heart-disease-api python -c "import flask; print('Flask OK')"
```

### Stop/Remove
```bash
docker stop heart-disease-api
docker rm heart-disease-api
```

---

## ✅ Status: RESOLVED

The Docker container now:
- ✅ Builds successfully without errors
- ✅ Runs on port 8000 with gunicorn
- ✅ Loads models correctly from models/best_model.pkl
- ✅ Health checks pass consistently
- ✅ Predictions work correctly
- ✅ Prometheus metrics are exposed
- ✅ Production-ready with proper error handling

---

## 📚 Additional Resources

- **Detailed Guide:** See `DOCKER_FIX.md`
- **Test Script:** Run `./test_docker.sh`
- **Sample Data:** Use `test_sample.json`
- **README:** Updated with complete instructions

---

## 🎯 Next Steps

1. ✅ **DONE:** Docker container working
2. **Optional:** Set up docker-compose for easier management
3. **Optional:** Deploy to cloud (AWS ECS, Google Cloud Run, etc.)
4. **Optional:** Set up CI/CD for automated builds
5. **Optional:** Add monitoring with Prometheus + Grafana

---

**Date Fixed:** December 24, 2025  
**Status:** ✅ All issues resolved  
**Docker Image:** heart-disease-api:latest  
**Port:** 8000  
**Server:** Gunicorn + Flask  

