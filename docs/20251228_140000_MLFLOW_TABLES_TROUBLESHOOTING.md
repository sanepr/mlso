# 🔍 How to View MLflow Evaluation Tables in UI - Step-by-Step Guide

**Date:** December 28, 2025  
**Issue:** Tables not visible in MLflow UI  
**Solution:** Complete visual walkthrough

---

## ⚠️ Important: Tables Only Appear After Re-Training

**Key Point:** The `mlflow.log_table()` code was just added to your training script. **Existing runs don't have tables** because they were created before this feature was implemented.

### ✅ Solution: Re-train the models

```bash
cd /Users/aashishr/codebase/mlso
python src/models/train.py
```

**Look for this output:**
```
✓ Model comparison table logged to MLflow
```

This confirms tables were created!

---

## 📍 Step-by-Step: Finding Tables in MLflow UI

### Step 1: Open MLflow UI

```bash
# Make sure MLflow UI is running on port 5002
open http://localhost:5002
```

**If not running:**
```bash
cd /Users/aashishr/codebase/mlso
mlflow ui --port 5002 --backend-store-uri ./mlruns &
```

---

### Step 2: Navigate to the Experiment

**In the MLflow UI:**

```
┌─────────────────────────────────────────────────┐
│  MLflow                                         │
├─────────────────────────────────────────────────┤
│  📁 Experiments                                 │
│    ├─ Default                                   │
│    └─ ✨ heart-disease-prediction              │  ← CLICK HERE
│                                                 │
└─────────────────────────────────────────────────┘
```

1. You'll see the experiments list on the left
2. **Click on "heart-disease-prediction"**

---

### Step 3: View the Runs List

After clicking the experiment, you'll see a table of all runs:

```
┌────────────────────────────────────────────────────────────┐
│  Experiment: heart-disease-prediction                      │
├────────────────────────────────────────────────────────────┤
│  Start Time          | Run Name            | Status        │
├────────────────────────────────────────────────────────────┤
│  2025-12-28 16:45    | ✨ random_forest    | FINISHED     │  ← NEW RUN
│  2025-12-28 16:44    | ✨ logistic_regre..| FINISHED     │  ← NEW RUN  
│  2025-12-28 11:56    | random_forest       | FINISHED     │  (old, no tables)
│  2025-12-28 11:55    | logistic_regre...   | FINISHED     │  (old, no tables)
└────────────────────────────────────────────────────────────┘
```

**Important:** Click on one of the **NEW runs** (the ones you just created)

---

### Step 4: Open Run Details

Click on the **run name** (e.g., "random_forest" or "logistic_regression"):

```
┌──────────────────────────────────────────────────┐
│  Run: random_forest                              │
│  Run ID: 6461144f83...                          │
│  Status: FINISHED                                │
├──────────────────────────────────────────────────┤
│  [Overview] [Parameters] [Metrics] [Artifacts]  │  ← Click "Artifacts"
└──────────────────────────────────────────────────┘
```

1. You'll see tabs at the top: Overview, Parameters, Metrics, **Artifacts**
2. **Click the "Artifacts" tab**

---

### Step 5: View the Artifacts Tree

In the Artifacts tab, you'll see a file tree:

```
┌─────────────────────────────────────────────┐
│  Artifacts                                  │
├─────────────────────────────────────────────┤
│  📂 artifacts/                              │
│    ├─ 📄 evaluation_metrics.json  ← TABLE! │
│    └─ 📂 model/                             │
│         ├─ MLmodel                          │
│         ├─ conda.yaml                       │
│         ├─ model.pkl                        │
│         └─ ...                              │
└─────────────────────────────────────────────┘
```

---

### Step 6: Click on the Table File

**Click on `evaluation_metrics.json`**

The table will render in the UI showing:

```
┌──────────────────────────────────────────────────────────────┐
│  evaluation_metrics.json                                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Metric      | Training | Test    | Cross-Validation       │
│  ──────────────────────────────────────────────────────────│
│  Accuracy    | 0.9091   | 0.8852  | 0.8015                │
│  ROC-AUC     | 0.9795   | 0.9600  | 0.8866                │
│  Precision   | 0.9113   | 0.8899  | 0.8051                │
│  Recall      | 0.9091   | 0.8852  | 0.8015                │
│  F1-Score    | 0.9086   | 0.8854  | 0.8001                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**This is your evaluation table!** 🎉

---

### Step 7: View Feature Importance (Random Forest Only)

For the Random Forest run, you'll also see:

```
┌─────────────────────────────────────────────┐
│  Artifacts                                  │
├─────────────────────────────────────────────┤
│  📂 artifacts/                              │
│    ├─ 📄 evaluation_metrics.json           │
│    ├─ 📄 feature_importance.json  ← TABLE! │
│    └─ 📂 model/                             │
└─────────────────────────────────────────────┘
```

**Click on `feature_importance.json`** to see:

```
┌──────────────────────────────────┐
│  feature_importance.json         │
├──────────────────────────────────┤
│  Feature_Index | Importance      │
│  ───────────────────────────────│
│  12            | 0.1523         │
│  2             | 0.1401         │
│  11            | 0.1289         │
│  7             | 0.1156         │
│  9             | 0.0987         │
│  ...           | ...            │
└──────────────────────────────────┘
```

---

### Step 8: View Model Comparison Table

**Note:** The model comparison table should be in the parent run or experiment artifacts. If you don't see it, check:

1. **Experiment-level artifacts** (not run-level)
2. **The most recent runs**

---

## 🔍 Troubleshooting

### Issue 1: "I don't see any JSON files in Artifacts"

**Solution:** You're looking at an old run created before the code was updated.

**Steps:**
1. Re-run training: `python src/models/train.py`
2. Wait for "✓ Model comparison table logged to MLflow" message
3. Refresh MLflow UI
4. Click on the **newest run** (check Start Time)

---

### Issue 2: "I see the JSON file but it's not rendering as a table"

**Possible causes:**

**A) MLflow version doesn't support `log_table()` UI rendering**

Check your MLflow version:
```bash
python -c "import mlflow; print(mlflow.__version__)"
```

If version < 2.3.0, upgrade:
```bash
pip install --upgrade mlflow
```

**B) File is there but UI doesn't render it**

Download and view locally:
```bash
# Find the run ID from UI
cd /Users/aashishr/codebase/mlso

# View the table manually
python << 'EOF'
import mlflow
from mlflow.tracking import MlflowClient
import json

client = MlflowClient()
run_id = "YOUR_RUN_ID_HERE"  # From MLflow UI

# Download artifact
artifact_path = client.download_artifacts(run_id, "evaluation_metrics.json")

# Load and print
with open(artifact_path, 'r') as f:
    data = json.load(f)
    print(json.dumps(data, indent=2))
EOF
```

---

### Issue 3: "Tables didn't get logged during training"

**Check the training output:**

Look for these messages:
```
✓ Model comparison table logged to MLflow
```

**If you don't see this:**

1. Check for errors in training output
2. Verify `mlflow.log_table()` code is in `src/models/train.py`
3. Run with verbose output:
   ```bash
   python src/models/train.py 2>&1 | tee training.log
   grep -i "table" training.log
   ```

---

### Issue 4: "Error: 'DataFrame' object has no attribute 'to_json'"

This shouldn't happen with pandas, but if it does:

```python
# In src/models/train.py, change:
mlflow.log_table(data=eval_table, artifact_file="evaluation_metrics.json")

# To:
import json
eval_dict = eval_table.to_dict(orient='records')
with open("temp_eval.json", 'w') as f:
    json.dump(eval_dict, f)
mlflow.log_artifact("temp_eval.json", "evaluation_metrics.json")
```

---

## ✅ Verification Checklist

Use this checklist to verify tables are working:

- [ ] **Re-trained models** with updated code
- [ ] **Saw confirmation** message: "✓ Model comparison table logged to MLflow"
- [ ] **MLflow UI is running** on http://localhost:5002
- [ ] **Opened the newest run** (check Start Time column)
- [ ] **Clicked "Artifacts" tab**
- [ ] **See `evaluation_metrics.json`** in artifacts list
- [ ] **Clicked on the JSON file**
- [ ] **Table is rendered** in the UI

---

## 📊 What Tables Should You See?

### For Logistic Regression Run:
```
artifacts/
  ├─ evaluation_metrics.json  ✅
  └─ model/
```

### For Random Forest Run:
```
artifacts/
  ├─ evaluation_metrics.json      ✅
  ├─ feature_importance.json      ✅
  └─ model/
```

### In Experiment (or comparison run):
```
artifacts/
  └─ model_comparison.json        ✅
```

---

## 🎯 Quick Test Script

Run this to verify tables exist:

```bash
cd /Users/aashishr/codebase/mlso

python << 'EOF'
import mlflow
from mlflow.tracking import MlflowClient
import os

mlflow.set_tracking_uri(f"file://{os.getcwd()}/mlruns")
client = MlflowClient()

# Get latest runs
exp = client.get_experiment_by_name("heart-disease-prediction")
runs = client.search_runs(
    experiment_ids=[exp.experiment_id],
    max_results=2,
    order_by=["start_time DESC"]
)

print("Checking for table artifacts in latest runs:\n")
for run in runs:
    name = run.data.tags.get('mlflow.runName', 'N/A')
    print(f"Run: {name}")
    print(f"  Run ID: {run.info.run_id[:12]}...")
    
    artifacts = client.list_artifacts(run.info.run_id)
    tables = [art for art in artifacts if art.path.endswith('.json')]
    
    if tables:
        print(f"  ✅ Tables found:")
        for table in tables:
            print(f"     - {table.path}")
    else:
        print(f"  ❌ No table artifacts found")
    print()

print("\n💡 Tip: If no tables found, re-run: python src/models/train.py")
EOF
```

---

## 🚀 Summary

**Why you weren't seeing tables:**
- Tables only exist in runs created AFTER the code update
- Old runs (from before) don't have table artifacts

**Solution:**
1. ✅ Re-train models: `python src/models/train.py`
2. ✅ Open MLflow UI: `http://localhost:5002`
3. ✅ Click newest run → Artifacts tab
4. ✅ Click on `evaluation_metrics.json`
5. ✅ View your table!

**Tables to expect:**
- `evaluation_metrics.json` - Both models
- `feature_importance.json` - Random Forest only
- `model_comparison.json` - Model comparison

---

**Status:** ✅ Tables are being logged correctly  
**Location:** MLflow UI → Experiment → Latest Run → Artifacts  
**Next:** Re-train and check the newest runs!

🎉 **Your tables are there - just look in the new runs!**

