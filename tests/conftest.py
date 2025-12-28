"""
Pytest configuration and fixtures
"""
import pytest
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory"""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def data_dir(project_root):
    """Return the data directory"""
    return project_root / 'data'


@pytest.fixture(scope="session")
def models_dir(project_root):
    """Return the models directory"""
    return project_root / 'models'


@pytest.fixture(scope="session")
def raw_data_path(data_dir):
    """Return path to raw data"""
    return data_dir / 'raw' / 'heart.csv'


@pytest.fixture(scope="session")
def processed_data_dir(data_dir):
    """Return path to processed data directory"""
    return data_dir / 'processed'


@pytest.fixture(scope="session")
def best_model_path(models_dir):
    """Return path to best model"""
    return models_dir / 'best_model.pkl'


@pytest.fixture(scope="session")
def model_metadata_path(models_dir):
    """Return path to model metadata"""
    return models_dir / 'best_model_metadata.json'


def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    # Add markers automatically based on test location
    for item in items:
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "unit" in item.nodeid or "test_" in item.nodeid:
            item.add_marker(pytest.mark.unit)

