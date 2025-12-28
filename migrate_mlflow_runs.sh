#!/bin/bash

# MLflow Runs Migration Helper Script
# This script helps migrate MLflow runs from local mlruns/ to MLflow server

set -e

echo "🔄 MLflow Runs Migration Tool"
echo "=============================="
echo ""

# Check if mlruns directory exists
if [ ! -d "mlruns" ]; then
    echo "⚠️  No mlruns/ folder found in current directory"
    echo "   Run some training jobs first: python src/models/train.py"
    exit 1
fi

# Count experiments and runs
EXPERIMENTS=$(find mlruns -maxdepth 1 -type d | tail -n +2 | wc -l | tr -d ' ')
RUNS=$(find mlruns -type d -name "meta.yaml" | wc -l | tr -d ' ')

echo "📊 Found in local mlruns/:"
echo "   Experiments: $EXPERIMENTS"
echo "   Runs: $RUNS"
echo ""

if [ "$RUNS" -eq 0 ]; then
    echo "⚠️  No runs found to migrate"
    echo "   Run training first: python src/models/train.py"
    exit 0
fi

# Ask for target server
echo "Where do you want to migrate runs to?"
echo ""
echo "1) Docker MLflow server (http://localhost:5001)"
echo "2) Production server (from mlflow_config.py)"
echo "3) Custom URL"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        TARGET="http://localhost:5001"

        # Check if Docker server is running
        if ! docker ps | grep -q mlflow-server; then
            echo ""
            echo "⚠️  Docker MLflow server is not running"
            read -p "Start it now? [y/N]: " start_server
            if [[ $start_server == "y" || $start_server == "Y" ]]; then
                echo "Starting MLflow server..."
                ./start_mlflow_server.sh
                echo "Waiting for server to be ready..."
                sleep 10
            else
                echo "❌ Cancelled. Start server first: ./start_mlflow_server.sh"
                exit 1
            fi
        fi
        ;;
    2)
        echo "Using production config..."
        USE_CONFIG="--use-config"
        TARGET=""
        ;;
    3)
        echo ""
        read -p "Enter target URL (e.g., http://mlflow.company.com): " TARGET
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "📋 Migration Options:"
echo ""
read -p "Copy artifacts? (slower but complete) [Y/n]: " copy_artifacts
read -p "Include failed runs? [y/N]: " include_failed

# Build command
CMD="python src/utils/migrate_mlflow_runs.py"

if [ -n "$TARGET" ]; then
    CMD="$CMD --target $TARGET"
fi

if [ -n "$USE_CONFIG" ]; then
    CMD="$CMD $USE_CONFIG"
fi

if [[ $copy_artifacts == "n" || $copy_artifacts == "N" ]]; then
    CMD="$CMD --no-artifacts"
fi

if [[ $include_failed == "y" || $include_failed == "Y" ]]; then
    CMD="$CMD --include-failed"
fi

echo ""
echo "🚀 Starting migration..."
echo "Command: $CMD"
echo ""

# Run migration
$CMD

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Migration completed successfully!"
    echo ""
    echo "🎯 Next steps:"
    if [[ $choice -eq 1 ]]; then
        echo "   View migrated runs: http://localhost:5001"
    else
        echo "   View migrated runs on your MLflow server"
    fi
else
    echo ""
    echo "❌ Migration failed with errors"
    echo "   Check the output above for details"
fi

exit $EXIT_CODE

