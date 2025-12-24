from setuptools import setup, find_packages

setup(
    name="mlso",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.3",
        "pandas>=2.0.3",
        "scikit-learn>=1.3.0",
        "mlflow>=2.7.1",
        "fastapi>=0.103.1",
        "uvicorn>=0.23.2",
    ],
    author="sanepr",
    description="MLOps Heart Disease Prediction Project",
    python_requires=">=3.9",
)
