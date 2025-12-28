# 📊 MLflow Dataset Logging - Complete Guide

**Date:** December 28, 2025  
**Feature:** `mlflow.log_input()` for dataset tracking  
**Status:** ✅ Implemented

---

## 🎯 Overview

MLflow's dataset logging feature (`mlflow.log_input()`) allows you to track which datasets were used to train each model. This provides:
- **Data versioning** - Track which data version trained which model
- **Reproducibility** - Know exactly what data was used
- **Data lineage** - Trace data from source to model
- **Dataset statistics** - View dataset properties and schema

---

## ✨ What Was Added

### Code Changes in `src/models/train.py`:

#### 1. **Import MLflow Data Module**
```python
import mlflow.data
from mlflow.data.pandas_dataset import PandasDataset
```

#### 2. **Updated load_data() Function**
Now returns both numpy arrays AND pandas DataFrames:
```python
def load_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, pd.DataFrame, pd.DataFrame]:
    # Returns: X_train, X_test, y_train, y_test, X_train_df, X_test_df
```

#### 3. **Dataset Logging in Training Functions**
Added to both `train_logistic_regression()` and `train_random_forest()`:

```python
# Create training dataset
train_df = X_train_df.copy()
train_df['target'] = y_train
train_dataset = mlflow.data.from_pandas(
    train_df,
    source="data/processed/X_train.pkl",
    name="heart_disease_training_data",
    targets="target"
)
mlflow.log_input(train_dataset, context="training")

# Create test dataset  
test_df = X_test_df.copy()
test_df['target'] = y_test
test_dataset = mlflow.data.from_pandas(
    test_df,
    source="data/processed/X_test.pkl",
    name="heart_disease_test_data",
    targets="target"
)
mlflow.log_input(test_dataset, context="testing")
```

---

## 📊 What Gets Logged

For each model run, MLflow now logs:

### Training Dataset:
- **Name:** `heart_disease_training_data`
- **Source:** `data/processed/X_train.pkl`
- **Context:** `training`
- **Samples:** 242 (from your data)
- **Features:** 13 features
- **Target:** `target` column (heart disease labels)

### Test Dataset:
- **Name:** `heart_disease_test_data`
- **Source:** `data/processed/X_test.pkl`
- **Context:** `testing`
- **Samples:** 61 (from your data)
- **Features:** 13 features
- **Target:** `target` column

### Dataset Metadata Logged:
- Number of rows
- Number of columns
- Column names
- Data types
- Target column
- Source path
- Dataset profile/schema

---

## 🔍 How to View Datasets in MLflow UI

### Method 1: MLflow UI (Recommended)

#### Step 1: Train Models
```bash
cd /Users/aashishr/codebase/mlso
python src/models/train.py
```

**Look for confirmation:**
```
✓ Training dataset logged to MLflow
✓ Test dataset logged to MLflow
```

#### Step 2: Open MLflow UI
```bash
open http://localhost:5002
```

#### Step 3: Navigate to Run
1. Click on experiment: **"heart-disease-prediction"**
2. Click on a run (e.g., "random_forest" or "logistic_regression")

#### Step 4: View Datasets Tab
In the run details page, you'll see tabs:
```
[Overview] [Parameters] [Metrics] [Artifacts] [Datasets] ← Click here
```

**Click on the "Datasets" tab** to see:

```
┌────────────────────────────────────────────────────────────┐
│  Datasets Used                                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  📊 Training Dataset                                       │
│     Name: heart_disease_training_data                     │
│     Context: training                                     │
│     Source: data/processed/X_train.pkl                    │
│     Rows: 242                                             │
│     Columns: 14 (13 features + target)                    │
│                                                            │
│  📊 Test Dataset                                           │
│     Name: heart_disease_test_data                         │
│     Context: testing                                      │
│     Source: data/processed/X_test.pkl                     │
│     Rows: 61                                              │
│     Columns: 14 (13 features + target)                    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

#### Step 5: View Dataset Details
Click on a dataset name to see:
- **Schema:** Column names and types
- **Profile:** Statistics about the data
- **Preview:** Sample rows from the dataset
- **Digest:** Dataset hash for versioning

---

### Method 2: Python API

```python
import mlflow
from mlflow.tracking import MlflowClient

# Connect to MLflow
mlflow.set_tracking_uri("./mlruns")
client = MlflowClient()

# Get a run
run_id = "your_run_id_here"  # From MLflow UI
run = client.get_run(run_id)

# Get dataset inputs
print("Datasets used in this run:")
print("=" * 60)

# Access via run data
if hasattr(run.data, 'inputs'):
    for dataset_input in run.data.inputs.dataset_inputs:
        print(f"\nDataset: {dataset_input.dataset.name}")
        print(f"  Context: {dataset_input.tags.get('mlflow.data.context', 'N/A')}")
        print(f"  Source: {dataset_input.dataset.source}")
        print(f"  Schema: {dataset_input.dataset.schema}")
        print(f"  Profile: {dataset_input.dataset.profile}")
```

---

### Method 3: Query via MLflow Search API

```python
import mlflow

mlflow.set_tracking_uri("./mlruns")

# Search runs and get dataset info
runs = mlflow.search_runs(
    experiment_names=["heart-disease-prediction"],
    filter_string="",
    max_results=5
)

for idx, run in runs.iterrows():
    run_id = run['run_id']
    print(f"\nRun: {run['tags.mlflow.runName']}")
    print(f"  Run ID: {run_id[:12]}...")
    
    # Get detailed run info
    client = mlflow.tracking.MlflowClient()
    run_details = client.get_run(run_id)
    
    # Check for datasets
    if hasattr(run_details.inputs, 'dataset_inputs'):
        print(f"  Datasets:")
        for ds in run_details.inputs.dataset_inputs:
            print(f"    - {ds.dataset.name} ({ds.tags.get('mlflow.data.context', 'unknown')})")
```

---

## 🗄️ Datasets in PostgreSQL

When using PostgreSQL backend, datasets are stored in these tables:

### Tables:
- `datasets` - Dataset metadata
- `inputs` - Links between runs and datasets
- `input_tags` - Tags for dataset inputs

### Query Datasets:

```sql
-- View all datasets
SELECT 
    dataset_uuid,
    name,
    digest,
    dataset_source_type
FROM datasets;

-- View dataset usage per run
SELECT 
    r.run_uuid,
    r.name as run_name,
    d.name as dataset_name,
    it.key as tag_key,
    it.value as tag_value
FROM runs r
JOIN inputs i ON r.run_uuid = i.destination_id
JOIN datasets d ON i.dataset_uuid = d.dataset_uuid
LEFT JOIN input_tags it ON i.input_uuid = it.input_uuid
ORDER BY r.start_time DESC;

-- Count dataset usage
SELECT 
    d.name,
    d.dataset_source_type,
    COUNT(DISTINCT i.destination_id) as times_used
FROM datasets d
LEFT JOIN inputs i ON d.dataset_uuid = i.dataset_uuid
GROUP BY d.dataset_uuid, d.name, d.dataset_source_type
ORDER BY times_used DESC;
```

---

## 📈 Benefits of Dataset Logging

### 1. **Reproducibility**
```
Model Version 2 trained with:
  - Training Data: heart_disease_training_data (242 samples)
  - Test Data: heart_disease_test_data (61 samples)
  - Data Source: data/processed/ (2025-12-28)
```

### 2. **Data Versioning**
Track changes in your data over time:
```
Run 1: Dataset v1 (300 samples) → 85% accuracy
Run 2: Dataset v2 (350 samples) → 90% accuracy
```

### 3. **Data Lineage**
```
Raw Data → Preprocessing → Training Set → Model → Predictions
   ↓            ↓              ↓            ↓          ↓
  CSV      cleaning.py     X_train.pkl   best.pkl  results
```

### 4. **Debugging**
If model performance drops, check:
- Did the dataset change?
- Are there data quality issues?
- Is the data distribution different?

### 5. **Compliance & Auditing**
Document exactly what data was used:
```
Audit Trail:
  Model ID: abc123
  Training Data: heart_disease_v2
  Data Source: UCI ML Repository
  Date: 2025-12-28
  Approved: Yes
```

---

## 🔧 Advanced Dataset Logging

### Example 1: Multiple Datasets

```python
# Log training, validation, and test sets
with mlflow.start_run():
    # Training
    train_dataset = mlflow.data.from_pandas(train_df, source="train.csv")
    mlflow.log_input(train_dataset, context="training")
    
    # Validation
    val_dataset = mlflow.data.from_pandas(val_df, source="val.csv")
    mlflow.log_input(val_dataset, context="validation")
    
    # Test
    test_dataset = mlflow.data.from_pandas(test_df, source="test.csv")
    mlflow.log_input(test_dataset, context="testing")
```

### Example 2: Dataset with Tags

```python
# Add custom tags to dataset
with mlflow.start_run():
    dataset = mlflow.data.from_pandas(
        df,
        source="data.csv",
        name="my_dataset",
        targets="target"
    )
    
    mlflow.log_input(
        dataset,
        context="training",
        tags={
            "data_version": "v2.0",
            "preprocessing": "standard_scaling",
            "split_ratio": "0.8",
            "stratified": "true"
        }
    )
```

### Example 3: Dataset from Other Sources

```python
# From numpy arrays
dataset = mlflow.data.from_numpy(
    features=X_train,
    source="numpy_array",
    targets=y_train,
    name="training_data"
)

# From Spark DataFrame
dataset = mlflow.data.from_spark(
    spark_df,
    source="hdfs://data/train.parquet",
    name="spark_training_data"
)

# From Delta table
dataset = mlflow.data.from_delta(
    delta_table_uri="dbfs:/delta/table",
    name="delta_training_data"
)
```

---

## 📊 Dataset Schema & Profile

MLflow automatically captures:

### Schema:
```json
{
  "columns": [
    {"name": "age", "type": "double"},
    {"name": "sex", "type": "long"},
    {"name": "cp", "type": "long"},
    ...
    {"name": "target", "type": "long"}
  ]
}
```

### Profile:
```json
{
  "num_rows": 242,
  "num_columns": 14,
  "column_statistics": {
    "age": {
      "min": 29.0,
      "max": 77.0,
      "mean": 54.5,
      "std": 9.1
    },
    ...
  }
}
```

### Digest (Hash):
```
SHA-256: a3f4b2c8d9e1f0...
```
Used for dataset version tracking

---

## ✅ Verification

### Check if Datasets Are Logged:

```bash
cd /Users/aashishr/codebase/mlso

python << 'EOF'
import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("./mlruns")
client = MlflowClient()

# Get latest runs
exp = client.get_experiment_by_name("heart-disease-prediction")
runs = client.search_runs(
    experiment_ids=[exp.experiment_id],
    max_results=2,
    order_by=["start_time DESC"]
)

print("Checking for dataset logging in latest runs:\n")
for run in runs:
    run_name = run.data.tags.get('mlflow.runName', 'N/A')
    print(f"Run: {run_name}")
    print(f"  Run ID: {run.info.run_id[:12]}...")
    
    # Check for dataset inputs
    run_details = client.get_run(run.info.run_id)
    
    if run_details.inputs.dataset_inputs:
        print(f"  ✅ Datasets logged:")
        for ds_input in run_details.inputs.dataset_inputs:
            context = ds_input.tags.get('mlflow.data.context', 'unknown')
            print(f"     - {ds_input.dataset.name} (context: {context})")
    else:
        print(f"  ❌ No datasets logged")
    print()
EOF
```

---

## 🚀 Running Training with Dataset Logging

### Train Models:
```bash
cd /Users/aashishr/codebase/mlso
python src/models/train.py
```

### Expected Output:
```
TRAINING LOGISTIC REGRESSION
================================================================================
✓ Training dataset logged to MLflow
✓ Test dataset logged to MLflow
...

TRAINING RANDOM FOREST
================================================================================
✓ Training dataset logged to MLflow
✓ Test dataset logged to MLflow
...
```

### View in MLflow UI:
```bash
open http://localhost:5002
# Navigate to: Experiment → Run → Datasets tab
```

---

## 📝 Best Practices

### 1. **Always Log Context**
```python
mlflow.log_input(train_dataset, context="training")
mlflow.log_input(val_dataset, context="validation")
mlflow.log_input(test_dataset, context="testing")
```

### 2. **Include Data Source**
```python
dataset = mlflow.data.from_pandas(
    df,
    source="s3://bucket/data/heart_disease_v2.csv",  # Full path
    name="heart_disease_training_data"
)
```

### 3. **Specify Target Column**
```python
dataset = mlflow.data.from_pandas(
    df,
    source="data.csv",
    targets="target"  # Column name for target variable
)
```

### 4. **Add Descriptive Names**
```python
# Good
name="heart_disease_training_data_v2_cleaned"

# Bad
name="data1"
```

### 5. **Log All Datasets Used**
```python
# Log training, validation, AND test sets
# Log any external datasets used for evaluation
# Log benchmark datasets
```

---

## 🔍 Troubleshooting

### Issue 1: "No Datasets tab in MLflow UI"

**Possible causes:**
- Using old MLflow version (< 2.3.0)
- Looking at old runs (before dataset logging was added)

**Solution:**
```bash
# Check MLflow version
python -c "import mlflow; print(mlflow.__version__)"

# Upgrade if needed
pip install --upgrade mlflow

# Re-train models
python src/models/train.py
```

### Issue 2: "Datasets not showing"

**Solution:**
1. Check training output for: "✓ Training dataset logged to MLflow"
2. Make sure you're viewing a NEW run (after code update)
3. Click on the "Datasets" tab (not "Artifacts")

### Issue 3: "Error logging dataset"

**Common errors:**
```python
# Error: DataFrame has no 'target' column
# Solution: Add target to DataFrame before logging
df['target'] = y_train

# Error: Source path doesn't exist
# Solution: Use relative path or full path
source="data/processed/X_train.pkl"
```

---

## ✅ Summary

### What Was Added:
- ✅ Dataset logging in training script
- ✅ Training dataset tracked
- ✅ Test dataset tracked
- ✅ Dataset context specified
- ✅ Source paths documented

### What You Can See:
- ✅ Datasets tab in MLflow UI
- ✅ Dataset names and contexts
- ✅ Row/column counts
- ✅ Schema information
- ✅ Dataset source paths

### Where to Find:
- **MLflow UI:** http://localhost:5002 → Run → Datasets tab
- **PostgreSQL:** `datasets`, `inputs`, `input_tags` tables
- **Python API:** `run.inputs.dataset_inputs`

### Next Steps:
1. Run training: `python src/models/train.py`
2. Open MLflow UI: `http://localhost:5002`
3. Click on a run
4. Click "Datasets" tab
5. View your dataset information!

---

**Documentation:** https://mlflow.org/docs/latest/python_api/mlflow.data.html  
**Status:** ✅ Implemented and ready to use  
**Next Run:** Datasets will be automatically logged!  

📊 **Your model training data is now tracked in MLflow!**

