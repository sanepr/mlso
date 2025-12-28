# 📊 MLflow Model Registry & Evaluation Tables Guide

**Date:** December 28, 2025  
**Purpose:** Access and query MLflow model registry and evaluation data

---

## 🎯 Understanding MLflow Model Registry Storage

### Current Setup in Your Project:

**Local File-Based Storage (mlruns/):**
- ✅ Contains your registered models
- ✅ Has all run data, parameters, metrics
- ✅ Accessible via MLflow UI on port 5002

**Docker PostgreSQL:**
- Running but currently empty (no registered models yet)
- Can be used for production MLflow server
- Separate from local file storage

---

## 📋 Model Registry Tables in PostgreSQL

When models are registered in PostgreSQL, these tables store the data:

### Core Tables:

```
registered_models          - Model names and metadata
model_versions            - Model versions (1, 2, 3, etc.)
model_version_tags        - Tags for each version
registered_model_tags     - Tags for models
registered_model_aliases  - Model aliases
```

### Related Tables:

```
runs                      - Training runs linked to models
params                    - Model hyperparameters
metrics                   - Model performance metrics
latest_metrics            - Latest metric values
tags                      - Run tags
```

---

## 🔍 Query Model Registry Data

### Method 1: From Local File Storage (Your Current Setup)

#### Using Python:

```python
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd

# Connect to local mlruns
mlflow.set_tracking_uri("file://./mlruns")
client = MlflowClient()

# Get all registered models
print("=" * 80)
print("REGISTERED MODELS")
print("=" * 80)

for model in client.search_registered_models():
    print(f"\n📦 Model: {model.name}")
    print(f"   Description: {model.description or 'N/A'}")
    print(f"   Created: {model.creation_timestamp}")
    print(f"   Updated: {model.last_updated_timestamp}")
    
    # Get versions
    for version in model.latest_versions:
        print(f"\n   Version {version.version}:")
        print(f"      Stage: {version.current_stage}")
        print(f"      Status: {version.status}")
        print(f"      Run ID: {version.run_id}")
        
        # Get run details (metrics, params)
        run = client.get_run(version.run_id)
        
        print(f"\n      Parameters:")
        for key, value in sorted(run.data.params.items()):
            print(f"         {key}: {value}")
        
        print(f"\n      Evaluation Metrics:")
        for key, value in sorted(run.data.metrics.items()):
            if 'test' in key or 'val' in key or 'cv' in key:
                print(f"         {key}: {value:.4f}")
        
        # Get tags
        if version.tags:
            print(f"\n      Tags:")
            for key, value in version.tags.items():
                print(f"         {key}: {value}")
```

#### Quick Script:

```bash
cd /Users/aashishr/codebase/mlso
python << 'EOF'
import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("file://./mlruns")
client = MlflowClient()

print("REGISTERED MODELS EVALUATION DATA")
print("=" * 80)

for model in client.search_registered_models():
    print(f"\nModel: {model.name}")
    for ver in model.latest_versions:
        run = client.get_run(ver.run_id)
        print(f"  Version {ver.version} ({ver.current_stage}):")
        
        # Key evaluation metrics
        metrics = run.data.metrics
        for metric_name in ['test_accuracy', 'test_roc_auc', 'test_f1', 'cv_accuracy']:
            if metric_name in metrics:
                print(f"    {metric_name}: {metrics[metric_name]:.4f}")
EOF
```

---

### Method 2: From PostgreSQL (When Models Are Registered There)

#### SQL Queries for Model Registry:

**1. List All Registered Models:**
```sql
SELECT 
    name as model_name,
    creation_time,
    last_updated_time
FROM registered_models
ORDER BY creation_time DESC;
```

**2. List Model Versions with Stages:**
```sql
SELECT 
    rm.name as model_name,
    mv.version,
    mv.current_stage,
    mv.status,
    mv.creation_time
FROM registered_models rm
JOIN model_versions mv ON rm.name = mv.name
ORDER BY rm.name, mv.version DESC;
```

**3. Get Model Evaluation Metrics:**
```sql
SELECT 
    rm.name as model_name,
    mv.version,
    mv.current_stage,
    lm.key as metric_name,
    lm.value as metric_value
FROM registered_models rm
JOIN model_versions mv ON rm.name = mv.name
JOIN latest_metrics lm ON mv.run_id = lm.run_uuid
WHERE lm.key LIKE '%test%' OR lm.key LIKE '%val%' OR lm.key LIKE '%cv%'
ORDER BY rm.name, mv.version, lm.key;
```

**4. Get Model Parameters:**
```sql
SELECT 
    rm.name as model_name,
    mv.version,
    p.key as param_name,
    p.value as param_value
FROM registered_models rm
JOIN model_versions mv ON rm.name = mv.name
JOIN params p ON mv.run_id = p.run_uuid
ORDER BY rm.name, mv.version, p.key;
```

**5. Complete Model Evaluation View:**
```sql
-- Create a comprehensive view of model evaluation data
SELECT 
    rm.name as model_name,
    mv.version,
    mv.current_stage,
    mv.status,
    r.status as run_status,
    r.start_time,
    r.end_time,
    COUNT(DISTINCT p.key) as total_params,
    COUNT(DISTINCT m.key) as total_metrics
FROM registered_models rm
JOIN model_versions mv ON rm.name = mv.name
JOIN runs r ON mv.run_id = r.run_uuid
LEFT JOIN params p ON r.run_uuid = p.run_uuid
LEFT JOIN metrics m ON r.run_uuid = m.run_uuid
GROUP BY rm.name, mv.version, mv.current_stage, mv.status, r.status, r.start_time, r.end_time
ORDER BY rm.name, mv.version DESC;
```

**6. Get Model Tags:**
```sql
SELECT 
    rm.name as model_name,
    mv.version,
    mvt.key as tag_key,
    mvt.value as tag_value
FROM registered_models rm
JOIN model_versions mv ON rm.name = mv.name
JOIN model_version_tags mvt ON mv.name = mvt.name AND mv.version = mvt.version
ORDER BY rm.name, mv.version;
```

---

## 📊 Create Model Evaluation Report

### Python Script: Generate Evaluation Report

Save as `model_evaluation_report.py`:

```python
#!/usr/bin/env python3
"""
Generate Model Evaluation Report from MLflow Registry
"""

import mlflow
from mlflow.tracking import MlflowClient
from datetime import datetime
import pandas as pd

def generate_report(tracking_uri="file://./mlruns"):
    """Generate comprehensive model evaluation report."""
    
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()
    
    print("=" * 100)
    print("MODEL REGISTRY EVALUATION REPORT")
    print("=" * 100)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Tracking URI: {tracking_uri}")
    print("=" * 100)
    
    # Get all registered models
    models = client.search_registered_models()
    
    if not models:
        print("\n⚠️  No registered models found")
        return
    
    print(f"\n📊 Total Registered Models: {len(models)}\n")
    
    # Collect data for summary table
    summary_data = []
    
    for model in models:
        print("=" * 100)
        print(f"📦 MODEL: {model.name}")
        print("=" * 100)
        
        for version in model.latest_versions:
            print(f"\n🔖 Version {version.version} - {version.current_stage}")
            print("-" * 100)
            
            # Get run data
            run = client.get_run(version.run_id)
            
            # Basic info
            print(f"   Run ID: {version.run_id}")
            print(f"   Status: {version.status}")
            print(f"   Created: {datetime.fromtimestamp(version.creation_timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Parameters
            print(f"\n   📝 Hyperparameters:")
            params = run.data.params
            for key, value in sorted(params.items()):
                print(f"      • {key:.<40} {value}")
            
            # Evaluation Metrics
            print(f"\n   📊 Evaluation Metrics:")
            metrics = run.data.metrics
            
            # Group metrics
            train_metrics = {k: v for k, v in metrics.items() if 'train' in k}
            test_metrics = {k: v for k, v in metrics.items() if 'test' in k}
            cv_metrics = {k: v for k, v in metrics.items() if 'cv' in k}
            
            if train_metrics:
                print(f"\n      Training Metrics:")
                for key, value in sorted(train_metrics.items()):
                    print(f"         {key:.<35} {value:.6f}")
            
            if test_metrics:
                print(f"\n      Test Metrics:")
                for key, value in sorted(test_metrics.items()):
                    print(f"         {key:.<35} {value:.6f}")
            
            if cv_metrics:
                print(f"\n      Cross-Validation Metrics:")
                for key, value in sorted(cv_metrics.items()):
                    print(f"         {key:.<35} {value:.6f}")
            
            # Tags
            if version.tags:
                print(f"\n   🏷️  Tags:")
                for key, value in version.tags.items():
                    print(f"      • {key}: {value}")
            
            # Add to summary
            summary_data.append({
                'Model': model.name,
                'Version': version.version,
                'Stage': version.current_stage,
                'Test Accuracy': test_metrics.get('test_accuracy', 0),
                'Test ROC-AUC': test_metrics.get('test_roc_auc', 0),
                'Test F1': test_metrics.get('test_f1', 0),
                'CV Accuracy': cv_metrics.get('cv_accuracy', 0),
                'CV ROC-AUC': cv_metrics.get('cv_roc_auc', 0),
            })
            
            print()
    
    # Print summary table
    print("\n" + "=" * 100)
    print("MODELS COMPARISON SUMMARY")
    print("=" * 100 + "\n")
    
    df = pd.DataFrame(summary_data)
    print(df.to_string(index=False))
    
    # Print best model
    if len(df) > 0:
        best_idx = df['Test ROC-AUC'].idxmax()
        best_model = df.iloc[best_idx]
        
        print("\n" + "=" * 100)
        print("🏆 BEST MODEL (by Test ROC-AUC)")
        print("=" * 100)
        print(f"   Model: {best_model['Model']}")
        print(f"   Version: {best_model['Version']}")
        print(f"   Stage: {best_model['Stage']}")
        print(f"   Test ROC-AUC: {best_model['Test ROC-AUC']:.4f}")
        print(f"   Test Accuracy: {best_model['Test Accuracy']:.4f}")
        print("=" * 100)

if __name__ == "__main__":
    generate_report()
```

**Run it:**
```bash
cd /Users/aashishr/codebase/mlso
python model_evaluation_report.py
```

---

## 🔄 Sync Models to PostgreSQL

If you want to move your registered models from file storage to PostgreSQL:

### Option 1: Re-train with PostgreSQL Backend

Update MLflow to use PostgreSQL:

```python
# In your training script
import mlflow

# Point to PostgreSQL
mlflow.set_tracking_uri("postgresql://mlflow:mlflow_password@localhost:5432/mlflow")

# Train and register models as usual
# They will now be stored in PostgreSQL
```

### Option 2: Copy Existing Models

```python
from mlflow.tracking import MlflowClient
import mlflow

# Source (file-based)
source_client = MlflowClient(tracking_uri="file://./mlruns")

# Target (PostgreSQL)
target_uri = "postgresql://mlflow:mlflow_password@localhost:5432/mlflow"
mlflow.set_tracking_uri(target_uri)
target_client = MlflowClient()

# Copy registered models
for model in source_client.search_registered_models():
    print(f"Copying model: {model.name}")
    
    for version in model.latest_versions:
        # Register in target
        model_uri = f"runs:/{version.run_id}/model"
        
        # Note: This requires the run to exist in target
        # You may need to copy runs first
        try:
            mlflow.register_model(
                model_uri=model_uri,
                name=model.name,
                tags=version.tags
            )
            print(f"  ✓ Copied version {version.version}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
```

---

## 📈 Query Evaluation Metrics from PostgreSQL

When your models are in PostgreSQL, use these queries:

### Get Latest Evaluation Metrics per Model:

```bash
docker exec mlflow-postgres psql -U mlflow -d mlflow << 'EOF'
SELECT 
    rm.name as model_name,
    mv.version,
    mv.current_stage,
    json_object_agg(lm.key, lm.value) as metrics
FROM registered_models rm
JOIN model_versions mv ON rm.name = mv.name
JOIN latest_metrics lm ON mv.run_id = lm.run_uuid
WHERE lm.key LIKE '%test%' OR lm.key LIKE '%accuracy%' OR lm.key LIKE '%auc%'
GROUP BY rm.name, mv.version, mv.current_stage
ORDER BY rm.name, mv.version;
EOF
```

### Compare Model Versions:

```sql
WITH model_metrics AS (
    SELECT 
        rm.name as model_name,
        mv.version,
        mv.current_stage,
        lm.key as metric_name,
        lm.value as metric_value
    FROM registered_models rm
    JOIN model_versions mv ON rm.name = mv.name
    JOIN latest_metrics lm ON mv.run_id = lm.run_uuid
)
SELECT 
    model_name,
    version,
    current_stage,
    MAX(CASE WHEN metric_name = 'test_accuracy' THEN metric_value END) as test_accuracy,
    MAX(CASE WHEN metric_name = 'test_roc_auc' THEN metric_value END) as test_roc_auc,
    MAX(CASE WHEN metric_name = 'test_f1' THEN metric_value END) as test_f1
FROM model_metrics
GROUP BY model_name, version, current_stage
ORDER BY test_roc_auc DESC;
```

---

## 🎯 Your Current Models (From File Storage)

### Quick View:

```bash
cd /Users/aashishr/codebase/mlso

python << 'EOF'
import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("file://./mlruns")
client = MlflowClient()

print("YOUR REGISTERED MODELS:")
print("=" * 80)

for model in client.search_registered_models():
    print(f"\n📦 {model.name}")
    for ver in model.latest_versions:
        run = client.get_run(ver.run_id)
        metrics = run.data.metrics
        
        print(f"   Version {ver.version} ({ver.current_stage}):")
        print(f"      Test Accuracy: {metrics.get('test_accuracy', 0):.4f}")
        print(f"      Test ROC-AUC: {metrics.get('test_roc_auc', 0):.4f}")
        print(f"      CV ROC-AUC: {metrics.get('cv_roc_auc', 0):.4f}")
        
        # Top parameters
        params = run.data.params
        print(f"      Key Params:")
        for param in ['model_type', 'n_estimators', 'max_depth', 'C']:
            if param in params:
                print(f"         {param}: {params[param]}")
EOF
```

---

## 📊 Export Model Evaluation to CSV

```python
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd

mlflow.set_tracking_uri("file://./mlruns")
client = MlflowClient()

# Collect data
data = []
for model in client.search_registered_models():
    for ver in model.latest_versions:
        run = client.get_run(ver.run_id)
        
        row = {
            'model_name': model.name,
            'version': ver.version,
            'stage': ver.current_stage,
            'run_id': ver.run_id,
        }
        
        # Add all metrics
        row.update(run.data.metrics)
        
        # Add key parameters
        for key, val in run.data.params.items():
            row[f'param_{key}'] = val
        
        data.append(row)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('model_evaluation_report.csv', index=False)
print(f"✓ Saved to model_evaluation_report.csv")
print(f"  Total models: {len(df)}")
print(f"  Columns: {len(df.columns)}")
```

---

## ✅ Summary

### For File-Based Storage (Your Current Setup):
✅ Use Python MLflow Client  
✅ Access via `mlflow.set_tracking_uri("file://./mlruns")`  
✅ View in MLflow UI: http://localhost:5002  
✅ Run `model_evaluation_report.py` script  

### For PostgreSQL Storage:
✅ Use SQL queries on `registered_models` and `model_versions` tables  
✅ Join with `runs`, `params`, `metrics` for evaluation data  
✅ Access via `docker exec` or Python psycopg2  
✅ Currently empty - needs models to be registered there  

### Key Tables for Model Evaluation:
- `registered_models` - Model names
- `model_versions` - Versions and stages
- `runs` - Training run data
- `params` - Hyperparameters
- `metrics` - Performance metrics
- `model_version_tags` - Model tags

---

**Generated:** December 28, 2025  
**Purpose:** Access MLflow model registry evaluation data  
**Status:** ✅ Complete guide for both storage types

🎯 **Your models' evaluation data is accessible!**

