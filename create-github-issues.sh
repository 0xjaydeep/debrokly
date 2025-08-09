#!/bin/bash

# GitHub Issues Creation Script for Debrokly
# Run this script to create all tracked issues in GitHub

echo "🚀 Creating GitHub Issues for Debrokly..."
echo "======================================="

# Check if gh CLI is authenticated
if ! gh auth status >/dev/null 2>&1; then
    echo "❌ Please authenticate with GitHub CLI first:"
    echo "   gh auth login"
    exit 1
fi

# Create labels first
echo "📋 Creating GitHub labels..."

gh label create "security" --color "d73a4a" --description "Security vulnerability or concern" 2>/dev/null || echo "Label 'security' already exists"
gh label create "bug" --color "d73a4a" --description "Something isn't working" 2>/dev/null || echo "Label 'bug' already exists"  
gh label create "enhancement" --color "a2eeef" --description "New feature or request" 2>/dev/null || echo "Label 'enhancement' already exists"
gh label create "critical" --color "b60205" --description "Critical priority - fix immediately" 2>/dev/null || echo "Label 'critical' already exists"
gh label create "high" --color "ff9500" --description "High priority" 2>/dev/null || echo "Label 'high' already exists"
gh label create "medium" --color "fbca04" --description "Medium priority" 2>/dev/null || echo "Label 'medium' already exists"
gh label create "low" --color "0e8a16" --description "Low priority" 2>/dev/null || echo "Label 'low' already exists"
gh label create "hdfc" --color "5319e7" --description "HDFC Bank related" 2>/dev/null || echo "Label 'hdfc' already exists"
gh label create "aubank" --color "5319e7" --description "AU Bank related" 2>/dev/null || echo "Label 'aubank' already exists"
gh label create "ocr" --color "c5def5" --description "OCR/image processing related" 2>/dev/null || echo "Label 'ocr' already exists"

echo ""
echo "🔴 Creating CRITICAL Issues..."

# CRITICAL ISSUE #1: Security - Path Traversal
gh issue create \
  --title "🚨 CRITICAL: Path Traversal Vulnerability in Export Path Construction" \
  --body "$(cat <<'EOF'
## Security Vulnerability - Path Traversal

**File**: `src/debrokly/core/exporter.py:89`  
**Severity**: 🔴 CRITICAL  
**Type**: Security Vulnerability  
**CVE Risk**: High  

### Problem
Bank name parameter is not validated before being used in file path construction. Malicious input could use "../" to write files outside the intended `outputs/` directory.

### Vulnerable Code
```python
# Line 89 in exporter.py
output_dir = self.base_output_dir / bank / year_month
output_dir.mkdir(parents=True, exist_ok=True)
```

### Attack Vector
- Input: `bank = "../../etc"`  
- Result: Files written to `/etc/` directory

### Impact
- Arbitrary file system write access
- Potential system compromise
- Data corruption outside application scope

### Solution
1. Sanitize bank name to alphanumeric characters only
2. Use whitelist validation against known bank names  
3. Add path validation to ensure output stays within bounds

### Testing Checklist
- [ ] Test with malicious inputs: `../`, `../../`, `../../../etc`
- [ ] Verify files only created in `outputs/` directory
- [ ] Test with special characters in bank names
- [ ] Security audit of path construction

### Priority
This is a **CRITICAL SECURITY ISSUE** that must be fixed before any production deployment.
EOF
)" \
  --label "security,critical,bug" \
  --assignee "@me"

# CRITICAL ISSUE #2: Date Parsing Bug
gh issue create \
  --title "🔴 CRITICAL: Date Parsing Priority Causes Wrong Transaction Dates" \
  --body "$(cat <<'EOF'
## Data Integrity Bug - Date Parsing

**File**: `src/debrokly/utils/helpers.py:41-51`  
**Severity**: 🔴 CRITICAL  
**Type**: Data Integrity Bug  
**Impact**: Incorrect transaction dates for international formats  

### Problem
MM/DD/YYYY format is tried before DD/MM/YYYY, causing ambiguous dates like "01/02/2025" to be parsed as January 2nd instead of February 1st for international users.

### Buggy Code
```python
date_formats = [
    '%m/%d/%Y',    # MM/DD/YYYY - TRIED FIRST (WRONG)
    '%d/%m/%Y',    # DD/MM/YYYY - TRIED SECOND
]
```

### Impact
- Financial data corruption
- Wrong transaction dating
- Incorrect monthly categorization
- User trust issues with data accuracy

### Examples
- `01/02/2025` → Parsed as `January 2, 2025` instead of `February 1, 2025`
- `12/01/2025` → Parsed as `December 1, 2025` instead of `January 12, 2025`

### Solution
1. Prioritize DD/MM/YYYY format for international compatibility
2. Add region detection or configuration option
3. Add date validation logic to detect impossible dates
4. Consider ISO 8601 format (YYYY-MM-DD) as primary

### Testing Checklist
- [ ] Test with ambiguous dates: 01/02/2025, 12/01/2025
- [ ] Verify correct parsing for different regions
- [ ] Test with edge cases: 29/02/2024 (leap year)
- [ ] Test with invalid dates: 32/01/2025, 01/13/2025

### Priority  
This affects **ALL transaction data integrity** and must be fixed immediately.
EOF
)" \
  --label "bug,critical,hdfc,aubank" \
  --assignee "@me"

# CRITICAL ISSUE #3: Month Folder Bug  
gh issue create \
  --title "🔴 CRITICAL: Month Folder Detection Uses Wrong Date Logic" \
  --body "$(cat <<'EOF'
## Logic Bug - Month Folder Organization

**File**: `src/debrokly/core/exporter.py:79-86`  
**Severity**: 🔴 CRITICAL  
**Type**: Logic Bug  
**Impact**: Same-month statements scattered across folders  

### Problem
Month folder determination uses the latest transaction date instead of the statement period/date, causing multiple statements from the same month to be placed in different folders.

### Current Buggy Logic
```python
# Lines 79-86 - WRONG APPROACH
# TODO: FIX - Using latest transaction date causes incorrect folder placement
latest_date = max(dates)
year_month = latest_date.strftime('%Y-%m')
```

### Impact
- Disorganized output structure: `outputs/hdfc/2025-06/` vs `outputs/hdfc/2025-05/`  
- Same-month statements scattered
- User confusion about file organization
- Breaks the organized folder promise

### Example Scenario
- HDFC Statement for May 2025 with transactions from April 30 to May 25
- Current logic: Uses May 25 → Places in `outputs/hdfc/2025-05/`
- Another May statement with transactions until June 2  
- Current logic: Uses June 2 → Places in `outputs/hdfc/2025-06/`
- **Result**: Same month's statements in different folders ❌

### Solution
Extract statement date from PDF metadata or content header instead of using transaction dates:
1. Parse statement date from PDF header/metadata
2. Use statement month for folder organization
3. Fallback to transaction date range if statement date unavailable
4. Add configuration option for folder organization preference

### Testing Checklist
- [ ] Process multiple HDFC statements from same month
- [ ] Verify consistent folder placement
- [ ] Test with statements spanning multiple months  
- [ ] Test edge cases: statements issued on different dates

### Priority
This is a **KNOWN CRITICAL ISSUE** affecting user experience and data organization.
EOF
)" \
  --label "bug,critical,hdfc" \
  --assignee "@me"

# CRITICAL ISSUE #4: Float Conversion Crash
gh issue create \
  --title "🔴 CRITICAL: Unvalidated Float Conversion Causes App Crashes" \
  --body "$(cat <<'EOF'
## Exception/Crash Bug - Amount Parsing

**File**: `src/debrokly/core/extractor.py:426`  
**Severity**: 🔴 CRITICAL  
**Type**: Exception/Crash Bug  
**Impact**: Application crash on malformed amounts  

### Problem
No validation before float conversion, causing ValueError on malformed decimal formats found in PDFs.

### Vulnerable Code
```python
# Line 426 - NO VALIDATION
amount = float(amount_match.group(1).replace(',', ''))
```

### Crash Examples
- Input: `"1,234,56"` → ValueError: invalid literal for float()
- Input: `"1.234,56"` → ValueError (European decimal format)
- Input: `"1..23"` → ValueError (double decimal point)
- Input: `"abc.def"` → ValueError (non-numeric)
- Input: `"1,234.56.78"` → ValueError (multiple decimals)

### Impact
- Complete application crash
- Loss of processing progress
- Poor user experience
- Data processing interruption

### Root Cause
PDF text extraction can produce malformed number strings due to:
- OCR errors
- PDF formatting issues  
- International number formats
- Corrupted PDF content

### Solution
Add format validation and exception handling:
```python
def safe_float_conversion(amount_str: str) -> Optional[float]:
    try:
        # Normalize different decimal formats
        normalized = normalize_decimal_format(amount_str)
        return float(normalized)
    except (ValueError, TypeError):
        logger.warning(f"Failed to parse amount: {amount_str}")
        return None
```

### Testing Checklist
- [ ] Test with various malformed amounts
- [ ] Verify graceful error handling  
- [ ] Test with different decimal separators (, vs .)
- [ ] Test with currency symbols and spaces
- [ ] Performance test with large datasets

### Priority
This causes **APPLICATION CRASHES** and must be fixed before processing real-world PDFs.
EOF
)" \
  --label "bug,critical" \
  --assignee "@me"

# CRITICAL ISSUE #5: Hard OCR Dependencies
gh issue create \
  --title "🔴 CRITICAL: Hard OCR Dependencies Cause Import Failures" \
  --body "$(cat <<'EOF'
## Dependency Bug - Optional Features Required

**File**: `src/debrokly/core/pdf_parser.py:8-11`  
**Severity**: 🔴 CRITICAL  
**Type**: Dependency Bug  
**Impact**: App crashes when OCR not needed  

### Problem
OCR dependencies (tesseract, pdf2image) are hard imports causing ImportError even when OCR functionality is not required for text-based PDFs.

### Current Code
```python
# Lines 8-11 - HARD IMPORTS
import pdf2image
import pytesseract
from PIL import Image
```

### Impact
- ImportError crashes on systems without tesseract
- Prevents using library for text-based PDFs only
- Unnecessary deployment complexity
- Poor user experience for basic use cases

### Error Example
```
ImportError: No module named 'pytesseract'
```
Even when processing text-based PDFs that don't need OCR.

### Solution
Implement conditional imports with graceful fallback:
```python
# Conditional OCR imports
try:
    import pdf2image
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError as e:
    OCR_AVAILABLE = False
    logger.info(f"OCR dependencies not available: {e}")

class PDFParser:
    def __init__(self):
        self.ocr_enabled = OCR_AVAILABLE
        if not self.ocr_enabled:
            logger.info("OCR functionality disabled - text-based PDFs only")
```

### Implementation Plan
1. Make OCR imports conditional
2. Add graceful degradation when OCR unavailable
3. Update documentation about optional dependencies
4. Add clear error messages for OCR-required scenarios
5. Consider separate OCR plugin/extension

### Testing Checklist
- [ ] Test without tesseract installed
- [ ] Verify text-based PDF processing still works
- [ ] Test OCR graceful degradation
- [ ] Test clear error messages for OCR-required cases
- [ ] Test with various deployment scenarios

### Priority
This prevents **basic library usage** and must be fixed for broader adoption.
EOF
)" \
  --label "bug,critical,ocr" \
  --assignee "@me"

echo ""
echo "🟡 Creating HIGH Priority Issues..."

# HIGH ISSUE #1: AU Bank Support
gh issue create \
  --title "🟡 HIGH: Complete AU Bank Transaction Extraction Support" \
  --body "$(cat <<'EOF'
## Feature Enhancement - AU Bank Support

**Priority**: 🟡 HIGH  
**Type**: Feature Enhancement  
**Impact**: Complete AU Bank support for production use  

### Current Status
- ✅ Bank detection working
- ✅ PDF parsing working  
- ❌ Transaction extraction returns 0 results
- ❌ Complex table structures not parsed

### Problem
AU Bank PDFs have complex table structures that current extraction logic cannot handle:
1. Multi-row transaction entries
2. Compressed transaction summaries  
3. Different table layouts across pages
4. Non-standard date/amount formats

### Sample Analysis
From `samples/pdfs/AUBANK.pdf`:
- Page 1: 5 tables detected, transaction summary in Table 3
- Page 5: Detailed transactions in Table 1 with proper structure
- Complex formats: Dates, descriptions, and amounts in merged cells

### Required Work
1. **Deep Table Analysis**: Study AU Bank table patterns thoroughly
2. **Custom Parser**: Implement AU Bank-specific parsing logic
3. **Multi-format Support**: Handle both summary and detailed formats
4. **Data Validation**: Ensure extracted data accuracy

### Implementation Plan
```python
def _parse_aubank_complex_tables(self, tables: List) -> List[Dict]:
    # Handle Page 1 compressed summaries
    # Handle Page 5+ detailed transactions  
    # Parse multi-row entries
    # Extract proper date/amount/description
```

### Success Criteria
- Extract all transactions from AUBANK.pdf sample
- Match manual extraction accuracy (100%)
- Handle edge cases and malformed data
- Performance acceptable for large statements

### Testing Checklist
- [ ] Extract transactions from AUBANK.pdf sample  
- [ ] Verify accuracy against manual extraction
- [ ] Test with multiple AU Bank statement formats
- [ ] Performance testing with large AU Bank statements
- [ ] Edge case testing (corrupted tables, missing data)

### Impact
This will bring AU Bank support to **production-ready** status, matching HDFC functionality.
EOF
)" \
  --label "enhancement,high,aubank" \
  --assignee "@me"

# HIGH ISSUE #2: Duplicate Detection Flaw
gh issue create \
  --title "🟡 HIGH: Fix Duplicate Detection Logic That Loses Valid Transactions" \
  --body "$(cat <<'EOF'
## Data Loss Bug - Duplicate Detection

**File**: `src/debrokly/core/extractor.py:484`  
**Severity**: 🟡 HIGH  
**Type**: Data Loss Bug  
**Impact**: False duplicate removal loses valid transactions  

### Problem
Description truncated to 50 characters for duplicate detection can cause different transactions to be incorrectly identified as duplicates.

### Vulnerable Code
```python
# Line 484 - FLAWED LOGIC
key = (txn['date'], txn['description'][:50], txn['amount'])
```

### Impact Examples
- Transaction 1: "AMAZON WEBSERVICES CLOUD COMPUTING CHARGES FOR MARCH 2025"
- Transaction 2: "AMAZON WEBSERVICES CLOUD COMPUTING CHARGES FOR APRIL 2025"  
- Truncated: Both become "AMAZON WEBSERVICES CLOUD COMPUTING CHARGES FOR"
- **Result**: Second transaction incorrectly removed as duplicate ❌

### Real-World Scenarios
1. **Recurring Services**: Netflix, AWS, utilities with monthly charges
2. **Similar Merchants**: Different Starbucks locations  
3. **Split Payments**: Same merchant, different amounts, same day

### Current Algorithm Problems
1. **Arbitrary Truncation**: 50 characters is not semantically meaningful
2. **No Context**: Ignores merchant codes, reference numbers
3. **Date Precision**: Same-day transactions from same merchant lost
4. **No User Control**: No way to review or override deduplication

### Solution Options
1. **Hash Full Description**: Use hash of complete description
2. **Semantic Deduplication**: Use merchant + date + amount + reference ID
3. **Fuzzy Matching**: Implement similarity threshold instead of exact match
4. **User Review**: Flag potential duplicates for manual review

### Proposed Implementation
```python
def create_transaction_key(self, txn: Dict) -> str:
    # Use multiple identifying factors
    key_parts = [
        txn.get('date', ''),
        txn.get('description', '').strip(),  # Full description
        str(txn.get('amount', 0)),
        txn.get('reference', ''),  # If available
        txn.get('merchant_code', '')  # If available
    ]
    return hashlib.md5('|'.join(key_parts).encode()).hexdigest()
```

### Testing Checklist
- [ ] Test with transactions having similar descriptions
- [ ] Verify no valid transactions are lost
- [ ] Test duplicate detection accuracy
- [ ] Test with recurring monthly charges
- [ ] Test with same-merchant, different-location scenarios
- [ ] Performance testing with large datasets

### Priority
This affects **data completeness** and user trust in extraction accuracy.
EOF
)" \
  --label "bug,high" \
  --assignee "@me"

echo ""
echo "🟢 Creating MEDIUM Priority Issues..."

# Add a few medium priority issues
gh issue create \
  --title "🟢 MEDIUM: Implement Proper Logging Instead of Print Statements" \
  --body "$(cat <<'EOF'
## Code Quality Enhancement - Logging System

**Priority**: 🟢 MEDIUM  
**Type**: Code Quality Enhancement  
**Impact**: Better debugging and production monitoring  

### Problem
Application uses print statements instead of proper logging, making debugging and production monitoring difficult.

### Current Issues
- No log levels (debug, info, warning, error)
- No log formatting or timestamps  
- No log file output options
- Hard to filter or search logs
- Not suitable for production deployment

### Solution
Implement proper Python logging with:
1. Structured logging with levels
2. Configurable log formatting
3. File and console output options
4. Logger per module
5. Performance logging for optimization

### Implementation
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debrokly.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Testing
- [ ] Replace all print statements
- [ ] Test log levels and filtering
- [ ] Test file output
- [ ] Performance impact assessment
EOF
)" \
  --label "enhancement,medium" \
  --assignee "@me"

gh issue create \
  --title "🟢 MEDIUM: Add Comprehensive Input Validation for File Processing" \
  --body "$(cat <<'EOF'
## Security Enhancement - Input Validation

**Priority**: 🟢 MEDIUM  
**Type**: Security Enhancement  
**Impact**: Prevent crashes and improve error handling  

### Problem
Insufficient input validation for:
- File types (accepting non-PDF files)
- File sizes (no limits)
- File permissions (no read permission checks)  
- Path validation (relative paths, special characters)

### Solution
Implement comprehensive validation:
1. File type verification (magic number check)
2. File size limits
3. Permission checks
4. Path sanitization
5. Content validation

### Testing
- [ ] Test with non-PDF files
- [ ] Test with unreadable files  
- [ ] Test with extremely large files
- [ ] Test with malicious file paths
EOF
)" \
  --label "enhancement,medium,security" \
  --assignee "@me"

echo ""
echo "✅ Issues Created Successfully!"
echo ""
echo "📊 Summary:"
echo "  🔴 Critical: 5 issues"  
echo "  🟡 High: 2 issues"
echo "  🟢 Medium: 2 issues"
echo "  📝 Total: 9 issues created"
echo ""
echo "🔗 View issues: gh issue list"
echo "📋 Create project board: gh project create"
echo ""
echo "🚀 Ready for development workflow!"