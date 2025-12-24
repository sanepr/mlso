#!/bin/bash

# MLOps Heart Disease Prediction - Linux/Mac Startup Script
# This script automates the setup and initialization of the project

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[X]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

echo "========================================"
echo "  MLOps Heart Disease Prediction"
echo "  Automated Setup Script (Linux/Mac)"
echo "========================================"
echo ""

# Check if Python is installed
print_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.9+ first."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python $PYTHON_VERSION detected"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip first."
    exit 1
fi
print_success "pip3 detected"
echo ""

# Create virtual environment
print_info "Creating virtual environment..."
if [ -d "venv" ]; then
    print_info "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi
echo ""

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"
echo ""

# Upgrade pip
print_info "Upgrading pip..."
python -m pip install --upgrade pip -q
print_success "pip upgraded"
echo ""

# Install requirements
print_info "Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt -q
if [ $? -eq 0 ]; then
    print_success "Dependencies installed"
else
    print_error "Failed to install dependencies. Please check requirements.txt"
    exit 1
fi
echo ""

# Create necessary directories
print_info "Creating project directories..."
mkdir -p data/raw data/processed models logs screenshots mlruns
print_success "Directories created"
echo ""

# Download dataset
print_info "Downloading Heart Disease dataset..."
if [ -f "data/raw/heart.csv" ]; then
    print_info "Dataset already exists. Skipping download."
else
    python src/data/download_data.py
    if [ $? -eq 0 ]; then
        print_success "Dataset downloaded"
    else
        print_error "Failed to download dataset."
        exit 1
    fi
fi
echo ""

# Preprocess data
print_info "Preprocessing data..."
if [ -f "data/processed/X_train.pkl" ]; then
    print_info "Preprocessed data already exists. Skipping preprocessing."
else
    python src/data/preprocessing.py
    if [ $? -eq 0 ]; then
        print_success "Data preprocessed"
    else
        print_error "Failed to preprocess data."
        exit 1
    fi
fi
echo ""

# Run tests
print_info "Running tests..."
pytest tests/ -v --tb=short
if [ $? -eq 0 ]; then
    print_success "All tests passed"
else
    print_warning "Some tests failed. Please check the output above."
fi
echo ""

# Train models (optional)
read -p "Do you want to train the models now? (y/n): " TRAIN_MODELS
if [[ "$TRAIN_MODELS" =~ ^[Yy]$ ]]; then
    print_info "Training models with MLflow tracking..."
    python src/models/train.py
    if [ $? -eq 0 ]; then
        print_success "Models trained successfully"
    else
        print_error "Model training failed."
    fi
else
    print_info "Skipping model training. You can train later with: python src/models/train.py"
fi
echo ""

# Setup complete
echo "========================================"
echo "  Setup Complete! 🎉"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Activate virtual environment (if not already active):"
echo "   source venv/bin/activate"
echo ""
echo "2. Start Jupyter for EDA:"
echo "   jupyter notebook notebooks/01_eda.ipynb"
echo ""
echo "3. Train models (if skipped):"
echo "   python src/models/train.py"
echo ""
echo "4. View MLflow UI:"
echo "   mlflow ui"
echo ""
echo "5. Start the API server:"
echo "   python src/api/app.py"
echo ""
echo "6. Run tests:"
echo "   pytest tests/ -v"
echo ""
echo "7. Build Docker image:"
echo "   docker build -t heart-disease-api:latest ."
echo ""
echo "Documentation:"
echo "  - README.md for project overview"
echo "  - QUICK_START.md for detailed instructions"
echo ""
echo "Happy MLOps! 🚀"
echo ""
