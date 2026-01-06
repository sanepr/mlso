# 🎯 Repository Rename - Quick Reference

**From:** `mlso` → **To:** `mlops-assign-heart-prediction`

---

## ⚡ Quick Steps

### 1️⃣ On GitHub (2 min)
```
Go to: https://github.com/sanepr/mlso/settings
→ Repository name: mlops-assign-heart-prediction
→ Click "Rename"
→ Confirm
```

### 2️⃣ Update Local Git (1 min)
```bash
cd /Users/aashishr/codebase/mlso
git remote set-url origin git@github.com:sanepr/mlops-assign-heart-prediction.git
git remote -v  # Verify
```

### 3️⃣ Optional: Rename Directory
```bash
cd /Users/aashishr/codebase
mv mlso mlops-assign-heart-prediction
cd mlops-assign-heart-prediction
```

---

## 🤖 Automated Script

We've created a helper script for you:

```bash
# Run the automated script
./update_repo_name.sh

# It will:
# ✅ Check current status
# ✅ Update git remote
# ✅ Test connection
# ✅ Optionally rename directory
# ✅ Verify everything works
```

---

## 📋 Command Cheat Sheet

| Action | Command |
|--------|---------|
| Check current remote | `git remote -v` |
| Update remote URL | `git remote set-url origin git@github.com:sanepr/mlops-assign-heart-prediction.git` |
| Test connection | `git fetch origin` |
| Check status | `git status` |
| Push to verify | `git push origin main` |
| View on GitHub | `https://github.com/sanepr/mlops-assign-heart-prediction` |

---

## ✅ Verification Checklist

- [ ] Renamed on GitHub
- [ ] Local remote updated (`git remote -v`)
- [ ] Connection works (`git fetch origin`)
- [ ] Can push (`git push origin main`)
- [ ] GitHub Actions still work
- [ ] Badges display correctly

---

## 🆘 Quick Fixes

**Problem:** Repository not found
```bash
# Make sure you renamed on GitHub first!
# Then update remote:
git remote set-url origin git@github.com:sanepr/mlops-assign-heart-prediction.git
```

**Problem:** Permission denied
```bash
# Check SSH key:
ssh -T git@github.com
```

**Problem:** Old URL showing
```bash
# Remove and re-add:
git remote remove origin
git remote add origin git@github.com:sanepr/mlops-assign-heart-prediction.git
```

---

## 📚 Full Documentation

See detailed guide:
- `docs/20260106_183000_HOW_TO_CHANGE_REPO_NAME.md`
- `docs/20260106_182957_REPOSITORY_NAME_CHANGE.md`

---

## 🎯 Status

**Code Changes:** ✅ Complete (11 files updated)  
**GitHub Rename:** ⏳ Pending (you need to do this)  
**Local Update:** ⏳ Pending (run script or commands)

**Total Time:** ~5 minutes

---

**Created:** January 6, 2026  
**Quick Script:** `./update_repo_name.sh`  
**New URL:** `https://github.com/sanepr/mlops-assign-heart-prediction`

