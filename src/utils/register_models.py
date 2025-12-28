"""
Register Models in MLflow Model Registry

This script registers the trained models from MLflow runs into the Model Registry,
making them visible and manageable in the MLflow UI.

Usage:
    python register_models.py
"""

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import os
from pathlib import Path


def register_models():
    """Register models from latest runs into Model Registry."""

    # Set tracking URI
    project_root = Path(__file__).resolve().parents[2]
    tracking_uri = f"file://{project_root}/mlruns"
    mlflow.set_tracking_uri(tracking_uri)

    print("=" * 80)
    print("REGISTERING MODELS IN MLFLOW MODEL REGISTRY")
    print("=" * 80)
    print(f"Tracking URI: {tracking_uri}\n")

    client = MlflowClient()

    # Get the experiment
    experiment = client.get_experiment_by_name("heart-disease-prediction")

    if not experiment:
        print("❌ Experiment 'heart-disease-prediction' not found!")
        print("   Please run training first: python src/models/train.py")
        return

    print(f"✓ Found experiment: {experiment.name} (ID: {experiment.experiment_id})")

    # Get all runs from the experiment
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"],
        max_results=10
    )

    if len(runs) == 0:
        print("❌ No runs found in experiment!")
        return

    print(f"✓ Found {len(runs)} runs\n")

    # Register models
    registered_count = 0

    for idx, run in runs.iterrows():
        run_id = run['run_id']
        model_type = run.get('params.model_type', 'unknown')
        roc_auc = run.get('metrics.test_roc_auc', 0)

        print(f"Processing run {run_id[:12]}... (Model: {model_type})")

        # Check if model artifact exists
        try:
            artifacts = client.list_artifacts(run_id)
            has_model = any('model' in art.path for art in artifacts)

            if not has_model:
                print(f"  ⚠️  No model artifact found, skipping")
                continue

            # Determine model name
            if model_type == 'LogisticRegression':
                model_name = "heart-disease-logistic-regression"
            elif model_type == 'RandomForest':
                model_name = "heart-disease-random-forest"
            else:
                model_name = f"heart-disease-{model_type.lower()}"

            # Register model
            model_uri = f"runs:/{run_id}/model"

            # Check if model already registered
            try:
                existing_model = client.get_registered_model(model_name)
                print(f"  ℹ️  Model '{model_name}' already exists, creating new version")
            except:
                print(f"  ➕ Creating new model '{model_name}'")

            # Register the model
            model_version = mlflow.register_model(
                model_uri=model_uri,
                name=model_name,
                tags={
                    "model_type": model_type,
                    "test_roc_auc": str(roc_auc),
                    "run_id": run_id
                }
            )

            print(f"  ✓ Registered as version {model_version.version}")
            print(f"    ROC-AUC: {roc_auc:.4f}")

            # Set production stage for best model
            if roc_auc > 0.95:  # High performance threshold
                client.transition_model_version_stage(
                    name=model_name,
                    version=model_version.version,
                    stage="Production",
                    archive_existing_versions=False
                )
                print(f"    🏆 Set to Production stage (ROC-AUC > 0.95)")
            else:
                client.transition_model_version_stage(
                    name=model_name,
                    version=model_version.version,
                    stage="Staging",
                    archive_existing_versions=False
                )
                print(f"    📋 Set to Staging stage")

            registered_count += 1
            print()

        except Exception as e:
            print(f"  ❌ Error: {e}\n")
            continue

    # Summary
    print("=" * 80)
    print(f"REGISTRATION COMPLETE: {registered_count} models registered")
    print("=" * 80)

    # List registered models
    print("\n📊 Registered Models Summary:\n")
    try:
        registered_models = client.search_registered_models()
        if registered_models:
            for model in registered_models:
                print(f"Model: {model.name}")
                for version in model.latest_versions:
                    stage = version.current_stage
                    tags = version.tags
                    roc_auc = tags.get('test_roc_auc', 'N/A')
                    print(f"  Version {version.version}: {stage} (ROC-AUC: {roc_auc})")
                print()
        else:
            print("  No registered models found")
    except Exception as e:
        print(f"  Error listing models: {e}")

    print("\n💡 To view in MLflow UI:")
    print("   1. Run: mlflow ui")
    print("   2. Open: http://localhost:5000")
    print("   3. Click 'Models' tab to see registered models")
    print()


if __name__ == "__main__":
    register_models()

