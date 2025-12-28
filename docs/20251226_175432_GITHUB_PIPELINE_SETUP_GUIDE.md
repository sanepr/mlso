# 📸 GitHub CI/CD Pipeline Setup & Screenshots Guide

## Complete Step-by-Step Guide for GitHub Actions Pipeline

**Date:** December 26, 2025  
**Purpose:** Set up CI/CD pipeline on GitHub and capture workflow screenshots

---

## 🎯 Prerequisites Checklist

Before starting, ensure you have:
- [x] GitHub account
- [x] Git installed locally
- [x] Repository committed locally
- [x] All files ready to push

---

## 📋 Part 1: Push Code to GitHub

### Step 1: Create GitHub Repository

1. **Go to GitHub**
   - Navigate to https://github.com
   - Log in to your account

2. **Create New Repository**
   - Click the `+` icon (top right)
   - Select "New repository"
   
   **Screenshot 1:** Capture the "New repository" page

3. **Configure Repository**
   - Repository name: `mlso` (or your preferred name)
   - Description: "MLOps Heart Disease Prediction with CI/CD"
   - Visibility: Public or Private
   - **DO NOT** initialize with README (you already have one)
   - Click "Create repository"
   
   **Screenshot 2:** Capture the repository creation form

### Step 2: Push Code to GitHub

1. **Link Remote Repository**
   ```bash
   cd /Users/aashishr/codebase/mlso
   
   # If you haven't set remote yet
   git remote add origin https://github.com/YOUR_USERNAME/mlso.git
   
   # Or if you need to update remote
   git remote set-url origin https://github.com/YOUR_USERNAME/mlso.git
   ```

2. **Verify Remote**
   ```bash
   git remote -v
   ```

3. **Push to GitHub**
   ```bash
   # Push main branch
   git push -u origin main
   
   # Enter your GitHub credentials when prompted
   ```
   
   **Screenshot 3:** Capture terminal showing successful push

4. **Verify on GitHub**
   - Refresh your GitHub repository page
   - You should see all files uploaded
   
   **Screenshot 4:** Capture GitHub repository homepage showing files

---

## 📋 Part 2: Enable and Configure GitHub Actions

### Step 3: Access GitHub Actions

1. **Navigate to Actions Tab**
   - Go to your repository: https://github.com/YOUR_USERNAME/mlso
   - Click on "Actions" tab (top menu)
   
   **Screenshot 5:** Capture the Actions tab landing page

2. **Initial Actions Page**
   - You should see your workflows automatically detected
   - Look for "CI/CD Pipeline" and "Model Training Pipeline"
   
   **Screenshot 6:** Capture detected workflows

### Step 4: Review Workflows

1. **View CI/CD Pipeline Workflow**
   - Click on "CI/CD Pipeline" in the left sidebar
   - Or navigate to: `.github/workflows/ci-cd.yml`
   
   **Screenshot 7:** Capture workflow file view

2. **View Model Training Workflow**
   - Click on "Model Training Pipeline"
   - Or navigate to: `.github/workflows/model-training.yml`
   
   **Screenshot 8:** Capture training workflow file

---

## 📋 Part 3: Trigger First Pipeline Run

### Step 5: Manual Workflow Trigger

1. **Trigger CI/CD Pipeline**
   - Go to Actions tab
   - Click "CI/CD Pipeline" in left sidebar
   - Click "Run workflow" button (right side)
   - Select branch: `main`
   - Click green "Run workflow" button
   
   **Screenshot 9:** Capture "Run workflow" dialog

2. **Observe Pipeline Start**
   - Wait a few seconds
   - You'll see a new workflow run appear
   - Status: Yellow circle (in progress)
   
   **Screenshot 10:** Capture workflow run starting

### Step 6: Monitor Workflow Execution

1. **Click on Running Workflow**
   - Click on the workflow run name
   - You'll see the workflow visualization
   
   **Screenshot 11:** Capture workflow visualization graph

2. **View Job Progress**
   - Left sidebar shows all jobs:
     - Lint (Code Quality)
     - Test (Unit Testing)
     - Train Model (only on main)
     - Build Docker (only on main)
     - Generate Report
   
   **Screenshot 12:** Capture jobs list with progress

3. **View Individual Job Logs**
   - Click on "Lint" job
   - See real-time logs
   
   **Screenshot 13:** Capture lint job logs

4. **View Test Job Details**
   - Click on "Test" job
   - Expand steps to see details
   - Look for pytest output
   
   **Screenshot 14:** Capture test execution logs showing pytest output

5. **View Test Results**
   - Scroll through test job logs
   - Find the test summary (60 tests passed)
   
   **Screenshot 15:** Capture test results summary

---

## 📋 Part 4: View Pipeline Completion

### Step 7: Successful Pipeline Completion

1. **Wait for Completion**
   - Full pipeline takes ~25-35 minutes
   - All jobs should turn green ✅
   
   **Screenshot 16:** Capture completed workflow (all green)

2. **View Workflow Summary**
   - Click on the workflow run title
   - See timing, jobs, and artifacts
   
   **Screenshot 17:** Capture workflow summary page

3. **Check Job Duration**
   - Each job shows duration
   - Total workflow time displayed
   
   **Screenshot 18:** Capture job timings

---

## 📋 Part 5: Download and View Artifacts

### Step 8: Access Artifacts

1. **Scroll to Artifacts Section**
   - At bottom of workflow run page
   - You'll see multiple artifacts:
     - lint-results
     - test-results
     - coverage-reports
     - trained-models
     - mlflow-artifacts
     - docker-image
     - pipeline-summary
   
   **Screenshot 19:** Capture artifacts list

2. **Download Test Results**
   - Click "test-results" to download
   - Extract the zip file
   - Open `test-report.html` in browser
   
   **Screenshot 20:** Capture HTML test report

3. **Download Coverage Reports**
   - Click "coverage-reports" to download
   - Extract and open `htmlcov/index.html`
   
   **Screenshot 21:** Capture HTML coverage report

4. **View Pipeline Summary**
   - Download "pipeline-summary" artifact
   - Open the markdown file
   
   **Screenshot 22:** Capture pipeline summary content

---

## 📋 Part 6: View Pull Request Integration

### Step 9: Create a Test Pull Request

1. **Create New Branch**
   ```bash
   cd /Users/aashishr/codebase/mlso
   git checkout -b feature/test-ci
   
   # Make a small change (e.g., update README)
   echo "\n## CI/CD Test" >> README.md
   
   git add README.md
   git commit -m "test: Trigger CI/CD pipeline"
   git push origin feature/test-ci
   ```

2. **Create Pull Request on GitHub**
   - Go to repository on GitHub
   - Click "Compare & pull request" button
   - Add title: "Test CI/CD Pipeline"
   - Add description
   - Click "Create pull request"
   
   **Screenshot 23:** Capture PR creation page

3. **View PR Checks**
   - PR page shows CI/CD checks running
   - Wait for checks to complete
   
   **Screenshot 24:** Capture PR with running checks

4. **View Check Details**
   - Click "Details" next to a check
   - See job execution in PR context
   
   **Screenshot 25:** Capture PR check details

5. **View Test Results on PR**
   - Automated comment with test results
   - Shows pass/fail status
   
   **Screenshot 26:** Capture PR with test results comment

6. **View All Checks Passed**
   - All checks turn green
   - "All checks have passed" message
   
   **Screenshot 27:** Capture PR with all checks passed

---

## 📋 Part 7: Model Training Pipeline

### Step 10: Trigger Model Training

1. **Go to Actions Tab**
   - Click "Model Training Pipeline" in sidebar
   
   **Screenshot 28:** Capture training pipeline page

2. **Run Training Workflow**
   - Click "Run workflow"
   - Add reason: "Manual training for demonstration"
   - Click "Run workflow"
   
   **Screenshot 29:** Capture training workflow trigger dialog

3. **Monitor Training Execution**
   - Click on running workflow
   - Watch progress through steps:
     - Download data
     - Preprocess data
     - Train models
     - Validate performance
   
   **Screenshot 30:** Capture training workflow in progress

4. **View Training Logs**
   - Click "train-and-validate" job
   - See model training output
   - Look for accuracy and ROC-AUC scores
   
   **Screenshot 31:** Capture training logs with metrics

5. **View Training Completion**
   - Green checkmark when complete
   - Performance metrics displayed
   
   **Screenshot 32:** Capture completed training workflow

6. **Download Trained Models**
   - Scroll to artifacts
   - Download "trained-models" artifact
   
   **Screenshot 33:** Capture training artifacts

---

## 📋 Part 8: Workflow Badges

### Step 11: Add Status Badges to README

1. **Get Badge Markdown**
   - Go to Actions tab
   - Click on workflow (CI/CD Pipeline)
   - Click "..." (three dots) top right
   - Select "Create status badge"
   - Copy markdown
   
   **Screenshot 34:** Capture status badge dialog

2. **View Badges on README**
   - Navigate to repository homepage
   - See badges at top of README
   - Shows current workflow status
   
   **Screenshot 35:** Capture README with status badges

---

## 📋 Part 9: Workflow Insights

### Step 12: View Workflow Analytics

1. **Go to Insights Tab**
   - Click "Insights" (top menu)
   - Then "Actions" in left sidebar
   
   **Screenshot 36:** Capture Actions insights page

2. **View Workflow Runs**
   - See history of all runs
   - Success/failure rates
   - Duration trends
   
   **Screenshot 37:** Capture workflow runs history

3. **View Workflow Usage**
   - See minutes used
   - Storage used for artifacts
   
   **Screenshot 38:** Capture usage statistics

---

## 📋 Part 10: Advanced Features

### Step 13: View Workflow Graph

1. **Workflow Visualization**
   - Click on any completed workflow run
   - View job dependencies and flow
   
   **Screenshot 39:** Capture workflow graph visualization

2. **Job Matrix (if using)**
   - Shows parallel jobs
   - Matrix strategy execution
   
   **Screenshot 40:** Capture job matrix view

### Step 14: View Re-run Options

1. **Re-run Failed Jobs**
   - Click "Re-run jobs" dropdown
   - Options:
     - Re-run all jobs
     - Re-run failed jobs
   
   **Screenshot 41:** Capture re-run options

2. **View Job Annotations**
   - Warnings or errors highlighted
   - Click to see details
   
   **Screenshot 42:** Capture job annotations

---

## 📋 Part 11: Documentation Screenshots

### Step 15: Project Structure Screenshots

1. **Repository File Structure**
   - Main repository page
   - Show folder structure
   
   **Screenshot 43:** Capture repository file tree

2. **Workflows Folder**
   - Navigate to `.github/workflows/`
   - Show workflow files
   
   **Screenshot 44:** Capture workflows directory

3. **Tests Folder**
   - Navigate to `tests/`
   - Show test files
   
   **Screenshot 45:** Capture tests directory

4. **Documentation**
   - Show list of markdown files
   - Highlight CI/CD documentation
   
   **Screenshot 46:** Capture documentation files

---

## 📋 Part 12: Deployment Screenshots (Bonus)

### Step 16: Docker Build Artifacts

1. **View Docker Job**
   - Click on "Build Docker" job
   - See Docker build steps
   
   **Screenshot 47:** Capture Docker build logs

2. **Docker Image Artifact**
   - Download docker-image artifact
   - Show file size and details
   
   **Screenshot 48:** Capture Docker artifact details

### Step 17: Kubernetes Deployment (if applicable)

1. **Show Kubernetes Manifests**
   - Navigate to `deployment/kubernetes/`
   - Show YAML files
   
   **Screenshot 49:** Capture Kubernetes manifests

2. **Deployment Configuration**
   - Open deployment.yaml
   - Show configuration
   
   **Screenshot 50:** Capture deployment configuration

---

## 📊 Complete Screenshot Checklist

### Essential Screenshots (Must Have):

#### Repository Setup
- [ ] Screenshot 1: GitHub new repository page
- [ ] Screenshot 2: Repository configuration
- [ ] Screenshot 3: Git push command successful
- [ ] Screenshot 4: Repository with all files

#### Actions Setup
- [ ] Screenshot 5: GitHub Actions tab
- [ ] Screenshot 6: Detected workflows
- [ ] Screenshot 7: CI/CD workflow file
- [ ] Screenshot 8: Training workflow file

#### Pipeline Execution
- [ ] Screenshot 9: Run workflow dialog
- [ ] Screenshot 10: Workflow starting
- [ ] Screenshot 11: Workflow visualization
- [ ] Screenshot 12: Jobs progress
- [ ] Screenshot 13: Lint job logs
- [ ] Screenshot 14: Test execution
- [ ] Screenshot 15: Test results summary
- [ ] Screenshot 16: Completed workflow (all green)
- [ ] Screenshot 17: Workflow summary
- [ ] Screenshot 18: Job timings

#### Artifacts & Results
- [ ] Screenshot 19: Artifacts list
- [ ] Screenshot 20: HTML test report
- [ ] Screenshot 21: Coverage report
- [ ] Screenshot 22: Pipeline summary

#### Pull Request Integration
- [ ] Screenshot 23: PR creation
- [ ] Screenshot 24: PR with checks running
- [ ] Screenshot 25: Check details
- [ ] Screenshot 26: Test results comment
- [ ] Screenshot 27: All checks passed

#### Model Training
- [ ] Screenshot 28: Training pipeline
- [ ] Screenshot 29: Training trigger
- [ ] Screenshot 30: Training in progress
- [ ] Screenshot 31: Training logs with metrics
- [ ] Screenshot 32: Training completed
- [ ] Screenshot 33: Training artifacts

#### Badges & Analytics
- [ ] Screenshot 34: Status badge
- [ ] Screenshot 35: README with badges
- [ ] Screenshot 36: Actions insights
- [ ] Screenshot 37: Workflow history
- [ ] Screenshot 38: Usage statistics

#### Additional
- [ ] Screenshot 39: Workflow graph
- [ ] Screenshot 40: Job matrix
- [ ] Screenshot 41: Re-run options
- [ ] Screenshot 42: Job annotations

#### Documentation
- [ ] Screenshot 43: Repository structure
- [ ] Screenshot 44: Workflows folder
- [ ] Screenshot 45: Tests folder
- [ ] Screenshot 46: Documentation files

#### Deployment
- [ ] Screenshot 47: Docker build
- [ ] Screenshot 48: Docker artifact
- [ ] Screenshot 49: K8s manifests
- [ ] Screenshot 50: Deployment config

---

## 🎨 Screenshot Best Practices

### Quality Guidelines

1. **Resolution**
   - Minimum: 1920x1080
   - Use full-screen captures when possible

2. **Annotations**
   - Use arrows to highlight important elements
   - Add text labels for clarity
   - Use consistent colors (red for important, blue for info)

3. **Naming Convention**
   ```
   01_github_new_repository.png
   02_repository_configuration.png
   03_git_push_success.png
   ...
   50_deployment_config.png
   ```

4. **Tools Recommended**
   - **macOS:** Cmd+Shift+4 (area), Cmd+Shift+3 (full screen)
   - **Windows:** Snipping Tool, Win+Shift+S
   - **Annotation:** Skitch, Snagit, or built-in Preview/Paint

5. **Storage**
   ```
   screenshots/
   ├── 01-repository-setup/
   ├── 02-actions-setup/
   ├── 03-pipeline-execution/
   ├── 04-artifacts/
   ├── 05-pull-request/
   └── 06-training/
   ```

---

## 📝 Documentation Template

### Create a Screenshots Document

```markdown
# CI/CD Pipeline Screenshots

## 1. Repository Setup
![Repository Creation](screenshots/01_github_new_repository.png)
*Creating new repository on GitHub*

![Repository Configuration](screenshots/02_repository_configuration.png)
*Configuring repository settings*

## 2. Pipeline Execution
![Workflow Running](screenshots/11_workflow_visualization.png)
*CI/CD pipeline executing all jobs*

![Test Results](screenshots/15_test_results_summary.png)
*60 tests passed successfully*

## 3. Artifacts
![Test Report](screenshots/20_html_test_report.png)
*Detailed HTML test report*

## 4. Pull Request Integration
![PR Checks](screenshots/27_all_checks_passed.png)
*All CI/CD checks passed on Pull Request*
```

---

## 🚀 Quick Command Reference

### Push to GitHub
```bash
cd /Users/aashishr/codebase/mlso
git push origin main
```

### Create Test Branch
```bash
git checkout -b feature/test-ci
echo "\n## CI/CD Test" >> README.md
git add README.md
git commit -m "test: Trigger CI/CD"
git push origin feature/test-ci
```

### View Workflows
```bash
# List workflow runs
gh run list

# View specific run
gh run view <run-id>

# Download artifacts
gh run download <run-id>
```

---

## ✅ Verification Checklist

Before sharing screenshots, verify:
- [ ] All workflows executed successfully (green checkmarks)
- [ ] Test results show 60 tests passed
- [ ] Coverage reports generated
- [ ] Artifacts available for download
- [ ] PR integration working
- [ ] Model training completed
- [ ] Status badges showing on README
- [ ] Screenshots are clear and annotated
- [ ] All critical steps documented

---

## 🎯 Timeline Estimate

| Task | Duration |
|------|----------|
| Push to GitHub | 5 min |
| Initial workflow run | 25-35 min |
| Capture execution screenshots | 10 min |
| Create test PR | 5 min |
| PR checks completion | 8-12 min |
| Capture PR screenshots | 5 min |
| Training pipeline run | 12-18 min |
| Capture training screenshots | 5 min |
| Organize and annotate | 15 min |
| **Total** | **90-120 min** |

---

## 📞 Troubleshooting

### Common Issues

1. **Workflows not appearing**
   - Ensure `.github/workflows/*.yml` files are pushed
   - Check Actions tab permissions (Settings → Actions)

2. **Workflow fails**
   - Check job logs for errors
   - Verify Python version compatibility
   - Check if secrets are needed

3. **Artifacts not appearing**
   - Wait for workflow to complete
   - Check artifact retention period
   - Verify artifact upload step succeeded

4. **PR checks not running**
   - Check branch protection rules
   - Verify workflow triggers include `pull_request`
   - Check Actions permissions

---

## 📚 Additional Resources

- **GitHub Actions Documentation:** https://docs.github.com/en/actions
- **Workflow Syntax:** https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions
- **Your CI/CD Guide:** `CI_CD_DOCUMENTATION.md`
- **Quick Reference:** `CI_CD_QUICK_REFERENCE.md`

---

**Created:** December 26, 2025  
**Purpose:** Complete guide for CI/CD pipeline setup and screenshot documentation  
**Total Screenshots:** 50 comprehensive screenshots  
**Estimated Time:** 90-120 minutes  

🎉 **Follow this guide to create professional CI/CD pipeline documentation with complete visual proof!**

