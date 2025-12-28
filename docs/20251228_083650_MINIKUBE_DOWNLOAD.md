# ⚠️ Minikube Binary Not Included

## Why?

The `minikube-darwin-arm64` binary (131 MB) exceeds GitHub's file size limit of 100 MB and is not included in this repository.

---

## 📥 How to Get Minikube

### Option 1: Use Download Script (Recommended)

```bash
# Download minikube binary
./download_minikube.sh

# Verify installation
./minikube-darwin-arm64 version
```

### Option 2: Download Manually

**For macOS ARM64 (M1/M2/M3):**
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-arm64
chmod +x minikube-darwin-arm64
```

**For macOS Intel:**
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
chmod +x minikube-darwin-amd64
mv minikube-darwin-amd64 minikube-darwin-arm64  # Or update scripts
```

**For Linux:**
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube-linux-amd64
```

### Option 3: Install via Package Manager

**macOS (Homebrew):**
```bash
brew install minikube
# Then create symlink
ln -s $(which minikube) minikube-darwin-arm64
```

**Linux:**
```bash
# Debian/Ubuntu
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb

# Or use binary
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

---

## ✅ Verification

After downloading, verify it works:

```bash
./minikube-darwin-arm64 version
./minikube-darwin-arm64 status
```

---

## 🚀 Using Kubernetes Scripts

All scripts expect `minikube-darwin-arm64` to be in the project root:

```bash
./deploy_k8s.sh       # Requires minikube
./kubectl.sh          # Requires minikube
./get_k8s_url.sh      # Requires minikube
./start_k8s_api.sh    # Requires minikube
```

**First time setup:**
```bash
# 1. Download minikube
./download_minikube.sh

# 2. Start minikube
./minikube-darwin-arm64 start --driver=docker

# 3. Deploy application
./deploy_k8s.sh
```

---

## 📚 Documentation

- [Minikube Official Site](https://minikube.sigs.k8s.io/)
- [Installation Guide](https://minikube.sigs.k8s.io/docs/start/)
- [GitHub Releases](https://github.com/kubernetes/minikube/releases)

---

## 🔧 Troubleshooting

### Script fails with "minikube-darwin-arm64 not found"
```bash
# Download it first
./download_minikube.sh

# Or manually
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-arm64
chmod +x minikube-darwin-arm64
```

### Wrong architecture
If you're on Intel Mac, download the amd64 version:
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
mv minikube-darwin-amd64 minikube-darwin-arm64
```

### Permission denied
```bash
chmod +x minikube-darwin-arm64
```

---

**Note:** The binary is ~131 MB and must be downloaded separately due to GitHub's file size restrictions.

**Quick Start:** Run `./download_minikube.sh` to get started!

