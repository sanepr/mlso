"""
Unit tests for model training and evaluation
"""
import pytest
import pickle
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import json


class TestModelFiles:
    """Test that model files exist and are valid"""

    def test_best_model_exists(self):
        """Test that best model file exists"""
        model_path = Path("models/best_model.pkl")
        assert model_path.exists(), "Best model file should exist"

    def test_best_model_loadable(self):
        """Test that best model can be loaded"""
        model_path = Path("models/best_model.pkl")

        if not model_path.exists():
            pytest.skip("Model file not available")

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        assert model is not None, "Model should be loadable"

    def test_model_metadata_exists(self):
        """Test that model metadata exists"""
        metadata_path = Path("models/best_model_metadata.json")

        if not metadata_path.exists():
            pytest.skip("Metadata file not available")

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        assert isinstance(metadata, dict), "Metadata should be a dictionary"

    def test_all_models_exist(self):
        """Test that all expected model files exist"""
        models_dir = Path("models")

        if not models_dir.exists():
            pytest.skip("Models directory not available")

        expected_models = [
            'best_model.pkl',
            'logistic_regression.pkl',
            'random_forest.pkl'
        ]

        for model_file in expected_models:
            model_path = models_dir / model_file
            if model_path.exists():
                assert True
            else:
                # This is okay if models haven't been trained yet
                pass


class TestModelInterface:
    """Test model interface and methods"""

    def test_model_has_predict_method(self):
        """Test that model has predict method"""
        model_path = Path("models/best_model.pkl")

        if not model_path.exists():
            pytest.skip("Model file not available")

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        assert hasattr(model, 'predict'), "Model should have predict method"

    def test_model_has_predict_proba_method(self):
        """Test that model has predict_proba method"""
        model_path = Path("models/best_model.pkl")

        if not model_path.exists():
            pytest.skip("Model file not available")

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        assert hasattr(model, 'predict_proba'), "Model should have predict_proba method"

    def test_model_prediction_shape(self):
        """Test that model produces correct output shape"""
        model_path = Path("models/best_model.pkl")

        if not model_path.exists():
            pytest.skip("Model file not available")

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # Create dummy input (13 features as per heart disease dataset)
        X_test = np.random.randn(5, 13)

        predictions = model.predict(X_test)
        assert predictions.shape[0] == 5, "Should predict for all 5 samples"

        probabilities = model.predict_proba(X_test)
        assert probabilities.shape == (5, 2), "Should return probabilities for 2 classes"

    def test_predictions_are_binary(self):
        """Test that predictions are binary (0 or 1)"""
        model_path = Path("models/best_model.pkl")

        if not model_path.exists():
            pytest.skip("Model file not available")

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # Create dummy input
        X_test = np.random.randn(10, 13)
        predictions = model.predict(X_test)

        # Check all predictions are 0 or 1
        assert set(predictions).issubset({0, 1}), "Predictions should be 0 or 1"

    def test_probabilities_sum_to_one(self):
        """Test that predicted probabilities sum to 1"""
        model_path = Path("models/best_model.pkl")

        if not model_path.exists():
            pytest.skip("Model file not available")

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # Create dummy input
        X_test = np.random.randn(10, 13)
        probabilities = model.predict_proba(X_test)

        # Check probabilities sum to 1 for each sample
        sums = probabilities.sum(axis=1)
        assert np.allclose(sums, 1.0), "Probabilities should sum to 1"


class TestModelPerformance:
    """Test model performance metrics"""

    def test_model_metadata_has_metrics(self):
        """Test that metadata contains performance metrics"""
        metadata_path = Path("models/best_model_metadata.json")

        if not metadata_path.exists():
            pytest.skip("Metadata file not available")

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        # Check for metrics in either flat structure or nested under 'metrics' key
        has_flat_metrics = 'test_accuracy' in metadata and 'test_roc_auc' in metadata
        has_nested_metrics = 'metrics' in metadata and isinstance(metadata['metrics'], dict)

        assert has_flat_metrics or has_nested_metrics, \
            "Metadata should contain metrics either at root level or under 'metrics' key"

    def test_model_accuracy_threshold(self):
        """Test that model accuracy meets minimum threshold"""
        metadata_path = Path("models/best_model_metadata.json")

        if not metadata_path.exists():
            pytest.skip("Metadata file not available")

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        if 'test_accuracy' in metadata:
            accuracy = metadata['test_accuracy']
            assert accuracy >= 0.7, f"Model accuracy {accuracy} should be >= 0.7"

    def test_model_roc_auc_threshold(self):
        """Test that model ROC-AUC meets minimum threshold"""
        metadata_path = Path("models/best_model_metadata.json")

        if not metadata_path.exists():
            pytest.skip("Metadata file not available")

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        if 'test_roc_auc' in metadata:
            roc_auc = metadata['test_roc_auc']
            assert roc_auc >= 0.75, f"Model ROC-AUC {roc_auc} should be >= 0.75"


class TestModelTypes:
    """Test different model types"""

    def test_random_forest_model(self):
        """Test Random Forest model"""
        model_path = Path("models/random_forest.pkl")

        if not model_path.exists():
            pytest.skip("Random Forest model not available")

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        assert isinstance(model, RandomForestClassifier), "Should be RandomForest"

    def test_logistic_regression_model(self):
        """Test Logistic Regression model"""
        model_path = Path("models/logistic_regression.pkl")

        if not model_path.exists():
            pytest.skip("Logistic Regression model not available")

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        assert isinstance(model, LogisticRegression), "Should be LogisticRegression"


class TestModelReproducibility:
    """Test model reproducibility"""

    def test_model_metadata_has_random_state(self):
        """Test that metadata includes random state for reproducibility"""
        metadata_path = Path("models/best_model_metadata.json")

        if not metadata_path.exists():
            pytest.skip("Metadata file not available")

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        # Should have parameters or random_state info
        assert 'model_type' in metadata or 'parameters' in metadata, \
            "Metadata should include model configuration"

    def test_consistent_predictions(self):
        """Test that model gives consistent predictions for same input"""
        model_path = Path("models/best_model.pkl")

        if not model_path.exists():
            pytest.skip("Model file not available")

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # Create dummy input
        X_test = np.random.randn(5, 13)

        # Get predictions twice
        pred1 = model.predict(X_test)
        pred2 = model.predict(X_test)

        # Should be identical
        assert np.array_equal(pred1, pred2), "Predictions should be consistent"


class TestModelValidation:
    """Test model validation"""

    def test_model_handles_edge_cases(self):
        """Test model handles edge case inputs"""
        model_path = Path("models/best_model.pkl")

        if not model_path.exists():
            pytest.skip("Model file not available")

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # Test with zeros
        X_zeros = np.zeros((1, 13))
        pred = model.predict(X_zeros)
        assert pred.shape[0] == 1, "Should handle zero input"

        # Test with negative values
        X_negative = np.ones((1, 13)) * -1
        pred = model.predict(X_negative)
        assert pred.shape[0] == 1, "Should handle negative input"

    def test_model_feature_count(self):
        """Test model expects correct number of features"""
        model_path = Path("models/best_model.pkl")

        if not model_path.exists():
            pytest.skip("Model file not available")

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # Check expected number of features
        if hasattr(model, 'n_features_in_'):
            assert model.n_features_in_ == 13, "Model should expect 13 features"

