#!/usr/bin/env python3
"""
Simple API Monitoring Dashboard

This script provides a real-time terminal dashboard for monitoring
the Heart Disease API metrics by querying Prometheus.
"""

import requests
import time
import os
from datetime import datetime
from typing import Dict, Any


class APIMonitor:
    """Monitor Heart Disease API via Prometheus metrics."""

    def __init__(self, prometheus_url: str = "http://localhost:9090"):
        self.prometheus_url = prometheus_url
        self.api_url = prometheus_url.replace(":9090", ":8002")

    def query_prometheus(self, query: str) -> Any:
        """Query Prometheus API."""
        try:
            response = requests.get(
                f"{self.prometheus_url}/api/v1/query",
                params={'query': query},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            if data['status'] == 'success' and data['data']['result']:
                return data['data']['result']
            return None
        except Exception as e:
            return None

    def get_total_predictions(self) -> int:
        """Get total number of predictions."""
        result = self.query_prometheus('sum(heart_disease_predictions_total)')
        if result:
            return int(float(result[0]['value'][1]))
        return 0

    def get_predictions_by_result(self) -> Dict[str, int]:
        """Get predictions grouped by result."""
        result = self.query_prometheus('sum by (prediction_result) (heart_disease_predictions_total)')
        predictions = {}
        if result:
            for item in result:
                pred_result = item['metric']['prediction_result']
                count = int(float(item['value'][1]))
                predictions[pred_result] = count
        return predictions

    def get_avg_latency(self) -> float:
        """Get average prediction latency."""
        query = 'rate(heart_disease_prediction_latency_seconds_sum[5m]) / rate(heart_disease_prediction_latency_seconds_count[5m])'
        result = self.query_prometheus(query)
        if result:
            return float(result[0]['value'][1]) * 1000  # Convert to ms
        return 0.0

    def get_error_rate(self) -> float:
        """Get error rate per second."""
        result = self.query_prometheus('rate(heart_disease_prediction_errors_total[5m])')
        if result:
            return float(result[0]['value'][1])
        return 0.0

    def get_active_requests(self) -> int:
        """Get number of active requests."""
        result = self.query_prometheus('heart_disease_active_requests')
        if result:
            return int(float(result[0]['value'][1]))
        return 0

    def get_model_status(self) -> bool:
        """Check if model is loaded."""
        result = self.query_prometheus('heart_disease_model_info')
        if result:
            return float(result[0]['value'][1]) == 1.0
        return False

    def check_api_health(self) -> bool:
        """Check if API is healthy."""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def display_dashboard(self):
        """Display monitoring dashboard in terminal."""
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')

        # Get metrics
        total_predictions = self.get_total_predictions()
        predictions_by_result = self.get_predictions_by_result()
        avg_latency = self.get_avg_latency()
        error_rate = self.get_error_rate()
        active_requests = self.get_active_requests()
        model_loaded = self.get_model_status()
        api_healthy = self.check_api_health()

        # Display header
        print("=" * 80)
        print(" " * 20 + "HEART DISEASE API MONITORING DASHBOARD")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Prometheus: {self.prometheus_url}")
        print(f"API: {self.api_url}")
        print("-" * 80)

        # System Status
        print("\n📊 SYSTEM STATUS")
        print("-" * 80)
        api_status = "🟢 HEALTHY" if api_healthy else "🔴 DOWN"
        model_status = "🟢 LOADED" if model_loaded else "🔴 NOT LOADED"
        print(f"API Status:          {api_status}")
        print(f"Model Status:        {model_status}")
        print(f"Active Requests:     {active_requests}")

        # Prediction Metrics
        print("\n📈 PREDICTION METRICS")
        print("-" * 80)
        print(f"Total Predictions:   {total_predictions:,}")

        if predictions_by_result:
            positive = predictions_by_result.get('positive', 0)
            negative = predictions_by_result.get('negative', 0)
            total = positive + negative

            if total > 0:
                positive_pct = (positive / total) * 100
                negative_pct = (negative / total) * 100
                print(f"  • Positive:        {positive:,} ({positive_pct:.1f}%)")
                print(f"  • Negative:        {negative:,} ({negative_pct:.1f}%)")

        # Performance Metrics
        print("\n⚡ PERFORMANCE METRICS")
        print("-" * 80)
        latency_status = "🟢" if avg_latency < 100 else "🟡" if avg_latency < 500 else "🔴"
        print(f"Avg Response Time:   {latency_status} {avg_latency:.2f} ms")

        error_status = "🟢" if error_rate == 0 else "🟡" if error_rate < 0.01 else "🔴"
        print(f"Error Rate:          {error_status} {error_rate:.4f} errors/sec")

        # Footer
        print("\n" + "=" * 80)
        print("Press Ctrl+C to exit | Refreshing every 5 seconds...")
        print("=" * 80)

    def run(self, refresh_interval: int = 5):
        """Run the monitoring dashboard with auto-refresh."""
        print("Starting API monitoring dashboard...")
        print(f"Connecting to Prometheus at {self.prometheus_url}...")
        time.sleep(2)

        try:
            while True:
                self.display_dashboard()
                time.sleep(refresh_interval)
        except KeyboardInterrupt:
            print("\n\n✓ Monitoring stopped.")
            print("Thank you for using the API Monitoring Dashboard!")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Heart Disease API Monitoring Dashboard')
    parser.add_argument(
        '--prometheus-url',
        default='http://localhost:9090',
        help='Prometheus server URL (default: http://localhost:9090)'
    )
    parser.add_argument(
        '--refresh',
        type=int,
        default=5,
        help='Dashboard refresh interval in seconds (default: 5)'
    )

    args = parser.parse_args()

    monitor = APIMonitor(prometheus_url=args.prometheus_url)
    monitor.run(refresh_interval=args.refresh)


if __name__ == "__main__":
    main()

