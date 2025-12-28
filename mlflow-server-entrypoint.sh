#!/bin/bash
set -e

echo "Installing MLflow and dependencies..."
pip install --no-cache-dir mlflow==2.9.2 psycopg2-binary==2.9.9 boto3==1.34.13

echo "Waiting for database to be ready..."
sleep 5

echo "Starting MLflow server..."
mlflow server \
    --backend-store-uri "${BACKEND_STORE_URI}" \
    --default-artifact-root "${ARTIFACT_ROOT}" \
    --host 0.0.0.0 \
    --port 5000 \
    --workers 2


