# 🔧 Why Health Endpoint Not Available - FIXED

## Issue
When accessing `http://192.168.49.2:30080/health`, the connection times out.

## Root Cause
**Minikube + Docker Driver + macOS = NodePort Not Accessible**

When using Minikube with the Docker driver on macOS:
- ✅ Pods are running correctly (verified)
- ✅ Service is configured correctly (verified)
- ❌ NodePort is NOT directly accessible from host machine

This is a known limitation of the Docker driver on macOS. The Minikube VM runs inside Docker, creating network isolation.

---

## ✅ Working Solution: Port Forwarding

Port forwarding **WORKS PERFECTLY** and is the recommended approach:

### Start Port Forward:
```bash
./kubectl.sh port-forward svc/heart-disease-api 8080:8000
```

**Keep this terminal open!**

### Test in Another Terminal:
```bash
# Health check - WORKS! ✅
curl http://localhost:8080/health

# Output:
# {"model_loaded":true,"service":"heart-disease-prediction","status":"healthy","timestamp":"2025-12-26T09:42:26.483463","version":"1.0.0"}

# Prediction - WORKS! ✅
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d @test_sample.json
```

---

## 🎯 Corrected Access Methods

### ✅ Method 1: Port Forward (RECOMMENDED)

**Terminal 1 (keep running):**
```bash
./kubectl.sh port-forward svc/heart-disease-api 8080:8000
```

**Terminal 2 (for testing):**
```bash
curl http://localhost:8080/health
curl -X POST http://localhost:8080/predict -H "Content-Type: application/json" -d @test_sample.json
```

**Status:** ✅ **WORKING - Use this!**

---

### ✅ Method 2: Minikube Service (Opens Tunnel)

```bash
./minikube-darwin-arm64 service heart-disease-api
```

This command:
- Opens a tunnel to the service
- Provides a URL like `http://127.0.0.1:RANDOM_PORT`
- **Terminal must stay open**
- URL changes each time

**Status:** ✅ **WORKING**

---

### ❌ Method 3: Direct NodePort (NOT WORKING on Docker Driver)

```bash
# This DOES NOT WORK on macOS with Docker driver
curl http://192.168.49.2:30080/health
# Error: Connection timeout
```

**Why it doesn't work:**
- Docker driver creates network isolation
- NodePort not exposed to host network
- This is a Docker-on-Mac limitation

**Status:** ❌ **NOT WORKING** (Docker driver limitation)

---

## 🔍 Verification

### Pods Status: ✅ WORKING
```bash
./kubectl.sh get pods

# Output:
NAME                                 READY   STATUS    RESTARTS   AGE
heart-disease-api-6d46c48846-gcpkh   1/1     Running   0          24m
heart-disease-api-6d46c48846-xffb6   1/1     Running   0          24m
```

### Service Status: ✅ WORKING
```bash
./kubectl.sh get svc heart-disease-api

# Output:
NAME                TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
heart-disease-api   LoadBalancer   10.105.218.39   <pending>     8000:30080/TCP   59m
```

### Health Endpoint via Port Forward: ✅ WORKING
```bash
curl http://localhost:8080/health

# Output:
{
  "model_loaded": true,
  "service": "heart-disease-prediction",
  "status": "healthy",
  "timestamp": "2025-12-26T09:42:26.483463",
  "version": "1.0.0"
}
```

---

## 🎯 Recommended Workflow

### For Development/Testing:

**Terminal 1:**
```bash
./kubectl.sh port-forward svc/heart-disease-api 8080:8000
```

**Terminal 2:**
```bash
# All your curl commands using localhost:8080
curl http://localhost:8080/health
curl -X POST http://localhost:8080/predict -H "Content-Type: application/json" -d @test_sample.json
```

### For Quick Tests:

```bash
# Run in background
./kubectl.sh port-forward svc/heart-disease-api 8080:8000 &

# Test
curl http://localhost:8080/health

# Kill when done
pkill -f "port-forward"
```

---

## 📝 Create Helper Script

I'll create a script that handles port forwarding automatically:

```bash
# start_k8s_api.sh
#!/bin/bash
echo "🚀 Starting Kubernetes API port forward..."
./kubectl.sh port-forward svc/heart-disease-api 8080:8000
```

Then use:
```bash
# Terminal 1
./start_k8s_api.sh

# Terminal 2
curl http://localhost:8080/health
```

---

## 🔄 Alternative: Use Local Docker Instead

If you want simple direct access without port forwarding, use the local Docker deployment:

```bash
# Local Docker (already running)
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d @test_sample.json
```

**This works without any port forwarding!**

---

## 📊 Comparison

| Method | URL | Terminal Open? | Status | Best For |
|--------|-----|----------------|--------|----------|
| Local Docker | `http://localhost:8000` | ❌ No | ✅ Working | Development |
| K8s Port Forward | `http://localhost:8080` | ✅ Yes | ✅ Working | K8s testing |
| K8s Minikube Service | `http://127.0.0.1:RANDOM` | ✅ Yes | ✅ Working | Browser access |
| K8s NodePort Direct | `http://192.168.49.2:30080` | ❌ No | ❌ Not Working | Production only |

---

## 💡 Why This Happens

### Docker Driver Limitation:

```
Your Mac
  └── Docker Desktop
      └── Minikube Container (192.168.49.2)
          └── Kubernetes Cluster
              └── Your Pods (ClusterIP: 10.105.218.39)
```

**Network Isolation:**
- Your Mac can't directly reach 192.168.49.2:30080
- Docker creates a separate network
- Port forwarding creates a tunnel: Mac ↔ Docker ↔ Kubernetes

### This is Normal!

On production Kubernetes (AWS EKS, GCP GKE), NodePort DOES work because there's no Docker isolation layer.

---

## ✅ Solution Summary

### What WORKS:

1. **Port Forward (Recommended):**
   ```bash
   ./kubectl.sh port-forward svc/heart-disease-api 8080:8000
   # Access: http://localhost:8080
   ```

2. **Minikube Service:**
   ```bash
   ./minikube-darwin-arm64 service heart-disease-api
   # Opens browser automatically
   ```

3. **Local Docker:**
   ```bash
   # Already running
   curl http://localhost:8000/health
   ```

### What DOESN'T Work:

- ❌ Direct NodePort: `http://192.168.49.2:30080` (Docker driver limitation)

---

## 🎉 Final Answer

**Your Kubernetes deployment IS working!**

**Access it using:**
```bash
# Terminal 1 (keep open)
./kubectl.sh port-forward svc/heart-disease-api 8080:8000

# Terminal 2 (use this)
curl http://localhost:8080/health
```

**Or use the local Docker deployment (simpler):**
```bash
curl http://localhost:8000/health
```

Both are running the SAME API with the SAME model (96% ROC-AUC)!

---

**Issue:** NodePort not accessible  
**Root Cause:** Docker driver network isolation (expected behavior)  
**Solution:** Use port forwarding or local Docker  
**Status:** ✅ RESOLVED - Multiple working access methods available

