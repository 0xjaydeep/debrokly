# Bug Tracking

## 🔴 **CRITICAL BUGS**

### Date Parsing Priority Bug - Priority 🔴

**File**: `src/debrokly/utils/helpers.py:41-51`  
**Type**: Data Integrity Bug  
**Impact**: Incorrect transaction dates for international formats  
**Status**: Open  

**Problem**: 
MM/DD/YYYY format is tried before DD/MM/YYYY, causing ambiguous dates like "01/02/2025" to be parsed as January 2nd instead of February 1st for international users.

```python
date_formats = [
    '%m/%d/%Y',    # MM/DD/YYYY - TRIED FIRST (WRONG)
    '%d/%m/%Y',    # DD/MM/YYYY - TRIED SECOND
]
```

**Impact**: Financial data corruption, wrong transaction dating

**Solution**: 
1. Prioritize DD/MM/YYYY format for international compatibility
2. Add region detection or configuration option
3. Add date validation logic

**Testing**: 
- [ ] Test with ambiguous dates: 01/02/2025, 12/01/2025
- [ ] Verify correct parsing for different regions
- [ ] Test with edge cases: 29/02/2024 (leap year)

---

### Month Folder Detection Bug - Priority 🔴

**File**: `src/debrokly/core/exporter.py:79-86`  
**Type**: Logic Bug  
**Impact**: Same-month statements scattered across folders  
**Status**: Open (Known Issue)  

**Problem**: 
Month folder determination uses the latest transaction date instead of the statement period/date, causing multiple statements from the same month to be placed in different folders.

```python
# Current buggy logic
latest_date = max(dates)
year_month = latest_date.strftime('%Y-%m')
```

**Impact**: Disorganized output structure, user confusion

**Solution**: 
Extract statement date from PDF metadata or content header instead of using transaction dates.

**Testing**: 
- [ ] Process multiple HDFC statements from same month
- [ ] Verify consistent folder placement
- [ ] Test with statements spanning multiple months

---

### Float Conversion Crash - Priority 🔴

**File**: `src/debrokly/core/extractor.py:426`  
**Type**: Exception/Crash Bug  
**Impact**: Application crash on malformed amounts  
**Status**: Open  

**Problem**: 
No validation before float conversion, causing ValueError on malformed decimal formats.

```python
amount = float(amount_match.group(1).replace(',', ''))
```

**Crash Examples**: "1,234,56", "1.234,56", "1..23", "abc.def"

**Solution**: 
Add format validation and exception handling with fallback values.

**Testing**: 
- [ ] Test with various malformed amounts
- [ ] Verify graceful error handling
- [ ] Test with different decimal separators

---

### Hard Dependency Import Failure - Priority 🔴

**File**: `src/debrokly/core/pdf_parser.py:8-11`  
**Type**: Dependency Bug  
**Impact**: App crashes when OCR not needed  
**Status**: Open  

**Problem**: 
OCR dependencies (tesseract, pdf2image) are hard imports causing ImportError even when OCR functionality is not required.

**Solution**: 
Implement conditional imports with graceful fallback.

```python
# Proposed fix
try:
    import pdf2image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
```

**Testing**: 
- [ ] Test without tesseract installed
- [ ] Verify text-based PDF processing still works
- [ ] Test OCR graceful degradation

---

## 🟡 **HIGH PRIORITY BUGS**

### Duplicate Detection Flaw - Priority 🟡

**File**: `src/debrokly/core/extractor.py:484`  
**Type**: Data Loss Bug  
**Impact**: False duplicate removal  
**Status**: Open  

**Problem**: 
Description truncated to 50 characters for duplicate detection can cause different transactions to be incorrectly identified as duplicates.

```python
key = (txn['date'], txn['description'][:50], txn['amount'])
```

**Solution**: 
Use hash of full description or implement better deduplication logic.

**Testing**: 
- [ ] Test with transactions having similar descriptions
- [ ] Verify no valid transactions are lost
- [ ] Test duplicate detection accuracy

---

### Silent Exception Handling - Priority 🟡

**File**: `src/debrokly/core/pdf_parser.py:185`  
**Type**: Error Handling Bug  
**Impact**: No debugging information on failures  
**Status**: Open  

**Problem**: 
Broad exception handling with no logging makes debugging impossible.

```python
except:
    return False  # No information about what failed
```

**Solution**: 
Implement specific exception handling with proper logging.

**Testing**: 
- [ ] Test with various PDF parsing failures
- [ ] Verify useful error messages are logged
- [ ] Test debugging capabilities

---

### OCR Password Not Used - Priority 🟡

**File**: `src/debrokly/core/pdf_parser.py:55`  
**Type**: Logic Bug  
**Impact**: OCR fails on password-protected PDFs  
**Status**: Open  

**Problem**: 
Password parameter passed to OCR function but never actually used in pdf2image conversion.

**Solution**: 
Implement password handling in OCR pipeline or document limitation.

**Testing**: 
- [ ] Test OCR with password-protected PDFs
- [ ] Verify proper error handling
- [ ] Document OCR limitations

---

### Version Inconsistency - Priority 🟡

**File**: `pyproject.toml` vs `requirements.txt`  
**Type**: Configuration Bug  
**Impact**: Inconsistent dependency versions  
**Status**: Open  

**Problem**: 
Different version specifications in pyproject.toml (>=0.9.0) vs requirements.txt (>=0.11.0) for pdfplumber.

**Solution**: 
Align version specifications across all configuration files.

**Testing**: 
- [ ] Test with both version ranges
- [ ] Verify compatibility
- [ ] Test fresh installations

---

## 🟢 **MEDIUM PRIORITY BUGS**

### Transaction Type Assumption - Priority 🟢

**File**: `src/debrokly/core/extractor.py:283`  
**Type**: Logic Bug  
**Impact**: Potential transaction misclassification  
**Status**: Open  

**Problem**: 
Assumes all non-Dr amounts are credits, which may not be accurate for all transaction types.

**Testing**: 
- [ ] Test with various transaction types
- [ ] Verify classification accuracy

---

### Hardcoded Header Row Count - Priority 🟢

**File**: `src/debrokly/core/extractor.py:198`  
**Type**: Logic Bug  
**Impact**: May skip valid data or include headers  
**Status**: Open  

**Problem**: 
Hardcoded `rows[2:]` assumes exactly 2 header rows, which may not be true for all bank formats.

**Testing**: 
- [ ] Test with different table structures
- [ ] Verify data extraction accuracy

---

### CLI Message Timing - Priority 🟢

**File**: `src/debrokly/cli.py:57`  
**Type**: UX Bug  
**Impact**: Confusing user feedback  
**Status**: Open  

**Problem**: 
Export message printed after export completion, misleading users about current operation.

**Testing**: 
- [ ] Test CLI user experience
- [ ] Verify message timing accuracy

---

## ✅ **COMPLETED BUG FIXES**

*No completed bug fixes yet*

---

## 🔍 **Testing Coverage**

### High Priority Testing Areas
- [ ] Date parsing with various formats
- [ ] Amount extraction edge cases
- [ ] Error handling scenarios
- [ ] AU Bank table structure parsing
- [ ] Memory management in batch processing

### Integration Testing
- [ ] CLI with various argument combinations
- [ ] Library integration scenarios
- [ ] Cross-platform compatibility
- [ ] Different PDF library versions

---

**Last Updated**: August 9, 2025  
**Priority Review**: Weekly for critical bugs  
**Release Blocker**: All critical bugs must be fixed before production