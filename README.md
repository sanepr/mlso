# MLOps Heart Disease Prediction Project

[![CI/CD Pipeline](https://github.com/sanepr/mlso/actions/workflows/ml-pipeline.yml/badge.svg)](https://github.com/sanepr/mlso/actions/workflows/ml-pipeline.yml)

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

```bash
pytest tests/ -v --cov=src
```

## 🐳 Docker Build & Run

Build the container:
```bash
docker build -t heart-disease-api:latest .
```

Run locally:
```bash
docker run -p 8000:8000 heart-disease-api:latest
```

Test the API:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1}'
```

## ☸️ Kubernetes Deployment

Deploy to cluster:
```bash
kubectl apply -f deployment/kubernetes/
```

Check deployment:
```bash
kubectl get pods
kubectl get services
```

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
