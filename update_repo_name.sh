#!/bin/bash

# Repository Name Change Script
# Automates local git remote update after GitHub repository rename
# From: mlso → mlops-assign-heart-prediction

set -e  # Exit on error

echo "=========================================="
echo "🔄 Repository Rename Helper Script"
echo "=========================================="
echo ""
echo "This script will help you update your local repository"
echo "after renaming on GitHub."
echo ""
echo "Old name: mlso"
echo "New name: mlops-assign-heart-prediction"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Error: Not a git repository!${NC}"
    echo "Please run this script from the project root directory."
    exit 1
fi

echo "=========================================="
echo "📍 Current Status"
echo "=========================================="
echo ""

# Show current location
echo -e "${BLUE}Current directory:${NC}"
pwd
echo ""

# Show current remote
echo -e "${BLUE}Current git remote:${NC}"
git remote -v
echo ""

# Check if already updated
CURRENT_REMOTE=$(git remote get-url origin)
if [[ "$CURRENT_REMOTE" == *"mlops-assign-heart-prediction"* ]]; then
    echo -e "${GREEN}✅ Remote is already updated!${NC}"
    echo "Current remote: $CURRENT_REMOTE"
    echo ""
    echo "Nothing to do. Your repository is already using the new name."
    exit 0
fi

echo "=========================================="
echo "⚠️  Important: GitHub Rename First!"
echo "=========================================="
echo ""
echo "Before running this script, you MUST rename the repository on GitHub:"
echo ""
echo "1. Go to: https://github.com/sanepr/mlso/settings"
echo "2. Find 'Repository name' section at the top"
echo "3. Change 'mlso' to 'mlops-assign-heart-prediction'"
echo "4. Click 'Rename' button"
echo "5. Confirm the rename"
echo ""
read -p "Have you renamed the repository on GitHub? (yes/no): " RENAMED

if [ "$RENAMED" != "yes" ] && [ "$RENAMED" != "y" ]; then
    echo ""
    echo -e "${YELLOW}Please complete the GitHub rename first, then run this script again.${NC}"
    exit 0
fi

echo ""
echo "=========================================="
echo "🔧 Step 1: Update Git Remote"
echo "=========================================="
echo ""

OLD_URL="git@github.com:sanepr/mlso.git"
NEW_URL="git@github.com:sanepr/mlops-assign-heart-prediction.git"

echo "Updating remote URL..."
echo "From: $OLD_URL"
echo "To:   $NEW_URL"
echo ""

git remote set-url origin "$NEW_URL"

echo -e "${GREEN}✅ Remote URL updated!${NC}"
echo ""

# Verify new remote
echo "New remote configuration:"
git remote -v
echo ""

# Test connection
echo "Testing connection to GitHub..."
if git fetch origin --dry-run 2>&1 | grep -q "fatal\|error"; then
    echo -e "${RED}❌ Connection test failed!${NC}"
    echo "Please check:"
    echo "1. Repository was renamed on GitHub"
    echo "2. Your SSH key is configured correctly"
    echo "3. You have access to the repository"
    exit 1
else
    echo -e "${GREEN}✅ Connection test successful!${NC}"
fi
echo ""

echo "=========================================="
echo "📁 Step 2: Rename Local Directory?"
echo "=========================================="
echo ""
echo "Current directory: $(pwd)"
echo ""
echo "Would you like to rename the local directory to match?"
echo "This will rename: mlso → mlops-assign-heart-prediction"
echo ""
read -p "Rename local directory? (yes/no): " RENAME_DIR

if [ "$RENAME_DIR" = "yes" ] || [ "$RENAME_DIR" = "y" ]; then
    echo ""
    CURRENT_DIR=$(basename "$(pwd)")
    PARENT_DIR=$(dirname "$(pwd)")

    if [ "$CURRENT_DIR" != "mlso" ]; then
        echo -e "${YELLOW}⚠️  Current directory is not named 'mlso'${NC}"
        echo "Current name: $CURRENT_DIR"
        echo "Skipping directory rename."
    else
        echo "Renaming directory..."
        cd "$PARENT_DIR"
        mv mlso mlops-assign-heart-prediction
        cd mlops-assign-heart-prediction
        echo -e "${GREEN}✅ Directory renamed!${NC}"
        echo "New location: $(pwd)"
    fi
else
    echo "Skipping directory rename."
fi

echo ""
echo "=========================================="
echo "✅ Verification"
echo "=========================================="
echo ""

# Show final status
echo -e "${BLUE}Git status:${NC}"
git status
echo ""

echo -e "${BLUE}Git remote:${NC}"
git remote -v
echo ""

echo -e "${BLUE}Current location:${NC}"
pwd
echo ""

echo "=========================================="
echo "🎉 Success!"
echo "=========================================="
echo ""
echo "Your repository has been successfully updated!"
echo ""
echo "Next steps:"
echo "1. Test pushing: git push origin main"
echo "2. View on GitHub: https://github.com/sanepr/mlops-assign-heart-prediction"
echo "3. Verify CI/CD pipelines still work"
echo ""
echo -e "${GREEN}✅ Repository rename complete!${NC}"
echo ""

# Optional: Show reminder for other machines
echo "=========================================="
echo "📝 For Other Machines"
echo "=========================================="
echo ""
echo "If you have clones on other computers, run this command on each:"
echo ""
echo -e "${YELLOW}git remote set-url origin git@github.com:sanepr/mlops-assign-heart-prediction.git${NC}"
echo ""

