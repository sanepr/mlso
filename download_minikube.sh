#!/bin/bash
# Download Minikube binary for macOS ARM64

set -e

echo "📥 Downloading Minikube for macOS ARM64..."

# Check if already exists
if [ -f "minikube-darwin-arm64" ]; then
    echo "✅ Minikube binary already exists"
    chmod +x minikube-darwin-arm64
    exit 0
fi

# Download latest version
MINIKUBE_VERSION="latest"
DOWNLOAD_URL="https://storage.googleapis.com/minikube/releases/${MINIKUBE_VERSION}/minikube-darwin-arm64"

echo "Downloading from: $DOWNLOAD_URL"
curl -LO "$DOWNLOAD_URL"

# Make executable
chmod +x minikube-darwin-arm64

echo "✅ Minikube downloaded successfully!"
echo "Version:"
./minikube-darwin-arm64 version

echo ""
echo "To use: ./minikube-darwin-arm64 [command]"

