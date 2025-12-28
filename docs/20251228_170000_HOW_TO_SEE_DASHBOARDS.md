# ✅ FINAL SOLUTION: How to See Grafana Dashboards

**Problem:** Can't see dashboards in Grafana  
**Solution:** Follow these exact steps

---

## 🎯 QUICK START (Copy & Paste These Commands)

### Step 1: Check Docker is Running
```bash
docker info
```
**If this fails:** Start Docker Desktop app and wait 1 minute, then retry

### Step 2: Start Monitoring Stack
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
echo "Waiting for services to start..."
sleep 20
```

### Step 3: Verify Containers are Running
```bash
docker ps | grep -E "prometheus|grafana"
```
**You should see 2 containers running**

### Step 4: Open Grafana
```bash
open http://localhost:3000
```
**Or manually open in browser:** http://localhost:3000

### Step 5: Login
- Username: `admin`
- Password: `admin`
- Click "Log In"
- (Skip password change if prompted)

### Step 6: Find Dashboards

**Option A: Browse**
1. Click "Dashboards" icon (📊) in left sidebar
2. Click "Browse"
3. Look for folder: "Heart Disease API"
4. Click on the folder
5. You'll see 2 dashboards:
   - Heart Disease API - Production Monitoring
   - Heart Disease API - Detailed Analytics

**Option B: Search**
1. Click search icon (🔍) or press "/"
2. Type: "Heart Disease"
3. Click on dashboard from results

### Step 7: View Dashboard

If you see panels but **NO DATA**:

**A. Start the API:**
```bash
cd /Users/aashishr/codebase/mlso
source venv/bin/activate
PORT=8002 python src/api/app.py &
```

**B. Generate Test Data:**
```bash
# Make 20 test predictions
for i in {1..20}; do
  curl -X POST http://localhost:8002/predict \
    -H "Content-Type: application/json" \
    -d '{
      "age": 63, "sex": 1, "cp": 3, "trestbps": 145,
      "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150,
      "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
    }' > /dev/null 2>&1
  echo "Prediction $i"
  sleep 1
done

echo "✓ Generated 20 predictions"
```

**C. Wait 30 seconds and refresh Grafana dashboard**

---

## 🔍 If Dashboards Still Don't Appear

### Manual Import Method:

1. **Download dashboard JSON to your desktop:**
   ```bash
   cp /Users/aashishr/codebase/mlso/monitoring/grafana-dashboard.json ~/Desktop/
   cp /Users/aashishr/codebase/mlso/monitoring/grafana-dashboard-analytics.json ~/Desktop/
   ```

2. **In Grafana:**
   - Click "+" icon in left sidebar
   - Click "Import dashboard"
   - Click "Upload JSON file"
   - Select `grafana-dashboard.json` from Desktop
   - In "Prometheus" dropdown, select "Prometheus"
   - Click "Import"
   
3. **Repeat for second dashboard** (`grafana-dashboard-analytics.json`)

---

## 📊 What You Should See

### Production Monitoring Dashboard:

**Top Row (6 stat panels):**
- Total Predictions: Shows cumulative count
- Positive Predictions: Red number
- Negative Predictions: Green number
- Model Status: Green box saying "LOADED"
- Avg Response Time: Number in ms (should be green if < 100ms)
- Active Requests: Current concurrent requests

**Below:**
- Graphs showing prediction rate over time
- Response time percentiles (p50, p90, p95, p99)
- Pie chart of positive vs negative predictions
- Error rate graph
- Active requests timeline

### Detailed Analytics Dashboard:

**Top Row:**
- Success Rate gauge (should be near 100%)
- Predictions per minute stat
- P99 latency stat
- Error count stat

**Below:**
- Bar gauge comparing current hour vs previous
- Heatmap showing latency distribution
- Time series of positive vs negative predictions
- Table showing error breakdown
- Throughput analysis graph

---

## ✅ Verification Commands

### Check Everything is Working:
```bash
cd /Users/aashishr/codebase/mlso/monitoring
./check_monitoring.sh
```

This will tell you:
- ✓ If Docker is running
- ✓ If containers are running
- ✓ If services are accessible
- ✓ If API is running
- ✓ If metrics are available

---

## 🚀 All-in-One Script

Save time with the automated script:

```bash
cd /Users/aashishr/codebase/mlso/monitoring
./setup_grafana_manual.sh
```

This script:
1. Checks Docker is running
2. Stops any existing containers
3. Starts Prometheus
4. Starts Grafana
5. Waits for services
6. Shows you the access URLs

---

## 📞 Still Not Working?

**Run this diagnostic:**

```bash
echo "=== Docker Check ==="
docker --version
docker info | head -3

echo ""
echo "=== Container Check ==="
docker ps -a | grep -E "prometheus|grafana"

echo ""
echo "=== Port Check ==="
lsof -i :3000
lsof -i :9090

echo ""
echo "=== Service Check ==="
curl -I http://localhost:3000
curl http://localhost:9090/-/healthy
```

**Send me the output** and I can help debug further.

---

## 🎯 Expected Behavior

After running the setup:

1. **Prometheus UI** should open at: http://localhost:9090
   - Go to Status → Targets
   - You should see "heart-disease-api" (may be DOWN if API not running)

2. **Grafana UI** should open at: http://localhost:3000
   - Login page appears
   - After login, see Grafana home page
   - Dashboards menu shows "Heart Disease API" folder

3. **Dashboards show data** after:
   - API is running on port 8002
   - At least 10 predictions have been made
   - Waited 1-2 minutes for metrics to populate

---

## 📝 Common Mistakes

### ❌ Mistake 1: Docker not running
**Fix:** Start Docker Desktop and wait for it to fully start

### ❌ Mistake 2: Using wrong URL
**Fix:** Use http://localhost:3000 NOT http://0.0.0.0:3000

### ❌ Mistake 3: Looking in wrong place
**Fix:** Go to Dashboards → Browse, NOT the home screen

### ❌ Mistake 4: API not running
**Fix:** Start API with: `PORT=8002 python src/api/app.py`

### ❌ Mistake 5: No test data
**Fix:** Make predictions with curl commands above

### ❌ Mistake 6: Impatient
**Fix:** Wait 1-2 minutes after first predictions for data to appear

---

## 🎉 Success Checklist

You'll know it's working when you can check all these:

- [ ] `docker ps` shows 2 containers (prometheus and grafana)
- [ ] http://localhost:3000 loads Grafana
- [ ] Can login with admin/admin
- [ ] See "Heart Disease API" in Dashboards → Browse
- [ ] Click on dashboard and see panels (may be empty at first)
- [ ] API running at http://localhost:8002
- [ ] After making predictions, panels show data
- [ ] Numbers in stat panels update
- [ ] Graphs show lines

---

## 💡 Pro Tips

1. **Keep Grafana open** while running API - watch metrics update in real-time
2. **Use auto-refresh** - Set to 5s or 10s in time picker
3. **Generate continuous traffic** - Use a loop to keep making predictions
4. **Check Prometheus first** - If queries work there, Grafana will work too
5. **Take screenshots** - Document your working dashboards!

---

## 🔗 Quick Links

- **Grafana:** http://localhost:3000
- **Prometheus:** http://localhost:9090
- **API Health:** http://localhost:8002/health
- **API Metrics:** http://localhost:8002/metrics

---

**TL;DR:**
```bash
cd /Users/aashishr/codebase/mlso/monitoring
./setup_grafana_manual.sh
# Wait 30 seconds
open http://localhost:3000
# Login: admin/admin
# Go to: Dashboards → Browse → Heart Disease API
```

**That's it! Your dashboards should be visible now! 🎉**

