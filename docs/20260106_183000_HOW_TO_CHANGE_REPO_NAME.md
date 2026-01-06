# 🔄 How to Change Git Repository Name

**Complete Guide to Rename Repository from `mlso` to `mlops-assign-heart-prediction`**

---

## 📋 Overview

**Current Name:** `mlso`  
**New Name:** `mlops-assign-heart-prediction`  
**Current Remote:** `git@github.com:sanepr/mlso.git`  
**New Remote:** `git@github.com:sanepr/mlops-assign-heart-prediction.git`

---

## ✅ Step-by-Step Process

### Step 1: Rename Repository on GitHub (Required)

1. **Go to GitHub Repository Settings:**
   ```
   https://github.com/sanepr/mlso/settings
   ```

2. **Find "Repository name" section:**
   - It's at the top of the General settings page
   - Current name shows: `mlso`

3. **Change the name:**
   - Type new name: `mlops-assign-heart-prediction`
   - Click "Rename" button

4. **Confirm:**
   - GitHub will show a warning about impacts
   - Type the repository name to confirm
   - Click "I understand, rename repository"

**⚠️ Important:**
- GitHub automatically redirects old URLs for a while
- Existing clones will still work temporarily
- Update local remotes to avoid confusion

---

### Step 2: Update Local Git Remote (Required)

After renaming on GitHub, update your local repository:

```bash
# Navigate to your project
cd /Users/aashishr/codebase/mlso

# Update remote URL to new repository name
git remote set-url origin git@github.com:sanepr/mlops-assign-heart-prediction.git

# Verify the change
git remote -v

# Expected output:
# origin  git@github.com:sanepr/mlops-assign-heart-prediction.git (fetch)
# origin  git@github.com:sanepr/mlops-assign-heart-prediction.git (push)

# Test the connection
git fetch origin

# Should work without errors
```

---

### Step 3: Rename Local Directory (Optional but Recommended)

Keep your local folder name in sync:

```bash
# Go to parent directory
cd /Users/aashishr/codebase

# Rename the directory
mv mlso mlops-assign-heart-prediction

# Navigate into renamed directory
cd mlops-assign-heart-prediction

# Verify git still works
git status

# Should show "On branch main" or your current branch
```

---

### Step 4: Update Documentation References (Already Done ✅)

The following files have already been updated with new repository name:

- ✅ `README.md` - All GitHub URLs and badges
- ✅ `setup.py` - Package name
- ✅ `notebooks/README.md` - Kernel names
- ✅ All documentation files in `docs/`
- ✅ `monitoring/check_monitoring.sh` - Path references

**No additional file changes needed!**

---

### Step 5: Push and Verify

```bash
# Make sure you're on the correct branch
git branch

# Push to verify new remote works
git push origin main

# Should push successfully to new repository name
```

---

## 🖥️ Complete Terminal Commands

Run these commands in order:

```bash
# ===================================
# STEP 1: CHECK CURRENT STATUS
# ===================================
cd /Users/aashishr/codebase/mlso
git remote -v
echo "Current remote shown above ☝️"
echo ""
echo "Now go to GitHub and rename the repository!"
echo "Visit: https://github.com/sanepr/mlso/settings"
echo ""
read -p "Press Enter after you've renamed the repo on GitHub..."

# ===================================
# STEP 2: UPDATE LOCAL GIT REMOTE
# ===================================
echo "Updating local git remote..."
git remote set-url origin git@github.com:sanepr/mlops-assign-heart-prediction.git

echo "Verifying new remote..."
git remote -v

echo "Testing connection..."
git fetch origin

echo "✅ Git remote updated successfully!"
echo ""

# ===================================
# STEP 3: RENAME LOCAL DIRECTORY
# ===================================
read -p "Do you want to rename the local directory too? (y/n): " RENAME_DIR

if [ "$RENAME_DIR" = "y" ] || [ "$RENAME_DIR" = "Y" ]; then
    echo "Renaming local directory..."
    cd /Users/aashishr/codebase
    mv mlso mlops-assign-heart-prediction
    cd mlops-assign-heart-prediction
    echo "✅ Directory renamed!"
    echo "New location: $(pwd)"
else
    echo "Skipping directory rename."
fi

# ===================================
# STEP 4: VERIFY EVERYTHING WORKS
# ===================================
echo ""
echo "Final verification..."
git status
echo ""
echo "✅ All done! Repository successfully renamed."
echo ""
echo "New repository URL: https://github.com/sanepr/mlops-assign-heart-prediction"
```

---

## 🎯 Quick Command Reference

### Check current remote:
```bash
git remote -v
```

### Update remote URL:
```bash
git remote set-url origin git@github.com:sanepr/mlops-assign-heart-prediction.git
```

### Verify change:
```bash
git fetch origin
git push origin main
```

### Rename local directory:
```bash
cd /Users/aashishr/codebase
mv mlso mlops-assign-heart-prediction
```

---

## 🔍 Verification Checklist

After completing all steps:

- [ ] GitHub repository shows new name: `mlops-assign-heart-prediction`
- [ ] `git remote -v` shows new URL
- [ ] `git fetch origin` works without errors
- [ ] `git push origin main` works successfully
- [ ] Local directory renamed (optional)
- [ ] GitHub Actions still work
- [ ] README badges display correctly
- [ ] All documentation links work

---

## 🚨 Troubleshooting

### Problem: "Repository not found" error

**Solution:**
```bash
# Make sure you completed Step 1 on GitHub first
# Then update remote:
git remote set-url origin git@github.com:sanepr/mlops-assign-heart-prediction.git
```

### Problem: Permission denied

**Solution:**
```bash
# Check SSH key is configured
ssh -T git@github.com

# Should show: "Hi sanepr! You've successfully authenticated..."
```

### Problem: Old URL still showing

**Solution:**
```bash
# Remove and re-add remote
git remote remove origin
git remote add origin git@github.com:sanepr/mlops-assign-heart-prediction.git
git fetch origin
```

---

## 📝 What Happens to Old URLs?

### GitHub Redirects (Automatic)
- `github.com/sanepr/mlso` → redirects to new name
- Old clone/push URLs continue to work temporarily
- Existing clones on other machines keep working

### But You Should Update Because:
- Redirects may not last forever
- Cleaner to use correct names
- Avoids confusion in logs/error messages
- Better for collaboration

---

## 👥 For Team Members / Other Machines

If you have clones on other computers:

```bash
# On each machine where you have a clone
cd /path/to/mlso

# Update the remote
git remote set-url origin git@github.com:sanepr/mlops-assign-heart-prediction.git

# Verify
git remote -v
git fetch origin

# Optionally rename directory
cd ..
mv mlso mlops-assign-heart-prediction
```

---

## 📊 Impact Analysis

### ✅ No Impact (Already Updated)
- All code references in files
- Documentation URLs
- Package names
- Script paths

### ⚠️ Requires Manual Action
1. **GitHub repository rename** (via Settings)
2. **Local git remote update** (via git command)
3. **Local directory rename** (optional)

### ℹ️ Auto-Handled by GitHub
- URL redirects (temporary)
- Issues and PRs
- Wiki pages
- GitHub Actions workflows

---

## 🎯 Summary

### Required Actions:
1. ✅ **On GitHub:** Rename repository in Settings
2. ✅ **Locally:** Update git remote URL
3. ⭕ **Optional:** Rename local directory

### Already Complete:
- All code files updated
- Documentation references fixed
- Package names changed
- Ready to use new name

**Total Time:** ~5 minutes

---

## 📚 Additional Resources

### GitHub Documentation:
- [Renaming a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository)
- [Changing a remote's URL](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories)

### Project Documentation:
- `docs/20260106_182957_REPOSITORY_NAME_CHANGE.md` - Technical change log
- `README.md` - Updated with new name

---

## ✅ Ready to Execute

All file changes have been completed. You just need to:

1. **Rename on GitHub** (2 minutes)
2. **Run update commands** (1 minute)
3. **Test and verify** (2 minutes)

**New Repository URL:**
```
https://github.com/sanepr/mlops-assign-heart-prediction
```

---

**Created:** January 6, 2026  
**Status:** Ready to Execute  
**Files Updated:** 11 (already complete)  
**Action Required:** GitHub rename + local git remote update

