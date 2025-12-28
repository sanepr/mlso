#!/bin/bash
# Start Kubernetes API with port forwarding

echo "🚀 Starting Kubernetes API Access..."
echo ""
echo "✅ Port forwarding: localhost:8080 → heart-disease-api:8000"
echo ""
echo "📝 Access your API at: http://localhost:8080"
echo ""
echo "🧪 Test commands:"
echo "   curl http://localhost:8080/health"
echo "   curl -X POST http://localhost:8080/predict -H 'Content-Type: application/json' -d @test_sample.json"
echo ""
echo "⚠️  Keep this terminal open! Press Ctrl+C to stop."
echo ""

./kubectl.sh port-forward svc/heart-disease-api 8080:8000

