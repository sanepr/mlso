# Registering MLflow Runs to MLflow Server - Complete Guide

## Problem Statement

You have multiple run files in the `mlruns/` folder from local training, and you want to register/migrate them to an MLflow tracking server so they're:
- Centrally accessible
- Backed up and persisted
- Shared across team
- Searchable and comparable

---

## Solution Overview

I've created a comprehensive migration tool that copies all your local MLflow runs to a remote MLflow server.

### What It Does:
✅ Migrates all experiments and runs  
✅ Copies parameters, metrics, and tags  
✅ Optionally copies artifacts (models, files)  
✅ Preserves run metadata  
✅ Adds migration tracking tags  
✅ Handles errors gracefully  

---

## Quick Start

### Option 1: Interactive Migration (Easiest)
```bash
cd /Users/aashishr/codebase/mlso

# Run interactive migration script
./migrate_mlflow_runs.sh
```

The script will:
1. Check if you have runs in `mlruns/`
2. Ask where to migrate (local server, production, or custom)
3. Ask about options (artifacts, failed runs)
4. Perform the migration
5. Show summary

### Option 2: Direct Python Script
```bash
# Migrate to Docker MLflow server
python src/utils/migrate_mlflow_runs.py \
  --target http://localhost:5001

# Migrate to production (uses mlflow_config.py)
python src/utils/migrate_mlflow_runs.py \
  --use-config

# Migrate specific experiment only
python src/utils/migrate_mlflow_runs.py \
  --target http://localhost:5001 \
  --experiment "heart-disease-prediction"
```

---

## Step-by-Step Guide

### Step 1: Check Your Local Runs

```bash
cd /Users/aashishr/codebase/mlso

# Check if you have runs
ls -la mlruns/

# Count experiments
find mlruns -maxdepth 1 -type d | tail -n +2 | wc -l

# Count runs
find mlruns -type f -name "meta.yaml" | wc -l
```

**If no runs exist:**
```bash
# Train a model first to create runs
python src/models/train.py
```

### Step 2: Start Target MLflow Server

**Option A: Docker MLflow Server (Recommended for testing)**
```bash
# Start Docker server
./start_mlflow_server.sh

# Choose option 1 (local filesystem) for quickest setup
# Server will be available at: http://localhost:5001
```

**Option B: Use Production Server**
```bash
# Configure environment
export MLFLOW_ENV=production
export MLFLOW_TRACKING_URI=https://mlflow.your-company.com

# Or create runs directly on production
# (migration script will use config from mlflow_config.py)
```

### Step 3: Run Migration

**Interactive Mode (Easiest):**
```bash
./migrate_mlflow_runs.sh
```

**Or Manual Mode:**
```bash
# Migrate everything to Docker server
python src/utils/migrate_mlflow_runs.py \
  --source file://./mlruns \
  --target http://localhost:5001

# Migrate without artifacts (faster)
python src/utils/migrate_mlflow_runs.py \
  --target http://localhost:5001 \
  --no-artifacts

# Include failed runs
python src/utils/migrate_mlflow_runs.py \
  --target http://localhost:5001 \
  --include-failed
```

### Step 4: Verify Migration

```bash
# Open MLflow UI
open http://localhost:5001

# Or check via API
curl http://localhost:5001/api/2.0/mlflow/experiments/search

# Or use Python
python -c "
import mlflow
mlflow.set_tracking_uri('http://localhost:5001')
experiments = mlflow.search_experiments()
for exp in experiments:
    print(f'Experiment: {exp.name}')
    runs = mlflow.search_runs(experiment_ids=[exp.experiment_id])
    print(f'  Runs: {len(runs)}')
"
```

---

## Migration Script Options

### Command Line Arguments

```bash
python src/utils/migrate_mlflow_runs.py [OPTIONS]

Options:
  --source URI          Source tracking URI (default: file://./mlruns)
  --target URI          Target tracking URI (required)
  --experiment NAME     Migrate specific experiment only
  --no-artifacts        Don't copy artifacts (faster)
  --include-failed      Include failed/incomplete runs
  --use-config          Use target from mlflow_config.py
  -h, --help           Show help message
```

### Examples

**1. Migrate to Docker server:**
```bash
python src/utils/migrate_mlflow_runs.py \
  --target http://localhost:5001
```

**2. Migrate to production:**
```bash
python src/utils/migrate_mlflow_runs.py \
  --use-config
```

**3. Migrate specific experiment:**
```bash
python src/utils/migrate_mlflow_runs.py \
  --target http://localhost:5001 \
  --experiment "model-training-comparison"
```

**4. Fast migration (no artifacts):**
```bash
python src/utils/migrate_mlflow_runs.py \
  --target http://localhost:5001 \
  --no-artifacts
```

**5. Migrate from different source:**
```bash
python src/utils/migrate_mlflow_runs.py \
  --source file:///path/to/old/mlruns \
  --target http://localhost:5001
```

---

## What Gets Migrated?

### ✅ Always Migrated:
- **Experiment names and metadata**
- **Run parameters** (hyperparameters)
- **Run metrics** (accuracy, loss, etc.)
- **Run tags** (custom metadata)
- **Run status** (finished, failed, running)
- **Start/end times**

### ✅ Optionally Migrated:
- **Artifacts** (models, plots, files)
  - Use `--no-artifacts` to skip
  - Speeds up migration significantly
  - Useful if you only need metrics/params

### ➕ Added During Migration:
- **Migration metadata tags:**
  - `mlflow.migration.source_run_id` - Original run ID
  - `mlflow.migration.timestamp` - When migrated
  - `mlflow.migration.source_uri` - Source location

---

## Migration Scenarios

### Scenario 1: Local Development → Team Server

**Situation:** You've been training locally, now want to share with team.

```bash
# 1. Start team's MLflow server (if using Docker)
./start_mlflow_server.sh

# 2. Migrate your local runs
./migrate_mlflow_runs.sh
# Choose option 1 (Docker server)

# 3. Team can now access your runs
# Share URL: http://localhost:5001
```

### Scenario 2: Multiple Local Folders → Consolidated Server

**Situation:** Runs scattered across multiple machines/folders.

```bash
# Machine 1
python src/utils/migrate_mlflow_runs.py \
  --source file://./mlruns \
  --target http://central-server:5001

# Machine 2  
python src/utils/migrate_mlflow_runs.py \
  --source file://./mlruns \
  --target http://central-server:5001

# All runs now in one place!
```

### Scenario 3: Backup Before Cleanup

**Situation:** Want to clean local mlruns/ but keep the data.

```bash
# 1. Migrate to server
python src/utils/migrate_mlflow_runs.py \
  --target http://localhost:5001

# 2. Verify migration successful
open http://localhost:5001

# 3. Clean local folder
rm -rf mlruns/

# Data is safe on server!
```

### Scenario 4: Selective Migration

**Situation:** Only want to migrate certain experiments.

```bash
# Migrate only production-ready experiments
python src/utils/migrate_mlflow_runs.py \
  --target http://localhost:5001 \
  --experiment "production-models"

# Migrate successful runs only
python src/utils/migrate_mlflow_runs.py \
  --target http://localhost:5001
# (by default skips failed runs)
```

---

## Troubleshooting

### Issue 1: No runs found

**Error:** `No mlruns/ folder found`

**Solution:**
```bash
# Train a model first
python src/models/train.py

# This creates runs in mlruns/
```

### Issue 2: Target server not accessible

**Error:** `Connection refused` or `Could not connect`

**Solution:**
```bash
# Check if server is running
docker ps | grep mlflow

# If not, start it
./start_mlflow_server.sh

# Test connection
curl http://localhost:5001/
```

### Issue 3: Migration fails for some runs

**Error:** `Failed to migrate run xxx`

**Solution:**
- Check the error message
- Common causes:
  - Corrupted run data
  - Missing artifact files
  - Permission issues
- Use `--no-artifacts` to skip artifact copying
- Check source run data: `ls mlruns/0/RUN_ID/`

### Issue 4: Artifacts not copying

**Warning:** `Could not copy artifacts`

**Solution:**
- Ensure source artifacts exist: `ls mlruns/0/RUN_ID/artifacts/`
- Check disk space on target server
- Verify artifact storage configuration
- For large artifacts, consider manual copy

### Issue 5: Duplicate runs

**Situation:** Running migration multiple times

**Solution:**
- Migration creates NEW runs each time
- Check run tags for `mlflow.migration.source_run_id`
- To avoid duplicates:
  ```python
  # Before migrating, check if already migrated
  target_runs = mlflow.search_runs(experiment_ids=[exp_id])
  migrated_ids = [
      run.data.tags.get('mlflow.migration.source_run_id')
      for run in target_runs
  ]
  # Skip if source_run_id in migrated_ids
  ```

---

## Advanced Usage

### Custom Migration Logic

Create your own migration script:

```python
from src.utils.migrate_mlflow_runs import MLflowRunsMigrator

# Initialize
migrator = MLflowRunsMigrator(
    source_uri="file://./mlruns",
    target_uri="http://localhost:5001"
)

# Migrate specific experiments
stats = migrator.migrate_experiment(
    "my-experiment",
    copy_artifacts=True,
    skip_failed=True
)

print(f"Migrated {stats['success']} runs")
```

### Filter Runs During Migration

```python
from mlflow.entities import RunStatus

# Get source client
source_client = migrator.source_client

# Get runs with filter
runs = source_client.search_runs(
    experiment_ids=['0'],
    filter_string="metrics.accuracy > 0.8",
    order_by=["metrics.accuracy DESC"],
    max_results=10
)

# Migrate only these runs
for run in runs:
    migrator.copy_run(run, target_experiment_id, copy_artifacts=True)
```

### Batch Migration with Progress

```python
from tqdm import tqdm

experiments = migrator.list_experiments(migrator.source_client)

for exp in tqdm(experiments, desc="Experiments"):
    runs = migrator.list_runs(migrator.source_client, exp.experiment_id)
    
    for run in tqdm(runs, desc=f"  Runs in {exp.name}", leave=False):
        try:
            migrator.copy_run(run, target_exp_id)
        except Exception as e:
            print(f"Error: {e}")
```

---

## Performance Considerations

### Migration Speed

| Scenario | Speed | Time (100 runs) |
|----------|-------|-----------------|
| Params + Metrics only | Fast | ~1-2 minutes |
| With small artifacts | Medium | ~5-10 minutes |
| With large models (100MB+) | Slow | ~30-60 minutes |

### Optimization Tips

1. **Use `--no-artifacts` for initial migration**
   - Migrate metadata first (fast)
   - Migrate artifacts separately if needed

2. **Parallel migration** (for large datasets)
   ```python
   from concurrent.futures import ThreadPoolExecutor
   
   with ThreadPoolExecutor(max_workers=4) as executor:
       futures = [
           executor.submit(migrator.copy_run, run, target_exp_id)
           for run in runs
       ]
   ```

3. **Network optimization**
   - Ensure good network connection to target
   - Use VPN if accessing remote server
   - Consider direct database access for very large migrations

---

## Best Practices

### ✅ Do:
- **Backup before migration** - Copy `mlruns/` folder
- **Test with one experiment first** - Use `--experiment` flag
- **Verify migration** - Check target server before deleting source
- **Use meaningful experiment names** - Easier to track
- **Document migration** - Keep record of what was migrated when

### ❌ Don't:
- **Delete source before verifying** - Ensure migration successful
- **Migrate to production directly** - Test on staging first
- **Ignore errors** - Check migration logs carefully
- **Run multiple migrations simultaneously** - Can cause conflicts

---

## Summary

### Files Created:
1. ✅ `src/utils/migrate_mlflow_runs.py` - Migration script (400+ lines)
2. ✅ `src/utils/__init__.py` - Utils package init
3. ✅ `migrate_mlflow_runs.sh` - Interactive helper script

### Quick Commands:
```bash
# Interactive migration
./migrate_mlflow_runs.sh

# Direct migration to Docker server
python src/utils/migrate_mlflow_runs.py --target http://localhost:5001

# Migration to production
python src/utils/migrate_mlflow_runs.py --use-config
```

### What You Get:
✅ All runs centralized on MLflow server  
✅ Parameters, metrics, and artifacts preserved  
✅ Team can access and compare runs  
✅ Data backed up and persistent  
✅ Migration fully tracked and auditable  

---

## Next Steps

1. **Train some models** (if you haven't):
   ```bash
   python src/models/train.py
   ```

2. **Start MLflow server:**
   ```bash
   ./start_mlflow_server.sh
   ```

3. **Migrate runs:**
   ```bash
   ./migrate_mlflow_runs.sh
   ```

4. **View on server:**
   ```bash
   open http://localhost:5001
   ```

---

**Created:** December 28, 2025  
**Purpose:** Migrate local MLflow runs to tracking server  
**Status:** ✅ Complete and ready to use  
**Files:** 3 files created (migration script + helper + docs)

🎉 **Your MLflow runs can now be registered on any MLflow server!**

