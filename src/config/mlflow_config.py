"""
MLflow Configuration for Development and Production

This module provides centralized MLflow configuration that works across
different environments (local development, CI/CD, production).

Features:
- Environment-based configuration (dev/staging/prod)
- Support for local and remote tracking servers
- AWS S3, Azure Blob, or GCS artifact storage
- PostgreSQL/MySQL backend store for production
- Automatic fallback to local storage in development

Usage:
    from src.config.mlflow_config import get_mlflow_config

    config = get_mlflow_config()
    mlflow.set_tracking_uri(config['tracking_uri'])
    mlflow.set_experiment(config['experiment_name'])
"""

import os
from pathlib import Path
from typing import Dict
from urllib.parse import quote_plus


def get_environment() -> str:
    """
    Determine current environment.

    Returns:
        Environment name: 'development', 'staging', or 'production'
    """
    return os.getenv('MLFLOW_ENV', 'development').lower()


def get_mlflow_config() -> Dict[str, str]:
    """
    Get MLflow configuration based on environment.

    Returns:
        Dictionary with MLflow configuration:
        - tracking_uri: MLflow tracking server URI
        - artifact_location: Artifact storage location
        - experiment_name: Default experiment name
        - backend_store_uri: Backend store for metadata (production)

    Environment Variables:
        MLFLOW_ENV: Environment (development/staging/production)
        MLFLOW_TRACKING_URI: Remote tracking server URI
        MLFLOW_S3_BUCKET: S3 bucket for artifacts (e.g., s3://my-bucket/mlflow)
        MLFLOW_AZURE_CONTAINER: Azure container (e.g., wasbs://container@account.blob.core.windows.net/mlflow)
        MLFLOW_GCS_BUCKET: GCS bucket (e.g., gs://my-bucket/mlflow)
        MLFLOW_DB_URI: Database URI for backend store (PostgreSQL/MySQL)
        MLFLOW_EXPERIMENT_NAME: Custom experiment name
    """
    env = get_environment()
    project_root = Path(__file__).resolve().parents[2]

    # Base configuration
    config = {
        'environment': env,
        'experiment_name': os.getenv('MLFLOW_EXPERIMENT_NAME', 'heart-disease-prediction'),
    }

    if env == 'production':
        config.update(_get_production_config(project_root))
    elif env == 'staging':
        config.update(_get_staging_config(project_root))
    else:  # development
        config.update(_get_development_config(project_root))

    return config


def _get_development_config(project_root: Path) -> Dict[str, str]:
    """Development environment configuration (local MLflow)."""
    return {
        'tracking_uri': f"file://{project_root}/mlruns",
        'artifact_location': f"{project_root}/mlruns",
        'backend_store_uri': None,
    }


def _get_staging_config(project_root: Path) -> Dict[str, str]:
    """
    Staging environment configuration.

    Can use either:
    1. Remote MLflow server with cloud storage
    2. Local storage with database backend
    """
    tracking_uri = os.getenv('MLFLOW_TRACKING_URI')

    if tracking_uri:
        # Remote MLflow server
        return {
            'tracking_uri': tracking_uri,
            'artifact_location': _get_artifact_location(),
            'backend_store_uri': os.getenv('MLFLOW_DB_URI'),
        }
    else:
        # Fallback to local with database
        db_uri = os.getenv('MLFLOW_DB_URI', f'sqlite:///{project_root}/mlflow.db')
        return {
            'tracking_uri': db_uri,
            'artifact_location': f"{project_root}/mlruns",
            'backend_store_uri': db_uri,
        }


def _get_production_config(project_root: Path) -> Dict[str, str]:
    """
    Production environment configuration.

    Requires:
    - Remote MLflow tracking server OR database backend
    - Cloud storage for artifacts (S3/Azure/GCS)
    """
    tracking_uri = os.getenv('MLFLOW_TRACKING_URI')

    if not tracking_uri:
        # Use database as tracking server
        db_uri = os.getenv('MLFLOW_DB_URI')
        if not db_uri:
            raise ValueError(
                "Production environment requires MLFLOW_TRACKING_URI or MLFLOW_DB_URI. "
                "Please set one of these environment variables."
            )
        tracking_uri = db_uri

    artifact_location = _get_artifact_location()

    return {
        'tracking_uri': tracking_uri,
        'artifact_location': artifact_location,
        'backend_store_uri': os.getenv('MLFLOW_DB_URI'),
    }


def _get_artifact_location() -> str:
    """
    Determine artifact storage location.

    Priority:
    1. AWS S3
    2. Azure Blob Storage
    3. Google Cloud Storage
    4. Local filesystem (fallback)
    """
    # AWS S3
    s3_bucket = os.getenv('MLFLOW_S3_BUCKET')
    if s3_bucket:
        return s3_bucket if s3_bucket.startswith('s3://') else f's3://{s3_bucket}'

    # Azure Blob Storage
    azure_container = os.getenv('MLFLOW_AZURE_CONTAINER')
    if azure_container:
        return azure_container

    # Google Cloud Storage
    gcs_bucket = os.getenv('MLFLOW_GCS_BUCKET')
    if gcs_bucket:
        return gcs_bucket if gcs_bucket.startswith('gs://') else f'gs://{gcs_bucket}'

    # Fallback to local
    project_root = Path(__file__).resolve().parents[2]
    return f"{project_root}/mlruns"


def get_database_uri(db_type: str = 'postgresql') -> str:
    """
    Construct database URI from environment variables.

    Args:
        db_type: Database type ('postgresql' or 'mysql')

    Environment Variables:
        MLFLOW_DB_HOST: Database host
        MLFLOW_DB_PORT: Database port
        MLFLOW_DB_NAME: Database name
        MLFLOW_DB_USER: Database user
        MLFLOW_DB_PASSWORD: Database password

    Returns:
        Database URI string
    """
    host = os.getenv('MLFLOW_DB_HOST', 'localhost')
    port = os.getenv('MLFLOW_DB_PORT', '5432' if db_type == 'postgresql' else '3306')
    db_name = os.getenv('MLFLOW_DB_NAME', 'mlflow')
    user = os.getenv('MLFLOW_DB_USER', 'mlflow')
    password = os.getenv('MLFLOW_DB_PASSWORD', '')

    if not password:
        raise ValueError("MLFLOW_DB_PASSWORD environment variable is required")

    # URL encode password to handle special characters
    encoded_password = quote_plus(password)

    if db_type == 'postgresql':
        return f"postgresql://{user}:{encoded_password}@{host}:{port}/{db_name}"
    elif db_type == 'mysql':
        return f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{db_name}"
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def print_config():
    """Print current MLflow configuration for debugging."""
    config = get_mlflow_config()
    print("\n" + "="*80)
    print("MLFLOW CONFIGURATION")
    print("="*80)
    print(f"Environment: {config['environment']}")
    print(f"Tracking URI: {config['tracking_uri']}")
    print(f"Artifact Location: {config.get('artifact_location', 'N/A')}")
    print(f"Backend Store: {config.get('backend_store_uri', 'N/A')}")
    print(f"Experiment Name: {config['experiment_name']}")
    print("="*80 + "\n")


if __name__ == "__main__":
    # Test configuration
    print_config()

