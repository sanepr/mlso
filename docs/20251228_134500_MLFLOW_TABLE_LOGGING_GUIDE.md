# 📊 MLflow Table Logging - Evaluation Tables Guide

**Date:** December 28, 2025  
**Feature:** `mlflow.log_table()` for model evaluation visualization

---

## 🎯 Overview

MLflow's `mlflow.log_table()` function allows you to log structured data (tables) as artifacts that can be viewed directly in the MLflow UI. This is perfect for logging:
- Model evaluation metrics comparison
- Feature importance rankings
- Cross-validation results
- Model performance across different datasets
- Hyperparameter tuning results

---

## 📋 What Was Added

### Tables Logged During Training:

#### 1. **Evaluation Metrics Table** (per model)
Logged for both Logistic Regression and Random Forest:

| Metric | Training | Test | Cross-Validation |
|--------|----------|------|------------------|
| Accuracy | 0.9091 | 0.8852 | 0.8015 |
| ROC-AUC | 0.9795 | 0.9600 | 0.8866 |
| Precision | 0.9113 | 0.8899 | 0.8051 |
| Recall | 0.9091 | 0.8852 | 0.8015 |
| F1-Score | 0.9086 | 0.8854 | 0.8001 |

**Artifact file:** `evaluation_metrics.json`

#### 2. **Feature Importance Table** (Random Forest only)
Top 10 most important features:

| Feature_Index | Importance |
|---------------|------------|
| 12 | 0.1523 |
| 2 | 0.1401 |
| 11 | 0.1289 |
| ... | ... |

**Artifact file:** `feature_importance.json`

#### 3. **Model Comparison Table** (final comparison)
Side-by-side comparison of both models:

| Model | Train Accuracy | Train ROC-AUC | Test Accuracy | Test ROC-AUC | Test Precision | Test Recall | Test F1 | CV ROC-AUC |
|-------|----------------|---------------|---------------|--------------|----------------|-------------|---------|------------|
| Logistic Regression | 0.8347 | 0.9172 | 0.8689 | 0.9567 | 0.8766 | 0.8689 | 0.8690 | 0.9001 |
| Random Forest | 0.9091 | 0.9795 | 0.8852 | 0.9600 | 0.8899 | 0.8852 | 0.8854 | 0.8866 |

**Artifact file:** `model_comparison.json`

---

## 🔍 How to View Tables in MLflow UI

### Step 1: Access MLflow UI
```bash
# MLflow UI on port 5002
open http://localhost:5002
```

### Step 2: Navigate to Experiment
1. Click on experiment: **"heart-disease-prediction"**
2. Click on a specific run (e.g., "random_forest" or "logistic_regression")

### Step 3: View Tables
1. In the run details page, scroll down to **"Artifacts"** section
2. Click on **"Tables"** in the artifacts tree
3. You'll see:
   - `evaluation_metrics.json` - Performance across train/test/CV
   - `feature_importance.json` (Random Forest only)
   - `model_comparison.json` (in parent experiment)

### Step 4: Interactive Table View
- Tables are rendered as interactive views in the MLflow UI
- You can sort by columns
- Export to CSV
- Compare across runs

---

## 💻 Code Implementation

### Basic Usage:

```python
import mlflow
import pandas as pd

# Create a DataFrame
eval_table = pd.DataFrame([{
    'Metric': 'Accuracy',
    'Training': 0.90,
    'Test': 0.85,
    'Cross-Validation': 0.82
}, {
    'Metric': 'ROC-AUC',
    'Training': 0.95,
    'Test': 0.92,
    'Cross-Validation': 0.89
}])

# Log the table (must be inside an active MLflow run)
with mlflow.start_run():
    mlflow.log_table(data=eval_table, artifact_file="evaluation_metrics.json")
```

### Advanced Usage - Multiple Tables:

```python
import mlflow
import pandas as pd

with mlflow.start_run(run_name="model_training"):
    # Train model
    model.fit(X_train, y_train)
    
    # Log evaluation metrics as table
    eval_table = pd.DataFrame({
        'Dataset': ['Train', 'Test', 'Validation'],
        'Accuracy': [0.90, 0.85, 0.83],
        'ROC-AUC': [0.95, 0.92, 0.90],
        'F1-Score': [0.89, 0.84, 0.82]
    })
    mlflow.log_table(data=eval_table, artifact_file="evaluation.json")
    
    # Log feature importance as table
    feature_importance = pd.DataFrame({
        'Feature': ['age', 'cp', 'thalach', 'oldpeak'],
        'Importance': [0.25, 0.20, 0.18, 0.15]
    }).sort_values('Importance', ascending=False)
    mlflow.log_table(data=feature_importance, artifact_file="feature_importance.json")
    
    # Log confusion matrix as table
    cm_table = pd.DataFrame({
        'Predicted_0': [45, 5],
        'Predicted_1': [3, 47]
    }, index=['Actual_0', 'Actual_1'])
    mlflow.log_table(data=cm_table, artifact_file="confusion_matrix.json")
```

---

## 📊 In Your Project

### Location in Code:
`src/models/train.py`

### What's Logged:

**For Logistic Regression run:**
```python
# Line ~265-295
eval_table = pd.DataFrame([{
    'Metric': 'Accuracy',
    'Training': metrics['train_accuracy'],
    'Test': metrics['test_accuracy'],
    'Cross-Validation': metrics['cv_accuracy']
}, {
    'Metric': 'ROC-AUC',
    'Training': metrics['train_roc_auc'],
    'Test': metrics['test_roc_auc'],
    'Cross-Validation': metrics['cv_roc_auc']
}, ...])

mlflow.log_table(data=eval_table, artifact_file="evaluation_metrics.json")
```

**For Random Forest run:**
```python
# Evaluation metrics (same as above)
mlflow.log_table(data=eval_table, artifact_file="evaluation_metrics.json")

# Feature importance (Line ~410-420)
feature_importance_table = pd.DataFrame({
    'Feature_Index': range(len(feature_importance)),
    'Importance': feature_importance
}).sort_values('Importance', ascending=False).head(10)

mlflow.log_table(data=feature_importance_table, artifact_file="feature_importance.json")
```

**Model comparison (after both models trained):**
```python
# Line ~470-495
comparison_table = pd.DataFrame([{
    'Model': 'Logistic Regression',
    'Train Accuracy': lr_metrics['train_accuracy'],
    'Test ROC-AUC': lr_metrics['test_roc_auc'],
    ...
}, {
    'Model': 'Random Forest',
    'Train Accuracy': rf_metrics['train_accuracy'],
    'Test ROC-AUC': rf_metrics['test_roc_auc'],
    ...
}])

mlflow.log_table(data=comparison_table, artifact_file="model_comparison.json")
```

---

## 🚀 Running Training with Table Logging

### Train Models:
```bash
cd /Users/aashishr/codebase/mlso
python src/models/train.py
```

### Output:
```
✓ Model comparison table logged to MLflow
✓ Evaluation metrics table logged
✓ Feature importance table logged
```

### View Results:
```bash
# Open MLflow UI
open http://localhost:5002

# Navigate to:
# 1. Experiment: heart-disease-prediction
# 2. Select a run
# 3. Click "Artifacts" → "Tables"
# 4. View interactive tables
```

---

## 📈 Benefits of Table Logging

### 1. **Structured Data Visualization**
- Tables rendered as proper HTML tables in MLflow UI
- Sortable columns
- Easy to compare values

### 2. **Easy Export**
- Download as JSON
- Convert to CSV
- Use in reports

### 3. **Version Control**
- Tables versioned with runs
- Historical comparison
- Reproducibility

### 4. **Team Collaboration**
- Share evaluation results
- Standardized format
- No manual spreadsheet creation

### 5. **Automated Reporting**
- Generate tables programmatically
- Consistent formatting
- Integrated with training pipeline

---

## 🔧 Advanced Table Logging Examples

### Example 1: Cross-Validation Fold Results

```python
# Log results for each CV fold
cv_results = pd.DataFrame({
    'Fold': [1, 2, 3, 4, 5],
    'Train_Accuracy': [0.89, 0.91, 0.90, 0.88, 0.92],
    'Val_Accuracy': [0.85, 0.87, 0.84, 0.86, 0.88],
    'Train_ROC_AUC': [0.94, 0.96, 0.95, 0.93, 0.97],
    'Val_ROC_AUC': [0.91, 0.92, 0.90, 0.91, 0.93]
})

mlflow.log_table(data=cv_results, artifact_file="cv_folds_results.json")
```

### Example 2: Threshold Analysis

```python
# Log performance at different decision thresholds
threshold_analysis = pd.DataFrame({
    'Threshold': [0.3, 0.4, 0.5, 0.6, 0.7],
    'Precision': [0.75, 0.80, 0.85, 0.90, 0.92],
    'Recall': [0.95, 0.90, 0.85, 0.78, 0.70],
    'F1_Score': [0.84, 0.85, 0.85, 0.83, 0.80]
})

mlflow.log_table(data=threshold_analysis, artifact_file="threshold_analysis.json")
```

### Example 3: Model Predictions Sample

```python
# Log sample predictions
predictions_sample = pd.DataFrame({
    'Patient_ID': range(1, 11),
    'Actual': y_test[:10],
    'Predicted': y_pred[:10],
    'Probability': y_proba[:10, 1],
    'Correct': y_test[:10] == y_pred[:10]
})

mlflow.log_table(data=predictions_sample, artifact_file="sample_predictions.json")
```

---

## 📝 Best Practices

### 1. **Meaningful Table Names**
```python
# ✅ Good
mlflow.log_table(data=df, artifact_file="model_comparison_by_roc_auc.json")

# ❌ Bad
mlflow.log_table(data=df, artifact_file="table1.json")
```

### 2. **Consistent Column Names**
```python
# Use consistent naming across tables
columns = ['Model', 'Test Accuracy', 'Test ROC-AUC', 'CV ROC-AUC']
```

### 3. **Round Numbers for Readability**
```python
# Round to appropriate decimal places
df['Accuracy'] = df['Accuracy'].round(4)
df['ROC-AUC'] = df['ROC-AUC'].round(4)
```

### 4. **Include Metadata**
```python
# Add context columns
df['Experiment'] = 'heart-disease-prediction'
df['Date'] = datetime.now().strftime('%Y-%m-%d')
df['Model_Version'] = '1.0'
```

### 5. **Error Handling**
```python
try:
    mlflow.log_table(data=eval_table, artifact_file="evaluation.json")
    print("✓ Table logged successfully")
except Exception as e:
    print(f"⚠️  Could not log table: {e}")
    # Continue training even if table logging fails
```

---

## 🔍 Querying Tables from MLflow

### Python Script to Read Tables:

```python
import mlflow
from mlflow.tracking import MlflowClient
import json

# Connect to MLflow
mlflow.set_tracking_uri("./mlruns")
client = MlflowClient()

# Get run
run_id = "your_run_id_here"

# Download table artifact
artifact_path = client.download_artifacts(run_id, "evaluation_metrics.json")

# Read table
with open(artifact_path, 'r') as f:
    table_data = json.load(f)
    
print(table_data)
```

---

## ✅ Summary

### What You Can Do Now:

1. **View evaluation tables in MLflow UI** (http://localhost:5002)
2. **Compare models side-by-side** using comparison table
3. **Analyze feature importance** for Random Forest
4. **Track metrics across train/test/CV** in one view
5. **Export tables** for reports and presentations

### Tables Available:
- ✅ `evaluation_metrics.json` - Per-model evaluation (2 files, one per model)
- ✅ `feature_importance.json` - Random Forest features (1 file)
- ✅ `model_comparison.json` - Side-by-side comparison (1 file)

### Where to Find:
- **MLflow UI:** http://localhost:5002 → Experiment → Run → Artifacts → Tables
- **File System:** `mlruns/[experiment_id]/[run_id]/artifacts/`
- **PostgreSQL:** Stored as artifacts in database (if using PostgreSQL backend)

---

**Documentation:** https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_table  
**Status:** ✅ Implemented and ready to use  
**Next Run:** Tables will be automatically logged when you train models  

📊 **Your model evaluation data is now beautifully organized in tables!**

