# 🚀 Quick Start Guide

This guide will help you set up and run the Heart Disease Prediction MLOps project.

## 📋 Prerequisites

- Python 3.9+
- Git
- Docker (for containerization)
- kubectl (for Kubernetes deployment)

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sanepr/mlso.git
cd mlso
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Download and Prepare Data

```bash
# Download the Heart Disease dataset
python src/data/download_data.py

# Preprocess the data
python src/data/preprocessing.py
```

### 5. Run Exploratory Data Analysis

```bash
# Start Jupyter Notebook (choose one of the following methods)

# Method 1: Using jupyter notebook directly
jupyter notebook

# Method 2: Using JupyterLab (modern interface)
jupyter lab

# Method 3: If jupyter command not found, use Python module
python -m notebook

# Method 4: Direct path to virtual environment
./venv/bin/jupyter notebook

# Open and run:
# - notebooks/01_eda.ipynb
# - notebooks/02_model_training.ipynb
```

### 6. Train Models

```bash
# Train models with MLflow tracking
python src/models/train.py

# View MLflow UI
mlflow ui
# Access at: http://localhost:5000
```

### 7. Test the API Locally

```bash
# Run Flask API
python src/api/app.py

# In another terminal, test the API:
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63,
    "sex": 1,
    "cp": 3,
    "trestbps": 145,
    "chol": 233,
    "fbs": 1,
    "restecg": 0,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 2.3,
    "slope": 0,
    "ca": 0,
    "thal": 1
  }'
```

### 8. Run Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html  # On Mac
# or
start htmlcov/index.html  # On Windows
```

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t heart-disease-api:latest .
```

### Run Docker Container

```bash
docker run -p 5000:5000 heart-disease-api:latest
```

### Using Docker Compose

```bash
cd deployment
docker-compose up -d

# Services will be available at:
# - API: http://localhost:5000
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
```

## ☸️ Kubernetes Deployment

### Using Minikube (Local)

```bash
# Start Minikube
minikube start

# Load Docker image into Minikube
minikube image load heart-disease-api:latest

# Deploy to Kubernetes
kubectl apply -f deployment/kubernetes/deployment.yaml
kubectl apply -f deployment/kubernetes/service.yaml

# Check deployment status
kubectl get pods
kubectl get services

# Access the service
minikube service heart-disease-api-service
```

### Using Cloud Kubernetes (GKE/EKS/AKS)

```bash
# Push image to container registry
docker tag heart-disease-api:latest <your-registry>/heart-disease-api:latest
docker push <your-registry>/heart-disease-api:latest

# Update deployment.yaml with your image path

# Deploy
kubectl apply -f deployment/kubernetes/deployment.yaml
kubectl apply -f deployment/kubernetes/service.yaml

# Get external IP
kubectl get service heart-disease-api-service
```

## 📊 Monitoring

### Prometheus Metrics

Access metrics at: `http://localhost:5000/metrics`

### Grafana Dashboard

1. Access Grafana: `http://localhost:3000`
2. Login: admin/admin
3. Add Prometheus data source: `http://prometheus:9090`
4. Import dashboard from `monitoring/grafana_dashboard.json`

## 🧪 CI/CD Pipeline

The GitHub Actions workflow automatically runs on push/PR:

1. **Linting**: Checks code quality with flake8 and black
2. **Testing**: Runs unit tests with pytest
3. **Training**: Validates model training pipeline
4. **Docker**: Builds Docker image

View workflow runs at: https://github.com/sanepr/mlso/actions

## 📁 Project Structure Overview

```
mlso/
├── src/                  # Source code
│   ├── data/            # Data processing scripts
│   ├── models/          # Model training & inference
│   ├── features/        # Feature engineering
│   └── api/             # Flask API
├── tests/               # Unit tests
├── notebooks/           # Jupyter notebooks for EDA
├── deployment/          # Docker & Kubernetes configs
├── monitoring/          # Prometheus & Grafana configs
└── config/              # Configuration files
```

## 📝 API Endpoints

- **GET /** - Health check
- **GET /health** - Detailed health status
- **POST /predict** - Single prediction
- **POST /predict/batch** - Batch predictions
- **GET /metrics** - Prometheus metrics
- **GET /model/info** - Model information

## 🔍 Example API Usage

### Single Prediction

```python
import requests

url = "http://localhost:5000/predict"
data = {
    "age": 63,
    "sex": 1,
    "cp": 3,
    "trestbps": 145,
    "chol": 233,
    "fbs": 1,
    "restecg": 0,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 2.3,
    "slope": 0,
    "ca": 0,
    "thal": 1
}

response = requests.post(url, json=data)
print(response.json())
```

### Batch Prediction

```python
import requests

url = "http://localhost:5000/predict/batch"
data = {
    "data": [
        {"age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1},
        {"age": 67, "sex": 1, "cp": 4, "trestbps": 160, "chol": 286, "fbs": 0, "restecg": 2, "thalach": 108, "exang": 1, "oldpeak": 1.5, "slope": 2, "ca": 3, "thal": 3}
    ]
}

response = requests.post(url, json=data)
print(response.json())
```

## 🐛 Troubleshooting

### Issue: Jupyter command not found

**Solution**: Make sure Jupyter is installed and your virtual environment is activated:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # On Mac/Linux
# or
venv\Scripts\activate  # On Windows

# Install/reinstall Jupyter
pip install jupyter notebook ipykernel

# Try alternative commands
python -m notebook
# or
jupyter lab
```

### Issue: Model not found

**Solution**: Make sure you've run the training script first:
```bash
python src/models/train.py
```

### Issue: Port already in use

**Solution**: Kill the process using the port:
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: Docker build fails

**Solution**: Ensure all required files are present and try rebuilding without cache:
```bash
docker build --no-cache -t heart-disease-api:latest .
```

## 📚 Additional Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Contact

**Author**: sanepr
**Repository**: https://github.com/sanepr/mlso

---

**Happy MLOps! 🚀**
