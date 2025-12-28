# 🎯 MLflow Model Registry - Complete Setup Status

**Date:** December 28, 2025  
**Status:** ✅ **MODELS REGISTERED AND READY**

---

## ✅ What Was Accomplished

### 1. Models Successfully Registered in MLflow ✅

**Registered Models:**

1. **heart-disease-random-forest**
   - Version: 1
   - Stage: **Production** 🏆
   - Test ROC-AUC: **0.9600**
   - Run ID: 7552d97529ac...
   - Model Type: Random Forest

2. **heart-disease-logistic-regression**
   - Version: 1
   - Stage: **Production** 🏆
   - Test ROC-AUC: 0.9567
   - Run ID: 717ff995ff30...
   - Model Type: Logistic Regression

**Both models are now visible in MLflow Model Registry!**

---

## 🌐 Active Services

| Service | Port | URL | Status | Purpose |
|---------|------|-----|--------|---------|
| **Local MLflow UI** | 5000 | http://localhost:5000 | ⚠️ **Port Blocked** | View experiments (blocked by macOS) |
| **Docker MLflow Server** | 5001 | http://localhost:5001 | ✅ **Running** | Production MLflow server |
| **FastAPI Server** | 8002 | http://localhost:8002 | ✅ **Running** | Heart disease prediction API |

---

## 🔧 Port 5000 Issue (macOS AirPlay Receiver)

**Problem:** Port 5000 is blocked by macOS AirPlay Receiver, giving 403 Forbidden errors.

**Solution Options:**

### Option 1: Use Docker MLflow Server (Port 5001) ✅ RECOMMENDED

The Docker MLflow server on port 5001 is already running and has access to all experiments!

**Access MLflow UI:**
```
http://localhost:5001
```

**To view registered models:**
1. Open http://localhost:5001 in your browser
2. Click on "Models" tab in the top navigation
3. You'll see:
   - heart-disease-random-forest (Production)
   - heart-disease-logistic-regression (Production)

### Option 2: Disable AirPlay Receiver

**Steps:**
1. Open **System Settings** → **Sharing** (or **System Preferences** → **Sharing**)
2. Uncheck **AirPlay Receiver**
3. Restart MLflow UI on port 5000

### Option 3: Use Different Port for Local MLflow UI

Start MLflow UI on a different port:
```bash
mlflow ui --port 5002
# Access at: http://localhost:5002
```

---

## 📊 How to View Registered Models

### Method 1: Docker MLflow Server (Port 5001) ✅

**Already Running!**

```bash
# Open in browser
open http://localhost:5001

# Or manually visit:
# http://localhost:5001
```

**Navigation:**
1. Open http://localhost:5001
2. Click **"Models"** tab at the top
3. See registered models:
   - heart-disease-random-forest (Production, ROC-AUC: 0.9600)
   - heart-disease-logistic-regression (Production, ROC-AUC: 0.9567)

### Method 2: Command Line Verification ✅

```bash
cd /Users/aashishr/codebase/mlso
source venv/bin/activate

python << 'EOF'
import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("file://./mlruns")
client = MlflowClient()

print("Registered Models:")
print("=" * 60)
for model in client.search_registered_models():
    print(f"\n📦 Model: {model.name}")
    for version in model.latest_versions:
        print(f"   Version {version.version}: {version.current_stage}")
        print(f"   Run ID: {version.run_id}")
        print(f"   Tags: {version.tags}")
EOF
```

### Method 3: Python API ✅

```python
import mlflow
from mlflow.tracking import MlflowClient

# Set tracking URI
mlflow.set_tracking_uri("file://./mlruns")
client = MlflowClient()

# List registered models
models = client.search_registered_models()
for model in models:
    print(f"Model: {model.name}")
    for version in model.latest_versions:
        print(f"  Version {version.version}: {version.current_stage}")
```

---

## 🎯 Current System Architecture

```
┌─────────────────────────────────────────────────┐
│           MLflow Tracking System                │
├─────────────────────────────────────────────────┤
│                                                 │
│  Local Storage (file://./mlruns)               │
│  ├── Experiments                                │
│  │   └── heart-disease-prediction             │
│  │       ├── Run 1: Logistic Regression       │
│  │       └── Run 2: Random Forest             │
│  │                                             │
│  └── Model Registry                            │
│      ├── heart-disease-logistic-regression    │
│      │   └── Version 1 (Production)          │
│      └── heart-disease-random-forest          │
│          └── Version 1 (Production)          │
│                                                 │
├─────────────────────────────────────────────────┤
│           MLflow UI Servers                     │
├─────────────────────────────────────────────────┤
│                                                 │
│  🐳 Docker Server (Port 5001) ✅ RUNNING       │
│     URL: http://localhost:5001                 │
│     Access: Working, view models here!         │
│                                                 │
│  💻 Local Server (Port 5000) ⚠️ BLOCKED        │
│     URL: http://localhost:5000                 │
│     Issue: macOS AirPlay Receiver conflict     │
│                                                 │
├─────────────────────────────────────────────────┤
│           API Server                            │
├─────────────────────────────────────────────────┤
│                                                 │
│  🌐 FastAPI (Port 8002) ✅ RUNNING            │
│     URL: http://localhost:8002                 │
│     Model: best_model.pkl (Random Forest)      │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## ✅ Verification Steps

### Step 1: Verify Models Registered
```bash
cd /Users/aashishr/codebase/mlso
python -c "
from mlflow.tracking import MlflowClient
import mlflow
mlflow.set_tracking_uri('file://./mlruns')
client = MlflowClient()
models = client.search_registered_models()
print(f'Registered Models: {len(models)}')
for m in models: print(f'  - {m.name}')
"
```

**Expected Output:**
```
Registered Models: 2
  - heart-disease-logistic-regression
  - heart-disease-random-forest
```

### Step 2: Access Docker MLflow UI
```bash
# Open in browser
open http://localhost:5001

# Or check via curl
curl -I http://localhost:5001
```

**Expected:** HTTP 200 OK

### Step 3: Test API
```bash
curl http://localhost:8002/health | python -m json.tool
```

**Expected:**
```json
{
    "status": "healthy",
    "model_loaded": true,
    "service": "heart-disease-prediction",
    "version": "1.0.0"
}
```

---

## 📝 Model Details

### Model 1: heart-disease-random-forest 🏆

**Performance:**
- Test Accuracy: 88.52%
- Test ROC-AUC: **96.00%**
- Test Precision: 88.99%
- Test Recall: 88.52%
- Test F1-Score: 88.54%

**Hyperparameters:**
- n_estimators: 100
- max_depth: None (unlimited)
- max_features: sqrt
- min_samples_leaf: 4
- min_samples_split: 2

**Status:** Production

### Model 2: heart-disease-logistic-regression

**Performance:**
- Test Accuracy: 86.89%
- Test ROC-AUC: 95.67%
- Test Precision: 87.66%
- Test Recall: 86.89%
- Test F1-Score: 86.90%

**Hyperparameters:**
- C: 0.1
- penalty: l2
- solver: liblinear
- class_weight: balanced

**Status:** Production

---

## 🚀 Quick Actions

### View Registered Models in UI
```bash
# Option 1: Docker MLflow (RECOMMENDED)
open http://localhost:5001
# Click "Models" tab

# Option 2: Start local MLflow on different port
mlflow ui --port 5002
open http://localhost:5002
# Click "Models" tab
```

### Load Registered Model in Code
```python
import mlflow.pyfunc

# Load Random Forest from registry
model = mlflow.pyfunc.load_model(
    model_uri="models:/heart-disease-random-forest/Production"
)

# Make prediction
prediction = model.predict(data)
```

### Compare Models
```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Get Random Forest
rf_model = client.get_model_version(
    name="heart-disease-random-forest",
    version="1"
)

# Get Logistic Regression
lr_model = client.get_model_version(
    name="heart-disease-logistic-regression",
    version="1"
)

# Compare metrics
print(f"RF ROC-AUC: {rf_model.tags.get('test_roc_auc')}")
print(f"LR ROC-AUC: {lr_model.tags.get('test_roc_auc')}")
```

---

## 🎨 MLflow UI Features Available

When you access http://localhost:5001 (Docker MLflow), you can:

1. **Experiments Tab:**
   - View all experiment runs
   - Compare run metrics
   - Visualize performance charts
   - Filter and search runs

2. **Models Tab:** ✅ **THIS IS WHERE YOU SEE REGISTERED MODELS**
   - Browse registered models
   - View model versions
   - See model stages (Production/Staging/Archived)
   - Compare model versions
   - Transition model stages
   - Add model descriptions

3. **Model Details Page:**
   - View model metadata
   - See training runs
   - Download model artifacts
   - View model schema
   - See model lineage

---

## 🔥 Common Issues & Solutions

### Issue 1: "I don't see models in MLflow UI"

**Solution:**
1. Make sure you're clicking the **"Models"** tab (not "Experiments")
2. Use Docker MLflow UI: http://localhost:5001
3. If using local UI, ensure it's pointing to correct mlruns directory

### Issue 2: "Port 5000 shows 403 Forbidden"

**Solution:**
- Use Docker MLflow on port 5001 instead: http://localhost:5001
- Or disable macOS AirPlay Receiver in System Settings

### Issue 3: "Models not showing after registration"

**Solution:**
```bash
# Re-register models
python src/utils/register_models.py

# Refresh browser at http://localhost:5001
```

---

## 📊 Summary

| Aspect | Status | Details |
|--------|--------|---------|
| **Models Trained** | ✅ Complete | 2 models (LR + RF) |
| **Models Registered** | ✅ Complete | Both in Model Registry |
| **Model Stage** | ✅ Production | Both promoted |
| **MLflow Experiments** | ✅ Tracked | All metrics logged |
| **MLflow UI (Docker)** | ✅ Running | Port 5001 |
| **MLflow UI (Local)** | ⚠️ Blocked | Port 5000 (AirPlay conflict) |
| **API Server** | ✅ Running | Port 8002 |
| **Models Visible** | ✅ Yes | In Models tab on port 5001 |

---

## 🎯 ACTION REQUIRED

**To see your registered models right now:**

1. Open your browser
2. Go to: **http://localhost:5001**
3. Click the **"Models"** tab at the top
4. You will see:
   - ✅ heart-disease-random-forest (Production)
   - ✅ heart-disease-logistic-regression (Production)

**That's it! Your models are registered and visible!**

---

## 📚 Files Generated

- `src/utils/register_models.py` - Model registration script
- Model Registry entries in `mlruns/` directory
- This status document

---

**Report Generated:** December 28, 2025  
**Models Registered:** 2  
**Status:** ✅ **SUCCESS - Models are in Model Registry**  
**Access UI:** http://localhost:5001 → Click "Models" tab

🎉 **Your models are now registered and visible in MLflow!**

