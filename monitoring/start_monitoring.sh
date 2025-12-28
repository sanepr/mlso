#!/bin/bash

# Heart Disease API Monitoring Stack Startup Script
# This script starts Prometheus and Grafana for API monitoring

set -e

echo "🚀 Starting Heart Disease API Monitoring Stack"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is running
echo "🐳 Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running!${NC}"
    echo "Please start Docker Desktop and try again."
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

# Navigate to monitoring directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if monitoring stack is already running
echo "📊 Checking existing containers..."
if docker ps | grep -q "heart-disease-prometheus\|heart-disease-grafana"; then
    echo -e "${YELLOW}⚠️  Monitoring stack is already running${NC}"
    echo ""
    echo "Options:"
    echo "  1. Stop and restart"
    echo "  2. Keep running and exit"
    echo "  3. View status only"
    read -p "Enter choice (1/2/3): " choice

    case $choice in
        1)
            echo ""
            echo "🛑 Stopping existing containers..."
            docker-compose -f docker-compose.monitoring.yml down
            echo -e "${GREEN}✓ Stopped${NC}"
            echo ""
            ;;
        2)
            echo ""
            echo -e "${GREEN}✓ Keeping existing stack running${NC}"
            echo ""
            echo "Access URLs:"
            echo "  • Prometheus: http://localhost:9090"
            echo "  • Grafana:    http://localhost:3000 (admin/admin)"
            exit 0
            ;;
        3)
            echo ""
            docker-compose -f docker-compose.monitoring.yml ps
            echo ""
            echo "Access URLs:"
            echo "  • Prometheus: http://localhost:9090"
            echo "  • Grafana:    http://localhost:3000 (admin/admin)"
            exit 0
            ;;
        *)
            echo "Invalid choice. Exiting."
            exit 1
            ;;
    esac
fi

# Start monitoring stack
echo "🚢 Starting Prometheus and Grafana..."
docker-compose -f docker-compose.monitoring.yml up -d

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 5

# Check Prometheus
echo ""
echo "Checking Prometheus..."
if curl -s http://localhost:9090/-/healthy > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Prometheus is healthy${NC}"
else
    echo -e "${YELLOW}⚠️  Prometheus is starting...${NC}"
fi

# Check Grafana
echo "Checking Grafana..."
if curl -s http://localhost:3000/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Grafana is healthy${NC}"
else
    echo -e "${YELLOW}⚠️  Grafana is starting...${NC}"
fi

echo ""
echo "=============================================="
echo -e "${GREEN}✓ Monitoring Stack Started Successfully!${NC}"
echo "=============================================="
echo ""

echo "📊 Access URLs:"
echo "  • Prometheus: http://localhost:9090"
echo "  • Grafana:    http://localhost:3000"
echo ""

echo "🔐 Grafana Credentials:"
echo "  • Username: admin"
echo "  • Password: admin"
echo "  (You'll be prompted to change password on first login)"
echo ""

echo "📈 Next Steps:"
echo "  1. Ensure API is running: PORT=8002 python src/api/app.py"
echo "  2. Open Grafana: http://localhost:3000"
echo "  3. Navigate to: Dashboards → Heart Disease API Monitoring"
echo "  4. Or use terminal dashboard: python monitoring/dashboard.py"
echo ""

echo "🛑 To stop monitoring:"
echo "  docker-compose -f docker-compose.monitoring.yml down"
echo ""

# Ask if user wants to open Grafana
read -p "Open Grafana in browser? (y/n): " open_browser
if [[ $open_browser == "y" || $open_browser == "Y" ]]; then
    echo ""
    echo "Opening Grafana..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open http://localhost:3000
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open http://localhost:3000 2>/dev/null || echo "Please open http://localhost:3000 in your browser"
    else
        echo "Please open http://localhost:3000 in your browser"
    fi
fi

echo ""
echo "✨ Happy Monitoring!"

