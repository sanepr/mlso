# MLflow Port Conflict - Quick Fix

## Error
```
Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:5000 -> 127.0.0.1:0: listen tcp 0.0.0.0:5000: bind: address already in use
```

## Cause
Port 5000 is already in use, likely by:
- Local MLflow UI (`mlflow ui`)
- Another Docker container
- Flask development server
- macOS AirPlay Receiver (since macOS Monterey)

## Solutions

### Solution 1: Use Port 5001 (RECOMMENDED - Already Fixed!)

The Docker Compose file has been updated to use port **5001** instead of 5000.

**Start MLflow server:**
```bash
./start_mlflow_server.sh
```

**Access MLflow UI:**
```
http://localhost:5001
```

**Configure training:**
```bash
export MLFLOW_TRACKING_URI=http://localhost:5001
python src/models/train.py
```

---

### Solution 2: Stop Local MLflow UI

If you're running `mlflow ui` locally:

```bash
# Find the process
ps aux | grep "mlflow ui"

# Kill it
pkill -f "mlflow ui"

# Or press Ctrl+C in the terminal running mlflow ui
```

Then use the original port 5000.

---

### Solution 3: Stop AirPlay Receiver (macOS)

If on macOS Monterey or later:

1. Open **System Preferences** → **Sharing**
2. Uncheck **AirPlay Receiver**

Or via command line:
```bash
sudo lsof -i :5000
# Note the PID, then:
sudo kill -9 <PID>
```

---

### Solution 4: Find and Kill Process on Port 5000

**macOS/Linux:**
```bash
# Find process using port 5000
lsof -ti:5000

# Kill it
kill -9 $(lsof -ti:5000)
```

**Or:**
```bash
sudo lsof -i :5000
# Note the PID
sudo kill -9 <PID>
```

---

### Solution 5: Use Different Port in Docker Compose

Edit `docker-compose.mlflow.yml`:

```yaml
mlflow-server:
  ports:
    - "5002:5000"  # Use any free port
```

Then access at `http://localhost:5002`

---

## Current Configuration

✅ **MLflow Docker Server:** Port **5001** (external) → 5000 (internal)  
✅ **Local MLflow UI:** Port **5000** (if running locally)  
✅ **No Conflict:** You can run both simultaneously!

---

## Quick Commands

### Start Docker MLflow Server (Port 5001)
```bash
./start_mlflow_server.sh
# Access: http://localhost:5001
```

### Start Local MLflow UI (Port 5000)
```bash
mlflow ui
# Access: http://localhost:5000
```

### Use Docker MLflow in Training
```bash
export MLFLOW_TRACKING_URI=http://localhost:5001
python src/models/train.py
```

### Use Local MLflow in Training
```bash
unset MLFLOW_TRACKING_URI  # Or don't set it
python src/models/train.py
```

---

## Verification

Check if ports are in use:
```bash
# Check port 5000
lsof -i :5000

# Check port 5001
lsof -i :5001

# Check if MLflow server is running
docker ps | grep mlflow-server

# Test MLflow server
curl http://localhost:5001/health
```

---

## Summary

| Service | Port | URL |
|---------|------|-----|
| **Docker MLflow Server** | 5001 | http://localhost:5001 |
| **Local MLflow UI** | 5000 | http://localhost:5000 |
| **PostgreSQL** | 5432 | localhost:5432 |
| **MinIO (optional)** | 9000, 9001 | http://localhost:9000 |

---

**Fixed:** December 28, 2025  
**Issue:** Port 5000 conflict  
**Solution:** Use port 5001 for Docker MLflow server  
**Status:** ✅ Resolved

