# Kubernetes Quick Reference

## 🚀 Quick Start
```bash
# Automated deployment
./deploy_k8s.sh
```

## 📋 Manual Deployment Steps

### 1. Start Minikube
```bash
./minikube-darwin-arm64 start --driver=docker
```

### 2. Load Image
```bash
./minikube-darwin-arm64 image load heart-disease-api:latest
```

### 3. Deploy
```bash
kubectl apply -f deployment/kubernetes/
```

### 4. Get Service URL
```bash
./minikube-darwin-arm64 service heart-disease-api --url
```

## 🔍 Check Status
```bash
# All resources
kubectl get all

# Pods
kubectl get pods

# Services
kubectl get svc

# Logs
kubectl logs -l app=heart-disease-api -f
```

## 🧪 Test API
```bash
SERVICE_URL=$(./minikube-darwin-arm64 service heart-disease-api --url)

# Health
curl $SERVICE_URL/health

# Predict
curl -X POST $SERVICE_URL/predict \
  -H "Content-Type: application/json" \
  -d @test_sample.json
```

## 📊 Scale
```bash
# Scale up
kubectl scale deployment heart-disease-api --replicas=3

# Scale down
kubectl scale deployment heart-disease-api --replicas=1
```

## 🔄 Update
```bash
# Apply changes
kubectl apply -f deployment/kubernetes/deployment.yaml

# Restart
kubectl rollout restart deployment heart-disease-api
```

## 🧹 Cleanup
```bash
# Delete deployment
kubectl delete -f deployment/kubernetes/

# Stop minikube
./minikube-darwin-arm64 stop

# Delete cluster
./minikube-darwin-arm64 delete
```

## 🐛 Debug
```bash
# Describe pod
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>

# Shell into pod
kubectl exec -it <pod-name> -- /bin/bash

# Port forward
kubectl port-forward svc/heart-disease-api 8080:8000
```

## 📈 Monitor
```bash
# Resource usage
kubectl top pods
kubectl top nodes

# Dashboard
./minikube-darwin-arm64 dashboard
```

## ⚠️ Troubleshooting

**Pods not starting?**
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**Image not found?**
```bash
./minikube-darwin-arm64 image load heart-disease-api:latest
```

**Service not accessible?**
```bash
kubectl port-forward svc/heart-disease-api 8080:8000
# Access at http://localhost:8080
```

**Minikube issues?**
```bash
./minikube-darwin-arm64 delete
./minikube-darwin-arm64 start --driver=docker
```

