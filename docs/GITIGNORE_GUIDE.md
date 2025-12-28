# .gitignore Configuration

## Overview

A comprehensive `.gitignore` file has been created to exclude unwanted files from version control while preserving important project structure.

---

## 🗂️ What's Being Ignored

### Python Files
- `__pycache__/` - Python cache directories
- `*.pyc`, `*.pyo` - Compiled Python files
- `*.egg-info/` - Package metadata
- `dist/`, `build/` - Distribution files
- `*.so` - Compiled extensions

### Virtual Environments
- `venv/`, `env/`, `.venv/` - Virtual environment directories
- `ENV/`, `env.bak/` - Environment backups

### IDE & Editor Files
- `.idea/` - PyCharm
- `.vscode/` - VS Code
- `*.swp`, `*.swo` - Vim swap files
- `.project`, `.pydevproject` - Eclipse

### Jupyter Notebooks
- `.ipynb_checkpoints/` - Notebook checkpoints
- `*/.ipynb_checkpoints/*` - All checkpoint directories

### Testing & Coverage
- `.pytest_cache/` - Pytest cache
- `.coverage`, `htmlcov/` - Coverage reports
- `test-report.html` - Test reports
- `junit.xml` - JUnit XML reports

### Data Files (Contents Ignored, Structure Kept)
- `data/raw/*.csv` - Raw data files
- `data/raw/*.txt` - Raw text files
- `data/processed/*.pkl` - Processed pickle files
- `data/processed/*.npy` - NumPy arrays

**Note:** `.gitkeep` files preserve empty directories

### Model Files
- `models/*.pkl` - Pickle model files
- `models/*.h5` - Keras/TensorFlow models
- `models/*.pt`, `models/*.pth` - PyTorch models
- `models/*.onnx` - ONNX models

### MLflow Artifacts
- `mlruns/` - MLflow experiment tracking
- `mlartifacts/` - MLflow artifacts

### Logs
- `logs/` - Log directory
- `*.log` - All log files

### Environment & Secrets
- `.env` - Environment variables
- `*.secret` - Secret files
- `secrets/`, `credentials/` - Credentials directories
- `*.pem`, `*.key` - Certificate files

### OS-Specific Files
- `.DS_Store` - macOS Finder metadata
- `Thumbs.db`, `Desktop.ini` - Windows metadata
- `.Spotlight-V100`, `.Trashes` - macOS system files

### Docker
- `*.tar`, `*.tar.gz` - Docker image archives
- `docker-compose.override.yml` - Local overrides

### Temporary Files
- `*.swp`, `*~` - Editor temporary files
- `.tmp/`, `tmp/` - Temporary directories
- `*.bak`, `*.backup` - Backup files

---

## ✅ What's NOT Ignored (Tracked in Git)

### Source Code
- `src/` - All Python source code
- `tests/` - All test files
- `notebooks/` - Jupyter notebooks (committed)

### Configuration
- `requirements.txt` - Python dependencies
- `pytest.ini` - Test configuration
- `pyproject.toml` - Project configuration
- `.flake8` - Linting configuration
- `Dockerfile` - Docker configuration

### Deployment
- `.github/workflows/` - CI/CD workflows
- `deployment/kubernetes/` - Kubernetes manifests
- `*.sh` - Shell scripts

### Documentation
- `README.md` - Project documentation
- `*.md` - All markdown files
- `docs/` - Documentation source files

### Structure Markers
- `.gitkeep` - Directory structure markers

---

## 📁 Directory Structure Preservation

The following directories are kept in git (with `.gitkeep` files) even when empty:
- `data/raw/.gitkeep`
- `data/processed/.gitkeep`
- `models/.gitkeep`
- `logs/.gitkeep`

This ensures the project structure is maintained when cloning the repository.

---

## 🔍 Verify What's Ignored

### Check current git status:
```bash
git status
```

### See what would be ignored:
```bash
git status --ignored
```

### Check if specific file is ignored:
```bash
git check-ignore -v <filename>
```

### List all ignored files:
```bash
git ls-files --others --ignored --exclude-standard
```

---

## 🛠️ Customization

### To ignore additional files:
Add patterns to `.gitignore`:
```bash
echo "your-pattern-here" >> .gitignore
```

### To stop ignoring a file:
Remove the pattern from `.gitignore` or use:
```bash
git add -f <filename>
```

### To ignore files already tracked:
```bash
git rm --cached <filename>
```

---

## 📊 Why These Files Are Ignored

### Security
- Environment files (`.env`) - Contains sensitive credentials
- Certificates (`*.pem`, `*.key`) - Private keys
- Secrets (`secrets/`) - API keys, passwords

### Performance
- Cache files (`__pycache__/`) - Generated automatically
- Virtual environments (`venv/`) - Large, user-specific
- Model files (`*.pkl`) - Often large, use Git LFS if needed

### Cleanliness
- OS files (`.DS_Store`) - System-specific
- IDE files (`.idea/`, `.vscode/`) - User preference
- Logs (`*.log`) - Runtime artifacts

### Reproducibility
- Data files - Should be downloaded via script
- Model files - Should be trained via pipeline
- MLflow artifacts - Generated during training

---

## 🎯 Best Practices

### Do Commit:
✅ Source code (`src/`)  
✅ Tests (`tests/`)  
✅ Configuration files  
✅ Documentation  
✅ Scripts  
✅ Requirements  

### Don't Commit:
❌ Virtual environments  
❌ Cache files  
❌ Secrets/credentials  
❌ Large data files  
❌ Generated artifacts  
❌ IDE-specific files  

---

## 🔄 Using with Git LFS (Optional)

For large model files, consider Git LFS:

```bash
# Install Git LFS
git lfs install

# Track large model files
git lfs track "models/*.pkl"
git lfs track "models/*.h5"

# Commit .gitattributes
git add .gitattributes
git commit -m "Configure Git LFS for model files"
```

---

## 📝 Common Operations

### After creating .gitignore:
```bash
# Add .gitignore to git
git add .gitignore

# Commit
git commit -m "Add comprehensive .gitignore"

# Remove previously tracked files that should be ignored
git rm -r --cached .
git add .
git commit -m "Clean up ignored files from git history"
```

### Clean up untracked files:
```bash
# See what would be removed
git clean -n -d

# Actually remove (be careful!)
git clean -f -d
```

---

## ✅ Verification

The `.gitignore` file is configured to:
- ✅ Ignore 100+ file patterns
- ✅ Preserve directory structure
- ✅ Protect sensitive information
- ✅ Reduce repository size
- ✅ Maintain clean git status

---

## 📚 References

- [Git Documentation - gitignore](https://git-scm.com/docs/gitignore)
- [GitHub gitignore templates](https://github.com/github/gitignore)
- [Python gitignore best practices](https://github.com/github/gitignore/blob/main/Python.gitignore)

---

**Created:** December 26, 2025  
**Purpose:** MLOps project cleanup and organization  
**Status:** ✅ Ready to use

