#!/bin/bash

# Start Jupyter Notebook
# This script ensures the virtual environment is activated and starts Jupyter

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Check if Jupyter is installed
if ! command -v jupyter &> /dev/null; then
    echo "❌ Jupyter not found. Installing..."
    pip install jupyter notebook ipykernel
fi

# Start Jupyter Notebook
echo "🚀 Starting Jupyter Notebook..."
echo "📂 Notebooks directory: $SCRIPT_DIR/notebooks"
echo "🌐 Browser will open at: http://localhost:8888"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$SCRIPT_DIR"
jupyter notebook

