"""
Test suite for data preprocessing module
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path


class TestDataPreprocessing:
    """Test data preprocessing functions"""

    def test_data_loading(self):
        """Test that data can be loaded"""
        data_path = Path("data/raw/heart.csv")
        assert data_path.exists(), "Dataset file should exist"

        df = pd.read_csv(data_path)
        assert not df.empty, "Dataset should not be empty"
        assert df.shape[0] > 0, "Dataset should have rows"
        assert df.shape[1] > 0, "Dataset should have columns"

    def test_data_shape(self):
        """Test dataset has expected shape"""
        df = pd.read_csv("data/raw/heart.csv")
        assert df.shape[1] == 14, "Dataset should have 14 columns"
        assert df.shape[0] > 200, "Dataset should have more than 200 rows"

    def test_required_columns(self):
        """Test that all required columns exist"""
        df = pd.read_csv("data/raw/heart.csv")
        required_cols = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                        'restecg', 'thalach', 'exang', 'oldpeak',
                        'slope', 'ca', 'thal', 'target']

        for col in required_cols:
            assert col in df.columns, f"Column {col} should exist"

    def test_target_values(self):
        """Test target column has binary values"""
        df = pd.read_csv("data/raw/heart.csv")
        unique_targets = df['target'].unique()
        assert len(unique_targets) == 2, "Target should be binary"
        assert set(unique_targets).issubset({0, 1}), "Target should be 0 or 1"

    def test_no_null_in_target(self):
        """Test target column has no null values"""
        df = pd.read_csv("data/raw/heart.csv")
        assert df['target'].isnull().sum() == 0, "Target should have no null values"


class TestProcessedData:
    """Test processed data files"""

    def test_processed_files_exist(self):
        """Test that processed data files exist"""
        processed_dir = Path("data/processed")
        assert processed_dir.exists(), "Processed data directory should exist"

        required_files = ['X_train.pkl', 'X_test.pkl', 'y_train.pkl', 'y_test.pkl']
        for file in required_files:
            file_path = processed_dir / file
            assert file_path.exists(), f"{file} should exist in processed directory"

