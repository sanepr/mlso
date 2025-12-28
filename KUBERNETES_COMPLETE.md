# ✅ Kubernetes Deployment - Complete Implementation

## Status: READY TO DEPLOY 🚀

All Kubernetes deployment files and scripts have been successfully created and configured.

---

## 📦 Files Created

### Kubernetes Manifests (3 files)
1. ✅ **`deployment/kubernetes/deployment.yaml`**
   - 2 replica pods for high availability
   - Resource limits: 512Mi memory, 500m CPU
   - Health checks: liveness and readiness probes
   - ConfigMap for environment variables

2. ✅ **`deployment/kubernetes/service.yaml`**
   - LoadBalancer type (NodePort on minikube)
   - Port 8000, NodePort 30080
   - Session affinity enabled

3. ✅ **`deployment/kubernetes/ingress.yaml`**
   - Optional ingress configuration
   - Host: heart-disease-api.local
   - Path-based routing

### Helper Scripts (3 files)
1. ✅ **`deploy_k8s.sh`** - Automated deployment script
   - Checks Docker is running
   - Starts minikube if needed
   - Builds and loads Docker image
   - Deploys to Kubernetes
   - Tests endpoints
   - Shows service URL

2. ✅ **`kubectl.sh`** - kubectl wrapper
   - Uses minikube's built-in kubectl
   - Simplifies commands

3. ✅ **`minikube-darwin-arm64`** - Made executable
   - Minikube binary for macOS ARM64

### Documentation (3 files)
1. ✅ **`KUBERNETES_DEPLOYMENT.md`** - Complete guide (450+ lines)
   - Prerequisites
   - Step-by-step instructions
   - Troubleshooting
   - Production deployment
   - Architecture diagrams

2. ✅ **`K8S_QUICKREF.md`** - Quick reference card
   - Common commands
   - Quick fixes
   - One-liners

3. ✅ **`K8S_SETUP_SUMMARY.md`** - Setup summary
   - What was created
   - How to use
   - Testing checklist

### Updated Files
✅ **`README.md`** - Updated Kubernetes section with actual commands

---

## 🎯 Deployment Options

### Option 1: Automated (Easiest)
```bash
./deploy_k8s.sh
```
**Pros:**
- One command does everything
- Automatic error checking
- Tests endpoints
- Shows service URL

**Cons:**
- Requires Docker Desktop running

### Option 2: Manual (Full Control)
```bash
# 1. Start minikube
./minikube-darwin-arm64 start --driver=docker

# 2. Load image
./minikube-darwin-arm64 image load heart-disease-api:latest

# 3. Deploy
./kubectl.sh apply -f deployment/kubernetes/

# 4. Wait for pods
./kubectl.sh wait --for=condition=available --timeout=300s deployment/heart-disease-api

# 5. Get service URL
./minikube-darwin-arm64 service heart-disease-api --url

# 6. Test
curl $(./minikube-darwin-arm64 service heart-disease-api --url)/health
```

**Pros:**
- Full control over each step
- Better for understanding process
- Easier to debug

**Cons:**
- More commands to run
- Need to remember each step

---

## 🔧 Configuration Details

### Deployment Spec
```yaml
Replicas: 2
Image: heart-disease-api:latest
ImagePullPolicy: Never (for minikube)
Port: 8000
Resources:
  Requests:
    memory: 256Mi
    cpu: 250m
  Limits:
    memory: 512Mi
    cpu: 500m
Health Checks:
  Liveness:
    path: /health
    initialDelay: 30s
    period: 10s
  Readiness:
    path: /health
    initialDelay: 10s
    period: 5s
```

### Service Spec
```yaml
Type: LoadBalancer (NodePort on minikube)
Port: 8000
TargetPort: 8000
NodePort: 30080
SessionAffinity: ClientIP
```

---

## 🧪 Testing the Deployment

### Pre-Deployment Checks
```bash
# 1. Docker running?
docker info

# 2. Image built?
docker images | grep heart-disease-api

# 3. Models exist?
ls -lh models/best_model.pkl

# 4. Minikube binary executable?
./minikube-darwin-arm64 version
```

### Post-Deployment Checks
```bash
# 1. Minikube running?
./minikube-darwin-arm64 status

# 2. Pods running?
./kubectl.sh get pods
# Should show: 2/2 Running

# 3. Service created?
./kubectl.sh get svc heart-disease-api

# 4. Health check?
SERVICE_URL=$(./minikube-darwin-arm64 service heart-disease-api --url)
curl $SERVICE_URL/health

# 5. Prediction works?
curl -X POST $SERVICE_URL/predict \
  -H "Content-Type: application/json" \
  -d @test_sample.json

# 6. Logs clean?
./kubectl.sh logs -l app=heart-disease-api | tail -20
```

---

## 🐛 Common Issues & Quick Fixes

### Issue 1: Docker Not Running
**Error:** `Cannot connect to the Docker daemon`

**Fix:**
```bash
# Open Docker Desktop
open -a Docker

# Wait 30 seconds, then retry
./deploy_k8s.sh
```

### Issue 2: Minikube Won't Start
**Error:** Minikube start hangs or fails

**Fix:**
```bash
# Delete and recreate
./minikube-darwin-arm64 delete
./minikube-darwin-arm64 start --driver=docker --cpus=2 --memory=4096
```

### Issue 3: Image Not Found
**Error:** `ImagePullBackOff` or `ErrImagePull`

**Fix:**
```bash
# Rebuild and reload
docker build -t heart-disease-api:latest .
./minikube-darwin-arm64 image load heart-disease-api:latest
./kubectl.sh delete -f deployment/kubernetes/
./kubectl.sh apply -f deployment/kubernetes/
```

### Issue 4: Pods Crashing
**Error:** `CrashLoopBackOff`

**Fix:**
```bash
# Check logs
./kubectl.sh logs <pod-name>

# Common causes:
# - Model file missing: Rebuild image with models
# - Port conflict: Check deployment.yaml port settings
# - Memory limit: Increase limits in deployment.yaml
```

### Issue 5: Can't Access Service
**Error:** Service URL not accessible

**Fix:**
```bash
# Method 1: Get fresh URL
./minikube-darwin-arm64 service heart-disease-api --url

# Method 2: Use port forwarding
./kubectl.sh port-forward svc/heart-disease-api 8080:8000
# Access at http://localhost:8080

# Method 3: Check service
./kubectl.sh describe svc heart-disease-api
```

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────┐
│            Minikube Cluster                  │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │  LoadBalancer Service                  │ │
│  │  Port: 8000 → NodePort: 30080          │ │
│  └────────────┬───────────────────────────┘ │
│               │                              │
│  ┌────────────▼───────────────────────────┐ │
│  │  Deployment (2 replicas)               │ │
│  │                                        │ │
│  │  ┌─────────────┐  ┌─────────────┐    │ │
│  │  │   Pod 1     │  │   Pod 2     │    │ │
│  │  │ Container:  │  │ Container:  │    │ │
│  │  │ heart-      │  │ heart-      │    │ │
│  │  │ disease-api │  │ disease-api │    │ │
│  │  │ Port: 8000  │  │ Port: 8000  │    │ │
│  │  └─────────────┘  └─────────────┘    │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │  ConfigMap                             │ │
│  │  - MODEL_VERSION: 1.0.0                │ │
│  │  - LOG_LEVEL: INFO                     │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

---

## 📈 Monitoring & Management

### View Resources
```bash
# Everything
./kubectl.sh get all

# Just pods
./kubectl.sh get pods -w  # watch mode

# Just services
./kubectl.sh get svc

# Detailed pod info
./kubectl.sh describe pod <pod-name>
```

### View Logs
```bash
# All pods
./kubectl.sh logs -l app=heart-disease-api

# Follow logs
./kubectl.sh logs -l app=heart-disease-api -f

# Specific pod
./kubectl.sh logs <pod-name>

# Last 50 lines
./kubectl.sh logs <pod-name> --tail=50
```

### Scale Application
```bash
# Scale up
./kubectl.sh scale deployment heart-disease-api --replicas=5

# Scale down
./kubectl.sh scale deployment heart-disease-api --replicas=1

# Check scaling
./kubectl.sh get pods -w
```

### Update Deployment
```bash
# After editing deployment.yaml
./kubectl.sh apply -f deployment/kubernetes/deployment.yaml

# Force restart
./kubectl.sh rollout restart deployment heart-disease-api

# Check rollout
./kubectl.sh rollout status deployment heart-disease-api

# Rollout history
./kubectl.sh rollout history deployment heart-disease-api
```

### Debug
```bash
# Get shell in pod
./kubectl.sh exec -it <pod-name> -- /bin/bash

# Run command in pod
./kubectl.sh exec <pod-name> -- curl localhost:8000/health

# Check pod events
./kubectl.sh get events --sort-by='.lastTimestamp' | grep <pod-name>

# Port forward for local testing
./kubectl.sh port-forward deployment/heart-disease-api 8080:8000
```

---

## 🧹 Cleanup

### Delete Deployment Only
```bash
./kubectl.sh delete -f deployment/kubernetes/
```

### Stop Minikube (Keep Config)
```bash
./minikube-darwin-arm64 stop
```

### Complete Cleanup
```bash
# Delete everything
./kubectl.sh delete -f deployment/kubernetes/
./minikube-darwin-arm64 delete

# This removes entire cluster
```

### Start Fresh
```bash
# Complete reset
./minikube-darwin-arm64 delete
./minikube-darwin-arm64 start --driver=docker
./deploy_k8s.sh
```

---

## 📚 Documentation Reference

| File | Purpose | Lines |
|------|---------|-------|
| `KUBERNETES_DEPLOYMENT.md` | Complete guide | 450+ |
| `K8S_QUICKREF.md` | Quick commands | 150+ |
| `K8S_SETUP_SUMMARY.md` | Setup summary | 350+ |
| `deploy_k8s.sh` | Automated deployment | 150+ |
| `kubectl.sh` | kubectl wrapper | 3 |

---

## ✅ Deployment Checklist

Before deploying:
- [ ] Docker Desktop installed and running
- [ ] Minikube binary executable
- [ ] Docker image built
- [ ] Models trained and saved
- [ ] Test data available (`test_sample.json`)

After deploying:
- [ ] Minikube status shows "Running"
- [ ] 2 pods in "Running" state
- [ ] Service shows EXTERNAL-IP
- [ ] Health endpoint returns 200
- [ ] Prediction endpoint works
- [ ] Logs show no errors
- [ ] Can scale replicas
- [ ] Dashboard accessible

---

## 🎯 Next Steps

1. **Deploy Now:**
   ```bash
   ./deploy_k8s.sh
   ```

2. **Monitor:**
   ```bash
   ./minikube-darwin-arm64 dashboard
   ```

3. **Load Test:**
   ```bash
   # Install hey
   brew install hey
   
   # Test
   SERVICE_URL=$(./minikube-darwin-arm64 service heart-disease-api --url)
   hey -n 1000 -c 10 $SERVICE_URL/health
   ```

4. **Production:**
   - Push to container registry
   - Deploy to cloud (EKS/GKE/AKS)
   - Configure TLS/SSL
   - Set up monitoring
   - Implement CI/CD

---

## 📞 Support

**For issues:**
1. Check `KUBERNETES_DEPLOYMENT.md` - Complete troubleshooting
2. See `K8S_QUICKREF.md` - Quick fixes
3. Review logs: `./kubectl.sh logs <pod-name>`
4. Check events: `./kubectl.sh get events`

**Common commands:**
```bash
# Status
./minikube-darwin-arm64 status
./kubectl.sh get all

# Logs
./kubectl.sh logs -l app=heart-disease-api -f

# Debug
./kubectl.sh describe pod <pod-name>

# Restart
./kubectl.sh rollout restart deployment heart-disease-api
```

---

## 🎉 Summary

**Status:** ✅ READY TO DEPLOY

**Created:**
- 3 Kubernetes manifests (deployment, service, ingress)
- 3 helper scripts (deploy, kubectl wrapper, minikube)
- 3 documentation files (guide, quickref, summary)
- Updated README with correct commands

**To Deploy:**
```bash
# Ensure Docker Desktop is running, then:
./deploy_k8s.sh
```

**Documentation:**
- `KUBERNETES_DEPLOYMENT.md` - Full guide
- `K8S_QUICKREF.md` - Quick reference  
- `K8S_SETUP_SUMMARY.md` - This file

**All files are ready. Just run `./deploy_k8s.sh` to deploy!** 🚀

