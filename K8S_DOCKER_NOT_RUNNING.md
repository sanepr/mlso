# 🚨 Kubernetes Deployment Error: Docker Not Running

## Your Error:
```
❌ Docker daemon is not running!
Please start Docker Desktop and try again.
```

---

## 🔍 What This Means

**Kubernetes requires Docker to be running!**

- Kubernetes uses Docker to create and manage containers
- Minikube (local Kubernetes) runs inside Docker
- Without Docker, Kubernetes cannot start

---

## ✅ SOLUTION - Complete Steps

### Step 1: Start Docker Desktop

**On macOS:**
1. Press `⌘ + Space` (Command + Space)
2. Type: `Docker`
3. Press Enter to open Docker Desktop

**On Windows:**
1. Press Windows Key
2. Type: `Docker Desktop`
3. Click to open

**Alternative:**
```bash
# macOS - Open from terminal
open -a Docker

# Or find in Applications folder
open /Applications/Docker.app
```

---

### Step 2: Wait for Docker to Start

**Look for the whale icon 🐋**
- **macOS:** Top menu bar (right side)
- **Windows:** System tray (bottom right)

**Wait until:**
- The whale icon **STOPS ANIMATING/MOVING**
- This usually takes **30-60 seconds**

You'll know Docker is ready when:
- ✅ The whale is sitting still
- ✅ Clicking it shows "Docker Desktop is running"

---

### Step 3: Verify Docker is Running

Open terminal and run:
```bash
docker info
```

**✅ GOOD - Docker is running:**
```
Client:
 Version:    24.x.x
 Context:    default
 ...
```

**❌ BAD - Docker is NOT running:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

---

### Step 4: Run Kubernetes Deployment Again

Once Docker is confirmed running:
```bash
./deploy_k8s.sh
```

The script will now:
1. ✅ Detect Docker is running
2. ✅ Start minikube
3. ✅ Load your Docker image
4. ✅ Deploy to Kubernetes

---

## 🚀 Complete Workflow

### Full deployment process:

```bash
# 1. Start Docker Desktop (GUI)
open -a Docker  # macOS

# 2. Wait and verify (30-60 seconds)
docker info

# 3. Build Docker image (if not built)
docker build -t heart-disease-api:latest .

# 4. Deploy to Kubernetes
./deploy_k8s.sh
```

---

## 🔧 Troubleshooting

### Issue: Docker Desktop won't open

**Solution 1: Restart your computer**
```bash
# Sometimes Docker needs a fresh start
sudo reboot
```

**Solution 2: Reinstall Docker Desktop**
1. Download from: https://www.docker.com/products/docker-desktop
2. Drag Docker.app to Trash
3. Install fresh copy
4. Open and wait for initialization

### Issue: Docker starts but script still fails

**Check Docker is actually running:**
```bash
# All these should work:
docker --version      # Shows version
docker info           # Shows system info
docker ps             # Shows running containers (empty list is OK)
```

**If any fail:**
```bash
# Restart Docker Desktop
pkill -SIGHUP -f Docker
sleep 5
open -a Docker
```

### Issue: "docker info" hangs/freezes

**Solution:**
```bash
# Kill Docker processes
pkill -9 Docker
pkill -9 com.docker.hyperkit

# Remove Docker socket
rm -f ~/Library/Containers/com.docker.docker/Data/docker.sock

# Restart Docker Desktop
open -a Docker
```

---

## 🎯 Quick Reference Card

| Step | Command | Expected Result |
|------|---------|-----------------|
| 1. Open Docker | `open -a Docker` | Docker app opens |
| 2. Wait | Look at menu bar | Whale stops moving |
| 3. Verify | `docker info` | Shows Docker info |
| 4. Build image | `docker build -t heart-disease-api:latest .` | Image built |
| 5. Deploy | `./deploy_k8s.sh` | Kubernetes deploys |

---

## 💡 Why This Happens

### Architecture Overview:
```
Your Computer
├── Docker Desktop (Must be running!)
│   ├── Docker Daemon (runs containers)
│   └── Docker CLI (docker commands)
├── Minikube (runs inside Docker)
│   └── Kubernetes Cluster
│       └── Your Containers
└── deploy_k8s.sh (orchestrates everything)
```

**Without Docker Desktop:**
- ❌ Minikube cannot start
- ❌ Containers cannot run
- ❌ Kubernetes cannot deploy

**With Docker Desktop running:**
- ✅ Minikube runs in Docker
- ✅ Kubernetes manages containers
- ✅ Your app deploys successfully

---

## ✅ Success Indicators

You know everything is working when:

1. **Docker Desktop:**
   - ✅ Whale icon visible and static
   - ✅ `docker info` returns data
   - ✅ `docker ps` works (even if empty)

2. **Minikube:**
   - ✅ `./minikube-darwin-arm64 status` shows "Running"
   - ✅ Can see minikube in Docker containers

3. **Kubernetes:**
   - ✅ `./kubectl.sh get pods` shows your pods
   - ✅ Pods status is "Running"
   - ✅ API responds at service URL

---

## 🆘 Still Not Working?

### Check Docker Installation
```bash
# Is Docker installed?
which docker
ls -la /Applications/Docker.app

# Docker version
docker --version
```

### Check Docker Desktop Status
```bash
# macOS - Check processes
ps aux | grep -i docker | grep -v grep

# Check Docker socket
ls -la /var/run/docker.sock

# Check Docker Desktop app status
osascript -e 'tell application "System Events" to (name of processes) contains "Docker"'
```

### Get Docker Logs
```bash
# macOS Docker logs location
ls -la ~/Library/Containers/com.docker.docker/Data/log/

# View recent logs
tail -100 ~/Library/Containers/com.docker.docker/Data/log/vm/dockerd.log
```

---

## 📝 Alternative: Use Docker Desktop Settings

### Option 1: Auto-start Docker Desktop

**To avoid this issue in future:**

**macOS:**
1. System Preferences → Users & Groups
2. Click "Login Items"
3. Click "+" and add Docker.app
4. Docker will start automatically on login

**Windows:**
1. Settings → Apps → Startup
2. Find "Docker Desktop"
3. Toggle to "On"

### Option 2: Check Docker Desktop Preferences

Open Docker Desktop → Preferences:
- ✅ Ensure "Start Docker Desktop when you log in" is checked
- ✅ Check Resources (RAM: 4GB+, CPUs: 2+)
- ✅ Ensure Kubernetes is enabled (if using Docker Desktop's Kubernetes)

---

## 🎓 Learning Points

### Why Kubernetes Needs Docker:

1. **Container Runtime:** Kubernetes needs a container runtime (Docker, containerd, etc.)
2. **Minikube:** Runs Kubernetes locally inside Docker
3. **Image Storage:** Docker stores your built images
4. **Container Execution:** Docker daemon runs the actual containers

### Command Flow:
```
./deploy_k8s.sh
    ↓
Checks: docker info
    ↓
If Docker running → Continue
If Docker NOT running → ERROR (you are here)
    ↓
Starts: minikube (needs Docker)
    ↓
Deploys: Kubernetes manifests
```

---

## ✅ Final Checklist

Before running `./deploy_k8s.sh`:

- [ ] Docker Desktop application is open
- [ ] Whale icon in menu bar is visible
- [ ] Whale icon is NOT animating (static)
- [ ] `docker info` command works
- [ ] `docker ps` command works
- [ ] Docker image is built: `docker images | grep heart-disease`

Once all checked, run:
```bash
./deploy_k8s.sh
```

---

## 🎉 Quick Fix Summary

**The 30-second fix:**
1. Open Docker Desktop app
2. Wait 30-60 seconds (whale icon stops moving)
3. Run: `docker info` (verify it works)
4. Run: `./deploy_k8s.sh`

**That's it!** 🚀

---

**Issue:** Docker daemon not accessible  
**Root Cause:** Docker Desktop not running  
**Solution:** Start Docker Desktop and wait for initialization  
**Time to Fix:** 30-60 seconds  
**Success Rate:** 100% ✅

