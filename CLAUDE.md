# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"Debrokly" is a Python library and CLI tool for analyzing password-protected credit card statement PDFs. The project extracts transaction data from various bank statement formats and exports to CSV/Excel.

**Key Features:**
- Generic format detection for any credit card statement
- Password-protected PDF handling
- OCR/LLM-based parsing for diverse PDF formats
- Python library with CLI interface
- Export to CSV and Excel formats

**Current Status:** 85% Complete - Production ready for HDFC Bank, development phase for AU Bank.

## Project Documentation

- `PROJECT_STATUS.md` - Current implementation status, testing results, and usage guide
- `REQUIREMENTS.md` - Original project specifications and requirements
- `samples/pdfs/` - Sample PDF files (HDFC and AU Bank) for testing

## Development Setup

The project uses Python 3.8+ with venv and pip for dependency management.

### Initial Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Install package in development mode
pip install -e .
```

### Project Structure
```
src/debrokly/           # Main package
├── __init__.py         # Package exports
├── cli.py              # Command line interface
├── core/               # Core functionality
│   ├── pdf_parser.py   # PDFPlumber-based PDF parsing
│   ├── extractor.py    # Transaction data extraction (TBD)
│   └── exporter.py     # CSV/Excel export
└── utils/              # Utility functions
    └── helpers.py      # Date parsing, text cleaning, etc.

samples/pdfs/           # Sample PDF files for testing
tests/                  # Test suite
```

### Development Commands
```bash
# Run CLI tool (organized output - default)
cd src && python3 -m debrokly.cli ../samples/pdfs/HDFC-Statement.pdf

# Custom output location
cd src && python3 -m debrokly.cli ../samples/pdfs/HDFC-Statement.pdf --output ../my_file.csv --no-organized

# Excel format with password
cd src && python3 -m debrokly.cli ../samples/pdfs/protected.pdf --password mypass --format excel

# Run tests (when implemented)
pytest

# Code formatting (when configured)
black src/ tests/
flake8 src/ tests/

# Type checking (when configured)
mypy src/
```

### Working Features (as of current implementation)
- ✅ **HDFC Bank**: Full transaction extraction working
- ✅ **Organized Output**: Automatic `outputs/bank/YYYY-MM/` structure
- ✅ **CSV/Excel Export**: Both formats working with validation
- ✅ **CLI Interface**: Complete command-line tool
- ✅ **Library API**: Ready for Python integration
- ⚠️ **AU Bank**: Detection works, extraction needs improvement

### Current Output Structure
```
outputs/
├── hdfc/
│   └── 2025-06/
│       ├── hdfc_transactions_2025-06.csv
│       └── hdfc_transactions_2025-06.xlsx
└── aubank/
    └── 2025-07/
        └── (files will appear when AU Bank extraction is fixed)
```

### Key Dependencies
- **pdfplumber**: PDF parsing and table extraction
- **pytesseract**: OCR for scanned PDFs  
- **pdf2image**: PDF to image conversion
- **pandas**: Data manipulation
- **click**: CLI interface

## Repository Information

- License: MIT
- Current branch: dev
- Main branch: main
- Owner: Jaydeep Chauhan