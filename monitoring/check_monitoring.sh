#!/bin/bash

# Monitoring Stack Status Check Script

echo "=============================="
echo "Monitoring Stack Status Check"
echo "=============================="
echo ""

echo "1. Docker Status:"
if docker info > /dev/null 2>&1; then
    echo "   ✓ Docker is running"
else
    echo "   ✗ Docker is NOT running"
    echo "   → Please start Docker Desktop"
    exit 1
fi
echo ""

echo "2. Container Status:"
if docker ps | grep -q heart-disease-prometheus; then
    echo "   ✓ Prometheus container is running"
    PROM_RUNNING=1
else
    echo "   ✗ Prometheus container is NOT running"
    PROM_RUNNING=0
fi

if docker ps | grep -q heart-disease-grafana; then
    echo "   ✓ Grafana container is running"
    GRAF_RUNNING=1
else
    echo "   ✗ Grafana container is NOT running"
    GRAF_RUNNING=0
fi
echo ""

echo "3. Service Accessibility:"
if curl -s -f http://localhost:9090/-/healthy > /dev/null 2>&1; then
    echo "   ✓ Prometheus is accessible at http://localhost:9090"
else
    echo "   ✗ Prometheus is NOT accessible"
fi

if curl -s -I http://localhost:3000 2>&1 | grep -q "HTTP"; then
    echo "   ✓ Grafana is accessible at http://localhost:3000"
else
    echo "   ✗ Grafana is NOT accessible"
fi
echo ""

echo "4. API Status:"
if curl -s -f http://localhost:8002/health > /dev/null 2>&1; then
    echo "   ✓ API is running at http://localhost:8002"
else
    echo "   ✗ API is NOT running"
    echo "   → Start with: PORT=8002 python src/api/app.py"
fi
echo ""

echo "5. Metrics Endpoint:"
if curl -s -f http://localhost:8002/metrics > /dev/null 2>&1; then
    echo "   ✓ Metrics are available"
else
    echo "   ✗ Metrics are NOT available"
fi
echo ""

echo "=============================="
echo "Summary"
echo "=============================="
echo ""

if [ $PROM_RUNNING -eq 1 ] && [ $GRAF_RUNNING -eq 1 ]; then
    echo "✅ Monitoring stack is RUNNING"
    echo ""
    echo "Access URLs:"
    echo "  • Grafana:    http://localhost:3000 (admin/admin)"
    echo "  • Prometheus: http://localhost:9090"
    echo "  • API:        http://localhost:8002"
    echo ""
    echo "To view dashboards:"
    echo "  1. Open http://localhost:3000"
    echo "  2. Login with admin/admin"
    echo "  3. Go to Dashboards → Browse"
    echo "  4. Look for 'Heart Disease API' folder"
    echo ""
else
    echo "⚠️  Monitoring stack is NOT fully running"
    echo ""
    echo "To start monitoring:"
    echo "  cd /Users/aashishr/codebase/mlso/monitoring"
    echo "  ./setup_grafana_manual.sh"
    echo ""
fi

echo "=============================="

