# 🎨 Grafana Dashboard Setup Guide

**Date:** December 28, 2025  
**Status:** ✅ **Complete - 2 Dashboards Created**

---

## 📊 Dashboards Created

### 1. **Heart Disease API - Production Monitoring**
**File:** `monitoring/grafana-dashboard.json`

**Panels (13 total):**
1. **Total Predictions** (Stat) - Cumulative prediction count
2. **Positive Predictions** (Stat) - Red colored stat
3. **Negative Predictions** (Stat) - Green colored stat
4. **Model Status** (Stat) - Background color changes: Red=Not Loaded, Green=Loaded
5. **Avg Response Time** (Stat) - Color coded: Green<100ms, Yellow<500ms, Red>500ms
6. **Active Requests** (Stat) - Current concurrent requests
7. **Prediction Rate** (Time Series) - Requests per second graph
8. **Response Time Percentiles** (Time Series) - p50, p90, p95, p99 lines
9. **Prediction Results Distribution** (Pie Chart) - Positive vs Negative donut chart
10. **Error Rate by Type** (Time Series) - Errors grouped by type with alerting
11. **Active Requests Over Time** (Time Series) - Real-time concurrent load
12. **Total Predictions Timeline** (Time Series) - Cumulative growth
13. **API Health Status** (Stat) - UP/DOWN indicator

**Features:**
- ✅ Auto-refresh every 10 seconds
- ✅ Default time range: Last 15 minutes
- ✅ Threshold-based coloring
- ✅ Alert annotations
- ✅ Professional layout

---

### 2. **Heart Disease API - Detailed Analytics**
**File:** `monitoring/grafana-dashboard-analytics.json`

**Panels (10 total):**
1. **Prediction Success Rate** (Gauge) - Percentage with color thresholds
2. **Predictions Per Minute** (Stat) - Rate calculation
3. **P99 Latency Trend** (Stat) - 99th percentile response time
4. **Error Count Last Hour** (Stat) - Hourly error aggregation
5. **Hourly Prediction Volume** (Bar Gauge) - Current vs previous hour comparison
6. **Latency Heatmap** (Heatmap) - Response time distribution visualization
7. **Positive vs Negative Over Time** (Time Series) - Separate colored lines
8. **Response Time by Percentile** (Stat) - p50, p75, p90, p95, p99 all visible
9. **Error Breakdown** (Table) - Detailed error types with counts
10. **Throughput Analysis** (Time Series) - Current, 5min avg, 15min avg comparison

**Features:**
- ✅ Auto-refresh every 30 seconds
- ✅ Default time range: Last 1 hour
- ✅ Advanced visualizations (heatmap, gauge, bar gauge)
- ✅ Template variable for time range selection
- ✅ Comparative analytics

---

## 🚀 How to Access Dashboards

### Step 1: Start Monitoring Stack

```bash
cd /Users/aashishr/codebase/mlso/monitoring
./start_monitoring.sh
```

**Or manually:**
```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

### Step 2: Wait for Services to Start

```bash
# Check containers are running
docker ps | grep -E "prometheus|grafana"

# Should show:
# heart-disease-prometheus
# heart-disease-grafana
```

### Step 3: Access Grafana

**URL:** http://localhost:3000

**Login Credentials:**
- Username: `admin`
- Password: `admin`

**First Login:**
- You'll be prompted to change password
- You can skip this or set a new password

### Step 4: Navigate to Dashboards

**Option A: From Home**
1. Click "Dashboards" in left sidebar
2. Click "Browse"
3. Open folder: "Heart Disease API"
4. You'll see both dashboards:
   - Heart Disease API - Production Monitoring
   - Heart Disease API - Detailed Analytics

**Option B: Direct Links**
- Production: http://localhost:3000/d/heart-disease-api
- Analytics: http://localhost:3000/d/heart-disease-api-analytics

---

## 📈 Dashboard Features Explained

### Production Monitoring Dashboard

#### **Top Row - Key Metrics**
```
┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│ Total        │ Positive     │ Negative     │ Model        │ Avg Response │ Active       │
│ Predictions  │ Predictions  │ Predictions  │ Status       │ Time         │ Requests     │
│   1,234      │    543       │    691       │ 🟢 LOADED   │   32.45 ms   │      2       │
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

#### **Middle Row - Performance**
```
┌────────────────────────────────────┬────────────────────────────────────┐
│ Prediction Rate (requests/sec)    │ Response Time Percentiles          │
│ [Line graph with positive/negative]│ [Multi-line: p50, p90, p95, p99]  │
└────────────────────────────────────┴────────────────────────────────────┘
```

#### **Bottom Rows - Analysis**
```
┌────────────────────────┬────────────────────────┬────────────────────────┐
│ Prediction Distribution│ Error Rate by Type     │ Active Requests        │
│ [Donut chart]          │ [Line graph]           │ [Time series]          │
└────────────────────────┴────────────────────────┴────────────────────────┘

┌────────────────────────────────────┬────────────────────────────────────┐
│ Total Predictions Timeline         │ API Health Status                  │
│ [Cumulative growth line]           │ [UP/DOWN indicator]                │
└────────────────────────────────────┴────────────────────────────────────┘
```

---

### Detailed Analytics Dashboard

#### **Top Row - KPIs**
```
┌───────────────┬───────────────┬───────────────┬───────────────┐
│ Success Rate  │ Predictions   │ P99 Latency   │ Error Count   │
│   99.8%       │ Per Minute    │    45.2 ms    │ (Last Hour)   │
│ [Gauge]       │     58.3      │ [Stat]        │      0        │
└───────────────┴───────────────┴───────────────┴───────────────┘
```

#### **Second Row - Comparisons**
```
┌────────────────────────────────────┬────────────────────────────────────┐
│ Hourly Prediction Volume           │ Latency Heatmap                    │
│ [Bar gauge: Current vs Previous]   │ [Heat map of response times]       │
└────────────────────────────────────┴────────────────────────────────────┘
```

#### **Third Row - Trends**
```
┌────────────────────────────────────┬────────────────────────────────────┐
│ Positive vs Negative Over Time     │ Response Time by Percentile        │
│ [Colored lines: Red vs Green]      │ [p50, p75, p90, p95, p99 stats]   │
└────────────────────────────────────┴────────────────────────────────────┘
```

#### **Fourth Row - Details**
```
┌────────────────────────────────────┬────────────────────────────────────┐
│ Error Breakdown                    │ Throughput Analysis                │
│ [Table with error types]           │ [Current + averages comparison]    │
└────────────────────────────────────┴────────────────────────────────────┘
```

---

## 🎯 Use Cases

### Use Case 1: Real-Time Monitoring
**Dashboard:** Production Monitoring  
**Focus:** Top row stats + Prediction Rate graph  
**Action:** Keep this dashboard open during deployments

### Use Case 2: Performance Analysis
**Dashboard:** Detailed Analytics  
**Focus:** Response Time by Percentile + Latency Heatmap  
**Action:** Identify performance bottlenecks

### Use Case 3: Error Investigation
**Dashboard:** Either  
**Focus:** Error Rate panel + Error Breakdown table  
**Action:** Drill down into specific error types

### Use Case 4: Capacity Planning
**Dashboard:** Detailed Analytics  
**Focus:** Throughput Analysis + Predictions Per Minute  
**Action:** Determine if scaling is needed

### Use Case 5: Model Health Check
**Dashboard:** Production Monitoring  
**Focus:** Model Status + API Health Status  
**Action:** Ensure model is loaded and API is up

---

## 🔧 Customization

### Change Refresh Rate

**In Grafana UI:**
1. Click time picker (top right)
2. Select refresh interval dropdown
3. Choose: 5s, 10s, 30s, 1m, etc.

**In JSON:**
```json
"refresh": "10s"  // Change to "5s", "30s", "1m", etc.
```

### Change Time Range

**In UI:**
- Click time picker
- Select from presets or custom range

**In JSON:**
```json
"time": {
  "from": "now-15m",  // Change to "now-1h", "now-6h", etc.
  "to": "now"
}
```

### Add New Panel

1. Click "Add panel" button
2. Select visualization type
3. Write PromQL query
4. Configure display options
5. Save dashboard

---

## 📊 PromQL Queries Used

### Prediction Metrics
```promql
# Total predictions
sum(heart_disease_predictions_total)

# Prediction rate (per second)
sum(rate(heart_disease_predictions_total[1m]))

# Predictions by result
sum by (prediction_result) (heart_disease_predictions_total)
```

### Performance Metrics
```promql
# Average latency
rate(heart_disease_prediction_latency_seconds_sum[5m]) / rate(heart_disease_prediction_latency_seconds_count[5m])

# P99 latency
histogram_quantile(0.99, rate(heart_disease_prediction_latency_seconds_bucket[5m]))

# All percentiles
histogram_quantile(0.50, rate(heart_disease_prediction_latency_seconds_bucket[5m]))
histogram_quantile(0.90, rate(heart_disease_prediction_latency_seconds_bucket[5m]))
histogram_quantile(0.95, rate(heart_disease_prediction_latency_seconds_bucket[5m]))
```

### Error Metrics
```promql
# Error rate
rate(heart_disease_prediction_errors_total[5m])

# Errors by type
sum by (error_type) (heart_disease_prediction_errors_total)

# Error count last hour
sum(increase(heart_disease_prediction_errors_total[1h]))
```

### System Metrics
```promql
# Model status
heart_disease_model_info

# Active requests
heart_disease_active_requests

# API health
up{job="heart-disease-api"}
```

---

## 🎨 Color Coding

### Thresholds

**Response Time:**
- 🟢 Green: < 100ms (Good)
- 🟡 Yellow: 100-500ms (Acceptable)
- 🔴 Red: > 500ms (Poor)

**Success Rate:**
- 🔴 Red: < 90%
- 🟡 Yellow: 90-99%
- 🟢 Green: > 99%

**Model Status:**
- 🔴 Red: Not Loaded (0)
- 🟢 Green: Loaded (1)

**Errors:**
- 🟢 Green: 0 errors
- 🟡 Yellow: 1-10 errors
- 🔴 Red: > 10 errors

---

## 🚨 Alerts Configured

### High Error Rate Alert
**Panel:** Error Rate by Type  
**Condition:** Error rate > 0.1 errors/sec  
**Duration:** 5 minutes  
**Action:** Alert fires and shows in annotations

**How to Configure:**
1. Edit panel
2. Go to "Alert" tab
3. Set conditions and notifications
4. Save

---

## 📸 Screenshots Checklist

For demonstration, capture these views:

- [ ] **Grafana Login Page**
- [ ] **Dashboard List** (showing both dashboards)
- [ ] **Production Monitoring** - Full view
- [ ] **Production Monitoring** - Top row (stats)
- [ ] **Production Monitoring** - Prediction rate graph
- [ ] **Production Monitoring** - Pie chart
- [ ] **Detailed Analytics** - Full view
- [ ] **Detailed Analytics** - Success rate gauge
- [ ] **Detailed Analytics** - Latency heatmap
- [ ] **Detailed Analytics** - Error breakdown table
- [ ] **Panel Edit View** - Showing query
- [ ] **Prometheus Data Source** - Configuration

---

## ✅ Verification Steps

### 1. Check Containers Running
```bash
docker ps | grep -E "prometheus|grafana"
```
✅ Should show 2 containers

### 2. Check Grafana Accessible
```bash
curl -I http://localhost:3000
```
✅ Should return HTTP 200

### 3. Check Dashboards Mounted
```bash
docker exec heart-disease-grafana ls -la /var/lib/grafana/dashboards/
```
✅ Should show:
- heart-disease-api.json
- heart-disease-api-analytics.json

### 4. Login to Grafana
- Open http://localhost:3000
- Login with admin/admin
✅ Should access successfully

### 5. View Dashboards
- Navigate to Dashboards → Browse
- Open Heart Disease API folder
✅ Should see both dashboards

### 6. Check Data Flowing
- Ensure API is running
- Make test predictions
- View dashboard panels
✅ Metrics should update

---

## 🎯 Quick Commands

### Start Monitoring
```bash
cd monitoring
./start_monitoring.sh
```

### Stop Monitoring
```bash
docker-compose -f docker-compose.monitoring.yml down
```

### Restart Monitoring
```bash
docker-compose -f docker-compose.monitoring.yml restart
```

### View Logs
```bash
# Grafana logs
docker logs heart-disease-grafana -f

# Prometheus logs
docker logs heart-disease-prometheus -f
```

### Reset Grafana Password
```bash
docker exec -it heart-disease-grafana grafana-cli admin reset-admin-password newpassword
```

---

## 📚 Resources

### Grafana Documentation
- Official Docs: https://grafana.com/docs/
- Panel Types: https://grafana.com/docs/grafana/latest/panels/
- PromQL Guide: https://grafana.com/docs/grafana/latest/datasources/prometheus/

### Dashboard Examples
- Official Library: https://grafana.com/grafana/dashboards/
- Prometheus Dashboards: https://grafana.com/grafana/dashboards/?dataSource=prometheus

---

## 🎉 Summary

**Dashboards Created:** 2  
**Total Panels:** 23  
**Metrics Tracked:** 15+  
**Visualizations:** Stats, Gauges, Time Series, Pie Charts, Heatmaps, Tables, Bar Gauges  

**Access:**
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090
- API Metrics: http://localhost:8002/metrics

**Status:** ✅ **Ready to Use!**

---

**Next Steps:**
1. Start monitoring stack: `./start_monitoring.sh`
2. Access Grafana: http://localhost:3000
3. Explore both dashboards
4. Generate API traffic to see live metrics
5. Take screenshots for documentation!

🎨 **Your beautiful Grafana dashboards are ready!**

