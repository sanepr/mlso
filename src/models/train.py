"""
Model Training Script with MLflow Tracking

This script trains and evaluates machine learning models (Logistic Regression and Random Forest)
with comprehensive hyperparameter tuning, cross-validation, and MLflow experiment tracking.

Features:
- Loads preprocessed data from data/processed/
- Hyperparameter tuning using GridSearchCV
- Cross-validation for robust model evaluation
- MLflow tracking for experiments, parameters, and metrics
- Comprehensive evaluation metrics (accuracy, precision, recall, F1, ROC-AUC)
- Model comparison and selection
- Saves best model to models/ directory

Author: sanepr
Date: 2025-12-24
"""

import sys
import pickle
import json
import warnings
from pathlib import Path
from typing import Dict, Tuple, Any

import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn
import mlflow.data
from mlflow.data.pandas_dataset import PandasDataset
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

# Import MLflow configuration
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.config.mlflow_config import get_mlflow_config, print_config

warnings.filterwarnings('ignore')

# Configure paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def setup_mlflow():
    """Initialize MLflow tracking with environment-aware configuration."""
    config = get_mlflow_config()
    mlflow.set_tracking_uri(config['tracking_uri'])
    mlflow.set_experiment(config['experiment_name'])

    # Print configuration for visibility
    print_config()


def load_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, pd.DataFrame, pd.DataFrame]:
    """
    Load preprocessed training and testing data.
    
    Returns:
        Tuple of (X_train, X_test, y_train, y_test, X_train_df, X_test_df)
    """
    print("\n" + "="*80)
    print("LOADING PREPROCESSED DATA")
    print("="*80)
    
    try:
        # Load pickle files (pandas DataFrames/Series)
        X_train_df = pd.read_pickle(DATA_DIR / "X_train.pkl")
        X_test_df = pd.read_pickle(DATA_DIR / "X_test.pkl")
        y_train_series = pd.read_pickle(DATA_DIR / "y_train.pkl")
        y_test_series = pd.read_pickle(DATA_DIR / "y_test.pkl")

        # Convert to numpy arrays for model training
        X_train = X_train_df.values
        X_test = X_test_df.values
        y_train = y_train_series.values
        y_test = y_test_series.values

        print(f"✓ Training set: {X_train.shape[0]} samples, {X_train.shape[1]} features")
        print(f"✓ Test set: {X_test.shape[0]} samples")
        print(f"✓ Class distribution (train): {np.bincount(y_train.astype(int))}")
        print(f"✓ Class distribution (test): {np.bincount(y_test.astype(int))}")
        
        return X_train, X_test, y_train, y_test, X_train_df, X_test_df

    except FileNotFoundError as e:
        print(f"✗ Error: Preprocessed data not found in {DATA_DIR}")
        print("  Please run the preprocessing script first:")
        print("  python src/data/preprocessing.py")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        print("  Please ensure preprocessing completed successfully.")
        sys.exit(1)


def get_logistic_regression_params() -> Dict:
    """Define hyperparameter grid for Logistic Regression."""
    return {
        'C': [0.001, 0.01, 0.1, 1, 10, 100],
        'penalty': ['l1', 'l2'],
        'solver': ['liblinear', 'saga'],
        'max_iter': [1000],
        'class_weight': [None, 'balanced']
    }


def get_random_forest_params() -> Dict:
    """Define hyperparameter grid for Random Forest."""
    return {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2'],
        'class_weight': [None, 'balanced']
    }


def evaluate_model(
    model,
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray
) -> Dict[str, float]:
    """
    Evaluate model and compute comprehensive metrics.
    
    Args:
        model: Trained model
        X_train: Training features
        X_test: Test features
        y_train: Training labels
        y_test: Test labels
    
    Returns:
        Dictionary of evaluation metrics
    """
    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Probability predictions for ROC-AUC
    y_train_proba = model.predict_proba(X_train)[:, 1]
    y_test_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    metrics = {
        # Training metrics
        'train_accuracy': accuracy_score(y_train, y_train_pred),
        'train_precision': precision_score(y_train, y_train_pred, average='weighted', zero_division=0),
        'train_recall': recall_score(y_train, y_train_pred, average='weighted', zero_division=0),
        'train_f1': f1_score(y_train, y_train_pred, average='weighted', zero_division=0),
        'train_roc_auc': roc_auc_score(y_train, y_train_proba),
        
        # Test metrics
        'test_accuracy': accuracy_score(y_test, y_test_pred),
        'test_precision': precision_score(y_test, y_test_pred, average='weighted', zero_division=0),
        'test_recall': recall_score(y_test, y_test_pred, average='weighted', zero_division=0),
        'test_f1': f1_score(y_test, y_test_pred, average='weighted', zero_division=0),
        'test_roc_auc': roc_auc_score(y_test, y_test_proba)
    }
    
    return metrics


def cross_validate_model(
    model,
    X: np.ndarray,
    y: np.ndarray,
    cv: int = 5
) -> Dict[str, float]:
    """
    Perform cross-validation and return mean scores.
    
    Args:
        model: Model to evaluate
        X: Features
        y: Labels
        cv: Number of cross-validation folds
    
    Returns:
        Dictionary of cross-validation metrics
    """
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    
    cv_metrics = {
        'cv_accuracy': cross_val_score(model, X, y, cv=skf, scoring='accuracy').mean(),
        'cv_precision': cross_val_score(model, X, y, cv=skf, scoring='precision_weighted').mean(),
        'cv_recall': cross_val_score(model, X, y, cv=skf, scoring='recall_weighted').mean(),
        'cv_f1': cross_val_score(model, X, y, cv=skf, scoring='f1_weighted').mean(),
        'cv_roc_auc': cross_val_score(model, X, y, cv=skf, scoring='roc_auc').mean()
    }
    
    return cv_metrics


def train_logistic_regression(
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
    X_train_df: pd.DataFrame = None,
    X_test_df: pd.DataFrame = None
) -> Tuple[Any, Dict[str, float], Dict[str, Any]]:
    """
    Train Logistic Regression with hyperparameter tuning.
    
    Args:
        X_train: Training features
        X_test: Test features
        y_train: Training labels
        y_test: Test labels
        X_train_df: Training features as DataFrame (for dataset logging)
        X_test_df: Test features as DataFrame (for dataset logging)

    Returns:
        Tuple of (best_model, metrics, best_params)
    """
    print("\n" + "="*80)
    print("TRAINING LOGISTIC REGRESSION")
    print("="*80)
    
    with mlflow.start_run(run_name="logistic_regression"):
        # Log model type
        mlflow.log_param("model_type", "LogisticRegression")
        
        # Log dataset information
        if X_train_df is not None:
            try:
                # Create training dataset
                train_df = X_train_df.copy()
                train_df['target'] = y_train
                train_dataset = mlflow.data.from_pandas(
                    train_df,
                    source="data/processed/X_train.pkl",
                    name="heart_disease_training_data",
                    targets="target"
                )
                mlflow.log_input(train_dataset, context="training")
                print(f"✓ Training dataset logged to MLflow")

                # Create test dataset
                test_df = X_test_df.copy()
                test_df['target'] = y_test
                test_dataset = mlflow.data.from_pandas(
                    test_df,
                    source="data/processed/X_test.pkl",
                    name="heart_disease_test_data",
                    targets="target"
                )
                mlflow.log_input(test_dataset, context="testing")
                print(f"✓ Test dataset logged to MLflow")
            except Exception as e:
                print(f"⚠️  Could not log datasets: {e}")

        # Initialize model
        lr = LogisticRegression(random_state=42)
        
        # Hyperparameter tuning
        print("Performing GridSearchCV for hyperparameter tuning...")
        param_grid = get_logistic_regression_params()
        
        grid_search = GridSearchCV(
            lr,
            param_grid,
            cv=5,
            scoring='roc_auc',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        best_model = grid_search.best_estimator_
        
        print(f"\n✓ Best parameters: {grid_search.best_params_}")
        print(f"✓ Best CV ROC-AUC score: {grid_search.best_score_:.4f}")
        
        # Log best parameters
        for param, value in grid_search.best_params_.items():
            mlflow.log_param(f"best_{param}", value)
        mlflow.log_metric("best_cv_score", grid_search.best_score_)
        
        # Evaluate model
        print("\nEvaluating model...")
        metrics = evaluate_model(best_model, X_train, X_test, y_train, y_test)
        
        # Cross-validation
        cv_metrics = cross_validate_model(best_model, X_train, y_train)
        metrics.update(cv_metrics)
        
        # Log all metrics
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)
        
        # Log evaluation metrics as table
        eval_table = pd.DataFrame([{
            'Metric': 'Accuracy',
            'Training': metrics['train_accuracy'],
            'Test': metrics['test_accuracy'],
            'Cross-Validation': metrics['cv_accuracy']
        }, {
            'Metric': 'ROC-AUC',
            'Training': metrics['train_roc_auc'],
            'Test': metrics['test_roc_auc'],
            'Cross-Validation': metrics['cv_roc_auc']
        }, {
            'Metric': 'Precision',
            'Training': metrics['train_precision'],
            'Test': metrics['test_precision'],
            'Cross-Validation': metrics['cv_precision']
        }, {
            'Metric': 'Recall',
            'Training': metrics['train_recall'],
            'Test': metrics['test_recall'],
            'Cross-Validation': metrics['cv_recall']
        }, {
            'Metric': 'F1-Score',
            'Training': metrics['train_f1'],
            'Test': metrics['test_f1'],
            'Cross-Validation': metrics['cv_f1']
        }])

        try:
            mlflow.log_table(data=eval_table, artifact_file="evaluation_metrics.json")
        except Exception as e:
            print(f"⚠️  Could not log evaluation table: {e}")

        # Print metrics
        print("\n" + "-"*80)
        print("EVALUATION METRICS")
        print("-"*80)
        print(f"Test Accuracy:  {metrics['test_accuracy']:.4f}")
        print(f"Test Precision: {metrics['test_precision']:.4f}")
        print(f"Test Recall:    {metrics['test_recall']:.4f}")
        print(f"Test F1-Score:  {metrics['test_f1']:.4f}")
        print(f"Test ROC-AUC:   {metrics['test_roc_auc']:.4f}")
        print("-"*80)
        print(f"CV Accuracy:    {metrics['cv_accuracy']:.4f}")
        print(f"CV ROC-AUC:     {metrics['cv_roc_auc']:.4f}")
        
        # Log model
        mlflow.sklearn.log_model(best_model, "model")
        
        return best_model, metrics, grid_search.best_params_


def train_random_forest(
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
    X_train_df: pd.DataFrame = None,
    X_test_df: pd.DataFrame = None
) -> Tuple[Any, Dict[str, float], Dict[str, Any]]:
    """
    Train Random Forest with hyperparameter tuning.
    
    Args:
        X_train: Training features
        X_test: Test features
        y_train: Training labels
        y_test: Test labels
        X_train_df: Training features as DataFrame (for dataset logging)
        X_test_df: Test features as DataFrame (for dataset logging)

    Returns:
        Tuple of (best_model, metrics, best_params)
    """
    print("\n" + "="*80)
    print("TRAINING RANDOM FOREST")
    print("="*80)
    
    with mlflow.start_run(run_name="random_forest"):
        # Log model type
        mlflow.log_param("model_type", "RandomForest")
        
        # Log dataset information
        if X_train_df is not None:
            try:
                # Create training dataset
                train_df = X_train_df.copy()
                train_df['target'] = y_train
                train_dataset = mlflow.data.from_pandas(
                    train_df,
                    source="data/processed/X_train.pkl",
                    name="heart_disease_training_data",
                    targets="target"
                )
                mlflow.log_input(train_dataset, context="training")
                print(f"✓ Training dataset logged to MLflow")

                # Create test dataset
                test_df = X_test_df.copy()
                test_df['target'] = y_test
                test_dataset = mlflow.data.from_pandas(
                    test_df,
                    source="data/processed/X_test.pkl",
                    name="heart_disease_test_data",
                    targets="target"
                )
                mlflow.log_input(test_dataset, context="testing")
                print(f"✓ Test dataset logged to MLflow")
            except Exception as e:
                print(f"⚠️  Could not log datasets: {e}")

        # Initialize model
        rf = RandomForestClassifier(random_state=42, n_jobs=-1)
        
        # Hyperparameter tuning
        print("Performing GridSearchCV for hyperparameter tuning...")
        param_grid = get_random_forest_params()
        
        grid_search = GridSearchCV(
            rf,
            param_grid,
            cv=5,
            scoring='roc_auc',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        best_model = grid_search.best_estimator_
        
        print(f"\n✓ Best parameters: {grid_search.best_params_}")
        print(f"✓ Best CV ROC-AUC score: {grid_search.best_score_:.4f}")
        
        # Log best parameters
        for param, value in grid_search.best_params_.items():
            mlflow.log_param(f"best_{param}", value)
        mlflow.log_metric("best_cv_score", grid_search.best_score_)
        
        # Evaluate model
        print("\nEvaluating model...")
        metrics = evaluate_model(best_model, X_train, X_test, y_train, y_test)
        
        # Cross-validation
        cv_metrics = cross_validate_model(best_model, X_train, y_train)
        metrics.update(cv_metrics)
        
        # Log all metrics
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)
        
        # Log evaluation metrics as table
        eval_table = pd.DataFrame([{
            'Metric': 'Accuracy',
            'Training': metrics['train_accuracy'],
            'Test': metrics['test_accuracy'],
            'Cross-Validation': metrics['cv_accuracy']
        }, {
            'Metric': 'ROC-AUC',
            'Training': metrics['train_roc_auc'],
            'Test': metrics['test_roc_auc'],
            'Cross-Validation': metrics['cv_roc_auc']
        }, {
            'Metric': 'Precision',
            'Training': metrics['train_precision'],
            'Test': metrics['test_precision'],
            'Cross-Validation': metrics['cv_precision']
        }, {
            'Metric': 'Recall',
            'Training': metrics['train_recall'],
            'Test': metrics['test_recall'],
            'Cross-Validation': metrics['cv_recall']
        }, {
            'Metric': 'F1-Score',
            'Training': metrics['train_f1'],
            'Test': metrics['test_f1'],
            'Cross-Validation': metrics['cv_f1']
        }])

        try:
            mlflow.log_table(data=eval_table, artifact_file="evaluation_metrics.json")
        except Exception as e:
            print(f"⚠️  Could not log evaluation table: {e}")

        # Feature importance
        if hasattr(best_model, 'feature_importances_'):
            feature_importance = best_model.feature_importances_
            top_features = np.argsort(feature_importance)[-10:][::-1]
            print(f"\n✓ Top 10 feature indices: {top_features.tolist()}")
            mlflow.log_param("top_10_features", top_features.tolist())

            # Log feature importance as table
            feature_importance_table = pd.DataFrame({
                'Feature_Index': range(len(feature_importance)),
                'Importance': feature_importance
            }).sort_values('Importance', ascending=False).head(10)

            try:
                mlflow.log_table(data=feature_importance_table, artifact_file="feature_importance.json")
            except Exception as e:
                print(f"⚠️  Could not log feature importance table: {e}")

        # Print metrics
        print("\n" + "-"*80)
        print("EVALUATION METRICS")
        print("-"*80)
        print(f"Test Accuracy:  {metrics['test_accuracy']:.4f}")
        print(f"Test Precision: {metrics['test_precision']:.4f}")
        print(f"Test Recall:    {metrics['test_recall']:.4f}")
        print(f"Test F1-Score:  {metrics['test_f1']:.4f}")
        print(f"Test ROC-AUC:   {metrics['test_roc_auc']:.4f}")
        print("-"*80)
        print(f"CV Accuracy:    {metrics['cv_accuracy']:.4f}")
        print(f"CV ROC-AUC:     {metrics['cv_roc_auc']:.4f}")
        
        # Log model
        mlflow.sklearn.log_model(best_model, "model")
        
        return best_model, metrics, grid_search.best_params_


def save_best_model(
    model,
    model_name: str,
    metrics: Dict[str, float],
    params: Dict[str, Any]
):
    """
    Save the best model and its metadata.
    
    Args:
        model: Trained model
        model_name: Name for the model file
        metrics: Model metrics
        params: Model parameters
    """
    print(f"\n✓ Saving model to {MODEL_DIR}/{model_name}.pkl")
    
    # Save model
    model_path = MODEL_DIR / f"{model_name}.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    # Save metadata
    metadata = {
        'model_name': model_name,
        'metrics': metrics,
        'parameters': params,
        'timestamp': '2025-12-24 08:49:33'
    }
    
    metadata_path = MODEL_DIR / f"{model_name}_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4, default=str)
    
    print(f"✓ Saved metadata to {metadata_path}")


def compare_models(
    lr_metrics: Dict[str, float],
    rf_metrics: Dict[str, float]
) -> str:
    """
    Compare models and select the best one.
    
    Args:
        lr_metrics: Logistic Regression metrics
        rf_metrics: Random Forest metrics
    
    Returns:
        Name of the best model
    """
    print("\n" + "="*80)
    print("MODEL COMPARISON")
    print("="*80)
    
    comparison_df = pd.DataFrame({
        'Logistic Regression': lr_metrics,
        'Random Forest': rf_metrics
    })
    
    print("\n" + comparison_df.to_string())
    
    # Log comparison table to MLflow for visualization
    # Create a table format suitable for MLflow UI
    comparison_table = pd.DataFrame([
        {
            'Model': 'Logistic Regression',
            'Train Accuracy': lr_metrics['train_accuracy'],
            'Train ROC-AUC': lr_metrics['train_roc_auc'],
            'Test Accuracy': lr_metrics['test_accuracy'],
            'Test ROC-AUC': lr_metrics['test_roc_auc'],
            'Test Precision': lr_metrics['test_precision'],
            'Test Recall': lr_metrics['test_recall'],
            'Test F1': lr_metrics['test_f1'],
            'CV ROC-AUC': lr_metrics['cv_roc_auc'],
        },
        {
            'Model': 'Random Forest',
            'Train Accuracy': rf_metrics['train_accuracy'],
            'Train ROC-AUC': rf_metrics['train_roc_auc'],
            'Test Accuracy': rf_metrics['test_accuracy'],
            'Test ROC-AUC': rf_metrics['test_roc_auc'],
            'Test Precision': rf_metrics['test_precision'],
            'Test Recall': rf_metrics['test_recall'],
            'Test F1': rf_metrics['test_f1'],
            'CV ROC-AUC': rf_metrics['cv_roc_auc'],
        }
    ])

    # Log table to MLflow - will be visible in MLflow UI under "Tables" tab
    try:
        mlflow.log_table(data=comparison_table, artifact_file="model_comparison.json")
        print("\n✓ Model comparison table logged to MLflow")
    except Exception as e:
        print(f"\n⚠️  Could not log table to MLflow: {e}")

    # Select best model based on test ROC-AUC
    lr_score = lr_metrics['test_roc_auc']
    rf_score = rf_metrics['test_roc_auc']
    
    print("\n" + "-"*80)
    if rf_score > lr_score:
        print(f"🏆 WINNER: Random Forest (ROC-AUC: {rf_score:.4f})")
        best_model_name = "random_forest"
    else:
        print(f"🏆 WINNER: Logistic Regression (ROC-AUC: {lr_score:.4f})")
        best_model_name = "logistic_regression"
    print("-"*80)
    
    return best_model_name


def main():
    """Main training pipeline."""
    print("\n" + "="*80)
    print("MODEL TRAINING PIPELINE")
    print("="*80)
    print(f"Timestamp: 2025-12-24 08:49:33 UTC")
    print(f"Author: sanepr")
    
    # Setup MLflow
    setup_mlflow()
    
    # Load data (now returns DataFrames too)
    X_train, X_test, y_train, y_test, X_train_df, X_test_df = load_data()

    # Train Logistic Regression (with dataset logging)
    lr_model, lr_metrics, lr_params = train_logistic_regression(
        X_train, X_test, y_train, y_test, X_train_df, X_test_df
    )
    
    # Train Random Forest (with dataset logging)
    rf_model, rf_metrics, rf_params = train_random_forest(
        X_train, X_test, y_train, y_test, X_train_df, X_test_df
    )
    
    # Compare models
    best_model_name = compare_models(lr_metrics, rf_metrics)
    
    # Save both models
    save_best_model(lr_model, "logistic_regression", lr_metrics, lr_params)
    save_best_model(rf_model, "random_forest", rf_metrics, rf_params)
    
    # Save the best model with a special name
    if best_model_name == "random_forest":
        save_best_model(rf_model, "best_model", rf_metrics, rf_params)
    else:
        save_best_model(lr_model, "best_model", lr_metrics, lr_params)
    
    print("\n" + "="*80)
    print("TRAINING COMPLETE")
    print("="*80)
    print(f"✓ Models saved to: {MODEL_DIR}")
    config = get_mlflow_config()
    print(f"✓ MLflow tracking: {config['tracking_uri']}")
    print(f"✓ Best model: {best_model_name}")
    print("\nTo view MLflow UI, run: mlflow ui")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
