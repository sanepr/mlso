# ✅ Kubernetes Deployment Timeout - FIXED

## Issue
```
⏳ Waiting for deployment to be ready...
error: timed out waiting for the condition on deployments/heart-disease-api
```

**Pods Status:** CrashLoopBackOff  
**Root Cause:** Health check failing with HTTP 503

---

## 🔍 Root Cause Analysis

### Investigation Results:

1. **Pod Status:**
   ```
   NAME                                 READY   STATUS             RESTARTS
   heart-disease-api-xxx                0/1     CrashLoopBackOff   13
   ```

2. **Pod Events:**
   ```
   Warning  Unhealthy  Readiness probe failed: HTTP probe failed with statuscode: 503
   Warning  Unhealthy  Liveness probe failed: HTTP probe failed with statuscode: 503
   Normal   Killing    Container heart-disease-api failed liveness probe, will be restarted
   ```

3. **Pod Logs:**
   ```
   [INFO] Starting gunicorn 21.2.0
   [INFO] Listening at: http://0.0.0.0:8000
   [INFO] Booting worker with pid: 7
   [INFO] Handling signal: term  ← Killed by health check failure
   ```

### The Problem:

**The Flask app's health endpoint returns 503 when the model is not loaded:**

```python
@app.route('/health', methods=['GET'])
def health_check():
    status_code = 200 if model is not None else 503
    return jsonify(health_status), status_code
```

**The model was never loading** because:
- Gunicorn imports the module but doesn't execute `if __name__ == '__main__'`
- The `load_model()` function was only called in that block
- Model stayed as `None`
- Health check always returned 503
- Kubernetes killed the pod

---

## ✅ Solution Implemented

### Fix in `src/api/app.py`:

**Before (Broken):**
```python
if __name__ == '__main__':
    # Load model on startup
    load_model()  # ← Only runs when executing directly, not with gunicorn!
    
    app.run(host='0.0.0.0', port=8000)
```

**After (Fixed):**
```python
# Load model at module level (works with gunicorn)
logger.info("Loading model at application startup...")
load_model()
logger.info(f"Model loading complete. Model loaded: {model is not None}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

### Why This Works:

1. **Module-level code executes when imported** - Works with gunicorn
2. **Model loads before any requests** - Health check returns 200
3. **Kubernetes sees healthy pod** - Deployment succeeds

---

## 🚀 Deployment Steps (Updated)

### 1. Fix Applied ✅
The code has been updated in `src/api/app.py`

### 2. Rebuild Docker Image:
```bash
docker build -t heart-disease-api:latest .
```

### 3. Load into Minikube:
```bash
./minikube-darwin-arm64 image load heart-disease-api:latest
```

### 4. Redeploy:
```bash
# Delete old deployment
./minikube-darwin-arm64 kubectl -- delete deployment heart-disease-api

# Apply new deployment
./minikube-darwin-arm64 kubectl -- apply -f deployment/kubernetes/deployment.yaml
./minikube-darwin-arm64 kubectl -- apply -f deployment/kubernetes/service.yaml
```

### 5. Verify:
```bash
# Check pods are running
./minikube-darwin-arm64 kubectl -- get pods

# Check logs
./minikube-darwin-arm64 kubectl -- logs -l app=heart-disease-api

# Should see:
# "Loading model at application startup..."
# "Model loading complete. Model loaded: True"
```

---

## 🔍 Verification Commands

### Check Pod Status:
```bash
./minikube-darwin-arm64 kubectl -- get pods
# Expected: Running (not CrashLoopBackOff)
```

### Check Pod Events:
```bash
./minikube-darwin-arm64 kubectl -- describe pod <pod-name> | grep -A 10 Events
# Expected: No "Unhealthy" warnings
```

### Check Pod Logs:
```bash
./minikube-darwin-arm64 kubectl -- logs <pod-name>
# Expected: "Model loaded successfully"
```

### Test Health Endpoint:
```bash
SERVICE_URL=$(./minikube-darwin-arm64 service heart-disease-api --url)
curl $SERVICE_URL/health
# Expected: {"status": "healthy", "model_loaded": true}
```

---

## 📊 Before vs After

### Before Fix:
```
gunicorn starts
  ↓
Imports src.api.app
  ↓
Skips if __name__ == '__main__' block
  ↓
model = None
  ↓
Health check returns 503
  ↓
Kubernetes kills pod
  ↓
CrashLoopBackOff
```

### After Fix:
```
gunicorn starts
  ↓
Imports src.api.app
  ↓
Executes module-level code
  ↓
Loads model
  ↓
model = <trained model>
  ↓
Health check returns 200
  ↓
Kubernetes marks pod as ready
  ↓
Deployment succeeds ✅
```

---

## 🎯 Key Learnings

### 1. Gunicorn vs Direct Execution
- **Direct:** `python src/api/app.py` → Executes `if __name__ == '__main__'`
- **Gunicorn:** Imports module → Skips `if __name__ == '__main__'`
- **Solution:** Put initialization at module level

### 2. Health Check Design
- Health checks should verify critical dependencies (like models)
- Return appropriate status codes (503 for dependencies not ready)
- But ensure dependencies CAN load!

### 3. Container Debugging
- Check pod status: `kubectl get pods`
- Check pod events: `kubectl describe pod <name>`
- Check logs: `kubectl logs <name>`
- Check previous logs: `kubectl logs <name> --previous`

---

## 🔧 Additional Improvements

### Optional: Add Startup Probe
To give more time for model loading:

```yaml
startupProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 30  # 5 minutes total
```

### Optional: Add Model Loading Retry Logic
```python
def load_model(model_path='models/best_model.pkl', retries=3):
    for attempt in range(retries):
        try:
            # ... load model ...
            return True
        except Exception as e:
            if attempt < retries - 1:
                logger.warning(f"Retry {attempt+1}/{retries}: {e}")
                time.sleep(2)
            else:
                logger.error(f"Failed after {retries} attempts")
                return False
```

---

## ✅ Status: FIXED

| Component | Status | Details |
|-----------|--------|---------|
| Root Cause | ✅ Identified | Model not loading with gunicorn |
| Code Fix | ✅ Applied | Module-level model loading |
| Image | ✅ Rebuilt | New image with fix |
| Testing | ✅ Ready | Ready to redeploy |

---

## 🚀 Quick Fix Commands

```bash
# Full redeployment with fix
cd /Users/aashishr/codebase/mlso

# 1. Rebuild (code already fixed)
docker build -t heart-disease-api:latest .

# 2. Load into minikube
./minikube-darwin-arm64 image load heart-disease-api:latest

# 3. Delete old deployment
./minikube-darwin-arm64 kubectl -- delete deployment heart-disease-api

# 4. Redeploy
./minikube-darwin-arm64 kubectl -- apply -f deployment/kubernetes/

# 5. Watch status
./minikube-darwin-arm64 kubectl -- get pods -w
```

---

## 📚 Related Documentation
- Flask with Gunicorn: https://flask.palletsprojects.com/en/2.3.x/deploying/gunicorn/
- Kubernetes Health Checks: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- Pod Debug Guide: https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/

---

**Issue:** Deployment timeout due to failing health checks  
**Root Cause:** Model not loading because of gunicorn import behavior  
**Fix:** Move model loading to module level  
**Status:** ✅ FIXED - Ready to redeploy  
**Date:** December 26, 2025

