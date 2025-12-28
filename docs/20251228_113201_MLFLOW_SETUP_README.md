# MLflow Production Setup - Quick Summary

## Problem
The `mlruns/` folder is local-only and not suitable for production. You need a scalable, shared MLflow tracking system.

## Solution Created

### ✅ Files Added

1. **`src/config/mlflow_config.py`** - Centralized MLflow configuration
   - Environment-aware (dev/staging/prod)
   - Supports local, database, and remote tracking
   - Cloud storage integration (S3/Azure/GCS)

2. **Environment Files**
   - `.env.development` - Local development config
   - `.env.production.example` - Production template

3. **Docker Deployment**
   - `docker-compose.mlflow.yml` - MLflow server with PostgreSQL
   - `mlflow-server-entrypoint.sh` - Server startup script
   - `start_mlflow_server.sh` - Quick start helper

4. **Documentation**
   - `docs/MLFLOW_PRODUCTION_DEPLOYMENT.md` - Complete deployment guide

### ✅ Changes Made

**Updated:** `src/models/train.py`
- Now uses centralized configuration
- Automatically adapts to environment

---

## 🚀 Quick Start

### Option 1: Local MLflow Server (Docker)

```bash
# Start MLflow server with PostgreSQL
./start_mlflow_server.sh

# In another terminal, train with remote tracking
export MLFLOW_TRACKING_URI=http://localhost:5001
python src/models/train.py

# View experiments
open http://localhost:5001
```

**Note:** Uses port **5001** to avoid conflict with local `mlflow ui` (port 5000).

### Option 2: Keep Using Local (Development)

```bash
# No changes needed - continues working as before
python src/models/train.py

# View local experiments
mlflow ui
```

---

## 📊 Architecture Comparison

### Before (Local Only)
```
Training → mlruns/ folder (local)
          ↓
       Lost on redeploy ❌
```

### After (Production Ready)
```
Training → MLflow Server → PostgreSQL (metadata) ✅
                        → S3/Azure/GCS (models) ✅
          ↓
    Shared across team ✅
    Persists forever ✅
```

---

## 🔧 Production Deployment Steps

### 1. Set Up Database (PostgreSQL)

**Docker:**
```bash
docker run -d \
  --name mlflow-postgres \
  -e POSTGRES_USER=mlflow \
  -e POSTGRES_PASSWORD=secure_password \
  -e POSTGRES_DB=mlflow \
  -p 5432:5432 \
  postgres:15-alpine
```

**Or use managed service:**
- AWS RDS PostgreSQL
- Azure Database for PostgreSQL
- Google Cloud SQL

### 2. Set Up Storage (S3)

```bash
# Create S3 bucket
aws s3 mb s3://your-mlflow-artifacts

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket your-mlflow-artifacts \
  --versioning-configuration Status=Enabled
```

### 3. Deploy MLflow Server

**Docker Compose:**
```bash
# Edit docker-compose.mlflow.yml with your settings
docker-compose -f docker-compose.mlflow.yml up -d
```

**Kubernetes:**
```bash
kubectl apply -f deployment/kubernetes/mlflow-server.yaml
```

### 4. Configure Application

**Set environment variables:**
```bash
export MLFLOW_ENV=production
export MLFLOW_TRACKING_URI=https://mlflow.your-domain.com
export MLFLOW_S3_BUCKET=s3://your-mlflow-artifacts
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
```

**Or create `.env` file:**
```bash
cp .env.production.example .env.production
# Edit .env.production with your values
```

### 5. Test

```bash
# Test configuration
python src/config/mlflow_config.py

# Run training
python src/models/train.py

# Check MLflow UI
open https://mlflow.your-domain.com
```

---

## 🎯 Configuration Examples

### Development (Local)
```bash
export MLFLOW_ENV=development
# Uses: file://./mlruns
```

### Staging (Docker + S3)
```bash
export MLFLOW_ENV=staging
export MLFLOW_TRACKING_URI=http://localhost:5001
export MLFLOW_S3_BUCKET=s3://mlflow-staging
```

### Production (Remote + S3)
```bash
export MLFLOW_ENV=production
export MLFLOW_TRACKING_URI=https://mlflow.company.com
export MLFLOW_S3_BUCKET=s3://mlflow-prod
export MLFLOW_DB_URI=postgresql://user:pass@db.host:5432/mlflow
```

---

## 📦 Storage Options

### 1. AWS S3 (Recommended)
```bash
export MLFLOW_S3_BUCKET=s3://your-bucket/mlflow
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=yyy
```

### 2. Azure Blob Storage
```bash
export MLFLOW_AZURE_CONTAINER=wasbs://mlflow@account.blob.core.windows.net
export AZURE_STORAGE_CONNECTION_STRING=xxx
```

### 3. Google Cloud Storage
```bash
export MLFLOW_GCS_BUCKET=gs://your-bucket/mlflow
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

### 4. Local (Development Only)
```bash
# No configuration needed - default
```

---

## 🔐 Security

**DO NOT commit:**
- ❌ Database passwords
- ❌ Cloud storage credentials
- ❌ MLflow server URLs (if private)

**Use instead:**
- ✅ Environment variables
- ✅ AWS Secrets Manager / Azure Key Vault
- ✅ Kubernetes Secrets
- ✅ `.env` files (add to `.gitignore`)

---

## 📚 Learn More

**Complete Guide:** `docs/MLFLOW_PRODUCTION_DEPLOYMENT.md`

**Key Topics:**
- Detailed architecture diagrams
- Step-by-step deployment for AWS/Azure/GCP
- Kubernetes deployment manifests
- Security best practices
- Monitoring and maintenance
- Migration from local to production
- CI/CD integration

---

## ✅ Summary

| Aspect | Before | After |
|--------|--------|-------|
| **Storage** | Local `mlruns/` | PostgreSQL + S3/Azure/GCS |
| **Accessibility** | Single machine | Team-wide access |
| **Persistence** | Lost on redeploy | Permanent storage |
| **Scalability** | Limited | Production-ready |
| **Cost** | Free | ~$50-100/month |

---

## 🚦 Next Steps

### Immediate (Development)
```bash
# Option A: Continue using local
python src/models/train.py  # Works as before

# Option B: Try Docker server
./start_mlflow_server.sh
export MLFLOW_TRACKING_URI=http://localhost:5000
python src/models/train.py
```

### For Production
1. Read `docs/MLFLOW_PRODUCTION_DEPLOYMENT.md`
2. Set up PostgreSQL database
3. Create S3 bucket (or Azure/GCS)
4. Deploy MLflow server
5. Configure environment variables
6. Update CI/CD pipeline

---

**Created:** December 28, 2025  
**Status:** ✅ Production Ready  
**Impact:** MLflow now works in production environments  
**Backward Compatible:** ✅ Yes - local development still works

