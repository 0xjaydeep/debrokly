# Security Issues

## 🚨 **CRITICAL SECURITY VULNERABILITIES**

### Path Traversal Vulnerability - Priority 🔴

**File**: `src/debrokly/core/exporter.py:89`  
**Type**: Security  
**Impact**: Arbitrary file system write access  
**Status**: Open  
**CVE Risk**: High

**Problem**: 
Bank name parameter is not validated before being used in file path construction. Malicious input could use "../" to write files outside the intended `outputs/` directory.

```python
# Vulnerable code
output_dir = self.base_output_dir / bank / year_month
output_dir.mkdir(parents=True, exist_ok=True)
```

**Attack Vector**:
- Input: `bank = "../../etc"`
- Result: Files written to `/etc/` directory

**Solution**: 
1. Sanitize bank name to alphanumeric characters only
2. Use whitelist validation against known bank names
3. Add path validation to ensure output stays within bounds

```python
# Proposed fix
def sanitize_bank_name(self, bank: str) -> str:
    # Only allow alphanumeric and safe characters
    safe_bank = re.sub(r'[^a-zA-Z0-9_-]', '', bank.lower())
    
    # Whitelist known banks
    valid_banks = {'hdfc', 'aubank', 'icici', 'sbi', 'axis'}
    if safe_bank not in valid_banks:
        safe_bank = 'unknown'
    
    return safe_bank
```

**Testing**: 
- [ ] Test with malicious inputs: `../`, `../../`, `../../../etc`
- [ ] Verify files only created in `outputs/` directory
- [ ] Test with special characters in bank names

---

## 🟡 **HIGH PRIORITY SECURITY ISSUES**

### Password Error Information Disclosure - Priority 🟡

**File**: `src/debrokly/core/pdf_parser.py:67-69`  
**Type**: Security  
**Impact**: Information disclosure  
**Status**: Open  

**Problem**: 
Password error detection relies on string matching which could expose library-specific error messages to users.

```python
if "incorrect password" in str(e).lower():
    raise ValueError("Incorrect password for encrypted PDF")
```

**Solution**: 
Catch specific exceptions and provide generic error messages.

**Testing**: 
- [ ] Test with various PDF libraries
- [ ] Ensure no sensitive library details leaked

---

## 🟢 **MEDIUM PRIORITY SECURITY ISSUES**

### Input Validation Missing - Priority 🟢

**File**: `src/debrokly/cli.py:17`  
**Type**: Security  
**Impact**: Potential file system issues  
**Status**: Open  

**Problem**: 
CLI only checks file existence, not read permissions or file type validation.

**Solution**: 
Add comprehensive input validation for file type, permissions, and size limits.

**Testing**: 
- [ ] Test with non-PDF files
- [ ] Test with unreadable files
- [ ] Test with extremely large files

---

## ✅ **COMPLETED SECURITY FIXES**

*No completed security fixes yet*

---

## 📋 **Security Best Practices Checklist**

### Input Validation
- [ ] File path validation
- [ ] Bank name sanitization  
- [ ] Password handling
- [ ] File type verification
- [ ] Size limit enforcement

### Output Security
- [ ] Directory traversal prevention
- [ ] File permission handling
- [ ] Sensitive data masking in logs
- [ ] Temporary file cleanup

### Error Handling
- [ ] Generic error messages
- [ ] No stack traces to users
- [ ] Secure logging practices

### Dependencies
- [ ] Security audit of dependencies
- [ ] Regular dependency updates
- [ ] Minimal privilege principle

---

**Last Updated**: August 9, 2025  
**Review Required**: After each critical fix  
**Security Contact**: Review with security team before production deployment