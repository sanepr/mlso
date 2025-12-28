# 🔧 Grafana Dashboard Troubleshooting & Alternative Setup

**Issue:** Dashboards not visible in Grafana  
**Date:** December 28, 2025

---

## ⚠️ Common Issues & Solutions

### Issue 1: Docker Not Running

**Symptoms:**
- Docker commands hang or don't respond
- No containers appear when running `docker ps`

**Solution:**
```bash
# Check if Docker is running
docker info

# If it fails, start Docker Desktop:
# 1. Open Docker Desktop application
# 2. Wait for whale icon to stop animating (30-60 seconds)
# 3. Verify: docker info
```

---

### Issue 2: Containers Not Starting

**Solution 1: Manual Docker Commands**

```bash
cd /Users/aashishr/codebase/mlso/monitoring

# Stop any existing containers
docker stop heart-disease-prometheus heart-disease-grafana 2>/dev/null
docker rm heart-disease-prometheus heart-disease-grafana 2>/dev/null

# Create network
docker network create monitoring 2>/dev/null

# Start Prometheus
docker run -d \
  --name heart-disease-prometheus \
  --network monitoring \
  -p 9090:9090 \
  -v "$(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml:ro" \
  prom/prometheus:latest

# Start Grafana
docker run -d \
  --name heart-disease-grafana \
  --network monitoring \
  -p 3000:3000 \
  -e "GF_SECURITY_ADMIN_PASSWORD=admin" \
  -e "GF_USERS_ALLOW_SIGN_UP=false" \
  -v "$(pwd)/grafana-datasource.yml:/etc/grafana/provisioning/datasources/datasource.yml:ro" \
  -v "$(pwd)/grafana-dashboard-provider.yml:/etc/grafana/provisioning/dashboards/provider.yml:ro" \
  -v "$(pwd)/grafana-dashboard.json:/var/lib/grafana/dashboards/heart-disease-api.json:ro" \
  -v "$(pwd)/grafana-dashboard-analytics.json:/var/lib/grafana/dashboards/heart-disease-api-analytics.json:ro" \
  grafana/grafana:latest

# Wait for startup
sleep 15

# Check status
docker ps | grep -E "prometheus|grafana"
```

---

### Issue 3: Dashboards Not Appearing in Grafana

**Solution: Manual Dashboard Import**

If dashboards don't auto-provision, import them manually:

1. **Access Grafana:** http://localhost:3000
2. **Login:** admin / admin
3. **Import Dashboard 1:**
   - Click "+" → "Import"
   - Click "Upload JSON file"
   - Select: `monitoring/grafana-dashboard.json`
   - Click "Load"
   - Select datasource: "Prometheus"
   - Click "Import"

4. **Import Dashboard 2:**
   - Repeat for `monitoring/grafana-dashboard-analytics.json`

---

### Issue 4: No Data in Dashboards

**Causes:**
- API not running
- Prometheus can't reach API
- No predictions made yet

**Solutions:**

**A. Ensure API is Running:**
```bash
# Check if API is running
curl http://localhost:8002/health

# If not, start it:
cd /Users/aashishr/codebase/mlso
source venv/bin/activate
PORT=8002 python src/api/app.py &
```

**B. Check Prometheus is Scraping:**
```bash
# Open Prometheus
open http://localhost:9090

# Go to: Status → Targets
# Check if "heart-disease-api" target is UP

# If DOWN, the API might not be accessible
# Try testing metrics endpoint:
curl http://localhost:8002/metrics
```

**C. Generate Test Data:**
```bash
# Make some predictions to generate metrics
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63, "sex": 1, "cp": 3, "trestbps": 145,
    "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150,
    "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
  }'

# Make multiple predictions
for i in {1..10}; do
  curl -X POST http://localhost:8002/predict \
    -H "Content-Type: application/json" \
    -d '{
      "age": 63, "sex": 1, "cp": 3, "trestbps": 145,
      "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150,
      "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
    }' > /dev/null 2>&1
  echo "Prediction $i sent"
  sleep 1
done
```

---

## 🎯 Step-by-Step Verification

### Step 1: Verify Docker
```bash
docker --version
# Should show: Docker version X.X.X

docker info | head -5
# Should show Docker info, not an error
```

### Step 2: Start Containers
```bash
cd /Users/aashishr/codebase/mlso/monitoring
./setup_grafana_manual.sh
```

### Step 3: Verify Containers Running
```bash
docker ps | grep -E "prometheus|grafana"

# Should show:
# heart-disease-prometheus  ... Up ... 0.0.0.0:9090->9090/tcp
# heart-disease-grafana     ... Up ... 0.0.0.0:3000->3000/tcp
```

### Step 4: Check Prometheus
```bash
curl http://localhost:9090/-/healthy
# Should return: Prometheus is Healthy.

open http://localhost:9090
# Should open Prometheus UI
```

### Step 5: Check Grafana
```bash
curl -I http://localhost:3000
# Should return: HTTP/1.1 302 Found

open http://localhost:3000
# Should open Grafana login page
```

### Step 6: Login to Grafana
- URL: http://localhost:3000
- Username: `admin`
- Password: `admin`
- Click "Log In"

### Step 7: Find Dashboards
- Click "Dashboards" (icon on left sidebar)
- Click "Browse"
- Look for folder: "Heart Disease API"
- OR search for: "Heart Disease"

### Step 8: If No Dashboards, Import Manually
- Click "+" → "Import"
- Upload `grafana-dashboard.json`
- Select "Prometheus" as datasource
- Click "Import"

---

## 📊 Alternative: Use Prometheus UI Directly

If Grafana is giving trouble, you can use Prometheus directly:

1. **Open Prometheus:** http://localhost:9090
2. **Click "Graph" tab**
3. **Run these queries:**

```promql
# Total predictions
sum(heart_disease_predictions_total)

# Prediction rate
rate(heart_disease_predictions_total[1m])

# Average latency (in ms)
(rate(heart_disease_prediction_latency_seconds_sum[5m]) / rate(heart_disease_prediction_latency_seconds_count[5m])) * 1000

# Error rate
rate(heart_disease_prediction_errors_total[5m])

# Active requests
heart_disease_active_requests

# Predictions by result
sum by (prediction_result) (heart_disease_predictions_total)
```

---

## 🔍 Debug Commands

### Check Container Logs
```bash
# Grafana logs
docker logs heart-disease-grafana

# Prometheus logs
docker logs heart-disease-prometheus

# Last 50 lines
docker logs heart-disease-grafana --tail 50
```

### Check If Dashboards Are Mounted
```bash
docker exec heart-disease-grafana ls -la /var/lib/grafana/dashboards/

# Should show:
# heart-disease-api.json
# heart-disease-api-analytics.json
```

### Check Datasource Configuration
```bash
docker exec heart-disease-grafana cat /etc/grafana/provisioning/datasources/datasource.yml
```

### Test Prometheus Connection from Grafana
```bash
# From inside Grafana container
docker exec heart-disease-grafana curl -I http://prometheus:9090
# Should return HTTP 200
```

---

## 🚀 Complete Fresh Start

If nothing works, do a complete reset:

```bash
# 1. Stop and remove everything
docker stop heart-disease-prometheus heart-disease-grafana
docker rm heart-disease-prometheus heart-disease-grafana
docker network rm monitoring

# 2. Remove volumes (if they exist)
docker volume rm monitoring_grafana-data monitoring_prometheus-data 2>/dev/null

# 3. Pull fresh images
docker pull prom/prometheus:latest
docker pull grafana/grafana:latest

# 4. Start fresh
cd /Users/aashishr/codebase/mlso/monitoring
./setup_grafana_manual.sh

# 5. Wait 30 seconds
sleep 30

# 6. Access Grafana
open http://localhost:3000
```

---

## 📱 Quick Status Check Script

Save this as `check_monitoring.sh`:

```bash
#!/bin/bash

echo "Monitoring Stack Status Check"
echo "=============================="
echo ""

echo "1. Docker Status:"
if docker info > /dev/null 2>&1; then
    echo "   ✓ Docker is running"
else
    echo "   ✗ Docker is not running"
    exit 1
fi
echo ""

echo "2. Container Status:"
if docker ps | grep -q heart-disease-prometheus; then
    echo "   ✓ Prometheus is running"
else
    echo "   ✗ Prometheus is not running"
fi

if docker ps | grep -q heart-disease-grafana; then
    echo "   ✓ Grafana is running"
else
    echo "   ✗ Grafana is not running"
fi
echo ""

echo "3. Service Accessibility:"
if curl -s http://localhost:9090/-/healthy > /dev/null 2>&1; then
    echo "   ✓ Prometheus is accessible"
else
    echo "   ✗ Prometheus is not accessible"
fi

if curl -s -I http://localhost:3000 | grep -q "HTTP"; then
    echo "   ✓ Grafana is accessible"
else
    echo "   ✗ Grafana is not accessible"
fi
echo ""

echo "4. API Status:"
if curl -s http://localhost:8002/health > /dev/null 2>&1; then
    echo "   ✓ API is running"
else
    echo "   ✗ API is not running"
fi
echo ""

echo "5. Metrics Endpoint:"
if curl -s http://localhost:8002/metrics > /dev/null 2>&1; then
    echo "   ✓ Metrics are available"
else
    echo "   ✗ Metrics are not available"
fi
echo ""

echo "Access URLs:"
echo "  Grafana:    http://localhost:3000"
echo "  Prometheus: http://localhost:9090"
echo "  API:        http://localhost:8002"
echo ""
```

---

## ✅ Final Checklist

Before reporting dashboards are not visible, verify:

- [ ] Docker Desktop is running
- [ ] `docker ps` shows prometheus and grafana containers
- [ ] http://localhost:3000 loads Grafana login page
- [ ] Can login with admin/admin
- [ ] Tried searching for "Heart Disease" in dashboard search
- [ ] Checked Dashboards → Browse
- [ ] Tried manual dashboard import
- [ ] API is running on port 8002
- [ ] Made at least 10 test predictions
- [ ] Prometheus shows API as "UP" target
- [ ] Waited at least 2 minutes for data to appear

---

## 📞 Still Not Working?

**Try this simple test:**

```bash
# 1. Open terminal, run:
cd /Users/aashishr/codebase/mlso/monitoring
docker run -d --name test-grafana -p 3000:3000 grafana/grafana:latest
sleep 20
open http://localhost:3000

# 2. If Grafana opens:
#    - The issue is with configuration files
#    - Try manual import method above

# 3. If Grafana doesn't open:
#    - Docker networking issue
#    - Try restarting Docker Desktop

# 4. Cleanup:
docker stop test-grafana && docker rm test-grafana
```

---

**Need Help?** Run the check script:
```bash
cd /Users/aashishr/codebase/mlso/monitoring
chmod +x check_monitoring.sh
./check_monitoring.sh
```

This will show exactly what's working and what's not!

