# 🚀 CI/CD Quick Reference Card

## ⚡ Quick Commands

### Run All Tests
```bash
./run_tests.sh
```

### Run Specific Tests
```bash
pytest tests/test_data_preprocessing.py -v    # Data tests
pytest tests/test_model_training.py -v        # Model tests
pytest tests/test_api_infrastructure.py -v    # Infrastructure tests
```

### Run with Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

### Code Quality Checks
```bash
flake8 src tests              # Linting
pylint src                    # Static analysis
black src tests               # Format code
isort src tests               # Sort imports
```

---

## 📊 Test Statistics

| Metric | Value |
|--------|-------|
| **Total Tests** | 60 |
| **Test Suites** | 3 |
| **Coverage Target** | ≥70% |
| **Pass Rate** | 100% |

---

## 🎯 Quality Gates

### Must Pass
- ✅ All 60 tests passing
- ✅ Coverage ≥70%
- ✅ Flake8 linting
- ✅ Model accuracy ≥70%
- ✅ Model ROC-AUC ≥75%

---

## 📁 Key Files

### Tests
- `tests/test_data_preprocessing.py` (18 tests)
- `tests/test_model_training.py` (20 tests)
- `tests/test_api_infrastructure.py` (22 tests)

### Workflows
- `.github/workflows/ci-cd.yml`
- `.github/workflows/model-training.yml`

### Configuration
- `pytest.ini`
- `pyproject.toml`
- `.flake8`

### Scripts
- `run_tests.sh`

### Documentation
- `CI_CD_DOCUMENTATION.md` (Complete guide)
- `CI_CD_IMPLEMENTATION_COMPLETE.md` (Summary)

---

## 🔄 Pipeline Triggers

### Automatic
- Push to `main` or `develop`
- Pull requests
- Weekly schedule (Sundays)

### Manual
```bash
gh workflow run ci-cd.yml
gh workflow run model-training.yml
```

---

## 📦 Artifacts

| Type | Retention | Location |
|------|-----------|----------|
| Test Reports | 30 days | Actions → Artifacts |
| Models | 90 days | Actions → Artifacts |
| Docker Image | 7 days | Actions → Artifacts |
| Coverage | 30 days | Actions → Artifacts |

---

## ⏱️ Pipeline Duration

| Pipeline | Duration |
|----------|----------|
| PR (Lint + Test) | 8-12 min |
| Full (All Jobs) | 25-35 min |
| Training Only | 12-18 min |

---

## ✅ Status

**Implementation:** ✅ COMPLETE  
**Tests:** ✅ 60/60 PASSING  
**Documentation:** ✅ COMPLETE  
**Production Ready:** ✅ YES  

---

**Last Updated:** December 26, 2025  
**Version:** 1.0.0

