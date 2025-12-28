# MLOps Heart Disease Prediction Project

[![CI/CD Pipeline](https://github.com/sanepr/mlso/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/sanepr/mlso/actions/workflows/ci-cd.yml)
[![Model Training](https://github.com/sanepr/mlso/actions/workflows/model-training.yml/badge.svg)](https://github.com/sanepr/mlso/actions/workflows/model-training.yml)
[![Tests](https://img.shields.io/badge/tests-60%20passed-brightgreen)](./tests/)
[![Coverage](https://img.shields.io/badge/coverage-70%25%2B-brightgreen)](./htmlcov/)
[![Python](https://img.shields.io/badge/python-3.10.11-blue)](https://www.python.org/)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Project Status](https://img.shields.io/badge/status-production%20ready-brightgreen)](./CI_CD_PIPELINE_SUMMARY.md)
[![Docker](https://img.shields.io/badge/docker-configured-blue)](./Dockerfile)
[![Kubernetes](https://img.shields.io/badge/kubernetes-ready-brightgreen)](./deployment/kubernetes/)

> **📊 Project Verified:** Complete CI/CD pipeline with 60 automated tests. See [CI/CD Summary](./CI_CD_PIPELINE_SUMMARY.md) for details.

## 📋 Project Overview

An end-to-end MLOps solution for predicting heart disease risk using the UCI Heart Disease dataset. This project demonstrates modern ML engineering practices including automated CI/CD, experiment tracking, containerization, and production deployment.

## 🎯 Objectives

- Build scalable ML classification models
- Implement automated CI/CD pipelines
- Track experiments with MLflow
- Deploy containerized API to cloud
- Monitor production model performance

## 📊 Dataset

**Heart Disease UCI Dataset**
- Source: UCI Machine Learning Repository
- Features: 14+ clinical features (age, sex, blood pressure, cholesterol, etc.)
- Target: Binary classification (presence/absence of heart disease)

## 🏗️ Project Structure

```
mlso/
├── data/
│   ├── raw/                    # Raw dataset files
│   ├── processed/              # Cleaned and processed data
│   └── download_data.py        # Data acquisition script
├── notebooks/
│   ├── 01_eda.ipynb           # Exploratory Data Analysis
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── preprocessing.py   # Data cleaning and preprocessing
│   ├── features/
│   │   ├── __init__.py
│   │   └── feature_engineering.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py          # Model training scripts
│   │   └── predict.py        # Prediction logic
│   └── api/
│       ├── __init__.py
│       └── app.py            # FastAPI application
├── tests/
│   ├── __init__.py
│   ├── test_preprocessing.py
│   ├── test_features.py
│   └── test_model.py
├── deployment/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   └── monitoring/
│       ├── prometheus.yml
│       └── grafana-dashboard.json
├── .github/
│   └── workflows/
│       └── ml-pipeline.yml    # CI/CD pipeline
├── models/                     # Saved model artifacts
├── screenshots/                # Documentation screenshots
├── mlruns/                     # MLflow tracking
├── .gitignore
├── requirements.txt
├── setup.py
├── Dockerfile
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Docker
- Kubernetes (Minikube/Docker Desktop) or cloud account
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sanepr/mlso.git
cd mlso
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download dataset:
```bash
python data/download_data.py
```

## 📈 Experiment Tracking

Start MLflow UI:
```bash
mlflow ui
```

Access at: http://localhost:5000

## 🧪 Running Tests

### Quick Test Run
```bash
# Run all tests with comprehensive report
./run_tests.sh
```

### Manual Testing
```bash
# Run all tests
pytest tests/ -v --cov=src

# Run specific test suite
pytest tests/test_data_preprocessing.py -v
pytest tests/test_model_training.py -v
pytest tests/test_api_infrastructure.py -v

# Run with coverage report
pytest tests/ -v --cov=src --cov-report=html --cov-report=term

# Run with specific markers
pytest tests/ -m unit
pytest tests/ -m "not slow"
```

### Test Coverage
- **Total Tests:** 60 comprehensive test cases
- **Coverage Target:** ≥70%
- **Test Suites:**
  - Data Processing (18 tests)
  - Model Training (20 tests)
  - API Infrastructure (22 tests)

**Reports Generated:**
- HTML coverage report: `htmlcov/index.html`
- Test report: `test-report.html`
- Coverage XML: `coverage.xml`

## 🔄 CI/CD Pipeline

### Automated Workflows

**CI/CD Pipeline** (`.github/workflows/ci-cd.yml`):
- **Lint:** Code quality checks (flake8, pylint, black, isort)
- **Test:** Unit tests with coverage (≥70%)
- **Train:** Model training and validation
- **Build:** Docker image creation
- **Report:** Pipeline summary generation

**Model Training Pipeline** (`.github/workflows/model-training.yml`):
- **Schedule:** Weekly retraining (Sundays at midnight)
- **Validation:** Performance threshold checks (Accuracy ≥70%, ROC-AUC ≥75%)
- **Artifacts:** Trained models, MLflow logs, training reports

### Running CI/CD Locally

```bash
# Run linting
flake8 src tests
pylint src
black --check src tests
isort --check-only src tests

# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run comprehensive test suite
./run_tests.sh
```

### Pipeline Features
- ✅ Automated testing on every push/PR
- ✅ Code quality enforcement
- ✅ Model performance validation
- ✅ Docker image building and testing
- ✅ Artifact storage (90 days for models)
- ✅ PR comments with test results

**📚 Complete CI/CD Documentation:** [CI_CD_DOCUMENTATION.md](./CI_CD_DOCUMENTATION.md)

## 🐳 Docker Build & Run

> **⚠️ IMPORTANT:** Docker Desktop must be installed and **running** before using Docker commands!

### Prerequisites
- ✅ Docker Desktop installed and **RUNNING** (whale icon in menu bar should be static)
- ✅ Models trained (run `python src/models/train.py` first)

### Quick Start (Recommended)
```bash
# Use the automated helper script (checks Docker, builds, and optionally runs)
./docker_start.sh

# Or use the test script
./test_docker.sh
```

### Manual Build & Run

Build the container:
```bash
docker build -t heart-disease-api:latest .
```

Run locally:
```bash
# Clean up any existing containers
docker stop heart-disease-api 2>/dev/null || true
docker rm heart-disease-api 2>/dev/null || true

# Run the container
docker run -d -p 8000:8000 --name heart-disease-api heart-disease-api:latest

# Check logs
docker logs -f heart-disease-api
```

Test the API:
```bash
# Health check
curl http://localhost:8000/health

# Prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @test_sample.json

# Or inline
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1}'
```

### Troubleshooting

#### ❌ Error: "Cannot connect to the Docker daemon"
**This means Docker Desktop is not running!**

**Solution:**
1. **Open Docker Desktop application** (search in Spotlight/Applications)
2. Wait for Docker to fully start (whale icon in menu bar should stop animating)
3. Verify Docker is running:
   ```bash
   docker info
   ```
4. If successful, you'll see Docker information. Now retry your command.

**Quick Check:**
```bash
# This should return version info, not an error
docker --version
docker info
```

**📚 See detailed guides:**
- [DOCKER_QUICK_FIX.md](./DOCKER_QUICK_FIX.md) - 3-step visual guide
- [DOCKER_DAEMON_FIX.md](./DOCKER_DAEMON_FIX.md) - Complete troubleshooting

#### Other Issues
See [DOCKER_FIX.md](DOCKER_FIX.md) for detailed troubleshooting guide.

## ☸️ Kubernetes Deployment

> **⚠️ CRITICAL:** Docker Desktop MUST be running before Kubernetes deployment!  
> Kubernetes uses Docker to run containers. Without Docker, deployment will fail.

### Prerequisites
- ✅ **Docker Desktop installed and RUNNING** (whale icon in menu bar must be static)
- ✅ Minikube binary available (`minikube-darwin-arm64` included in project)
- ✅ Docker image built (`docker build -t heart-disease-api:latest .`)

### Quick Start (Recommended)
```bash
# Automated deployment
./deploy_k8s.sh
```

This will:
- Start minikube if needed
- Load Docker image
- Deploy to Kubernetes
- Test endpoints

### Manual Deployment

**Step 1: Start Minikube**
```bash
./minikube-darwin-arm64 start --driver=docker
```

**Step 2: Load Image**
```bash
./minikube-darwin-arm64 image load heart-disease-api:latest
```

**Step 3: Deploy**
```bash
# Using minikube's kubectl
./minikube-darwin-arm64 kubectl -- apply -f deployment/kubernetes/

# Or use the wrapper
./kubectl.sh apply -f deployment/kubernetes/
```

**Step 4: Check Status**
```bash
./kubectl.sh get pods
./kubectl.sh get services
```

**Step 5: Access Service**
```bash
# Get service URL
./minikube-darwin-arm64 service heart-disease-api --url

# Or use port forwarding
./kubectl.sh port-forward svc/heart-disease-api 8080:8000
```

### Access Your Deployment

After successful deployment, access your API:

#### Option 1: Direct NodePort (Easiest)
```bash
# Get the URL
./get_k8s_url.sh

# Or manually construct: http://<MINIKUBE_IP>:30080
curl http://192.168.49.2:30080/health
```

#### Option 2: Port Forward
```bash
./minikube-darwin-arm64 kubectl -- port-forward svc/heart-disease-api 8080:8000
# Access at http://localhost:8080
```

#### Option 3: Minikube Service
```bash
./minikube-darwin-arm64 service heart-disease-api
# Opens browser with service URL
```

**📚 Complete access guide:** [MINIKUBE_ACCESS_GUIDE.md](./MINIKUBE_ACCESS_GUIDE.md)

### Troubleshooting

#### ❌ Error: "Docker daemon is not running"
**Kubernetes requires Docker Desktop to be running!**

**Quick Fix:**
1. Open Docker Desktop application
2. Wait for whale icon to stop animating (30-60 seconds)
3. Verify: `docker info`
4. Retry: `./deploy_k8s.sh`

**📚 Detailed guides:**
- [K8S_DOCKER_NOT_RUNNING.md](./K8S_DOCKER_NOT_RUNNING.md) - Complete Docker fix guide
- [K8S_SETUP_SUMMARY.md](./K8S_SETUP_SUMMARY.md) - Full Kubernetes troubleshooting

#### Other Issues
See [K8S_SETUP_SUMMARY.md](K8S_SETUP_SUMMARY.md) for complete guide and troubleshooting.

## 📊 Monitoring

Access Prometheus: http://localhost:9090
Access Grafana: http://localhost:3000

## 📝 Model Training

```bash
python src/models/train.py
```

## 🔄 CI/CD Pipeline

The GitHub Actions pipeline automatically:
- Runs linting and code quality checks
- Executes unit tests
- Trains and validates models
- Builds Docker images
- Deploys to staging/production

## 📄 Documentation

Detailed documentation available in `docs/REPORT.md`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📧 Contact

Your Name - sanepr

Project Link: [https://github.com/sanepr/mlso](https://github.com/sanepr/mlso)

## 📜 License

This project is for educational purposes as part of MLOps coursework.
