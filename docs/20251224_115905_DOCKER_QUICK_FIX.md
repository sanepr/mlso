# 🚨 DOCKER ERROR: Quick Fix in 3 Steps

## Your Error:
```
ERROR: Cannot connect to the Docker daemon
```

## The Problem:
**Docker Desktop is NOT running!**

---

## ✅ THE FIX (3 Easy Steps)

### 1️⃣ OPEN DOCKER DESKTOP

**On Mac:**
- Press `⌘ + Space` (Command + Space)
- Type: `Docker`
- Press Enter

**On Windows:**
- Press Windows Key
- Type: `Docker Desktop`
- Press Enter

---

### 2️⃣ WAIT FOR IT TO START

Look for the **whale icon** 🐋 in your menu bar (top right on Mac, system tray on Windows)

**Wait until:**
- The whale icon **STOPS MOVING/ANIMATING**
- Usually takes 30-60 seconds

You'll know it's ready when the whale is sitting still!

---

### 3️⃣ TRY YOUR COMMAND AGAIN

```bash
docker build -t heart-disease-api:latest .
```

**OR use our helper script:**
```bash
./docker_start.sh
```

---

## 🔍 Verify Docker is Running

Run this command:
```bash
docker info
```

**✅ GOOD:** Shows Docker information  
**❌ BAD:** Shows "Cannot connect" error

---

## 🚀 One-Line Solution

```bash
# Run our automated helper - it checks everything!
./docker_start.sh
```

This script will:
1. Check if Docker is installed
2. Check if Docker is running
3. Start Docker if needed (Mac)
4. Build your image automatically
5. Optionally run the container

---

## 💡 Why This Happens

Docker has two parts:
1. **Docker CLI** - The commands you type (`docker build`, `docker run`, etc.)
2. **Docker Desktop** - The app that actually does the work

The error means Docker CLI can't find Docker Desktop because **the app isn't running**.

---

## 🆘 Still Not Working?

### Quick Checks:

**Is Docker installed?**
```bash
docker --version
```
Should show: `Docker version X.X.X`

If not: Download from https://www.docker.com/products/docker-desktop

**Is Docker Desktop open?**
Look for the whale icon 🐋 in:
- **Mac:** Top menu bar (right side)
- **Windows:** System tray (bottom right)

**Try restarting Docker:**
- Quit Docker Desktop completely
- Open it again
- Wait for whale icon to stop moving

---

## 📖 Need More Help?

See the complete guide: [DOCKER_DAEMON_FIX.md](./DOCKER_DAEMON_FIX.md)

---

## ✅ Success Checklist

- [ ] Docker Desktop application is open
- [ ] Whale icon is visible and NOT animating
- [ ] `docker info` command works
- [ ] Ready to build!

---

**TL;DR: Open Docker Desktop app, wait for it to start, then retry your command!**

