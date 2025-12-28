# Documentation File Naming Instructions for AI Tools

## Purpose
This file provides instructions for AI assistants (GitHub Copilot, ChatGPT, etc.) on how to name documentation files in this project.

---

## File Naming Convention

### Format
All documentation files (except `README.md`) MUST follow this naming pattern:

```
YYYYMMDD_HHMMSS_DESCRIPTIVE_NAME.md
```

### Components
- **YYYYMMDD**: Date in format Year-Month-Day (e.g., 20251228)
- **HHMMSS**: Time in 24-hour format Hour-Minute-Second (e.g., 143022)
- **DESCRIPTIVE_NAME**: Clear, descriptive filename in UPPERCASE_SNAKE_CASE
- **.md**: Markdown file extension

### Examples
```
✅ CORRECT:
20251228_143022_DOCKER_FIX_GUIDE.md
20251228_090530_API_DEPLOYMENT_STEPS.md
20251227_155500_KUBERNETES_TROUBLESHOOTING.md
20251226_120000_TEST_FAILURES_RESOLVED.md

❌ INCORRECT:
DOCKER_FIX_GUIDE.md              (missing datetime)
20251228_docker_fix.md           (lowercase, missing time)
docker-fix-guide.md              (no datetime, wrong case)
2025-12-28_DOCKER_FIX.md        (wrong date format)
```

---

## When to Apply This Convention

### Apply Datetime Prefix To:
- ✅ Fix documentation (e.g., `DOCKER_FIX.md`, `TEST_FAILURES.md`)
- ✅ Troubleshooting guides (e.g., `K8S_TIMEOUT_FIX.md`)
- ✅ Implementation summaries (e.g., `CI_CD_IMPLEMENTATION.md`)
- ✅ Status reports (e.g., `DEPLOYMENT_STATUS.md`)
- ✅ Quick reference guides (e.g., `DOCKER_QUICKREF.md`)
- ✅ Setup guides (e.g., `GITHUB_SETUP_GUIDE.md`)
- ✅ Any timestamped documentation

### Do NOT Apply To:
- ❌ `README.md` (main project README - always keep this name)
- ❌ `docs/README.md` (documentation index - always keep this name)
- ❌ Configuration files (`.gitignore`, `pytest.ini`, etc.)
- ❌ Source code files (`.py`, `.js`, etc.)

---

## Location

### Documentation Directory
All documentation files MUST be placed in:
```
/docs/
```

### Root Directory
Only `README.md` should remain in the root directory.

---

## Implementation Instructions for AI Tools

### When Creating a New Documentation File:

1. **Determine Current Datetime**
   ```python
   from datetime import datetime
   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   ```

2. **Create Descriptive Name**
   - Use UPPERCASE_SNAKE_CASE
   - Be specific and clear
   - Use common prefixes:
     - `DOCKER_` - Docker related
     - `K8S_` or `KUBERNETES_` - Kubernetes related
     - `CI_CD_` - CI/CD pipeline related
     - `TEST_` - Testing related
     - `MODEL_` - Model/ML related
     - `API_` - API related
     - `FIX_` or `_FIXED` - Problem resolution

3. **Construct Filename**
   ```
   filename = f"{timestamp}_{descriptive_name}.md"
   # Example: "20251228_143022_DOCKER_DEPLOYMENT_FIX.md"
   ```

4. **Set Full Path**
   ```
   filepath = f"docs/{filename}"
   # Full path: "docs/20251228_143022_DOCKER_DEPLOYMENT_FIX.md"
   ```

5. **Create File**
   - Create the file in the `docs/` directory
   - Use the constructed filename
   - Include proper markdown formatting

---

## Python Implementation Example

```python
from datetime import datetime
from pathlib import Path

def create_doc_file(descriptive_name: str, content: str) -> str:
    """
    Create a documentation file with proper naming convention.
    
    Args:
        descriptive_name: Descriptive name in UPPERCASE_SNAKE_CASE
        content: File content
        
    Returns:
        Created filename
    """
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Construct filename
    filename = f"{timestamp}_{descriptive_name}.md"
    
    # Full path
    filepath = Path("docs") / filename
    
    # Ensure docs directory exists
    filepath.parent.mkdir(exist_ok=True)
    
    # Write file
    filepath.write_text(content)
    
    return str(filepath)

# Usage example
create_doc_file(
    "DOCKER_FIX_SUMMARY",
    "# Docker Fix Summary\n\n..."
)
# Creates: docs/20251228_143022_DOCKER_FIX_SUMMARY.md
```

---

## Bash Implementation Example

```bash
#!/bin/bash

# Function to create documentation file
create_doc_file() {
    local descriptive_name="$1"
    local content="$2"
    
    # Get current timestamp
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    
    # Construct filename
    local filename="${timestamp}_${descriptive_name}.md"
    
    # Full path
    local filepath="docs/${filename}"
    
    # Create docs directory if needed
    mkdir -p docs
    
    # Write file
    echo "$content" > "$filepath"
    
    echo "Created: $filepath"
}

# Usage example
create_doc_file "DOCKER_FIX_SUMMARY" "# Docker Fix Summary

..."
# Creates: docs/20251228_143022_DOCKER_FIX_SUMMARY.md
```

---

## Naming Guidelines

### Descriptive Name Best Practices

#### Good Names (Clear and Specific):
- `DOCKER_DAEMON_CONNECTION_FIX`
- `K8S_DEPLOYMENT_TIMEOUT_RESOLVED`
- `CI_CD_ARTIFACT_VERSION_UPDATE`
- `MODEL_VALIDATION_METADATA_FIX`
- `API_HEALTH_ENDPOINT_NOT_RESPONDING`

#### Poor Names (Too Generic):
- `FIX` (what fix?)
- `ISSUE` (what issue?)
- `UPDATE` (update what?)
- `CHANGES` (what changes?)
- `DOC` (too vague)

#### Name Structure:
```
[COMPONENT]_[SPECIFIC_ISSUE]_[ACTION]

Examples:
DOCKER_DAEMON_FIX           (Component: Docker, Issue: Daemon, Action: Fix)
K8S_TIMEOUT_RESOLVED        (Component: K8s, Issue: Timeout, Action: Resolved)
CI_CD_TEST_FAILURES_FIXED   (Component: CI/CD, Issue: Test Failures, Action: Fixed)
```

---

## File Content Template

When creating a new documentation file, use this template:

```markdown
# [Title]

## Issue/Purpose

[Brief description of what this document addresses]

---

## [Main Content Sections]

[Detailed content here]

---

## Summary

[Quick summary]

---

**Created:** [Date in human readable format, e.g., December 28, 2025]
**Status:** ✅ [Status]
**Related:** [Links to related docs if any]
```

---

## Verification Checklist

Before creating a documentation file, verify:

- [ ] Filename starts with `YYYYMMDD_HHMMSS_`
- [ ] Descriptive name is in UPPERCASE_SNAKE_CASE
- [ ] File extension is `.md`
- [ ] File is placed in `docs/` directory
- [ ] Name is descriptive and specific
- [ ] Follows component naming conventions
- [ ] Not conflicting with special files (`README.md`)

---

## Git Operations

When creating new documentation files:

```bash
# After creating the file
git add docs/YYYYMMDD_HHMMSS_FILENAME.md
git commit -m "docs: Add [descriptive message]"
git push origin main
```

---

## Integration with AI Tools

### For GitHub Copilot
Add this instruction in comments before generating files:
```python
# INSTRUCTION: Create documentation file following naming convention
# Format: YYYYMMDD_HHMMSS_DESCRIPTIVE_NAME.md in docs/ folder
# Example: docs/20251228_143022_DOCKER_FIX.md
```

### For ChatGPT/Claude/Other AI
Include this prompt:
```
"Create a documentation file following our naming convention:
Format: docs/YYYYMMDD_HHMMSS_DESCRIPTIVE_NAME.md
Use current datetime and an appropriate descriptive name in UPPERCASE_SNAKE_CASE"
```

---

## Exceptions

### When NOT to Use Datetime Prefix:

1. **README.md files**
   - Project root: `README.md`
   - Docs folder: `docs/README.md`

2. **Configuration files**
   - `.gitignore`, `pytest.ini`, `.flake8`, etc.

3. **Source code**
   - Python: `*.py`
   - JavaScript: `*.js`, `*.ts`
   - Any programming language files

4. **Data files**
   - CSV, JSON, pickle files
   - Model files (`.pkl`, `.h5`, etc.)

---

## Migration of Existing Files

If you encounter files without datetime prefixes:

```bash
# Use this script to add datetime prefix
for file in docs/*.md; do
    if [ "$file" != "docs/README.md" ]; then
        timestamp=$(stat -f "%Sm" -t "%Y%m%d_%H%M%S" "$file")
        newname="docs/${timestamp}_$(basename "$file")"
        git mv "$file" "$newname"
    fi
done
```

---

## FAQ

**Q: What if two files are created in the same second?**
A: Add a suffix like `_v2` or wait 1 second before creating the next file.

**Q: Can I use lowercase in the descriptive name?**
A: No, always use UPPERCASE_SNAKE_CASE for consistency.

**Q: Should I rename README.md?**
A: No, README.md should never have a datetime prefix.

**Q: What timezone should I use?**
A: Use local system time. The important part is having a timestamp, not the timezone.

**Q: Can I modify the datetime of an existing file?**
A: No, the datetime represents when the file was created. Don't modify it.

---

## Summary

### Quick Rules:
1. ✅ Format: `YYYYMMDD_HHMMSS_DESCRIPTIVE_NAME.md`
2. ✅ Location: `docs/` folder
3. ✅ Case: UPPERCASE_SNAKE_CASE
4. ✅ Exception: `README.md` (no prefix)
5. ✅ Be descriptive and specific

### Example Workflow:
```python
# 1. Get timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# 2. Create descriptive name
name = "DOCKER_DEPLOYMENT_FIX"

# 3. Construct filename
filename = f"docs/{timestamp}_{name}.md"

# 4. Create file
with open(filename, 'w') as f:
    f.write(content)
```

---

**This file:** `AI_DOCUMENTATION_NAMING_INSTRUCTIONS.md`  
**Created:** December 28, 2025  
**Status:** ✅ Active  
**Purpose:** Guide AI tools in creating properly named documentation files

