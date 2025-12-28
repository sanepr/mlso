# CI/CD Pipeline Documentation

## Overview

This project implements a comprehensive CI/CD pipeline using GitHub Actions for automated testing, model training, and deployment of the Heart Disease Prediction ML model.

---

## Pipeline Architecture

### 1. Main CI/CD Pipeline (`ci-cd.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch

**Jobs:**

#### Job 1: Lint (Code Quality)
- **Purpose:** Ensure code quality and consistency
- **Tools:** flake8, pylint, black, isort
- **Duration:** ~2-3 minutes
- **Artifacts:** Lint results

#### Job 2: Test (Unit Testing)
- **Purpose:** Run comprehensive unit tests
- **Tools:** pytest, pytest-cov, pytest-html
- **Coverage Target:** ≥70%
- **Duration:** ~5-7 minutes
- **Artifacts:** 
  - Test reports (HTML, JUnit XML)
  - Coverage reports (HTML, XML)
  - Test results

#### Job 3: Train Model
- **Purpose:** Train and validate ML models
- **Trigger:** Only on `main` branch
- **Validation:** 
  - Min Accuracy: 70%
  - Min ROC-AUC: 75%
- **Duration:** ~10-15 minutes
- **Artifacts:**
  - Trained model files (.pkl)
  - Model metadata (JSON)
  - MLflow experiment logs

#### Job 4: Build Docker
- **Purpose:** Build and test Docker image
- **Trigger:** Only on `main` branch after successful training
- **Tests:** Health endpoint validation
- **Duration:** ~5-8 minutes
- **Artifacts:**
  - Docker image (TAR file)

#### Job 5: Generate Report
- **Purpose:** Create pipeline summary
- **Trigger:** Always runs (even on failure)
- **Duration:** ~1 minute
- **Artifacts:**
  - Pipeline summary (Markdown)

---

### 2. Model Training Pipeline (`model-training.yml`)

**Triggers:**
- Weekly schedule (Sundays at midnight)
- Manual workflow dispatch

**Features:**
- Automated model retraining
- Performance validation
- Model comparison with previous version
- Training report generation
- Failure notifications

**Validation Thresholds:**
- Minimum Accuracy: 70%
- Minimum ROC-AUC: 75%

**Artifacts:**
- Trained models with timestamps
- Training logs
- MLflow artifacts
- Training report

---

## Testing Strategy

### Unit Tests

**Coverage:**
1. **Data Processing Tests** (`test_data_preprocessing.py`)
   - Data loading
   - Data preprocessing
   - Train/test split
   - Feature scaling
   - Data quality checks

2. **Model Training Tests** (`test_model_training.py`)
   - Model file existence
   - Model interface validation
   - Performance metrics
   - Model types
   - Reproducibility

3. **API Infrastructure Tests** (`test_api_infrastructure.py`)
   - API file structure
   - Docker configuration
   - Kubernetes manifests
   - Project structure

**Test Markers:**
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow tests (skipped in CI)
- `@pytest.mark.api` - API tests
- `@pytest.mark.model` - Model tests
- `@pytest.mark.data` - Data tests

### Running Tests Locally

```bash
# Run all tests
./run_tests.sh

# Run specific test file
pytest tests/test_data_preprocessing.py -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific markers
pytest tests/ -m "unit and not slow"

# Run and generate HTML report
pytest tests/ -v --html=test-report.html --self-contained-html
```

---

## Code Quality Tools

### 1. Flake8
**Purpose:** Python linting and style checking
**Configuration:** `.flake8`
**Max Line Length:** 127 characters
**Max Complexity:** 10

```bash
flake8 src tests --count --statistics
```

### 2. Pylint
**Purpose:** Advanced code analysis
**Configuration:** `.flake8` (pylint section)
**Disabled Checks:** C0111, C0103, R0913, R0914

```bash
pylint src --exit-zero
```

### 3. Black
**Purpose:** Code formatting
**Configuration:** `pyproject.toml`
**Line Length:** 127 characters

```bash
# Check formatting
black --check src tests

# Auto-format
black src tests
```

### 4. isort
**Purpose:** Import sorting
**Configuration:** `pyproject.toml`
**Profile:** black

```bash
# Check imports
isort --check-only src tests

# Auto-sort
isort src tests
```

---

## Artifacts & Logging

### Artifacts Generated

#### Lint Job:
- Lint results logs
- **Retention:** 7 days

#### Test Job:
- `test-report.html` - HTML test report
- `junit.xml` - JUnit XML for CI integration
- `htmlcov/` - HTML coverage report
- `coverage.xml` - XML coverage report
- **Retention:** 30 days

#### Train Model Job:
- `models/*.pkl` - Trained model files
- `models/*.json` - Model metadata
- `mlruns/` - MLflow experiment data
- **Retention:** 90 days

#### Build Docker Job:
- `heart-disease-api.tar` - Docker image
- **Retention:** 7 days

#### Generate Report Job:
- `pipeline-summary.md` - Pipeline summary
- **Retention:** 90 days

### Accessing Artifacts

**Via GitHub UI:**
1. Go to repository → Actions
2. Click on workflow run
3. Scroll to "Artifacts" section
4. Download desired artifact

**Via GitHub CLI:**
```bash
# List artifacts
gh run view <run-id> --log

# Download artifact
gh run download <run-id> -n <artifact-name>
```

---

## Model Validation

### Performance Thresholds

| Metric | Minimum | Current |
|--------|---------|---------|
| Accuracy | 70% | ~88% |
| ROC-AUC | 75% | ~96% |
| F1-Score | - | ~88% |

### Validation Process

1. **Training Phase:**
   - Train multiple models (Logistic Regression, Random Forest)
   - Perform cross-validation
   - Log metrics to MLflow

2. **Selection Phase:**
   - Compare model performances
   - Select best model based on ROC-AUC
   - Save best model and metadata

3. **Validation Phase:**
   - Load model metadata
   - Check performance thresholds
   - Fail pipeline if thresholds not met

4. **Deployment Decision:**
   - Compare with production model (if exists)
   - Approve for deployment if improved

---

## Environment Variables

### CI/CD Pipeline
- `PYTHON_VERSION` - Python version (default: 3.10)

### Model Training Pipeline
- `PYTHON_VERSION` - Python version (default: 3.10)
- `MIN_ACCURACY` - Minimum accuracy threshold (default: 0.70)
- `MIN_ROC_AUC` - Minimum ROC-AUC threshold (default: 0.75)

### Secrets (Required for Production)
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password
- `SLACK_WEBHOOK_URL` - Slack notification webhook (optional)

---

## Workflow Triggers

### Automatic Triggers

**Push Events:**
```yaml
on:
  push:
    branches: [ main, develop ]
```

**Pull Request Events:**
```yaml
on:
  pull_request:
    branches: [ main, develop ]
```

**Scheduled Events:**
```yaml
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
```

### Manual Triggers

**Via GitHub UI:**
1. Go to Actions tab
2. Select workflow
3. Click "Run workflow"
4. Fill in inputs (if any)
5. Click "Run workflow"

**Via GitHub CLI:**
```bash
# Trigger CI/CD pipeline
gh workflow run ci-cd.yml

# Trigger model training
gh workflow run model-training.yml -f retrain_reason="Manual retrain for testing"
```

---

## Monitoring & Notifications

### Build Status

**Badges:**
Add to README.md:
```markdown
[![CI/CD Pipeline](https://github.com/USERNAME/mlso/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/USERNAME/mlso/actions/workflows/ci-cd.yml)
[![Model Training](https://github.com/USERNAME/mlso/actions/workflows/model-training.yml/badge.svg)](https://github.com/USERNAME/mlso/actions/workflows/model-training.yml)
```

### Failure Notifications

**Current:**
- GitHub Actions built-in notifications
- Email to commit author

**Configurable (Commented in workflows):**
- Slack notifications
- Email notifications
- Custom webhooks

**Enable Slack Notifications:**
1. Create Slack incoming webhook
2. Add `SLACK_WEBHOOK_URL` to repository secrets
3. Uncomment notification steps in workflows

---

## Best Practices

### For Contributors

1. **Before Pushing:**
   ```bash
   # Run tests locally
   ./run_tests.sh
   
   # Format code
   black src tests
   isort src tests
   
   # Check linting
   flake8 src tests
   ```

2. **Pull Requests:**
   - All tests must pass
   - Code coverage must be ≥70%
   - Code must pass linting
   - Review pipeline summary in PR comments

3. **Commit Messages:**
   - Use conventional commits format
   - Examples: `feat:`, `fix:`, `test:`, `ci:`

### For Maintainers

1. **Merging PRs:**
   - Ensure all checks pass
   - Review test coverage changes
   - Check for performance regressions

2. **Model Updates:**
   - Review training metrics
   - Compare with previous models
   - Validate on test set

3. **Pipeline Maintenance:**
   - Keep actions up to date
   - Monitor artifact storage usage
   - Review and update thresholds

---

## Troubleshooting

### Common Issues

#### 1. Tests Failing Locally But Passing in CI

**Cause:** Different environments
**Solution:**
```bash
# Use same Python version
python --version  # Should match CI (3.10)

# Install exact dependencies
pip install -r requirements.txt --no-cache-dir

# Clear pytest cache
rm -rf .pytest_cache __pycache__
```

#### 2. Coverage Below Threshold

**Cause:** Insufficient test coverage
**Solution:**
```bash
# Check coverage report
pytest tests/ --cov=src --cov-report=term-missing

# Add tests for uncovered code
# Focus on files with <70% coverage
```

#### 3. Model Training Fails

**Cause:** Data download or preprocessing issues
**Solution:**
```bash
# Test data pipeline locally
python src/data/download_data.py
python src/data/preprocessing.py
python src/models/train.py
```

#### 4. Docker Build Fails

**Cause:** Missing files or dependencies
**Solution:**
```bash
# Test Docker build locally
docker build -t heart-disease-api:test .

# Check for missing files
docker run -it heart-disease-api:test ls -la /app/models/
```

---

## Pipeline Optimization

### Current Performance
- Lint: ~2-3 minutes
- Test: ~5-7 minutes
- Train: ~10-15 minutes
- Docker: ~5-8 minutes
- **Total:** ~25-35 minutes

### Optimization Strategies

1. **Caching:**
   - ✅ pip packages cached
   - Consider: Docker layer caching

2. **Parallel Jobs:**
   - ✅ Lint and Test run in parallel
   - Consider: Multiple model training in parallel

3. **Skip Conditions:**
   - ✅ Docker/Train only on main branch
   - Consider: Skip tests for documentation changes

4. **Artifact Management:**
   - Review retention periods
   - Clean up old artifacts regularly

---

## Future Enhancements

### Planned Features
- [ ] Integration tests with API
- [ ] Performance testing
- [ ] Security scanning (Snyk, Trivy)
- [ ] Automated deployment to staging
- [ ] A/B testing framework
- [ ] Model monitoring and drift detection

### Infrastructure
- [ ] Self-hosted runners for faster builds
- [ ] Multi-environment deployments (dev, staging, prod)
- [ ] Blue-green deployment strategy
- [ ] Automated rollback on failure

---

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Last Updated:** December 26, 2025  
**Pipeline Version:** 1.0.0  
**Status:** ✅ Operational

