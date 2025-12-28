#!/bin/bash

# MLflow Server Quick Start Script
# This script starts a local MLflow server with PostgreSQL backend

set -e

echo "🚀 Starting MLflow Server with PostgreSQL Backend"
echo "=================================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose."
    exit 1
fi

# Ask user which artifact store to use
echo "Choose artifact storage:"
echo "1) Local filesystem (development)"
echo "2) MinIO (S3-compatible, local)"
echo "3) AWS S3 (production)"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo "📦 Using local filesystem for artifacts"
        export MLFLOW_ARTIFACT_ROOT="file:///mlflow/artifacts"
        docker-compose -f docker-compose.mlflow.yml up -d mlflow-db mlflow-server
        ;;
    2)
        echo "📦 Using MinIO (S3-compatible) for artifacts"
        export MLFLOW_ARTIFACT_ROOT="s3://mlflow-artifacts"
        export AWS_ACCESS_KEY_ID="minioadmin"
        export AWS_SECRET_ACCESS_KEY="minioadmin"
        export MLFLOW_S3_ENDPOINT_URL="http://minio:9000"
        docker-compose --profile with-minio -f docker-compose.mlflow.yml up -d
        echo ""
        echo "MinIO Console: http://localhost:9001"
        echo "Username: minioadmin"
        echo "Password: minioadmin"
        ;;
    3)
        echo "📦 Using AWS S3 for artifacts"
        echo ""
        read -p "Enter S3 bucket name (e.g., s3://my-mlflow-bucket): " s3_bucket
        read -p "Enter AWS Access Key ID: " aws_key
        read -s -p "Enter AWS Secret Access Key: " aws_secret
        echo ""
        read -p "Enter AWS Region [us-east-1]: " aws_region
        aws_region=${aws_region:-us-east-1}

        export MLFLOW_ARTIFACT_ROOT="$s3_bucket/artifacts"
        export AWS_ACCESS_KEY_ID="$aws_key"
        export AWS_SECRET_ACCESS_KEY="$aws_secret"
        export AWS_DEFAULT_REGION="$aws_region"

        docker-compose -f docker-compose.mlflow.yml up -d mlflow-db mlflow-server
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check if MLflow server is running
if docker ps | grep -q mlflow-server; then
    echo "✅ MLflow Server is running!"
    echo ""
    echo "📊 MLflow UI: http://localhost:5001"
    echo "🗄️  PostgreSQL: localhost:5432 (user: mlflow, password: mlflow_password)"
    echo ""
    echo "To stop: docker-compose -f docker-compose.mlflow.yml down"
    echo "To view logs: docker-compose -f docker-compose.mlflow.yml logs -f mlflow-server"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Set environment variable: export MLFLOW_TRACKING_URI=http://localhost:5001"
    echo "2. Run training: python src/models/train.py"
    echo "3. View experiments at: http://localhost:5001"
else
    echo "❌ Failed to start MLflow Server"
    echo "Check logs with: docker-compose -f docker-compose.mlflow.yml logs"
    exit 1
fi

