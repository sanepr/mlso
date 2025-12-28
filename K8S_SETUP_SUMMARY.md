# 🎉 Kubernetes Deployment - Complete Setup

## Status: ✅ READY FOR DEPLOYMENT

All Kubernetes configuration files and deployment scripts have been created and are ready to use.

---

## 📦 What Was Created

### Kubernetes Manifests
1. ✅ **`deployment/kubernetes/deployment.yaml`** - Application deployment with 2 replicas
2. ✅ **`deployment/kubernetes/service.yaml`** - LoadBalancer service on port 8000
3. ✅ **`deployment/kubernetes/ingress.yaml`** - Ingress configuration (optional)

### Helper Scripts
1. ✅ **`deploy_k8s.sh`** - Automated deployment script
2. ✅ **`kubectl.sh`** - kubectl wrapper using minikube

### Documentation
1. ✅ **`KUBERNETES_DEPLOYMENT.md`** - Complete deployment guide
2. ✅ **`K8S_QUICKREF.md`** - Quick reference card

---

## 🚀 Quick Start

### Prerequisites Check
Before deploying, ensure:
- ✅ Docker Desktop is installed and **running**
- ✅ Minikube binary is available (`minikube-darwin-arm64`)
- ✅ Docker image is built (`heart-disease-api:latest`)
- ✅ Models are trained (`models/best_model.pkl` exists)

### Deployment Methods

#### Method 1: Automated (Recommended)
```bash
# One command to deploy everything
./deploy_k8s.sh
```

This script will:
1. Check if Docker is running
2. Start minikube if needed
3. Build Docker image if missing
4. Load image into minikube
5. Deploy to Kubernetes
6. Wait for pods to be ready
7. Test health and prediction endpoints
8. Display service URL

#### Method 2: Manual Step-by-Step

**Step 1: Ensure Docker Desktop is Running**
```bash
docker info
# Should show Docker info without errors
```

**Step 2: Start Minikube**
```bash
./minikube-darwin-arm64 start --driver=docker --cpus=2 --memory=4096
```
*First start may take 2-5 minutes*

**Step 3: Verify Minikube**
```bash
./minikube-darwin-arm64 status
```

**Step 4: Build Docker Image** (if not already built)
```bash
docker build -t heart-disease-api:latest .
```

**Step 5: Load Image into Minikube**
```bash
./minikube-darwin-arm64 image load heart-disease-api:latest
```
*This makes the image available inside minikube cluster*

**Step 6: Deploy to Kubernetes**
```bash
# Using minikube's kubectl
./minikube-darwin-arm64 kubectl -- apply -f deployment/kubernetes/

# Or using the wrapper script
./kubectl.sh apply -f deployment/kubernetes/
```

**Step 7: Wait for Deployment**
```bash
./kubectl.sh wait --for=condition=available --timeout=300s deployment/heart-disease-api
```

**Step 8: Check Status**
```bash
./kubectl.sh get pods
./kubectl.sh get services
./kubectl.sh get deployments
```

**Step 9: Get Service URL**
```bash
./minikube-darwin-arm64 service heart-disease-api --url
```

**Step 10: Test the API**
```bash
# Save the service URL
SERVICE_URL=$(./minikube-darwin-arm64 service heart-disease-api --url)

# Test health endpoint
curl $SERVICE_URL/health

# Test prediction endpoint
curl -X POST $SERVICE_URL/predict \
  -H "Content-Type: application/json" \
  -d @test_sample.json
```

---

## 📊 Architecture

### Deployment Configuration
- **Replicas:** 2 pods (for high availability)
- **Image:** heart-disease-api:latest
- **Port:** 8000
- **Resources:**
  - Requests: 256Mi memory, 250m CPU
  - Limits: 512Mi memory, 500m CPU
- **Health Checks:**
  - Liveness Probe: HTTP GET /health
  - Readiness Probe: HTTP GET /health

### Service Configuration
- **Type:** LoadBalancer (NodePort on minikube)
- **Port:** 8000
- **NodePort:** 30080
- **Session Affinity:** ClientIP

---

## 🔍 Monitoring & Management

### View Resources
```bash
# All resources
./kubectl.sh get all

# Specific resources
./kubectl.sh get pods
./kubectl.sh get services
./kubectl.sh get deployments
```

### View Logs
```bash
# All pods logs
./kubectl.sh logs -l app=heart-disease-api

# Follow logs in real-time
./kubectl.sh logs -l app=heart-disease-api -f

# Specific pod
./kubectl.sh logs <pod-name>
```

### Scale Deployment
```bash
# Scale up to 3 replicas
./kubectl.sh scale deployment heart-disease-api --replicas=3

# Scale down to 1 replica
./kubectl.sh scale deployment heart-disease-api --replicas=1
```

### Update Deployment
```bash
# After modifying deployment files
./kubectl.sh apply -f deployment/kubernetes/deployment.yaml

# Force restart
./kubectl.sh rollout restart deployment heart-disease-api

# Check rollout status
./kubectl.sh rollout status deployment heart-disease-api
```

### Dashboard
```bash
# Open Kubernetes dashboard
./minikube-darwin-arm64 dashboard
```

---

## 🐛 Troubleshooting

### Issue: Docker Desktop Not Running
**Symptoms:** Minikube fails to start with Docker driver errors

**Solution:**
1. Open Docker Desktop application
2. Wait for Docker to fully start (whale icon in menu bar)
3. Verify: `docker info`
4. Retry: `./deploy_k8s.sh`

### Issue: Minikube Won't Start
**Symptoms:** Hangs on `./minikube-darwin-arm64 start`

**Solution:**
```bash
# Delete existing cluster
./minikube-darwin-arm64 delete

# Start fresh
./minikube-darwin-arm64 start --driver=docker

# Or try different settings
./minikube-darwin-arm64 start --driver=docker --cpus=2 --memory=2048
```

### Issue: Pods Stuck in ImagePullBackOff
**Symptoms:** Pods can't pull the Docker image

**Solution:**
```bash
# Ensure image is loaded into minikube
./minikube-darwin-arm64 image load heart-disease-api:latest

# Verify image exists
./minikube-darwin-arm64 image ls | grep heart-disease

# Delete and recreate pods
./kubectl.sh delete -f deployment/kubernetes/
./kubectl.sh apply -f deployment/kubernetes/
```

### Issue: Pods Crash (CrashLoopBackOff)
**Symptoms:** Pods keep restarting

**Solution:**
```bash
# Check logs
./kubectl.sh logs <pod-name>

# Common causes:
# 1. Model file missing - rebuild image with models
# 2. Port conflict - check deployment.yaml
# 3. Memory limits - increase in deployment.yaml

# Describe pod for details
./kubectl.sh describe pod <pod-name>
```

### Issue: Service Not Accessible
**Symptoms:** Can't access service URL from browser

**Solution 1: Use minikube service command**
```bash
./minikube-darwin-arm64 service heart-disease-api
# This opens browser automatically
```

**Solution 2: Use port forwarding**
```bash
./kubectl.sh port-forward svc/heart-disease-api 8080:8000
# Access at http://localhost:8080
```

**Solution 3: Check service status**
```bash
./kubectl.sh get svc heart-disease-api
./kubectl.sh describe svc heart-disease-api
```

### Issue: Health Check Fails
**Symptoms:** Pods not becoming ready, readiness probe fails

**Solution:**
```bash
# Test health endpoint inside pod
./kubectl.sh exec <pod-name> -- curl localhost:8000/health

# Check application logs
./kubectl.sh logs <pod-name>

# Increase initialDelaySeconds if app needs more startup time
# Edit deployment/kubernetes/deployment.yaml
```

---

## 🧹 Cleanup

### Delete Deployment (Keep Minikube)
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

# This removes the entire cluster
```

---

## 📚 Useful Commands

### Debugging
```bash
# Get pod details
./kubectl.sh describe pod <pod-name>

# Execute command in pod
./kubectl.sh exec <pod-name> -- ls -la /app/models/

# Get shell in pod
./kubectl.sh exec -it <pod-name> -- /bin/bash

# Port forward for testing
./kubectl.sh port-forward deployment/heart-disease-api 8080:8000
```

### Resource Monitoring
```bash
# Pod resource usage
./kubectl.sh top pods

# Node resource usage
./kubectl.sh top nodes

# Events
./kubectl.sh get events --sort-by='.lastTimestamp'
```

### Configuration
```bash
# View ConfigMap
./kubectl.sh get configmap heart-disease-api-config -o yaml

# Edit ConfigMap
./kubectl.sh edit configmap heart-disease-api-config

# View deployment YAML
./kubectl.sh get deployment heart-disease-api -o yaml
```

---

## 🎯 Testing Checklist

Before marking deployment as successful, verify:

- [ ] Minikube is running: `./minikube-darwin-arm64 status`
- [ ] Docker image exists: `docker images | grep heart-disease`
- [ ] Image loaded in minikube: `./minikube-darwin-arm64 image ls | grep heart-disease`
- [ ] Deployment created: `./kubectl.sh get deployment heart-disease-api`
- [ ] Pods are running: `./kubectl.sh get pods` (should show 2/2 Running)
- [ ] Service is created: `./kubectl.sh get svc heart-disease-api`
- [ ] Service URL works: `curl $(./minikube-darwin-arm64 service heart-disease-api --url)/health`
- [ ] Prediction works: Test with `test_sample.json`
- [ ] Logs are clean: `./kubectl.sh logs -l app=heart-disease-api`
- [ ] Can scale: `./kubectl.sh scale deployment heart-disease-api --replicas=3`

---

## 📈 Next Steps

### 1. Monitor Performance
```bash
# Start dashboard
./minikube-darwin-arm64 dashboard

# Watch resource usage
watch ./kubectl.sh top pods
```

### 2. Load Testing
```bash
# Install hey (HTTP load testing tool)
brew install hey

# Run load test
SERVICE_URL=$(./minikube-darwin-arm64 service heart-disease-api --url)
hey -n 1000 -c 10 $SERVICE_URL/health
```

### 3. Configure Autoscaling
Create `hpa.yaml`:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: heart-disease-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: heart-disease-api
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

Deploy: `./kubectl.sh apply -f hpa.yaml`

### 4. Production Deployment
For deploying to AWS EKS, GCP GKE, or Azure AKS:
1. Push image to container registry
2. Update image path in deployment.yaml
3. Configure ingress with TLS
4. Set up monitoring (Prometheus + Grafana)
5. Configure secrets management
6. Implement CI/CD pipeline

---

## 📞 Support

For issues:
1. Check `KUBERNETES_DEPLOYMENT.md` for detailed guide
2. See `K8S_QUICKREF.md` for quick commands
3. Review pod logs: `./kubectl.sh logs <pod-name>`
4. Check events: `./kubectl.sh get events`

---

## ✅ Summary

**Created:**
- ✅ 3 Kubernetes manifests (deployment, service, ingress)
- ✅ Automated deployment script
- ✅ kubectl wrapper script
- ✅ Comprehensive documentation

**Status:**
- ✅ Ready to deploy
- ✅ All files configured
- ✅ Scripts executable
- ✅ Documentation complete

**To Deploy:**
```bash
# Make sure Docker Desktop is running, then:
./deploy_k8s.sh
```

**Documentation:**
- `KUBERNETES_DEPLOYMENT.md` - Full guide
- `K8S_QUICKREF.md` - Quick reference
- `K8S_SETUP_SUMMARY.md` - This file

🎉 **Kubernetes deployment is ready to use!**

