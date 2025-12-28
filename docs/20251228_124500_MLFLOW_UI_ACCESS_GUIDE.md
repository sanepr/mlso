# ✅ MLflow UI Access Guide - Models with Parameters

**Date:** December 28, 2025  
**Status:** ✅ **MLFLOW UI RUNNING WITH MODELS VISIBLE**

---

## 🎯 SOLUTION: Access MLflow UI on Port 5002

Your MLflow UI is now running and accessible at:

```
http://localhost:5002
```

**This UI has access to:**
- ✅ All experiments (heart-disease-prediction, model-training-comparison)
- ✅ All runs with parameters and metrics
- ✅ Registered models (2 models in registry)
- ✅ Model artifacts and metadata

---

## 🌐 Current Services Configuration

| Service | Port | URL | Status | Purpose |
|---------|------|-----|--------|---------|
| **Local MLflow UI** ✅ | 5002 | http://localhost:5002 | **WORKING** | View experiments & models |
| Docker MLflow Server | 5001 | http://localhost:5001 | Running (isolated) | Separate server |
| Local MLflow UI | 5000 | http://localhost:5000 | Blocked (AirPlay) | macOS conflict |
| FastAPI Server | 8002 | http://localhost:8002 | Running | Prediction API |

**Use Port 5002** for viewing all your experiments and models!

---

## 📊 How to View Models with Parameters

### Step 1: Open MLflow UI

```bash
# In your browser, go to:
http://localhost:5002
```

Or from command line:
```bash
open http://localhost:5002
```

### Step 2: View Experiments and Runs

1. **On the home page**, you'll see the "Experiments" list
2. Click on **"heart-disease-prediction"** experiment
3. You'll see all runs with their metrics:
   - Random Forest run
   - Logistic Regression run

### Step 3: View Run Parameters

For each run, you can see:

**Click on a run** → You'll see tabs:
- **Overview**: Run metadata, status, duration
- **Parameters**: All hyperparameters (C, n_estimators, max_depth, etc.)
- **Metrics**: All metrics (accuracy, ROC-AUC, F1, etc.) with charts
- **Artifacts**: Saved models, plots, files
- **Tags**: Custom tags and metadata

### Step 4: View Registered Models

1. Click the **"Models"** tab at the top of the page
2. You'll see registered models:
   - heart-disease-random-forest (Version 1, Production)
   - heart-disease-logistic-regression (Version 1, Production)

3. **Click on a model name** to see:
   - Model versions and stages
   - Source run with all parameters
   - Model schema
   - Performance metrics from tags

---

## 🔍 Quick Verification

### Check Registered Models (Command Line)

```bash
cd /Users/aashishr/codebase/mlso
source venv/bin/activate

python << 'EOF'
import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("file://./mlruns")
client = MlflowClient()

print("=" * 80)
print("REGISTERED MODELS WITH DETAILS")
print("=" * 80)

for model in client.search_registered_models():
    print(f"\n📦 Model: {model.name}")
    for version in model.latest_versions:
        print(f"   Version: {version.version}")
        print(f"   Stage: {version.current_stage}")
        print(f"   Run ID: {version.run_id}")
        
        # Get run details
        run = client.get_run(version.run_id)
        print(f"\n   Parameters:")
        for key, value in sorted(run.data.params.items()):
            print(f"      {key}: {value}")
        
        print(f"\n   Test Metrics:")
        for key, value in sorted(run.data.metrics.items()):
            if 'test' in key:
                print(f"      {key}: {value:.4f}")
        print()
EOF
```

**Expected Output:**
```
================================================================================
REGISTERED MODELS WITH DETAILS
================================================================================

📦 Model: heart-disease-logistic-regression
   Version: 1
   Stage: Production
   Run ID: 717ff995ff304075b0e6e2ee2c03064e

   Parameters:
      C: 0.1
      class_weight: balanced
      max_iter: 1000
      penalty: l2
      solver: liblinear

   Test Metrics:
      test_accuracy: 0.8689
      test_f1: 0.8690
      test_precision: 0.8766
      test_recall: 0.8689
      test_roc_auc: 0.9567

📦 Model: heart-disease-random-forest
   Version: 1
   Stage: Production
   Run ID: 7552d97529ac4da0be90b0d3de0d6be3

   Parameters:
      class_weight: None
      max_depth: None
      max_features: sqrt
      min_samples_leaf: 4
      min_samples_split: 2
      n_estimators: 100

   Test Metrics:
      test_accuracy: 0.8852
      test_f1: 0.8854
      test_precision: 0.8899
      test_recall: 0.8852
      test_roc_auc: 0.9600
```

---

## 🎨 MLflow UI Features

### Experiments Page (http://localhost:5002)

**What you can do:**
1. **View all experiments** in the left sidebar
2. **Compare runs** side by side
3. **Filter runs** by parameters or metrics
4. **Visualize metrics** in charts
5. **Download artifacts** (models, plots, etc.)

### Models Page (Models tab)

**What you can do:**
1. **Browse registered models**
2. **View model versions** and their stages
3. **Compare model versions**
4. **Transition model stages** (Staging → Production)
5. **Add model descriptions** and aliases
6. **See source run** with all training details

### Run Details Page

**What you see:**
1. **Parameters**: All hyperparameters used for training
2. **Metrics**: Performance metrics with visualization
3. **Artifacts**: Saved models, plots, feature importance
4. **Tags**: Custom metadata tags
5. **System Info**: Python version, Git commit, etc.

---

## 🔎 Finding Specific Information

### To See Random Forest Parameters:

1. Go to http://localhost:5002
2. Click "heart-disease-prediction" experiment
3. Find the run with "RandomForest" tag
4. Click on the run
5. Click "Parameters" tab
6. See all parameters:
   - n_estimators: 100
   - max_depth: None
   - max_features: sqrt
   - min_samples_leaf: 4
   - min_samples_split: 2
   - class_weight: None

### To See Logistic Regression Parameters:

1. Same steps as above
2. Find the run with "LogisticRegression" tag
3. Parameters tab shows:
   - C: 0.1
   - penalty: l2
   - solver: liblinear
   - class_weight: balanced
   - max_iter: 1000

### To Compare Both Models:

1. Select both runs (checkboxes)
2. Click "Compare" button
3. See side-by-side comparison of:
   - Parameters
   - Metrics  
   - Performance charts

---

## 📸 What You Should See in MLflow UI

### Home Page
```
┌─────────────────────────────────────────┐
│  Experiments                            │
├─────────────────────────────────────────┤
│  ├─ heart-disease-prediction   (2 runs)│
│  └─ model-training-comparison  (6 runs)│
│                                         │
│  Recent Runs:                           │
│  • Random Forest (ROC-AUC: 0.9600)     │
│  • Logistic Regression (ROC-AUC: 0.9567)│
└─────────────────────────────────────────┘
```

### Models Tab
```
┌─────────────────────────────────────────┐
│  Registered Models                      │
├─────────────────────────────────────────┤
│  🏆 heart-disease-random-forest         │
│     Version 1 (Production)              │
│     ROC-AUC: 0.9600                    │
│                                         │
│  📊 heart-disease-logistic-regression   │
│     Version 1 (Production)              │
│     ROC-AUC: 0.9567                    │
└─────────────────────────────────────────┘
```

### Run Details Page
```
┌─────────────────────────────────────────┐
│  Run: Random Forest                     │
│  Status: FINISHED                       │
├─────────────────────────────────────────┤
│  [Overview] [Parameters] [Metrics] [...] │
│                                         │
│  Parameters:                            │
│  • n_estimators: 100                   │
│  • max_depth: None                     │
│  • max_features: sqrt                  │
│  • min_samples_leaf: 4                 │
│  • ...                                 │
│                                         │
│  Metrics:                               │
│  • test_accuracy: 0.8852              │
│  • test_roc_auc: 0.9600               │
│  • test_f1: 0.8854                    │
│  [Chart showing metric trends]         │
└─────────────────────────────────────────┘
```

---

## 🔧 Troubleshooting

### Issue: "Page won't load"

**Solution:**
```bash
# Check if MLflow UI is running
ps aux | grep "mlflow ui"

# If not running, start it
cd /Users/aashishr/codebase/mlso
source venv/bin/activate
nohup mlflow ui --port 5002 --backend-store-uri ./mlruns > mlflow_ui_5002.log 2>&1 &

# Wait 5 seconds, then access
sleep 5
open http://localhost:5002
```

### Issue: "No experiments showing"

**Solution:**
```bash
# Verify mlruns directory exists and has data
ls -la mlruns/

# Should show numbered directories like:
# 640360924472580988 (heart-disease-prediction)
# 212463099734530815 (model-training-comparison)
```

### Issue: "Models tab is empty"

**Solution:**
```bash
# Re-register models
python src/utils/register_models.py

# Refresh browser
# Models should appear immediately
```

---

## 📋 Quick Reference Commands

### Start MLflow UI
```bash
cd /Users/aashishr/codebase/mlso
source venv/bin/activate
mlflow ui --port 5002 --backend-store-uri ./mlruns
```

### Access MLflow UI
```bash
open http://localhost:5002
```

### List Models via Python
```python
import mlflow
mlflow.set_tracking_uri("file://./mlruns")
models = mlflow.search_registered_models()
for m in models:
    print(f"Model: {m.name}")
```

### Get Run Parameters via Python
```python
from mlflow.tracking import MlflowClient
client = MlflowClient()
run = client.get_run("RUN_ID")
print(run.data.params)
```

---

## ✅ Summary

| Question | Answer |
|----------|--------|
| **Where is MLflow UI?** | http://localhost:5002 ✅ |
| **Can I see experiments?** | Yes, click experiment name ✅ |
| **Can I see run parameters?** | Yes, click run → Parameters tab ✅ |
| **Can I see metrics?** | Yes, click run → Metrics tab ✅ |
| **Can I see registered models?** | Yes, click Models tab ✅ |
| **Can I see model parameters?** | Yes, click model → view source run ✅ |
| **Are all models visible?** | Yes, 2 models registered ✅ |

---

## 🎯 ACTION ITEMS

**To see your models with parameters right now:**

1. **Open:** http://localhost:5002
2. **Click:** "heart-disease-prediction" experiment
3. **Select a run** (Random Forest or Logistic Regression)
4. **Click:** "Parameters" tab
5. **See:** All hyperparameters used for training

**That's it! Everything is visible and accessible!**

---

## 📊 Model Details Available

### Random Forest (heart-disease-random-forest)
**Parameters visible in UI:**
- n_estimators: 100
- max_depth: None
- max_features: sqrt
- min_samples_leaf: 4
- min_samples_split: 2
- class_weight: None

**Metrics visible in UI:**
- test_accuracy: 0.8852
- test_roc_auc: 0.9600 🏆
- test_precision: 0.8899
- test_recall: 0.8852
- test_f1: 0.8854

### Logistic Regression (heart-disease-logistic-regression)
**Parameters visible in UI:**
- C: 0.1
- penalty: l2
- solver: liblinear
- class_weight: balanced
- max_iter: 1000

**Metrics visible in UI:**
- test_accuracy: 0.8689
- test_roc_auc: 0.9567
- test_precision: 0.8766
- test_recall: 0.8689
- test_f1: 0.8690

---

**Report Generated:** December 28, 2025  
**MLflow UI:** http://localhost:5002 ✅  
**Status:** WORKING - All models and parameters visible  
**Action:** Open http://localhost:5002 in your browser NOW!

🎉 **Your MLflow UI is ready with all models and parameters!**

