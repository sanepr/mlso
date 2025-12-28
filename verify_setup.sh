#!/bin/bash
# Comprehensive verification script for README commands

echo "🔍 MLOps Heart Disease Prediction - Verification Report"
echo "========================================================"
echo ""

# Track overall status
ALL_TESTS_PASSED=true

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

check_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $2"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}: $2"
        ((FAILED++))
        ALL_TESTS_PASSED=false
    fi
}

echo "📋 1. ENVIRONMENT CHECK"
echo "----------------------------------------"

# Check Python version
echo -n "Checking Python version... "
python --version > /dev/null 2>&1
check_status $? "Python installed"

# Check virtual environment
echo -n "Checking virtual environment... "
if [ -d "venv" ]; then
    check_status 0 "Virtual environment exists"
else
    check_status 1 "Virtual environment missing"
fi

# Check requirements
echo -n "Checking installed packages... "
pip list > /dev/null 2>&1
check_status $? "Pip packages accessible"

echo ""
echo "📊 2. DATA CHECK"
echo "----------------------------------------"

# Check dataset
echo -n "Checking dataset... "
if [ -f "data/raw/heart.csv" ]; then
    ROWS=$(wc -l < data/raw/heart.csv)
    check_status 0 "Dataset exists ($ROWS rows)"
else
    check_status 1 "Dataset missing"
fi

# Check processed data
echo -n "Checking processed data... "
if [ -d "data/processed" ] && [ "$(ls -A data/processed)" ]; then
    FILES=$(ls data/processed | wc -l)
    check_status 0 "Processed data exists ($FILES files)"
else
    check_status 1 "Processed data missing"
fi

echo ""
echo "🤖 3. MODEL CHECK"
echo "----------------------------------------"

# Check models
echo -n "Checking trained models... "
if [ -f "models/best_model.pkl" ]; then
    SIZE=$(ls -lh models/best_model.pkl | awk '{print $5}')
    check_status 0 "Best model exists ($SIZE)"
else
    check_status 1 "Best model missing"
fi

echo -n "Checking model metadata... "
if [ -f "models/best_model_metadata.json" ]; then
    check_status 0 "Model metadata exists"
else
    check_status 1 "Model metadata missing"
fi

# Count all models
echo -n "Counting all models... "
MODEL_COUNT=$(ls models/*.pkl 2>/dev/null | wc -l)
check_status 0 "Found $MODEL_COUNT model file(s)"

echo ""
echo "📈 4. MLFLOW TRACKING"
echo "----------------------------------------"

# Check MLflow experiments
echo -n "Checking MLflow experiments... "
if [ -d "mlruns" ]; then
    EXPERIMENTS=$(find mlruns -name "meta.yaml" 2>/dev/null | wc -l)
    check_status 0 "MLflow tracking exists ($EXPERIMENTS experiment(s))"
else
    check_status 1 "MLflow tracking missing"
fi

echo ""
echo "🐳 5. DOCKER CHECK"
echo "----------------------------------------"

# Check Docker
echo -n "Checking Docker daemon... "
docker info > /dev/null 2>&1
DOCKER_STATUS=$?
if [ $DOCKER_STATUS -eq 0 ]; then
    check_status 0 "Docker is running"

    # Check Docker image
    echo -n "Checking Docker image... "
    if docker images | grep -q "heart-disease-api"; then
        SIZE=$(docker images heart-disease-api:latest --format "{{.Size}}")
        check_status 0 "Docker image exists ($SIZE)"
    else
        check_status 1 "Docker image not built"
    fi
else
    check_status 1 "Docker is not running"
fi

# Check Dockerfile
echo -n "Checking Dockerfile... "
if [ -f "Dockerfile" ]; then
    check_status 0 "Dockerfile exists"
else
    check_status 1 "Dockerfile missing"
fi

echo ""
echo "☸️  6. KUBERNETES CHECK"
echo "----------------------------------------"

# Check Kubernetes manifests
echo -n "Checking deployment.yaml... "
if [ -f "deployment/kubernetes/deployment.yaml" ]; then
    check_status 0 "Deployment manifest exists"
else
    check_status 1 "Deployment manifest missing"
fi

echo -n "Checking service.yaml... "
if [ -f "deployment/kubernetes/service.yaml" ]; then
    check_status 0 "Service manifest exists"
else
    check_status 1 "Service manifest missing"
fi

# Check minikube
echo -n "Checking minikube binary... "
if [ -f "minikube-darwin-arm64" ] && [ -x "minikube-darwin-arm64" ]; then
    VERSION=$(./minikube-darwin-arm64 version --short 2>/dev/null)
    check_status 0 "Minikube binary ready ($VERSION)"
else
    check_status 1 "Minikube binary not executable"
fi

echo ""
echo "📝 7. SCRIPTS CHECK"
echo "----------------------------------------"

# Check helper scripts
SCRIPTS=("deploy_k8s.sh" "kubectl.sh" "test_docker.sh" "start_jupyter.sh")
for script in "${SCRIPTS[@]}"; do
    echo -n "Checking $script... "
    if [ -f "$script" ] && [ -x "$script" ]; then
        check_status 0 "$script is executable"
    else
        check_status 1 "$script missing or not executable"
    fi
done

echo ""
echo "📚 8. DOCUMENTATION CHECK"
echo "----------------------------------------"

# Check documentation files
DOCS=("README.md" "QUICK_START.md" "DOCKER_FIX.md" "K8S_SETUP_SUMMARY.md")
for doc in "${DOCS[@]}"; do
    echo -n "Checking $doc... "
    if [ -f "$doc" ]; then
        LINES=$(wc -l < "$doc")
        check_status 0 "$doc exists ($LINES lines)"
    else
        check_status 1 "$doc missing"
    fi
done

echo ""
echo "🧪 9. TEST FILES CHECK"
echo "----------------------------------------"

# Check if tests directory exists
echo -n "Checking tests directory... "
if [ -d "tests" ]; then
    TEST_FILES=$(find tests -name "test_*.py" 2>/dev/null | wc -l)
    check_status 0 "Tests directory exists ($TEST_FILES test files)"
else
    check_status 1 "Tests directory missing"
fi

echo ""
echo "📦 10. PROJECT STRUCTURE"
echo "----------------------------------------"

# Check key directories
DIRS=("src" "src/api" "src/models" "src/data" "data" "notebooks" "deployment")
for dir in "${DIRS[@]}"; do
    echo -n "Checking $dir/... "
    if [ -d "$dir" ]; then
        check_status 0 "$dir/ exists"
    else
        check_status 1 "$dir/ missing"
    fi
done

echo ""
echo "========================================================"
echo "📊 SUMMARY"
echo "========================================================"
echo ""
echo -e "Total Tests: $((PASSED + FAILED))"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ "$ALL_TESTS_PASSED" = true ]; then
    echo -e "${GREEN}🎉 ALL CHECKS PASSED! Project is ready.${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some checks failed. See details above.${NC}"
    echo ""
    echo "Common fixes:"
    echo "  - Dataset missing: Run 'python src/data/download_data.py'"
    echo "  - Models missing: Run 'python src/models/train.py'"
    echo "  - Docker not running: Start Docker Desktop"
    echo "  - Image not built: Run 'docker build -t heart-disease-api:latest .'"
    exit 1
fi

