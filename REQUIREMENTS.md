# Debrokly - Credit Card Statement Analyzer
## Requirements Document

### Project Overview
**Purpose**: Analyze password-protected credit card statement PDFs, extract transaction data, and export to CSV/Excel formats.

**Type**: Python library with CLI interface for integration with other applications.

### Target Users
- Developers integrating statement analysis into applications
- CLI users processing credit card statements
- Applications requiring automated transaction data extraction

### Core Features

#### 1. PDF Processing
- **Format Support**: Generic format detection for any credit card statement
- **Multi-Bank Compatibility**: Support different layouts/templates from various banks
- **Language**: English statements only
- **PDF Types**: 
  - Multi-page statements
  - Different table structures
  - Both text-based and scanned PDFs (OCR capability)
- **Password Protection**: Handle password-protected PDFs

#### 2. Authentication
- **Password Input**: CLI argument (`--password`) for initial implementation
- **Security**: Secure handling of PDF passwords

#### 3. Data Extraction
- **Fields**: Extract all available transaction fields that can be detected:
  - Date, Description, Amount (minimum)
  - Transaction type, Category, Reference numbers
  - Merchant details, Location information
  - Any other detectable fields
- **Technology**: OCR/LLM-based approach for handling diverse PDF formats

#### 4. Input/Output
- **Processing**: Single file processing (batch processing planned for future)
- **Output Formats**: 
  - CSV export
  - Excel export
  - Library API returns: Dictionary format
- **File Size**: Target 1-5MB PDFs initially, scale incrementally

#### 5. Interface
- **Primary**: Python library for integration
- **Secondary**: CLI tool functionality
- **API**: Return extracted data as dictionary structure

### Technical Requirements

#### Dependencies & Technology Stack
- **PDF Processing**: OCR/LLM-based solution for format flexibility
- **Python Version**: TBD (recommend Python 3.8+)
- **OCR Libraries**: Consider tesseract, easyocr, or similar
- **LLM Integration**: For intelligent format detection and parsing

#### Performance
- **File Size**: 1-5MB PDF files initially
- **Processing Time**: TBD - measure and optimize incrementally
- **Memory Usage**: Optimize for reasonable memory footprint

#### Error Handling
- Handle incorrect PDF passwords
- Manage unreadable/corrupted PDFs  
- Process PDFs with no detectable transaction tables
- Graceful handling of unsupported statement formats
- Comprehensive logging and error reporting

### Future Enhancements
- **Batch Processing**: Multiple PDF files
- **Configuration System**: Custom parsing rules for specific banks
- **Additional Output Formats**: JSON, database exports
- **GUI Interface**: Optional graphical interface
- **Plugin System**: Extensible architecture for new bank formats

### Development Approach
1. **Phase 1**: Core library with basic PDF processing
2. **Phase 2**: OCR/LLM integration for format flexibility
3. **Phase 3**: CLI interface and export functionality
4. **Phase 4**: Enhanced error handling and optimization
5. **Phase 5**: Batch processing and configuration system

### Sample Data
- User will provide sample PDFs from different banks for testing and development
- Use samples to refine parsing algorithms and format detection
### Success Criteria
- Successfully extract transaction data from major bank statement formats
- Reliable password-protected PDF handling
- Clean CSV/Excel export functionality
- Easy integration as Python library
- Robust error handling for edge cases


### Quick Test All HDFC Files
```bash
cd src && source ../.venv/bin/activate
python3 -m debrokly.cli ../samples/pdfs/HDFC-Statement.pdf --no-organized
python3 -m debrokly.cli ../samples/pdfs/HDFC-Statement-2.pdf --no-organized  
python3 -m debrokly.cli ../samples/pdfs/hdfc_may_millennia.pdf --no-organized
```


---
*Document Version: 1.0*  
*Last Updated: 2025-08-05*  
*Owner: Jaydeep Chauhan*
