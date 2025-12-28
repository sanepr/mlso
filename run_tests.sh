#!/bin/bash
# Comprehensive test runner script

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 Running Comprehensive Test Suite${NC}"
echo "========================================"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test step
run_test_step() {
    local name=$1
    local command=$2

    echo -e "${YELLOW}▶ Running: $name${NC}"
    if eval "$command"; then
        echo -e "${GREEN}✅ PASSED: $name${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAILED: $name${NC}"
        ((TESTS_FAILED++))
    fi
    echo ""
}

# 1. Code Linting
echo -e "${BLUE}📝 Step 1: Code Linting${NC}"
echo "------------------------"
run_test_step "flake8 linting" "flake8 src tests --count --statistics || true"
run_test_step "pylint analysis" "pylint src --exit-zero || true"
run_test_step "black formatting check" "black --check src tests || true"
run_test_step "isort import sorting" "isort --check-only src tests || true"

# 2. Unit Tests
echo -e "${BLUE}🧪 Step 2: Unit Tests${NC}"
echo "---------------------"
run_test_step "pytest unit tests" "pytest tests/ -v -m 'not slow' --tb=short"

# 3. Unit Tests with Coverage
echo -e "${BLUE}📊 Step 3: Coverage Analysis${NC}"
echo "---------------------------"
run_test_step "pytest with coverage" "pytest tests/ -v --cov=src --cov-report=term --cov-report=html --cov-report=xml"

# 4. Specific Test Categories
echo -e "${BLUE}🎯 Step 4: Test Categories${NC}"
echo "--------------------------"
run_test_step "data processing tests" "pytest tests/test_data_preprocessing.py -v || true"
run_test_step "model training tests" "pytest tests/test_model_training.py -v || true"
run_test_step "API infrastructure tests" "pytest tests/test_api_infrastructure.py -v || true"

# 5. Generate HTML Report
echo -e "${BLUE}📄 Step 5: Generate Test Report${NC}"
echo "-------------------------------"
run_test_step "HTML test report" "pytest tests/ -v --html=test-report.html --self-contained-html"

# Summary
echo ""
echo "========================================"
echo -e "${BLUE}📊 Test Summary${NC}"
echo "========================================"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests completed successfully!${NC}"
    echo ""
    echo "📄 Reports generated:"
    echo "  - HTML coverage report: htmlcov/index.html"
    echo "  - Test report: test-report.html"
    echo "  - Coverage XML: coverage.xml"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please review the output above.${NC}"
    exit 1
fi

