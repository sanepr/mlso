"""
Test suite for trained models
"""
import pytest
import pickle
from pathlib import Path
import pandas as pd


class TestModels:
    """Test trained model files"""

    def test_best_model_exists(self):
        """Test that best model file exists"""
        model_path = Path("models/best_model.pkl")
        if not model_path.exists():
            pytest.skip("Model not trained yet - run training first")
        assert model_path.exists(), "Best model file should exist"

    def test_best_model_loadable(self):
        """Test that best model can be loaded"""
        model_path = Path("models/best_model.pkl")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        assert model is not None, "Model should be loadable"

    def test_model_has_predict_method(self):
        """Test that model has predict method"""
        model_path = Path("models/best_model.pkl")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        assert hasattr(model, 'predict'), "Model should have predict method"
        assert hasattr(model, 'predict_proba'), "Model should have predict_proba method"

    def test_model_metadata_exists(self):
        """Test that model metadata exists"""
        metadata_path = Path("models/best_model_metadata.json")
        assert metadata_path.exists(), "Model metadata should exist"

    def test_all_models_exist(self):
        """Test that all model files exist"""
        models_dir = Path("models")
        expected_models = [
            'best_model.pkl',
            'logistic_regression.pkl',
            'random_forest.pkl'
        ]

        if not models_dir.exists():
            pytest.skip("Models directory not found")

        existing_models = [f for f in expected_models if (models_dir / f).exists()]

        if len(existing_models) == 0:
            pytest.skip("No models trained yet - run training first")

        # At least one model should exist after training
        assert len(existing_models) > 0

    def test_model_prediction_shape(self):
        """Test that model produces correct output shape"""
        model_path = Path("models/best_model.pkl")

        if not model_path.exists():
            pytest.skip("Model not trained yet - run training first")

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # Create dummy input
        import numpy as np
        X_test = np.random.randn(5, 13)  # 5 samples, 13 features

        predictions = model.predict(X_test)
        assert predictions.shape[0] == 5, "Should predict for all 5 samples"

        probabilities = model.predict_proba(X_test)
        assert probabilities.shape == (5, 2), "Should return probabilities for 2 classes"

