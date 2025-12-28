# 🌐 Accessing Minikube Kubernetes Deployment

## Your Deployment Information

**Service Name:** heart-disease-api  
**Service Type:** LoadBalancer (NodePort on Minikube)  
**Port:** 8000  
**NodePort:** 30080  
**Minikube IP:** 192.168.49.2  

---

## 🚀 3 Ways to Access Your Deployment

### Method 1: Direct NodePort Access (Recommended for Quick Testing)

**URL:** `http://192.168.49.2:30080`

```bash
# Health check
curl http://192.168.49.2:30080/health

# Prediction
curl -X POST http://192.168.49.2:30080/predict \
  -H "Content-Type: application/json" \
  -d @test_sample.json
```

**Pros:** Simple, direct access  
**Cons:** Need to know NodePort (30080)

---

### Method 2: Minikube Service Command (Opens Browser/Terminal)

```bash
./minikube-darwin-arm64 service heart-disease-api
```

**What this does:**
- Opens a tunnel to the service
- Provides a localhost URL (e.g., http://127.0.0.1:56279)
- **Must keep terminal open** while using the service
- Auto-assigns a random local port

**Example:**
```bash
./minikube-darwin-arm64 service heart-disease-api
# Output: http://127.0.0.1:56279
# ❗ Because you are using a Docker driver, the terminal needs to be open
```

Then in another terminal:
```bash
curl http://127.0.0.1:56279/health
```

**Pros:** Easy to use, handles port forwarding  
**Cons:** Terminal must stay open

---

### Method 3: kubectl Port Forward (Best for Development)

```bash
# Forward port 8080 on localhost to port 8000 in the service
./minikube-darwin-arm64 kubectl -- port-forward svc/heart-disease-api 8080:8000
```

Then access at: `http://localhost:8080`

**Test it:**
```bash
# In another terminal
curl http://localhost:8080/health
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d @test_sample.json
```

**Pros:** Use familiar localhost URL, stable port  
**Cons:** Terminal must stay open

---

## 🧪 Quick Test Commands

### Using Direct NodePort (192.168.49.2:30080):

```bash
# Health check
curl http://192.168.49.2:30080/health

# Sample prediction
curl -X POST http://192.168.49.2:30080/predict \
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

# Model info
curl http://192.168.49.2:30080/model/info

# Metrics
curl http://192.168.49.2:30080/metrics
```

---

## 📋 Service Information

### Get Service Details:
```bash
./minikube-darwin-arm64 kubectl -- get svc heart-disease-api
```

**Output:**
```
NAME                TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
heart-disease-api   LoadBalancer   10.105.218.39   <pending>     8000:30080/TCP   52m
```

**Key Info:**
- **CLUSTER-IP:** 10.105.218.39 (internal only)
- **PORT(S):** 8000:30080 (8000 is container port, 30080 is NodePort)
- **EXTERNAL-IP:** `<pending>` (normal for Minikube)

### Get Minikube IP:
```bash
./minikube-darwin-arm64 ip
# Output: 192.168.49.2
```

### Get Pods:
```bash
./minikube-darwin-arm64 kubectl -- get pods
```

**Expected:**
```
NAME                                 READY   STATUS    RESTARTS   AGE
heart-disease-api-xxx                1/1     Running   0          15m
heart-disease-api-xxx                1/1     Running   0          15m
```

---

## 🔧 Troubleshooting

### Issue: Connection Refused or Timeout

**Check 1: Are pods running?**
```bash
./minikube-darwin-arm64 kubectl -- get pods
# Should show: READY 1/1, STATUS Running
```

**Check 2: Is service created?**
```bash
./minikube-darwin-arm64 kubectl -- get svc heart-disease-api
# Should show the service details
```

**Check 3: Can you access from inside the cluster?**
```bash
# Get pod name
POD_NAME=$(./minikube-darwin-arm64 kubectl -- get pods -l app=heart-disease-api -o jsonpath='{.items[0].metadata.name}')

# Test from inside pod
./minikube-darwin-arm64 kubectl -- exec -it $POD_NAME -- curl localhost:8000/health
```

**Check 4: Check pod logs**
```bash
./minikube-darwin-arm64 kubectl -- logs -l app=heart-disease-api
# Should show: "Model loaded successfully"
```

---

## 🎯 Recommended Workflow

### For Quick Testing:
```bash
# Use direct NodePort access
curl http://192.168.49.2:30080/health
```

### For Development:
```bash
# Terminal 1: Port forward
./minikube-darwin-arm64 kubectl -- port-forward svc/heart-disease-api 8080:8000

# Terminal 2: Test
curl http://localhost:8080/health
```

### For Browser Access:
```bash
# This will open in browser
./minikube-darwin-arm64 service heart-disease-api
```

---

## 📊 Complete Example

### Setup (one time):
```bash
# 1. Get Minikube IP
MINIKUBE_IP=$(./minikube-darwin-arm64 ip)
echo "Minikube IP: $MINIKUBE_IP"

# 2. Get NodePort
NODE_PORT=$(./minikube-darwin-arm64 kubectl -- get svc heart-disease-api -o jsonpath='{.spec.ports[0].nodePort}')
echo "NodePort: $NODE_PORT"

# 3. Build URL
SERVICE_URL="http://${MINIKUBE_IP}:${NODE_PORT}"
echo "Service URL: $SERVICE_URL"
```

### Test:
```bash
# Health check
curl $SERVICE_URL/health

# Prediction
curl -X POST $SERVICE_URL/predict \
  -H "Content-Type: application/json" \
  -d @test_sample.json
```

---

## 🌐 URL Summary

You have **multiple options** to access your deployment:

| Method | URL | Terminal Open? | Best For |
|--------|-----|----------------|----------|
| NodePort | `http://192.168.49.2:30080` | ❌ No | Quick tests, scripts |
| Minikube Service | `http://127.0.0.1:RANDOM` | ✅ Yes | Browser access |
| Port Forward | `http://localhost:8080` | ✅ Yes | Development |
| Local Docker | `http://localhost:8000` | ❌ No | Local testing |

---

## 💡 Tips

### Save the URL for easy access:
```bash
# Add to your shell profile (~/.zshrc or ~/.bashrc)
export K8S_API="http://192.168.49.2:30080"

# Then use:
curl $K8S_API/health
```

### Create an alias:
```bash
# Add to ~/.zshrc
alias k8s-health='curl http://192.168.49.2:30080/health'
alias k8s-predict='curl -X POST http://192.168.49.2:30080/predict -H "Content-Type: application/json" -d @test_sample.json'

# Use:
k8s-health
k8s-predict
```

### Use a helper script:
```bash
# Create get-k8s-url.sh
#!/bin/bash
MINIKUBE_IP=$(./minikube-darwin-arm64 ip)
NODE_PORT=$(./minikube-darwin-arm64 kubectl -- get svc heart-disease-api -o jsonpath='{.spec.ports[0].nodePort}')
echo "http://${MINIKUBE_IP}:${NODE_PORT}"

# Use:
./get-k8s-url.sh
```

---

## ✅ Verification

### Check everything is working:
```bash
# 1. Pods running
./minikube-darwin-arm64 kubectl -- get pods
# Expected: 2/2 Running

# 2. Service exists
./minikube-darwin-arm64 kubectl -- get svc heart-disease-api
# Expected: LoadBalancer with NodePort 30080

# 3. Health check works
curl http://192.168.49.2:30080/health
# Expected: {"status": "healthy", "model_loaded": true}

# 4. Prediction works
curl -X POST http://192.168.49.2:30080/predict \
  -H "Content-Type: application/json" \
  -d @test_sample.json
# Expected: Prediction response with confidence scores
```

---

## 🎉 Quick Access

**Your Kubernetes deployment is accessible at:**

### Primary URL (Direct Access):
```
http://192.168.49.2:30080
```

### Alternative (Port Forward):
```bash
# Run this in a terminal (keep it open)
./minikube-darwin-arm64 kubectl -- port-forward svc/heart-disease-api 8080:8000

# Access at:
http://localhost:8080
```

### Alternative (Minikube Service):
```bash
# Run this (opens browser)
./minikube-darwin-arm64 service heart-disease-api
```

---

**Recommendation:** Use `http://192.168.49.2:30080` for the simplest access without keeping a terminal open!

**Status:** ✅ Kubernetes deployment accessible and ready to use

