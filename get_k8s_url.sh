#!/bin/bash
# Get Minikube service URL for Heart Disease API

echo "🌐 Getting Kubernetes Service URL..."
echo ""

# Get Minikube IP
MINIKUBE_IP=$(./minikube-darwin-arm64 ip 2>/dev/null)

if [ -z "$MINIKUBE_IP" ]; then
    echo "❌ Error: Minikube is not running or not accessible"
    echo ""
    echo "Start minikube with: ./minikube-darwin-arm64 start"
    exit 1
fi

# Get NodePort
NODE_PORT=$(./minikube-darwin-arm64 kubectl -- get svc heart-disease-api -o jsonpath='{.spec.ports[0].nodePort}' 2>/dev/null)

if [ -z "$NODE_PORT" ]; then
    echo "❌ Error: Service 'heart-disease-api' not found"
    echo ""
    echo "Deploy with: ./deploy_k8s.sh"
    exit 1
fi

# Build URL
SERVICE_URL="http://${MINIKUBE_IP}:${NODE_PORT}"

echo "✅ Service Information:"
echo "   Minikube IP: $MINIKUBE_IP"
echo "   NodePort:    $NODE_PORT"
echo ""
echo "🌐 Access URL:"
echo "   $SERVICE_URL"
echo ""
echo "📝 Quick Test Commands:"
echo ""
echo "   # Health check"
echo "   curl $SERVICE_URL/health"
echo ""
echo "   # Prediction"
echo "   curl -X POST $SERVICE_URL/predict \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d @test_sample.json"
echo ""
echo "   # Model info"
echo "   curl $SERVICE_URL/model/info"
echo ""

# Test if service is responding
echo "🧪 Testing connection..."
if curl -s -o /dev/null -w "%{http_code}" "$SERVICE_URL/health" 2>/dev/null | grep -q "200"; then
    echo "✅ Service is responding!"
    echo ""
    curl -s "$SERVICE_URL/health" | python3 -m json.tool 2>/dev/null || curl -s "$SERVICE_URL/health"
else
    echo "⚠️  Service not responding. Check if pods are ready:"
    echo "   ./minikube-darwin-arm64 kubectl -- get pods"
fi

echo ""

