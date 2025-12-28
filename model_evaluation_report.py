#!/usr/bin/env python3
"""
Generate Model Evaluation Report from MLflow Registry

This script generates a comprehensive evaluation report for all registered
models in the MLflow registry, including parameters, metrics, and comparisons.
"""

import mlflow
from mlflow.tracking import MlflowClient
from datetime import datetime
import pandas as pd
import sys
from pathlib import Path


def generate_report(tracking_uri="file://./mlruns", output_csv=False):
    """Generate comprehensive model evaluation report."""

    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()

    print("=" * 100)
    print("MODEL REGISTRY EVALUATION REPORT")
    print("=" * 100)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Tracking URI: {tracking_uri}")
    print("=" * 100)

    # Get all registered models
    try:
        models = client.search_registered_models()
    except Exception as e:
        print(f"\n❌ Error accessing registry: {e}")
        return

    if not models:
        print("\n⚠️  No registered models found")
        print("   Run: python src/utils/register_models.py")
        return

    print(f"\n📊 Total Registered Models: {len(models)}\n")

    # Collect data for summary table
    summary_data = []

    for model in models:
        print("=" * 100)
        print(f"📦 MODEL: {model.name}")
        print("=" * 100)

        for version in model.latest_versions:
            print(f"\n🔖 Version {version.version} - {version.current_stage}")
            print("-" * 100)

            try:
                # Get run data
                run = client.get_run(version.run_id)

                # Basic info
                print(f"   Run ID: {version.run_id}")
                print(f"   Status: {version.status}")
                created = datetime.fromtimestamp(version.creation_timestamp/1000)
                print(f"   Created: {created.strftime('%Y-%m-%d %H:%M:%S')}")

                # Parameters
                print(f"\n   📝 Hyperparameters:")
                params = run.data.params
                for key, value in sorted(params.items()):
                    print(f"      • {key:.<40} {value}")

                # Evaluation Metrics
                print(f"\n   📊 Evaluation Metrics:")
                metrics = run.data.metrics

                # Group metrics
                train_metrics = {k: v for k, v in metrics.items() if 'train' in k}
                test_metrics = {k: v for k, v in metrics.items() if 'test' in k}
                cv_metrics = {k: v for k, v in metrics.items() if 'cv' in k}

                if train_metrics:
                    print(f"\n      Training Metrics:")
                    for key, value in sorted(train_metrics.items()):
                        print(f"         {key:.<35} {value:.6f}")

                if test_metrics:
                    print(f"\n      Test Metrics (Evaluation Set):")
                    for key, value in sorted(test_metrics.items()):
                        print(f"         {key:.<35} {value:.6f}")

                if cv_metrics:
                    print(f"\n      Cross-Validation Metrics:")
                    for key, value in sorted(cv_metrics.items()):
                        print(f"         {key:.<35} {value:.6f}")

                # Tags
                if version.tags:
                    print(f"\n   🏷️  Tags:")
                    for key, value in version.tags.items():
                        print(f"      • {key}: {value}")

                # Add to summary
                summary_data.append({
                    'Model': model.name,
                    'Version': version.version,
                    'Stage': version.current_stage,
                    'Test Accuracy': test_metrics.get('test_accuracy', 0),
                    'Test ROC-AUC': test_metrics.get('test_roc_auc', 0),
                    'Test F1': test_metrics.get('test_f1', 0),
                    'Test Precision': test_metrics.get('test_precision', 0),
                    'Test Recall': test_metrics.get('test_recall', 0),
                    'CV Accuracy': cv_metrics.get('cv_accuracy', 0),
                    'CV ROC-AUC': cv_metrics.get('cv_roc_auc', 0),
                    'Run ID': version.run_id[:12] + '...',
                })

                print()

            except Exception as e:
                print(f"   ❌ Error loading version data: {e}\n")
                continue

    # Print summary table
    print("\n" + "=" * 100)
    print("MODELS COMPARISON SUMMARY")
    print("=" * 100 + "\n")

    if summary_data:
        df = pd.DataFrame(summary_data)
        print(df.to_string(index=False))

        # Print best model
        if 'Test ROC-AUC' in df.columns and df['Test ROC-AUC'].max() > 0:
            best_idx = df['Test ROC-AUC'].idxmax()
            best_model = df.iloc[best_idx]

            print("\n" + "=" * 100)
            print("🏆 BEST MODEL (by Test ROC-AUC)")
            print("=" * 100)
            print(f"   Model: {best_model['Model']}")
            print(f"   Version: {best_model['Version']}")
            print(f"   Stage: {best_model['Stage']}")
            print(f"   Test ROC-AUC: {best_model['Test ROC-AUC']:.4f}")
            print(f"   Test Accuracy: {best_model['Test Accuracy']:.4f}")
            print(f"   Test F1: {best_model['Test F1']:.4f}")
            print("=" * 100)

        # Save to CSV if requested
        if output_csv:
            csv_filename = 'model_evaluation_report.csv'
            df.to_csv(csv_filename, index=False)
            print(f"\n✓ Report saved to: {csv_filename}")
    else:
        print("   No data to display")

    print("\n" + "=" * 100)
    print("Report Complete")
    print("=" * 100)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate MLflow model evaluation report')
    parser.add_argument('--tracking-uri', default='file://./mlruns',
                       help='MLflow tracking URI (default: file://./mlruns)')
    parser.add_argument('--csv', action='store_true',
                       help='Export report to CSV file')

    args = parser.parse_args()

    generate_report(tracking_uri=args.tracking_uri, output_csv=args.csv)

