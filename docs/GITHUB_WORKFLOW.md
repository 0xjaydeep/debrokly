# GitHub Workflow Guide

## 🚀 **Quick Setup**

### 1. Create All Issues
```bash
# Run the automated script
./create-github-issues.sh

# Or manually review and create selected issues
gh issue list  # View created issues
```

### 2. Create Project Board (Optional)
```bash
gh project create --title "Debrokly Development" --body "Credit card statement analyzer development tracking"
```

### 3. Start Development
```bash
# Example: Work on critical path traversal fix
git checkout -b security/issue-1-path-traversal
# Make your changes
git commit -m "Security: Fix path traversal vulnerability in exporter

- Sanitize bank names before path construction  
- Add whitelist validation for known banks
- Prevent directory traversal attacks

Fixes #1"
git push -u origin security/issue-1-path-traversal
gh pr create --title "🔒 Fix Critical Path Traversal Vulnerability" --body "Fixes #1"
```

---

## 📋 **Issue Templates Created**

### **🔴 Critical Issues (5)**
1. **#1** - 🚨 Path Traversal Vulnerability (Security)
2. **#2** - 🔴 Date Parsing Priority Bug (Data Integrity)  
3. **#3** - 🔴 Month Folder Detection Bug (Organization)
4. **#4** - 🔴 Float Conversion Crash (Stability)
5. **#5** - 🔴 Hard OCR Dependencies (Deployment)

### **🟡 High Priority Issues (2)**  
6. **#6** - 🟡 AU Bank Transaction Extraction (Feature)
7. **#7** - 🟡 Duplicate Detection Flaw (Data Loss)

### **🟢 Medium Priority Issues (2)**
8. **#8** - 🟢 Proper Logging System (Code Quality)  
9. **#9** - 🟢 Input Validation (Security Enhancement)

---

## 🌿 **Branch Naming Convention**

### **Format**: `type/issue-number-short-description`

**Types:**
- `security/` - Security fixes
- `bugfix/` - Bug fixes  
- `feature/` - New features
- `enhancement/` - Improvements
- `hotfix/` - Critical production fixes

**Examples:**
```bash
security/issue-1-path-traversal
bugfix/issue-2-date-parsing-priority  
bugfix/issue-3-month-folder-detection
bugfix/issue-4-float-conversion-crash
bugfix/issue-5-ocr-dependencies
feature/issue-6-au-bank-support
bugfix/issue-7-duplicate-detection
enhancement/issue-8-logging-system
enhancement/issue-9-input-validation
```

---

## 🏷️ **GitHub Labels Created**

### **Priority Labels**
- `critical` 🔴 - Fix immediately
- `high` 🟡 - High priority  
- `medium` 🟢 - Medium priority
- `low` 🔵 - Low priority

### **Type Labels**
- `security` - Security vulnerability
- `bug` - Something isn't working
- `enhancement` - New feature or improvement

### **Component Labels**  
- `hdfc` - HDFC Bank related
- `aubank` - AU Bank related
- `ocr` - OCR/image processing

---

## 🔄 **Development Workflow**

### **1. Issue Selection**
```bash
# View all issues
gh issue list

# View by priority  
gh issue list --label "critical"
gh issue list --label "high"

# View by type
gh issue list --label "security"
gh issue list --label "bug"
```

### **2. Branch Creation**
```bash
# Create branch for issue
git checkout -b security/issue-1-path-traversal

# Or use GitHub CLI
gh issue develop 1 --checkout
```

### **3. Development**
```bash
# Make changes, commit with issue reference
git commit -m "Security: Fix path traversal vulnerability

- Add bank name sanitization
- Implement whitelist validation  
- Add path bounds checking

Fixes #1"
```

### **4. Pull Request**
```bash
# Create PR with issue linking
gh pr create \
  --title "🔒 Security: Fix Path Traversal Vulnerability" \
  --body "Fixes #1

## Changes
- Added bank name sanitization  
- Implemented whitelist validation
- Added comprehensive tests

## Testing
- [x] Path traversal attack prevention
- [x] Whitelist validation works
- [x] Existing functionality preserved"
```

### **5. Issue Closure**
Issues automatically close when PRs with "Fixes #N" are merged.

---

## 📊 **Project Management**

### **Milestones Suggested**
```bash
# Create milestones
gh api repos/:owner/:repo/milestones \
  --method POST \
  --field title="Security Fixes" \
  --field description="Address all critical security vulnerabilities" \
  --field due_on="2025-08-16T00:00:00Z"

gh api repos/:owner/:repo/milestones \
  --method POST \
  --field title="Data Integrity" \
  --field description="Fix all data corruption and parsing issues" \
  --field due_on="2025-08-23T00:00:00Z"

gh api repos/:owner/:repo/milestones \
  --method POST \
  --field title="AU Bank Support" \
  --field description="Complete AU Bank transaction extraction" \
  --field due_on="2025-08-30T00:00:00Z"
```

### **Development Priority**
1. **Week 1**: Security fixes (#1, #9)
2. **Week 2**: Critical bugs (#2, #3, #4, #5) 
3. **Week 3**: AU Bank support (#6)
4. **Week 4**: Code quality (#7, #8)

---

## 🧪 **Testing Integration**

### **PR Requirements**
- All critical issues must have tests
- Security fixes require security tests
- AU Bank support needs sample verification

### **CI/CD Integration** (Future)
```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Test Security Fixes
        run: python -m pytest tests/security/
      - name: Test AU Bank Extraction  
        run: python -m pytest tests/aubank/
```

---

## 📈 **Progress Tracking**

### **Commands for Status**
```bash
# View issue status
gh issue list --state open
gh issue list --state closed

# View by assignee  
gh issue list --assignee "@me"

# View PR status
gh pr list --state open
gh pr list --state merged
```

### **Reporting**
```bash
# Generate progress report
gh issue list --json number,title,labels,state | jq '.[] | select(.state=="closed") | .title'
```

---

**Ready to run**: `./create-github-issues.sh` 🚀

This setup provides:
- ✅ **9 detailed GitHub issues** ready to create
- ✅ **Complete branch naming strategy**  
- ✅ **Professional workflow documentation**
- ✅ **Priority-based development plan**
- ✅ **Automated issue creation script**

Your development workflow is now ready for professional GitHub-based development! 🎉