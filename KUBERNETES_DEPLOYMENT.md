# Kubernetes Deployment Guide

## Overview
This guide will help you deploy the Heart Disease API to a Kubernetes cluster using Minikube.

---

## Prerequisites

1. **Docker Desktop** - Must be running
2. **Minikube** - Already available as `minikube-darwin-arm64` in the project
3. **kubectl** - Kubernetes command-line tool
4. **Docker image** - Heart Disease API image built

---

## Quick Start

### Option 1: Automated Deployment (Recommended)
```bash
./deploy_k8s.sh
```

This script will automatically:
- ✅ Start minikube if not running
- ✅ Build Docker image if needed
- ✅ Load image into minikube
- ✅ Deploy to Kubernetes
- ✅ Test the endpoints

### Option 2: Manual Deployment

#### Step 1: Start Docker Desktop
Make sure Docker Desktop is running. Check with:
```bash
docker info
```

#### Step 2: Start Minikube
```bash
./minikube-darwin-arm64 start --driver=docker --cpus=2 --memory=4096
```

Wait for minikube to start (this may take 2-5 minutes on first run).

#### Step 3: Verify Minikube is Running
```bash
./minikube-darwin-arm64 status
```

Expected output:
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

#### Step 4: Build Docker Image (if not already built)
```bash
docker build -t heart-disease-api:latest .
```

#### Step 5: Load Image into Minikube
```bash
./minikube-darwin-arm64 image load heart-disease-api:latest
```

This makes the Docker image available inside the minikube cluster.

#### Step 6: Deploy to Kubernetes
```bash
# Deploy the application
kubectl apply -f deployment/kubernetes/deployment.yaml

# Deploy the service
kubectl apply -f deployment/kubernetes/service.yaml

# (Optional) Deploy ingress
kubectl apply -f deployment/kubernetes/ingress.yaml
```

#### Step 7: Wait for Deployment
```bash
# Wait for pods to be ready
kubectl wait --for=condition=available --timeout=300s deployment/heart-disease-api

# Check status
kubectl get pods
kubectl get services
kubectl get deployments
```

#### Step 8: Access the Service

Get the service URL:
```bash
./minikube-darwin-arm64 service heart-disease-api --url
```

This will output something like: `http://192.168.49.2:30080`

#### Step 9: Test the API

**Health Check:**
```bash
# Replace with your actual service URL
SERVICE_URL=$(./minikube-darwin-arm64 service heart-disease-api --url)
curl $SERVICE_URL/health
```

**Prediction:**
```bash
curl -X POST $SERVICE_URL/predict \
  -H "Content-Type: application/json" \
  -d @test_sample.json
```

---

## Kubernetes Resources Created

### 1. Deployment (`deployment.yaml`)
- **Replicas:** 2 pods for high availability
- **Container:** heart-disease-api:latest
- **Port:** 8000
- **Resources:** 256Mi-512Mi memory, 250m-500m CPU
- **Health checks:** Liveness and readiness probes
- **ConfigMap:** Environment configuration

### 2. Service (`service.yaml`)
- **Type:** LoadBalancer (NodePort on minikube)
- **Port:** 8000
- **NodePort:** 30080 (for external access)
- **Session Affinity:** ClientIP

### 3. Ingress (`ingress.yaml`) - Optional
- **Host:** heart-disease-api.local
- **Path:** /
- **Backend:** heart-disease-api service on port 8000

---

## Useful Commands

### View Resources
```bash
# View all resources
kubectl get all

# View pods
kubectl get pods

# View services
kubectl get services

# View deployments
kubectl get deployments

# Describe pod (for troubleshooting)
kubectl describe pod <pod-name>
```

### View Logs
```bash
# View logs from all pods
kubectl logs -l app=heart-disease-api

# Follow logs in real-time
kubectl logs -l app=heart-disease-api -f

# View logs from specific pod
kubectl logs <pod-name>
```

### Scale Deployment
```bash
# Scale to 3 replicas
kubectl scale deployment heart-disease-api --replicas=3

# Scale to 1 replica
kubectl scale deployment heart-disease-api --replicas=1
```

### Update Deployment
```bash
# After making changes to deployment.yaml
kubectl apply -f deployment/kubernetes/deployment.yaml

# Restart pods
kubectl rollout restart deployment heart-disease-api

# Check rollout status
kubectl rollout status deployment heart-disease-api
```

### Execute Commands in Pod
```bash
# Get a shell in a pod
kubectl exec -it <pod-name> -- /bin/bash

# Run a command in a pod
kubectl exec <pod-name> -- ls -la /app/models/
```

### Port Forwarding (Alternative Access)
```bash
# Forward local port 8080 to pod port 8000
kubectl port-forward deployment/heart-disease-api 8080:8000

# Then access at: http://localhost:8080
```

---

## Troubleshooting

### Issue: Minikube won't start
**Symptoms:** `./minikube-darwin-arm64 start` hangs or fails

**Solutions:**
1. Check Docker Desktop is running:
   ```bash
   docker info
   ```

2. Delete and recreate minikube:
   ```bash
   ./minikube-darwin-arm64 delete
   ./minikube-darwin-arm64 start --driver=docker
   ```

3. Try different driver:
   ```bash
   ./minikube-darwin-arm64 start --driver=hyperkit
   ```

### Issue: Pods stuck in "ImagePullBackOff"
**Symptoms:** Pods can't pull the image

**Solutions:**
1. Load image into minikube:
   ```bash
   ./minikube-darwin-arm64 image load heart-disease-api:latest
   ```

2. Verify image exists in minikube:
   ```bash
   ./minikube-darwin-arm64 image ls | grep heart-disease
   ```

3. Check deployment uses `imagePullPolicy: Never`

### Issue: Pods crash with "CrashLoopBackOff"
**Symptoms:** Pods keep restarting

**Solutions:**
1. Check logs:
   ```bash
   kubectl logs <pod-name>
   ```

2. Common causes:
   - Model file not found (rebuild image with models)
   - Port already in use
   - Missing dependencies

3. Describe pod for more details:
   ```bash
   kubectl describe pod <pod-name>
   ```

### Issue: Health check fails
**Symptoms:** Pods not becoming ready

**Solutions:**
1. Check health endpoint inside pod:
   ```bash
   kubectl exec <pod-name> -- curl localhost:8000/health
   ```

2. Increase `initialDelaySeconds` in deployment.yaml
3. Check application logs for errors

### Issue: Service URL not accessible
**Symptoms:** Can't access the service from browser

**Solutions:**
1. Get service URL:
   ```bash
   ./minikube-darwin-arm64 service heart-disease-api --url
   ```

2. Check service is running:
   ```bash
   kubectl get svc heart-disease-api
   ```

3. Use port forwarding as alternative:
   ```bash
   kubectl port-forward svc/heart-disease-api 8080:8000
   # Access at http://localhost:8080
   ```

### Issue: kubectl command not found
**Symptoms:** `kubectl: command not found`

**Solutions:**
1. Use minikube's kubectl:
   ```bash
   ./minikube-darwin-arm64 kubectl -- get pods
   ```

2. Or install kubectl:
   ```bash
   brew install kubectl
   ```

---

## Monitoring

### View Resource Usage
```bash
# Pod resource usage
kubectl top pods

# Node resource usage
kubectl top nodes
```

### Dashboard
```bash
# Start Kubernetes dashboard
./minikube-darwin-arm64 dashboard

# Or get dashboard URL
./minikube-darwin-arm64 dashboard --url
```

---

## Cleanup

### Delete Deployment
```bash
# Delete all resources
kubectl delete -f deployment/kubernetes/

# Or delete individually
kubectl delete deployment heart-disease-api
kubectl delete service heart-disease-api
kubectl delete configmap heart-disease-api-config
```

### Stop Minikube
```bash
# Stop minikube (keeps cluster config)
./minikube-darwin-arm64 stop

# Delete minikube cluster (complete cleanup)
./minikube-darwin-arm64 delete
```

---

## Production Deployment

For production deployment to cloud platforms (AWS EKS, GCP GKE, Azure AKS):

### 1. Push Image to Registry
```bash
# Tag image
docker tag heart-disease-api:latest your-registry/heart-disease-api:v1.0.0

# Push to registry
docker push your-registry/heart-disease-api:v1.0.0
```

### 2. Update Deployment
Change in `deployment.yaml`:
```yaml
image: your-registry/heart-disease-api:v1.0.0
imagePullPolicy: Always  # Change from Never
```

### 3. Configure Secrets
```bash
# Create secret for registry access
kubectl create secret docker-registry regcred \
  --docker-server=<your-registry> \
  --docker-username=<username> \
  --docker-password=<password> \
  --docker-email=<email>
```

### 4. Configure TLS/SSL
Add TLS configuration to ingress.yaml for HTTPS

### 5. Set up Autoscaling
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
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Architecture

```
┌─────────────────────────────────────────────┐
│          Kubernetes Cluster                  │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │  Service (LoadBalancer)                │ │
│  │  Port: 8000, NodePort: 30080           │ │
│  └─────────────┬──────────────────────────┘ │
│                │                             │
│  ┌─────────────▼──────────────────────────┐ │
│  │  Deployment: heart-disease-api         │ │
│  │  Replicas: 2                           │ │
│  │                                        │ │
│  │  ┌──────────┐      ┌──────────┐      │ │
│  │  │  Pod 1   │      │  Pod 2   │      │ │
│  │  │  Port:   │      │  Port:   │      │ │
│  │  │  8000    │      │  8000    │      │ │
│  │  └──────────┘      └──────────┘      │ │
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

## Testing Checklist

- [ ] Minikube is running
- [ ] Docker image is built
- [ ] Image loaded into minikube
- [ ] Deployment is created
- [ ] Pods are running (2/2)
- [ ] Service is created
- [ ] Health check returns 200
- [ ] Prediction endpoint works
- [ ] Logs show no errors
- [ ] Can scale deployment
- [ ] Resource limits working

---

## Status

✅ Kubernetes manifests created  
✅ Deployment script created  
✅ Documentation complete  

**Ready for deployment!**

Run `./deploy_k8s.sh` to get started.

