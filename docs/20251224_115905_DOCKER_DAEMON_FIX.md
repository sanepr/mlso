# 🐳 Docker Daemon Error - Complete Fix Guide

## Error Message
```
ERROR: Cannot connect to the Docker daemon at unix:///Users/aashishr/.docker/run/docker.sock. 
Is the docker daemon running?
```

## What This Means
This error occurs when **Docker Desktop is not running**. Docker commands require the Docker daemon (background service) to be active.

---

## ✅ Solution

### Step 1: Open Docker Desktop
**macOS:**
1. Press `Cmd + Space` (Spotlight Search)
2. Type "Docker"
3. Click on "Docker" application
4. OR: Find Docker in Applications folder and open it

**Windows:**
1. Press Windows key
2. Type "Docker Desktop"
3. Click on Docker Desktop application

### Step 2: Wait for Docker to Start
- Look for the **whale icon** in your menu bar (macOS) or system tray (Windows)
- Wait until the icon **stops animating** (becomes static)
- This usually takes 30-60 seconds

### Step 3: Verify Docker is Running
```bash
docker info
```

**Expected output:** Docker system information (server version, containers, images, etc.)

**If it still fails:** See troubleshooting below

---

## 🚀 Quick Fix Script

Use the automated helper script:
```bash
./docker_start.sh
```

This script will:
1. ✅ Check if Docker is installed
2. ✅ Check if Docker daemon is running
3. ✅ Attempt to start Docker Desktop automatically (macOS)
4. ✅ Wait for Docker to be ready
5. ✅ Build the Docker image
6. ✅ Optionally run the container

---

## 🔍 Verification Steps

### 1. Check Docker Installation
```bash
docker --version
```
**Expected:** `Docker version 24.x.x` or similar

**If not found:**
- Install Docker Desktop from: https://www.docker.com/products/docker-desktop

### 2. Check Docker Daemon
```bash
docker info
```
**Expected:** System information output

**If fails with "Cannot connect":**
- Docker Desktop is not running
- Follow Step 1 above

### 3. Check Docker Process
**macOS/Linux:**
```bash
ps aux | grep -i docker
```

**Windows (PowerShell):**
```powershell
Get-Process | Where-Object {$_.Name -like "*docker*"}
```

**Expected:** Multiple Docker processes running

---

## 🐛 Troubleshooting

### Issue 1: Docker Desktop Won't Open
**Symptoms:** Application won't launch or crashes

**Solutions:**
1. **Restart your computer**
2. **Reinstall Docker Desktop:**
   ```bash
   # macOS - Uninstall
   # Drag Docker.app to Trash, then download fresh copy
   
   # Download from:
   # https://www.docker.com/products/docker-desktop
   ```

3. **Check system requirements:**
   - macOS: Requires macOS 11 or newer
   - Windows: Requires Windows 10/11 Pro, Enterprise, or Education

### Issue 2: Docker Desktop Stuck on Starting
**Symptoms:** Whale icon keeps animating for > 5 minutes

**Solutions:**
1. **Quit Docker Desktop completely:**
   ```bash
   # macOS
   pkill -SIGHUP -f Docker
   
   # Windows
   # Right-click Docker icon → Quit Docker Desktop
   ```

2. **Remove Docker config (if corrupted):**
   ```bash
   # macOS
   rm -rf ~/Library/Group\ Containers/group.com.docker
   rm -rf ~/Library/Containers/com.docker.docker
   
   # Windows
   # Delete: %APPDATA%\Docker
   ```

3. **Restart Docker Desktop**

### Issue 3: Permission Denied
**Symptoms:** `permission denied while trying to connect to the Docker daemon`

**Solutions:**
**macOS/Linux:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again
```

**Windows:**
- Ensure Docker Desktop is running as Administrator

### Issue 4: Port Already in Use
**Symptoms:** Docker starts but build fails with port conflicts

**Solution:**
```bash
# Check what's using Docker's port
lsof -i :2375
lsof -i :2376

# Kill the process if needed
kill -9 <PID>
```

---

## 📝 Manual Build After Fix

Once Docker is running:

```bash
# 1. Verify Docker is working
docker info

# 2. Build the image
docker build -t heart-disease-api:latest .

# 3. Run the container
docker run -d -p 8000:8000 --name heart-disease-api heart-disease-api:latest

# 4. Verify it's running
docker ps

# 5. Test the API
curl http://localhost:8000/health
```

---

## 🎯 Prevention

To avoid this issue in the future:

### Option 1: Auto-start Docker Desktop
**macOS:**
1. System Preferences → Users & Groups → Login Items
2. Add Docker.app

**Windows:**
1. Settings → Apps → Startup
2. Enable Docker Desktop

### Option 2: Use Helper Script
Always use the helper script which checks Docker first:
```bash
./docker_start.sh
```

---

## 💡 Understanding the Error

### Why This Happens
Docker uses a client-server architecture:
- **Docker CLI** (client): The `docker` command you run
- **Docker Daemon** (server): Background service that does the work

The error means the CLI can't find the daemon because:
1. Docker Desktop app is not running (most common)
2. Docker daemon crashed
3. Socket file is missing/corrupted
4. Permission issues

### The Socket File
- **macOS/Linux:** `/var/run/docker.sock`
- **Windows:** Named pipe

This is how the CLI communicates with the daemon.

---

## 🆘 Still Not Working?

### Check Docker Desktop Status
**macOS:**
```bash
# Check if Docker Desktop is installed
ls -la /Applications/Docker.app

# Check for Docker processes
ps aux | grep -i docker | grep -v grep

# Check Docker socket
ls -la /var/run/docker.sock
```

**Windows:**
```powershell
# Check if Docker Desktop is installed
Get-ItemProperty -Path "HKLM:\Software\Docker Inc.\Docker"

# Check Docker service
Get-Service | Where-Object {$_.Name -like "*docker*"}
```

### Get Help
1. **Docker Desktop logs:**
   - macOS: `~/Library/Containers/com.docker.docker/Data/log/`
   - Windows: `%LOCALAPPDATA%\Docker\log.txt`

2. **Docker forums:** https://forums.docker.com/

3. **Check project issues:** Open an issue on GitHub

---

## ✅ Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Daemon not running | Start Docker Desktop |
| Desktop won't start | Restart computer |
| Stuck on starting | Quit and restart Docker |
| Permission denied | Add user to docker group |
| Port conflicts | Kill process using port |

---

## 🎉 Success Indicators

You know Docker is working when:
- ✅ `docker info` returns system information
- ✅ `docker ps` shows running containers (or empty list)
- ✅ Whale icon in menu bar is static (not animating)
- ✅ `docker version` shows both client and server versions

---

**Last Updated:** December 24, 2025  
**Tested On:** macOS (ARM64), Windows 10/11  
**Docker Version:** 24.x and newer

