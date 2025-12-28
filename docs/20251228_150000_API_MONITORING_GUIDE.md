# 📊 API Monitoring & Logging - Complete Guide

**Date:** December 28, 2025  
**Status:** ✅ **Fully Implemented**

---

## 🎯 Overview

Complete monitoring and logging solution for the Heart Disease API, featuring:
- **Comprehensive Request/Response Logging**
- **Prometheus Metrics Collection**
- **Grafana Dashboards**
- **Real-time Terminal Dashboard**
- **API Health Monitoring**

---

## 📋 What Was Implemented

### 1. **Enhanced API Logging** ✅

#### Request Logging:
- HTTP method and path
- Client IP address
- User-Agent
- Request timestamp

#### Response Logging:
- HTTP status code
- Response duration (ms)
- Response size (bytes)
- Completion timestamp

#### Prediction Logging:
- Input features (sample)
- Prediction result
- Confidence scores
- Risk level
- Processing time

**Location:** `src/api/app.py`

---

### 2. **Prometheus Metrics** ✅

#### Metrics Collected:

**Counters:**
- `heart_disease_predictions_total` - Total predictions made
  - Labels: `model_version`, `prediction_result` (positive/negative)
- `heart_disease_prediction_errors_total` - Total errors
  - Labels: `error_type`

**Histograms:**
- `heart_disease_prediction_latency_seconds` - Response time distribution
  - Labels: `model_version`

**Gauges:**
- `heart_disease_model_info` - Model status (0=not loaded, 1=loaded)
  - Labels: `model_version`, `model_type`
- `heart_disease_active_requests` - Current active requests

**Metrics Endpoint:** `http://localhost:8002/metrics`

---

### 3. **Monitoring Stack** ✅

#### Components:
1. **Prometheus** - Metrics collection and storage
2. **Grafana** - Visualization and dashboards
3. **Terminal Dashboard** - Simple real-time monitoring

**Files Created:**
- `monitoring/prometheus.yml` - Prometheus configuration
- `monitoring/grafana-dashboard.json` - Grafana dashboard
- `monitoring/grafana-datasource.yml` - Grafana data source
- `monitoring/grafana-dashboard-provider.yml` - Dashboard provisioning
- `monitoring/docker-compose.monitoring.yml` - Docker setup
- `monitoring/dashboard.py` - Terminal dashboard script

---

## 🚀 Quick Start

### Option 1: Full Monitoring Stack (Prometheus + Grafana)

#### Step 1: Start Monitoring Stack
```bash
cd /Users/aashishr/codebase/mlso/monitoring
docker-compose -f docker-compose.monitoring.yml up -d
```

**Services Started:**
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

#### Step 2: Start API (if not running)
```bash
cd /Users/aashishr/codebase/mlso
source venv/bin/activate
PORT=8002 python src/api/app.py
```

#### Step 3: Access Dashboards

**Grafana Dashboard:**
1. Open http://localhost:3000
2. Login: username=`admin`, password=`admin`
3. Navigate to Dashboards → Heart Disease API Monitoring

**Prometheus:**
1. Open http://localhost:9090
2. Status → Targets (check API is being scraped)
3. Graph tab - query metrics

#### Step 4: Generate Traffic
```bash
# Test prediction
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63, "sex": 1, "cp": 3, "trestbps": 145,
    "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150,
    "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
  }'
```

---

### Option 2: Terminal Dashboard (Lightweight)

#### Step 1: Start Prometheus Only
```bash
cd /Users/aashishr/codebase/mlso/monitoring
docker run -d --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

#### Step 2: Run Terminal Dashboard
```bash
cd /Users/aashishr/codebase/mlso
source venv/bin/activate
python monitoring/dashboard.py
```

**Terminal Dashboard Features:**
```
================================================================================
                    HEART DISEASE API MONITORING DASHBOARD
================================================================================
Timestamp: 2025-12-28 16:30:45
Prometheus: http://localhost:9090
API: http://localhost:8002
--------------------------------------------------------------------------------

📊 SYSTEM STATUS
--------------------------------------------------------------------------------
API Status:          🟢 HEALTHY
Model Status:        🟢 LOADED
Active Requests:     2

📈 PREDICTION METRICS
--------------------------------------------------------------------------------
Total Predictions:   1,234
  • Positive:        543 (44.0%)
  • Negative:        691 (56.0%)

⚡ PERFORMANCE METRICS
--------------------------------------------------------------------------------
Avg Response Time:   🟢 32.45 ms
Error Rate:          🟢 0.0000 errors/sec

================================================================================
Press Ctrl+C to exit | Refreshing every 5 seconds...
================================================================================
```

---

### Option 3: View Logs Only

#### View API Logs:
```bash
# If running in terminal
# Logs appear in console output

# If running in background
tail -f api.log

# Or check Docker logs
docker logs heart-disease-api
```

#### Log Format:
```
2025-12-28 16:30:45,123 - __main__ - INFO - Incoming request: POST /predict from 127.0.0.1 User-Agent: curl/7.79.1
2025-12-28 16:30:45,125 - __main__ - INFO - Prediction request received with features: age=63, sex=1, cp=3
2025-12-28 16:30:45,157 - __main__ - INFO - Prediction completed: result=positive, confidence=0.8117, risk_level=Very High, processing_time=32.45ms
2025-12-28 16:30:45,158 - __main__ - INFO - Request completed: POST /predict Status: 200 Duration: 35.12ms Size: 256 bytes
```

---

## 📊 Grafana Dashboard Panels

### Dashboard Layout:

#### Row 1: Overview
1. **Total Predictions** (Stat)
   - Aggregated count of all predictions
   
2. **Prediction Rate** (Graph)
   - Requests per minute by result type

#### Row 2: Performance
3. **Average Response Time** (Stat)
   - Mean latency in seconds
   
4. **Response Time Distribution** (Graph)
   - p50, p90, p99 percentiles

#### Row 3: Errors & Load
5. **Error Rate** (Graph)
   - Errors per second by type
   - Alert: triggers if > 0.1 errors/sec
   
6. **Active Requests** (Graph)
   - Current concurrent requests

#### Row 4: Results & Status
7. **Prediction Results Distribution** (Pie Chart)
   - Breakdown of positive vs negative predictions
   
8. **Model Status** (Stat)
   - Green: Model loaded
   - Red: Model not loaded

---

## 🔍 Prometheus Queries

### Useful PromQL Queries:

#### Total Predictions:
```promql
sum(heart_disease_predictions_total)
```

#### Prediction Rate (per second):
```promql
rate(heart_disease_predictions_total[1m])
```

#### Average Latency:
```promql
rate(heart_disease_prediction_latency_seconds_sum[5m]) 
/ 
rate(heart_disease_prediction_latency_seconds_count[5m])
```

#### Error Rate:
```promql
rate(heart_disease_prediction_errors_total[5m])
```

#### 95th Percentile Latency:
```promql
histogram_quantile(0.95, rate(heart_disease_prediction_latency_seconds_bucket[5m]))
```

#### Predictions by Result:
```promql
sum by (prediction_result) (heart_disease_predictions_total)
```

---

## 📈 Monitoring Use Cases

### 1. Performance Monitoring

**Check if API is fast enough:**
```promql
# Alert if p99 latency > 500ms
histogram_quantile(0.99, rate(heart_disease_prediction_latency_seconds_bucket[5m])) > 0.5
```

### 2. Error Detection

**Alert on high error rate:**
```promql
# Alert if error rate > 1%
rate(heart_disease_prediction_errors_total[5m]) > 0.01
```

### 3. Load Monitoring

**Check current load:**
```promql
# Current requests per second
rate(heart_disease_predictions_total[1m])

# Active concurrent requests
heart_disease_active_requests
```

### 4. Model Health

**Ensure model is loaded:**
```promql
# Alert if model is not loaded
heart_disease_model_info == 0
```

### 5. Prediction Analysis

**Analyze prediction distribution:**
```promql
# Percentage of positive predictions
sum(heart_disease_predictions_total{prediction_result="positive"}) 
/ 
sum(heart_disease_predictions_total) * 100
```

---

## 🛠️ Configuration

### Prometheus Configuration

**File:** `monitoring/prometheus.yml`

**Key Settings:**
- `scrape_interval: 15s` - How often to collect metrics
- `evaluation_interval: 15s` - How often to evaluate rules
- Target: API at `host.docker.internal:8002/metrics`

**Modify scrape interval:**
```yaml
scrape_configs:
  - job_name: 'heart-disease-api'
    scrape_interval: 10s  # Change to 5s, 30s, etc.
```

### Grafana Configuration

**Default Credentials:**
- Username: `admin`
- Password: `admin` (change on first login)

**Dashboard Auto-Refresh:**
- Current: 10 seconds
- Modify in Grafana UI: Dashboard Settings → Time Options

---

## 📝 Log Analysis

### View Specific Log Types:

#### Prediction Logs Only:
```bash
tail -f api.log | grep "Prediction completed"
```

#### Error Logs Only:
```bash
tail -f api.log | grep "ERROR"
```

#### Request Duration > 100ms:
```bash
tail -f api.log | grep "Duration:" | awk '{if ($NF > 100) print}'
```

### Log Aggregation:

Create a log analysis script:
```bash
#!/bin/bash
# analyze_logs.sh

echo "API Log Analysis"
echo "================"
echo ""
echo "Total Requests:"
grep "Request completed" api.log | wc -l

echo ""
echo "Status Code Distribution:"
grep "Request completed" api.log | awk '{print $(NF-5)}' | sort | uniq -c

echo ""
echo "Average Response Time:"
grep "Duration:" api.log | awk '{sum+=$(NF-1); count++} END {print sum/count "ms"}'

echo ""
echo "Error Count:"
grep "ERROR" api.log | wc -l
```

---

## 🚨 Alerting

### Prometheus Alerting Rules

Create `monitoring/alerts.yml`:
```yaml
groups:
  - name: api_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(heart_disease_prediction_errors_total[5m]) > 0.01
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/sec"
      
      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(heart_disease_prediction_latency_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "p99 latency is {{ $value }}s"
      
      - alert: ModelNotLoaded
        expr: heart_disease_model_info == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Model is not loaded"
          description: "Prediction model is unavailable"
```

---

## 🔧 Troubleshooting

### Issue 1: Prometheus Can't Scrape API

**Symptoms:** Targets show as "DOWN" in Prometheus

**Solutions:**

1. **Check API is running:**
   ```bash
   curl http://localhost:8002/health
   ```

2. **Check metrics endpoint:**
   ```bash
   curl http://localhost:8002/metrics
   ```

3. **Fix Docker networking (Mac/Windows):**
   ```yaml
   # In prometheus.yml, use:
   - targets: ['host.docker.internal:8002']
   ```

4. **Fix Docker networking (Linux):**
   ```yaml
   # In prometheus.yml, use:
   - targets: ['172.17.0.1:8002']
   ```

### Issue 2: Grafana Dashboard Not Showing Data

**Solutions:**

1. **Check Prometheus data source:**
   - Grafana → Configuration → Data Sources
   - Test connection

2. **Check time range:**
   - Ensure dashboard time range includes current data
   - Try "Last 5 minutes"

3. **Check metrics exist:**
   - Go to Prometheus → Graph
   - Query: `heart_disease_predictions_total`

### Issue 3: Terminal Dashboard Shows No Data

**Solutions:**

1. **Check Prometheus is running:**
   ```bash
   curl http://localhost:9090/-/healthy
   ```

2. **Generate some traffic:**
   ```bash
   curl -X POST http://localhost:8002/predict -H "Content-Type: application/json" -d '{...}'
   ```

3. **Check Python dependencies:**
   ```bash
   pip install requests
   ```

---

## 📊 Monitoring Best Practices

### 1. **Set Up Alerts**
- Configure email/Slack notifications
- Set appropriate thresholds
- Test alert firing

### 2. **Regular Review**
- Check dashboards daily
- Analyze trends weekly
- Adjust baselines monthly

### 3. **Log Rotation**
- Prevent disk space issues
- Archive old logs
- Set retention policies

### 4. **Backup Metrics**
- Regular Prometheus data backup
- Export important dashboards
- Document alert rules

### 5. **Performance Baselines**
- Document normal behavior
- Set SLOs (Service Level Objectives)
- Track SLIs (Service Level Indicators)

---

## ✅ Verification Checklist

- [ ] API is running on port 8002
- [ ] Prometheus is running on port 9090
- [ ] Grafana is running on port 3000
- [ ] Metrics endpoint accessible: `curl http://localhost:8002/metrics`
- [ ] Prometheus scraping API: Check http://localhost:9090/targets
- [ ] Grafana dashboard visible: http://localhost:3000
- [ ] Terminal dashboard working: `python monitoring/dashboard.py`
- [ ] Logs are being written
- [ ] Test prediction generates metrics
- [ ] Grafana panels show data

---

## 🎯 Quick Commands

### Start Everything:
```bash
# 1. Start monitoring stack
cd monitoring && docker-compose -f docker-compose.monitoring.yml up -d

# 2. Start API
cd .. && source venv/bin/activate && PORT=8002 python src/api/app.py &

# 3. Open dashboards
open http://localhost:3000  # Grafana
open http://localhost:9090  # Prometheus

# 4. Or use terminal dashboard
python monitoring/dashboard.py
```

### Stop Everything:
```bash
# Stop monitoring stack
cd monitoring && docker-compose -f docker-compose.monitoring.yml down

# Stop API
pkill -f "python src/api/app.py"
```

### Generate Test Traffic:
```bash
# Single prediction
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1}'

# Health check
curl http://localhost:8002/health

# View metrics
curl http://localhost:8002/metrics
```

---

## 📚 Additional Resources

### Prometheus:
- Official Docs: https://prometheus.io/docs/
- PromQL Guide: https://prometheus.io/docs/prometheus/latest/querying/basics/
- Best Practices: https://prometheus.io/docs/practices/

### Grafana:
- Official Docs: https://grafana.com/docs/
- Dashboard Gallery: https://grafana.com/grafana/dashboards/
- Alerting Guide: https://grafana.com/docs/grafana/latest/alerting/

### Python Logging:
- Logging Module: https://docs.python.org/3/library/logging.html
- Best Practices: https://docs.python-guide.org/writing/logging/

---

## 🎉 Summary

**Status:** ✅ **Complete Monitoring Solution Implemented**

**What You Have:**
- ✅ Comprehensive API logging
- ✅ Prometheus metrics collection
- ✅ Grafana visualization dashboards
- ✅ Terminal monitoring dashboard
- ✅ Docker-based monitoring stack
- ✅ Complete documentation

**Access URLs:**
- API: http://localhost:8002
- Metrics: http://localhost:8002/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

**Next Steps:**
1. Start monitoring stack
2. Generate API traffic
3. View dashboards
4. Set up alerts
5. Monitor in production!

📊 **Your API is now fully monitored!**

