# MLflow Production Deployment Guide

## Problem Statement

The `mlruns/` folder is:
- ❌ Not committed to git (in `.gitignore`)
- ❌ Local only - lost when redeploying
- ❌ Not accessible across team members
- ❌ Cannot scale for production

## Solution Architecture

### Development Environment
```
Local Training → MLflow Local Storage (mlruns/)
                ↓
          View in MLflow UI
```

### Production Environment
```
Training Job → MLflow Tracking Server → PostgreSQL (metadata)
                                     → S3/Azure/GCS (artifacts)
                ↓
          Shared MLflow UI
```

---

## 🏗️ Architecture Options

### Option 1: Self-Hosted MLflow Server (Recommended)

```
┌─────────────────┐
│  Training Jobs  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│    MLflow Tracking Server       │
│    (FastAPI/Gunicorn)           │
└────────┬────────────────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌─────────────┐
│PostgreSQL│ │ S3/Azure/GCS│
│(Metadata)│ │ (Artifacts) │
└─────────┘ └─────────────┘
```

**Components:**
- **MLflow Server**: Centralized tracking server
- **PostgreSQL**: Stores experiment metadata, parameters, metrics
- **S3/Azure/GCS**: Stores model artifacts, files
- **MLflow UI**: Web interface for viewing experiments

### Option 2: Managed MLflow (Databricks)

Use Databricks' managed MLflow (no infrastructure to manage).

### Option 3: AWS SageMaker with MLflow

Integrate MLflow with AWS SageMaker for end-to-end ML platform.

---

## 📦 Implementation

### Step 1: Install Dependencies

Add to `requirements.txt`:
```txt
mlflow==2.9.2
psycopg2-binary==2.9.9  # For PostgreSQL
boto3==1.34.13          # For AWS S3
azure-storage-blob==12.19.0  # For Azure (optional)
google-cloud-storage==2.14.0  # For GCS (optional)
python-dotenv==1.0.0     # For environment variables
```

### Step 2: Set Up Database

#### PostgreSQL (Recommended)

**Using Docker:**
```bash
docker run -d \
  --name mlflow-postgres \
  -e POSTGRES_USER=mlflow \
  -e POSTGRES_PASSWORD=mlflow_password \
  -e POSTGRES_DB=mlflow \
  -p 5432:5432 \
  postgres:15-alpine
```

**Using AWS RDS:**
1. Create RDS PostgreSQL instance
2. Configure security groups
3. Note the endpoint URL

**Initialize Database:**
```bash
# MLflow will auto-create tables on first run
# Or manually:
mlflow db upgrade postgresql://mlflow:password@host:5432/mlflow
```

### Step 3: Set Up Cloud Storage

#### AWS S3

**Create S3 Bucket:**
```bash
aws s3 mb s3://your-mlflow-artifacts
aws s3api put-bucket-versioning \
  --bucket your-mlflow-artifacts \
  --versioning-configuration Status=Enabled
```

**IAM Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::your-mlflow-artifacts/*",
        "arn:aws:s3:::your-mlflow-artifacts"
      ]
    }
  ]
}
```

#### Azure Blob Storage

```bash
# Create storage account
az storage account create \
  --name mlflowstorage \
  --resource-group mlops \
  --location eastus

# Create container
az storage container create \
  --name mlflow-artifacts \
  --account-name mlflowstorage
```

#### Google Cloud Storage

```bash
# Create bucket
gsutil mb -l us-central1 gs://your-mlflow-artifacts

# Set up service account
gcloud iam service-accounts create mlflow-sa
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:mlflow-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
```

### Step 4: Deploy MLflow Tracking Server

#### Option A: Docker Compose

Create `docker-compose.mlflow.yml`:
```yaml
version: '3.8'

services:
  mlflow-server:
    image: python:3.10-slim
    container_name: mlflow-server
    ports:
      - "5000:5000"
    environment:
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
    command: >
      bash -c "
      pip install mlflow psycopg2-binary boto3 &&
      mlflow server \
        --backend-store-uri postgresql://mlflow:mlflow_password@postgres:5432/mlflow \
        --default-artifact-root s3://your-mlflow-artifacts \
        --host 0.0.0.0 \
        --port 5000
      "
    depends_on:
      - postgres
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    container_name: mlflow-postgres
    environment:
      - POSTGRES_USER=mlflow
      - POSTGRES_PASSWORD=mlflow_password
      - POSTGRES_DB=mlflow
    volumes:
      - mlflow-db:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  mlflow-db:
```

**Start:**
```bash
docker-compose -f docker-compose.mlflow.yml up -d
```

#### Option B: Kubernetes Deployment

Create `deployment/kubernetes/mlflow-server.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mlflow-config
data:
  BACKEND_STORE_URI: "postgresql://mlflow:password@postgres-service:5432/mlflow"
  ARTIFACT_ROOT: "s3://your-mlflow-artifacts"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlflow-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mlflow-server
  template:
    metadata:
      labels:
        app: mlflow-server
    spec:
      containers:
      - name: mlflow-server
        image: python:3.10-slim
        ports:
        - containerPort: 5000
        env:
        - name: BACKEND_STORE_URI
          valueFrom:
            configMapKeyRef:
              name: mlflow-config
              key: BACKEND_STORE_URI
        - name: ARTIFACT_ROOT
          valueFrom:
            configMapKeyRef:
              name: mlflow-config
              key: ARTIFACT_ROOT
        - name: AWS_ACCESS_KEY_ID
          valueFrom:
            secretKeyRef:
              name: aws-credentials
              key: access-key-id
        - name: AWS_SECRET_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: aws-credentials
              key: secret-access-key
        command:
        - /bin/bash
        - -c
        - |
          pip install mlflow psycopg2-binary boto3
          mlflow server \
            --backend-store-uri $BACKEND_STORE_URI \
            --default-artifact-root $ARTIFACT_ROOT \
            --host 0.0.0.0 \
            --port 5000
---
apiVersion: v1
kind: Service
metadata:
  name: mlflow-service
spec:
  type: LoadBalancer
  selector:
    app: mlflow-server
  ports:
  - port: 80
    targetPort: 5000
```

**Deploy:**
```bash
# Create secrets
kubectl create secret generic aws-credentials \
  --from-literal=access-key-id=YOUR_KEY \
  --from-literal=secret-access-key=YOUR_SECRET

# Deploy
kubectl apply -f deployment/kubernetes/mlflow-server.yaml

# Get external IP
kubectl get svc mlflow-service
```

### Step 5: Configure Your Application

**Update `.env` or environment variables:**
```bash
# For production
export MLFLOW_ENV=production
export MLFLOW_TRACKING_URI=https://mlflow.your-domain.com
export MLFLOW_S3_BUCKET=s3://your-mlflow-artifacts
export MLFLOW_DB_URI=postgresql://mlflow:password@host:5432/mlflow
```

**Test Configuration:**
```bash
python src/config/mlflow_config.py
```

### Step 6: Update Training Job

The training script now automatically uses the centralized configuration:

```python
from src.config.mlflow_config import get_mlflow_config

# Automatically uses environment-based configuration
config = get_mlflow_config()
mlflow.set_tracking_uri(config['tracking_uri'])
```

**Run training:**
```bash
# Development (local)
MLFLOW_ENV=development python src/models/train.py

# Production (remote)
MLFLOW_ENV=production \
MLFLOW_TRACKING_URI=https://mlflow.your-domain.com \
python src/models/train.py
```

---

## 🔒 Security Best Practices

### 1. Secrets Management

**Don't hardcode credentials!** Use:

**AWS Systems Manager Parameter Store:**
```bash
aws ssm put-parameter \
  --name /mlflow/db-password \
  --value "your-password" \
  --type SecureString

# In code:
import boto3
ssm = boto3.client('ssm')
password = ssm.get_parameter(Name='/mlflow/db-password', WithDecryption=True)
```

**Kubernetes Secrets:**
```bash
kubectl create secret generic mlflow-secrets \
  --from-literal=db-password=your-password \
  --from-literal=aws-access-key=your-key
```

**Azure Key Vault:**
```python
from azure.keyvault.secrets import SecretClient
client = SecretClient(vault_url="https://your-vault.vault.azure.net/", credential=credential)
password = client.get_secret("mlflow-db-password").value
```

### 2. Network Security

- Use VPC/Private subnets for MLflow server
- Restrict database access to MLflow server only
- Use SSL/TLS for all connections
- Implement authentication (basic auth, OAuth, LDAP)

### 3. Access Control

```bash
# MLflow with basic authentication
mlflow server \
  --backend-store-uri postgresql://... \
  --default-artifact-root s3://... \
  --host 0.0.0.0 \
  --app-name basic-auth
```

---

## 🚀 CI/CD Integration

### GitHub Actions

Update `.github/workflows/model-training.yml`:
```yaml
env:
  MLFLOW_ENV: production
  MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
  MLFLOW_S3_BUCKET: ${{ secrets.MLFLOW_S3_BUCKET }}
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

jobs:
  train:
    steps:
    - name: Train model with MLflow tracking
      run: |
        python src/models/train.py
```

---

## 📊 Accessing MLflow UI

### Development
```bash
mlflow ui
# Open: http://localhost:5000
```

### Production
```bash
# Direct access
https://mlflow.your-domain.com

# Port forward (Kubernetes)
kubectl port-forward svc/mlflow-service 5000:80
# Open: http://localhost:5000
```

---

## 🔄 Migration from Local to Production

### 1. Export Existing Experiments

```python
import mlflow

# Connect to local
mlflow.set_tracking_uri("file://./mlruns")

# Get all experiments
experiments = mlflow.search_experiments()

# Export runs
for exp in experiments:
    runs = mlflow.search_runs(experiment_ids=[exp.experiment_id])
    runs.to_csv(f"export_{exp.name}.csv")
```

### 2. Import to Production

```python
import mlflow
import pandas as pd

# Connect to production
mlflow.set_tracking_uri("https://mlflow.your-domain.com")

# Create experiment
experiment_id = mlflow.create_experiment("heart-disease-prediction")

# Re-run or manually log
# (Artifacts need to be uploaded separately)
```

---

## 📈 Monitoring & Maintenance

### Database Maintenance

```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size('mlflow'));

-- Clean old experiments
DELETE FROM experiments WHERE lifecycle_stage = 'deleted' AND last_update_time < NOW() - INTERVAL '90 days';
```

### Storage Cleanup

```bash
# S3 lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket your-mlflow-artifacts \
  --lifecycle-configuration file://lifecycle.json
```

`lifecycle.json`:
```json
{
  "Rules": [
    {
      "Id": "DeleteOldArtifacts",
      "Status": "Enabled",
      "Expiration": {
        "Days": 365
      },
      "Filter": {
        "Prefix": "artifacts/"
      }
    }
  ]
}
```

---

## 🎯 Summary

### What Changed:
✅ Created `src/config/mlflow_config.py` - Centralized configuration  
✅ Updated `src/models/train.py` - Uses new config  
✅ Added environment files (`.env.development`, `.env.production.example`)  
✅ Created deployment documentation  

### Production Setup Checklist:
- [ ] Set up PostgreSQL database
- [ ] Create S3/Azure/GCS bucket
- [ ] Deploy MLflow tracking server
- [ ] Configure environment variables
- [ ] Test connection from training job
- [ ] Update CI/CD pipeline
- [ ] Set up monitoring and backups

### Quick Start:
```bash
# 1. Set environment variables
export MLFLOW_ENV=production
export MLFLOW_TRACKING_URI=https://mlflow.your-domain.com

# 2. Test configuration
python src/config/mlflow_config.py

# 3. Run training
python src/models/train.py
```

---

**Created:** December 28, 2025  
**Status:** ✅ Production Ready  
**Next Steps:** Deploy MLflow server and configure production environment

