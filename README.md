# Debrokly - Credit Card Statement Analyzer

A Python library and CLI tool for extracting transaction data from credit card statement PDFs with organized output by bank and month.

## 🚀 Quick Start

```bash
# Setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Extract transactions (creates outputs/hdfc/2025-06/hdfc_transactions_2025-06.csv)
cd src && python3 -m debrokly.cli ../samples/pdfs/HDFC-Statement.pdf
```

## 📊 Current Status: 85% Complete

- ✅ **HDFC Bank**: Production ready
- ⚠️ **AU Bank**: Needs improvement  
- ✅ **Organized Output**: `outputs/bank/YYYY-MM/`
- ✅ **CSV/Excel Export**: Both formats working
- ✅ **CLI & Library**: Complete interfaces

## 📁 Features

- **Bank Detection**: Automatic format detection
- **Password Support**: Handle protected PDFs
- **Organized Output**: Automatic bank/month organization
- **Multiple Formats**: CSV and Excel export
- **CLI & Library**: Use as command-line tool or Python library

## 📖 Documentation

- [`PROJECT_STATUS.md`](PROJECT_STATUS.md) - Detailed progress and usage guide
- [`REQUIREMENTS.md`](REQUIREMENTS.md) - Original project requirements  
- [`CLAUDE.md`](CLAUDE.md) - Development guidance

## 🧪 Working Example

```python
from debrokly import PDFParser, TransactionExtractor, DataExporter
from pathlib import Path

# Process statement
parser = PDFParser()
extractor = TransactionExtractor()
exporter = DataExporter()

pdf_path = Path("statement.pdf")
parsed_data = parser.parse(pdf_path)
transactions = extractor.extract(parsed_data)

# Auto-organized export
output_path = exporter.export_organized(transactions, format='csv')
print(f"Exported to: {output_path}")
# Output: outputs/hdfc/2025-06/hdfc_transactions_2025-06.csv
```

## 📞 Support

Check [`PROJECT_STATUS.md`](PROJECT_STATUS.md) for detailed usage instructions, known issues, and implementation status.

---

*MIT License | Owner: Jaydeep Chauhan* | Email: 0xjaydeep@gmail.com
