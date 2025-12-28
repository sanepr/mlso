#!/bin/bash

# Manual Grafana Dashboard Setup Script
# This script manually starts Prometheus and Grafana without docker-compose

set -e

echo "🚀 Starting Grafana Dashboard Setup"
echo "===================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running!"
    echo ""
    echo "Please start Docker Desktop:"
    echo "1. Open Docker Desktop app"
    echo "2. Wait for it to fully start (whale icon stops animating)"
    echo "3. Run this script again"
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Stop and remove any existing containers
echo "Cleaning up existing containers..."
docker stop heart-disease-prometheus heart-disease-grafana 2>/dev/null || true
docker rm heart-disease-prometheus heart-disease-grafana 2>/dev/null || true
echo "✓ Cleanup complete"
echo ""

# Create network
echo "Creating Docker network..."
docker network create monitoring 2>/dev/null || echo "  (network already exists)"
echo ""

# Start Prometheus
echo "Starting Prometheus..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run -d \
  --name heart-disease-prometheus \
  --network monitoring \
  -p 9090:9090 \
  -v "${SCRIPT_DIR}/prometheus.yml:/etc/prometheus/prometheus.yml:ro" \
  prom/prometheus:latest \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/prometheus \
  --web.console.libraries=/usr/share/prometheus/console_libraries \
  --web.console.templates=/usr/share/prometheus/consoles

if [ $? -eq 0 ]; then
    echo "✓ Prometheus started successfully"
else
    echo "❌ Failed to start Prometheus"
    exit 1
fi
echo ""

# Wait for Prometheus
echo "Waiting for Prometheus to be ready..."
sleep 5
echo ""

# Start Grafana
echo "Starting Grafana..."
docker run -d \
  --name heart-disease-grafana \
  --network monitoring \
  -p 3000:3000 \
  -e "GF_SECURITY_ADMIN_PASSWORD=admin" \
  -e "GF_USERS_ALLOW_SIGN_UP=false" \
  -v "${SCRIPT_DIR}/grafana-datasource.yml:/etc/grafana/provisioning/datasources/datasource.yml:ro" \
  -v "${SCRIPT_DIR}/grafana-dashboard-provider.yml:/etc/grafana/provisioning/dashboards/provider.yml:ro" \
  -v "${SCRIPT_DIR}/grafana-dashboard.json:/var/lib/grafana/dashboards/heart-disease-api.json:ro" \
  -v "${SCRIPT_DIR}/grafana-dashboard-analytics.json:/var/lib/grafana/dashboards/heart-disease-api-analytics.json:ro" \
  grafana/grafana:latest

if [ $? -eq 0 ]; then
    echo "✓ Grafana started successfully"
else
    echo "❌ Failed to start Grafana"
    exit 1
fi
echo ""

# Wait for services
echo "Waiting for services to initialize..."
sleep 10
echo ""

# Check status
echo "Checking service status..."
echo ""

if docker ps | grep -q heart-disease-prometheus; then
    echo "✓ Prometheus is running"
else
    echo "❌ Prometheus failed to start"
fi

if docker ps | grep -q heart-disease-grafana; then
    echo "✓ Grafana is running"
else
    echo "❌ Grafana failed to start"
fi

echo ""
echo "===================================="
echo "✅ Setup Complete!"
echo "===================================="
echo ""
echo "Access URLs:"
echo "  • Prometheus: http://localhost:9090"
echo "  • Grafana:    http://localhost:3000"
echo ""
echo "Grafana Login:"
echo "  • Username: admin"
echo "  • Password: admin"
echo ""
echo "To view dashboards:"
echo "  1. Open http://localhost:3000"
echo "  2. Login with admin/admin"
echo "  3. Go to Dashboards → Browse"
echo "  4. Look for 'Heart Disease API' dashboards"
echo ""
echo "To stop:"
echo "  docker stop heart-disease-prometheus heart-disease-grafana"
echo ""
echo "To remove:"
echo "  docker rm heart-disease-prometheus heart-disease-grafana"
echo ""

