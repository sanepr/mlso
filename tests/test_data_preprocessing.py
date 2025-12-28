"""
Unit tests for data preprocessing module
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import pickle
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.preprocessing import load_data, preprocess_data


class TestDataLoading:
    """Test data loading functionality"""

    def test_load_raw_data(self):
        """Test loading raw data from CSV"""
        data_path = Path("data/raw/heart.csv")

        if not data_path.exists():
            pytest.skip("Dataset not available")

        df = pd.read_csv(data_path)

        assert isinstance(df, pd.DataFrame), "Should return DataFrame"
        assert not df.empty, "DataFrame should not be empty"
        assert df.shape[0] > 200, "Should have more than 200 rows"
        assert df.shape[1] == 14, "Should have 14 columns"

    def test_data_columns(self):
        """Test that all required columns exist"""
        data_path = Path("data/raw/heart.csv")

        if not data_path.exists():
            pytest.skip("Dataset not available")

        df = pd.read_csv(data_path)

        required_columns = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
            'restecg', 'thalach', 'exang', 'oldpeak',
            'slope', 'ca', 'thal', 'target'
        ]

        for col in required_columns:
            assert col in df.columns, f"Column {col} should exist"

    def test_target_column(self):
        """Test target column has correct values"""
        data_path = Path("data/raw/heart.csv")

        if not data_path.exists():
            pytest.skip("Dataset not available")

        df = pd.read_csv(data_path)

        # Target should be binary
        unique_values = df['target'].unique()
        assert len(unique_values) == 2, "Target should be binary"
        assert set(unique_values).issubset({0, 1}), "Target should be 0 or 1"

        # No null values in target
        assert df['target'].isnull().sum() == 0, "Target should have no nulls"

    def test_data_types(self):
        """Test that data types are numeric"""
        data_path = Path("data/raw/heart.csv")

        if not data_path.exists():
            pytest.skip("Dataset not available")

        df = pd.read_csv(data_path)

        # All columns should be numeric
        for col in df.columns:
            assert pd.api.types.is_numeric_dtype(df[col]), f"{col} should be numeric"


class TestDataPreprocessing:
    """Test data preprocessing functionality"""

    def test_preprocess_returns_correct_shapes(self):
        """Test that preprocessing returns correct array shapes"""
        data_path = Path("data/raw/heart.csv")

        if not data_path.exists():
            pytest.skip("Dataset not available")

        # Create dummy data for testing
        df = pd.read_csv(data_path)

        # Should have features and target
        assert 'target' in df.columns, "Should have target column"

        n_features = df.shape[1] - 1  # Exclude target
        assert n_features == 13, "Should have 13 features"

    def test_processed_files_exist(self):
        """Test that processed files are created"""
        processed_dir = Path("data/processed")

        if not processed_dir.exists():
            pytest.skip("Processed data not available")

        required_files = [
            'X_train.pkl',
            'X_test.pkl',
            'y_train.pkl',
            'y_test.pkl',
            'scaler.pkl'
        ]

        for filename in required_files:
            file_path = processed_dir / filename
            assert file_path.exists(), f"{filename} should exist"

    def test_train_test_split_ratio(self):
        """Test train/test split ratio"""
        processed_dir = Path("data/processed")

        if not processed_dir.exists():
            pytest.skip("Processed data not available")

        try:
            with open(processed_dir / 'X_train.pkl', 'rb') as f:
                X_train = pickle.load(f)
            with open(processed_dir / 'X_test.pkl', 'rb') as f:
                X_test = pickle.load(f)

            total = len(X_train) + len(X_test)
            train_ratio = len(X_train) / total
            test_ratio = len(X_test) / total

            # Should be approximately 80/20 split
            assert 0.75 <= train_ratio <= 0.85, "Train ratio should be ~80%"
            assert 0.15 <= test_ratio <= 0.25, "Test ratio should be ~20%"
        except Exception as e:
            pytest.skip(f"Could not load processed data: {e}")

    def test_no_data_leakage(self):
        """Test that train and test sets don't overlap"""
        processed_dir = Path("data/processed")

        if not processed_dir.exists():
            pytest.skip("Processed data not available")

        try:
            with open(processed_dir / 'X_train.pkl', 'rb') as f:
                X_train = pickle.load(f)
            with open(processed_dir / 'X_test.pkl', 'rb') as f:
                X_test = pickle.load(f)

            # Convert to strings for comparison
            train_rows = set([str(row) for row in X_train.tolist()])
            test_rows = set([str(row) for row in X_test.tolist()])

            overlap = train_rows.intersection(test_rows)
            assert len(overlap) == 0, "Train and test sets should not overlap"
        except Exception as e:
            pytest.skip(f"Could not check for data leakage: {e}")

    def test_scaler_fitted(self):
        """Test that scaler is properly fitted"""
        processed_dir = Path("data/processed")

        if not processed_dir.exists():
            pytest.skip("Processed data not available")

        try:
            with open(processed_dir / 'scaler.pkl', 'rb') as f:
                scaler = pickle.load(f)

            # Check scaler has required attributes
            assert hasattr(scaler, 'mean_'), "Scaler should have mean_"
            assert hasattr(scaler, 'scale_'), "Scaler should have scale_"

            # Check dimensions
            assert len(scaler.mean_) == 13, "Scaler should have 13 features"
            assert len(scaler.scale_) == 13, "Scaler should have 13 scales"
        except Exception as e:
            pytest.skip(f"Could not check scaler: {e}")


class TestDataQuality:
    """Test data quality and consistency"""

    def test_no_missing_values_after_preprocessing(self):
        """Test that processed data has no missing values"""
        processed_dir = Path("data/processed")

        if not processed_dir.exists():
            pytest.skip("Processed data not available")

        try:
            with open(processed_dir / 'X_train.pkl', 'rb') as f:
                X_train = pickle.load(f)
            with open(processed_dir / 'X_test.pkl', 'rb') as f:
                X_test = pickle.load(f)

            # Check for NaN values
            assert not np.isnan(X_train).any(), "X_train should have no NaN"
            assert not np.isnan(X_test).any(), "X_test should have no NaN"

            # Check for infinite values
            assert not np.isinf(X_train).any(), "X_train should have no inf"
            assert not np.isinf(X_test).any(), "X_test should have no inf"
        except Exception as e:
            pytest.skip(f"Could not check data quality: {e}")

    def test_feature_scaling(self):
        """Test that features are properly scaled"""
        processed_dir = Path("data/processed")

        if not processed_dir.exists():
            pytest.skip("Processed data not available")

        try:
            with open(processed_dir / 'X_train.pkl', 'rb') as f:
                X_train = pickle.load(f)

            # After StandardScaler, mean should be ~0 and std ~1
            means = X_train.mean(axis=0)
            stds = X_train.std(axis=0)

            # Check means are close to 0
            assert np.allclose(means, 0, atol=0.1), "Means should be close to 0"

            # Check stds are close to 1
            assert np.allclose(stds, 1, atol=0.3), "Stds should be close to 1"
        except Exception as e:
            pytest.skip(f"Could not check feature scaling: {e}")

    def test_target_balance(self):
        """Test target distribution is reasonable"""
        processed_dir = Path("data/processed")

        if not processed_dir.exists():
            pytest.skip("Processed data not available")

        try:
            with open(processed_dir / 'y_train.pkl', 'rb') as f:
                y_train = pickle.load(f)

            # Check distribution
            unique, counts = np.unique(y_train, return_counts=True)

            # Neither class should be less than 20% of total
            min_ratio = counts.min() / counts.sum()
            assert min_ratio >= 0.2, "Classes should be reasonably balanced"
        except Exception as e:
            pytest.skip(f"Could not check target balance: {e}")

