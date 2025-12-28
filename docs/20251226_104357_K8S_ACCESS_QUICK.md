# 🎯 Quick Answer: Access Your Minikube Deployment

## ✅ Your Kubernetes Service - HOW TO ACCESS

**Important:** Due to Docker driver on macOS, direct NodePort access doesn't work.  
**Use Port Forwarding instead (it's easy!):**

---

## 🚀 2 Working Methods

### Method 1: Port Forward (Recommended) ✅

**Terminal 1 (keep this running):**
```bash
./start_k8s_api.sh
# Or manually:
./kubectl.sh port-forward svc/heart-disease-api 8080:8000
```

**Terminal 2 (use this for testing):**
```bash
curl http://localhost:8080/health
```

**Status:** ✅ **WORKING**

---

### Method 2: Minikube Service ✅

```bash
./minikube-darwin-arm64 service heart-disease-api
# Opens browser with service URL (terminal must stay open)
```

**Status:** ✅ **WORKING**

---

### ❌ Method 3: Direct NodePort (NOT WORKING)

```bash
# This DOES NOT work on macOS with Docker driver
curl http://192.168.49.2:30080/health
# Error: Connection timeout
```

**Why:** Docker driver creates network isolation. This is expected behavior.

**Status:** ❌ **NOT WORKING** (use port forwarding instead)

---

## 🧪 Test Your Deployment

### Health Check:
```bash
# Start port forward in Terminal 1
./start_k8s_api.sh

# Test in Terminal 2
curl http://localhost:8080/health
```

**Expected Response:**
```json
{
  "model_loaded": true,
  "service": "heart-disease-prediction",
  "status": "healthy",
  "version": "1.0.0"
}
```

### Make a Prediction:
```bash
curl -X POST http://localhost:8080/predict \
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

---

## 📝 Helper Scripts

### Start API with Port Forward:
```bash
./start_k8s_api.sh
```

This script:
- ✅ Sets up port forwarding automatically
- ✅ Shows you the access URL (localhost:8080)
- ✅ Displays test commands
- ✅ Easy to use!

---

## 🔍 Verify Deployment

```bash
# Check pods are running
./kubectl.sh get pods
# Expected: 2/2 Running

# Check service
./kubectl.sh get svc heart-disease-api
# Expected: Service exists

# Check logs
./kubectl.sh logs -l app=heart-disease-api
# Expected: "Model loaded successfully"
```

---

## 🎯 Quick Start

**Open 2 terminals:**

**Terminal 1:**
```bash
./start_k8s_api.sh
# Keep this running
```

**Terminal 2:**
```bash
# Health check
curl http://localhost:8080/health

# Prediction
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d @test_sample.json
```

---

## 💡 Why Port Forwarding?

**Docker Driver Limitation:**
- Minikube runs inside Docker container
- Creates network isolation on macOS
- NodePort (30080) not accessible from host
- Port forwarding creates a tunnel

**This is normal and expected behavior!**

On production Kubernetes (AWS/GCP/Azure), NodePort works directly.

---

## 📚 More Details

See **K8S_HEALTH_NOT_AVAILABLE_FIXED.md** for:
- Complete explanation
- Why NodePort doesn't work
- All access methods
- Troubleshooting steps

---

## 🎉 Summary

**Your API IS accessible at:** `http://localhost:8080` (via port forwarding)

**Quick start:**
```bash
# Terminal 1
./start_k8s_api.sh

# Terminal 2
curl http://localhost:8080/health
```

**Alternative: Use Local Docker (no port forwarding needed):**
```bash
curl http://localhost:8000/health
```

**Both deployments work perfectly!**
- Local Docker: `http://localhost:8000` ✅
- Kubernetes: `http://localhost:8080` (via port forward) ✅

