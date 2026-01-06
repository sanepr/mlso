"""
MLflow Runs Migration Script

This script migrates existing MLflow runs from local mlruns/ folder to a remote
MLflow tracking server (or different backend).

Use cases:
- Migrate from local file storage to remote server
- Copy runs to different MLflow server
- Backup and restore runs
- Consolidate runs from multiple sources

Author: AI Assistant
Date: 2025-12-28
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import RunStatus

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.config.mlflow_config import get_mlflow_config


class MLflowRunsMigrator:
    """Migrate MLflow runs from one tracking server to another."""

    def __init__(self, source_uri: str, target_uri: str):
        """
        Initialize migrator.

        Args:
            source_uri: Source tracking URI (e.g., "file://./mlruns")
            target_uri: Target tracking URI (e.g., "http://localhost:5001")
        """
        self.source_uri = source_uri
        self.target_uri = target_uri
        self.source_client = MlflowClient(tracking_uri=source_uri)
        self.target_client = MlflowClient(tracking_uri=target_uri)

    def list_experiments(self, client: MlflowClient) -> List:
        """List all experiments."""
        return client.search_experiments()

    def list_runs(self, client: MlflowClient, experiment_id: str) -> List:
        """List all runs in an experiment."""
        return client.search_runs(experiment_ids=[experiment_id])

    def create_experiment_if_not_exists(self, experiment_name: str) -> str:
        """
        Create experiment in target if it doesn't exist.

        Returns:
            Experiment ID
        """
        try:
            experiment = self.target_client.get_experiment_by_name(experiment_name)
            if experiment:
                print(f"  Experiment '{experiment_name}' already exists (ID: {experiment.experiment_id})")
                return experiment.experiment_id
        except Exception:
            pass

        # Create new experiment
        experiment_id = self.target_client.create_experiment(experiment_name)
        print(f"  Created experiment '{experiment_name}' (ID: {experiment_id})")
        return experiment_id

    def copy_run(self, source_run, target_experiment_id: str, copy_artifacts: bool = True) -> str:
        """
        Copy a run from source to target.

        Args:
            source_run: Source run object
            target_experiment_id: Target experiment ID
            copy_artifacts: Whether to copy artifacts

        Returns:
            New run ID in target
        """
        # Start new run in target
        with mlflow.start_run(
            experiment_id=target_experiment_id,
            run_name=source_run.info.run_name or f"migrated_{source_run.info.run_id[:8]}"
        ) as target_run:

            # Copy parameters
            for key, value in source_run.data.params.items():
                mlflow.log_param(key, value)

            # Copy metrics
            for key, value in source_run.data.metrics.items():
                mlflow.log_metric(key, value)

            # Copy tags
            for key, value in source_run.data.tags.items():
                # Skip system tags
                if not key.startswith('mlflow.'):
                    mlflow.set_tag(key, value)

            # Add migration metadata
            mlflow.set_tag("mlflow.migration.source_run_id", source_run.info.run_id)
            mlflow.set_tag("mlflow.migration.timestamp", datetime.now().isoformat())
            mlflow.set_tag("mlflow.migration.source_uri", self.source_uri)

            # Copy artifacts if requested
            if copy_artifacts:
                self._copy_artifacts(source_run, target_run)

            return target_run.info.run_id

    def _copy_artifacts(self, source_run, target_run):
        """Copy artifacts from source run to target run."""
        try:
            # Download artifacts from source
            source_path = self.source_client.download_artifacts(
                source_run.info.run_id, ""
            )

            # Log artifacts to target
            if os.path.exists(source_path):
                mlflow.log_artifacts(source_path)
                print(f"    ✓ Copied artifacts")
        except Exception as e:
            print(f"    ⚠ Warning: Could not copy artifacts - {e}")

    def migrate_experiment(
        self,
        experiment_name: str,
        copy_artifacts: bool = True,
        skip_failed: bool = True
    ) -> Dict:
        """
        Migrate all runs from an experiment.

        Args:
            experiment_name: Name of experiment to migrate
            copy_artifacts: Whether to copy artifacts
            skip_failed: Whether to skip failed runs

        Returns:
            Migration statistics
        """
        print(f"\n📦 Migrating experiment: {experiment_name}")

        # Get source experiment
        source_experiment = self.source_client.get_experiment_by_name(experiment_name)
        if not source_experiment:
            print(f"  ❌ Experiment '{experiment_name}' not found in source")
            return {"success": 0, "failed": 0, "skipped": 0}

        # Create target experiment
        target_experiment_id = self.create_experiment_if_not_exists(experiment_name)

        # Get all runs
        source_runs = self.list_runs(self.source_client, source_experiment.experiment_id)
        print(f"  Found {len(source_runs)} runs to migrate")

        stats = {"success": 0, "failed": 0, "skipped": 0}

        for i, run in enumerate(source_runs, 1):
            print(f"  [{i}/{len(source_runs)}] Migrating run {run.info.run_id[:8]}...", end="")

            # Skip failed runs if requested
            if skip_failed and run.info.status != RunStatus.to_string(RunStatus.FINISHED):
                print(" SKIPPED (not finished)")
                stats["skipped"] += 1
                continue

            try:
                new_run_id = self.copy_run(run, target_experiment_id, copy_artifacts)
                print(f" ✓ SUCCESS (new ID: {new_run_id[:8]})")
                stats["success"] += 1
            except Exception as e:
                print(f" ✗ FAILED: {e}")
                stats["failed"] += 1

        return stats

    def migrate_all(self, copy_artifacts: bool = True, skip_failed: bool = True) -> Dict:
        """
        Migrate all experiments and runs.

        Args:
            copy_artifacts: Whether to copy artifacts
            skip_failed: Whether to skip failed runs

        Returns:
            Overall migration statistics
        """
        print("="*80)
        print("MLFLOW RUNS MIGRATION")
        print("="*80)
        print(f"Source: {self.source_uri}")
        print(f"Target: {self.target_uri}")

        # Get all experiments
        source_experiments = self.list_experiments(self.source_client)
        print(f"\nFound {len(source_experiments)} experiments in source")

        overall_stats = {"experiments": 0, "success": 0, "failed": 0, "skipped": 0}

        for experiment in source_experiments:
            # Skip default experiment if it's empty
            if experiment.name == "Default" and experiment.lifecycle_stage == "deleted":
                continue

            stats = self.migrate_experiment(
                experiment.name,
                copy_artifacts=copy_artifacts,
                skip_failed=skip_failed
            )

            overall_stats["experiments"] += 1
            overall_stats["success"] += stats["success"]
            overall_stats["failed"] += stats["failed"]
            overall_stats["skipped"] += stats["skipped"]

        return overall_stats

    def print_summary(self, stats: Dict):
        """Print migration summary."""
        print("\n" + "="*80)
        print("MIGRATION SUMMARY")
        print("="*80)
        print(f"Experiments migrated: {stats['experiments']}")
        print(f"Runs successfully migrated: {stats['success']}")
        print(f"Runs failed: {stats['failed']}")
        print(f"Runs skipped: {stats['skipped']}")
        print(f"Total runs processed: {stats['success'] + stats['failed'] + stats['skipped']}")
        print("="*80)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Migrate MLflow runs from local storage to remote server"
    )

    parser.add_argument(
        "--source",
        type=str,
        default="file://./mlruns",
        help="Source tracking URI (default: file://./mlruns)"
    )

    parser.add_argument(
        "--target",
        type=str,
        help="Target tracking URI (e.g., http://localhost:5001)"
    )

    parser.add_argument(
        "--experiment",
        type=str,
        help="Migrate specific experiment only (otherwise migrates all)"
    )

    parser.add_argument(
        "--no-artifacts",
        action="store_true",
        help="Don't copy artifacts (faster, but incomplete)"
    )

    parser.add_argument(
        "--include-failed",
        action="store_true",
        help="Include failed/incomplete runs"
    )

    parser.add_argument(
        "--use-config",
        action="store_true",
        help="Use target from mlflow_config.py (production server)"
    )

    args = parser.parse_args()

    # Determine target URI
    if args.use_config:
        config = get_mlflow_config()
        target_uri = config['tracking_uri']
        print(f"Using target from config: {target_uri}")
    elif args.target:
        target_uri = args.target
    else:
        print("❌ Error: Must specify --target or --use-config")
        sys.exit(1)

    # Create migrator
    migrator = MLflowRunsMigrator(args.source, target_uri)

    # Migrate
    if args.experiment:
        # Migrate specific experiment
        stats = migrator.migrate_experiment(
            args.experiment,
            copy_artifacts=not args.no_artifacts,
            skip_failed=not args.include_failed
        )
        overall_stats = {
            "experiments": 1,
            "success": stats["success"],
            "failed": stats["failed"],
            "skipped": stats["skipped"]
        }
    else:
        # Migrate all experiments
        overall_stats = migrator.migrate_all(
            copy_artifacts=not args.no_artifacts,
            skip_failed=not args.include_failed
        )

    # Print summary
    migrator.print_summary(overall_stats)

    # Exit code
    if overall_stats["failed"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

