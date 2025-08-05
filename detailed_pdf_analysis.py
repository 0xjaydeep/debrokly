#!/usr/bin/env python3
"""
Detailed analysis of PDF extraction quality for credit card statements
"""

import pdfplumber
import pypdf
import fitz  # PyMuPDF

def analyze_with_pdfplumber():
    """Detailed analysis with pdfplumber"""
    print("=" * 60)
    print("PDFPLUMBER ANALYSIS")
    print("=" * 60)
    
    with pdfplumber.open("samples/pdfs/HDFC-Statement.pdf") as pdf:
        for i, page in enumerate(pdf.pages):
            print(f"\nPage {i+1}:")
            print("-" * 30)
            
            # Extract tables
            tables = page.extract_tables()
            print(f"Tables found: {len(tables)}")
            
            if tables:
                for j, table in enumerate(tables):
                    print(f"\nTable {j+1}:")
                    for row in table[:3]:  # Show first 3 rows
                        print(f"  {row}")
                    if len(table) > 3:
                        print(f"  ... ({len(table)-3} more rows)")
            
            # Show text structure
            text = page.extract_text()
            lines = text.split('\n')[:10]  # First 10 lines
            print(f"\nText preview (first 10 lines):")
            for line in lines:
                if line.strip():
                    print(f"  {line[:80]}...")

def analyze_with_pymupdf():
    """Detailed analysis with PyMuPDF"""
    print("\n" + "=" * 60)
    print("PYMUPDF ANALYSIS")
    print("=" * 60)
    
    doc = fitz.open("samples/pdfs/HDFC-Statement.pdf")
    
    for i in range(doc.page_count):
        page = doc[i]
        print(f"\nPage {i+1}:")
        print("-" * 30)
        
        # Get text with layout info
        text_dict = page.get_text("dict")
        
        print(f"Text blocks found: {len(text_dict['blocks'])}")
        
        # Extract images
        images = page.get_images()
        print(f"Images found: {len(images)}")
        
        # Show text structure
        text = page.get_text()
        lines = text.split('\n')[:10]
        print(f"\nText preview (first 10 lines):")
        for line in lines:
            if line.strip():
                print(f"  {line[:80]}...")
                
        # Check for potential table structures
        try:
            tables = page.find_tables()
            print(f"Table-like structures: {len(tables.tables) if hasattr(tables, 'tables') else 'N/A'}")
        except:
            print("Table detection: Not available")
    
    doc.close()

def find_transaction_patterns():
    """Look for transaction patterns in the text"""
    print("\n" + "=" * 60)
    print("TRANSACTION PATTERN ANALYSIS")
    print("=" * 60)
    
    with pdfplumber.open("samples/pdfs/HDFC-Statement.pdf") as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
        
        lines = full_text.split('\n')
        
        # Look for patterns that might be transactions
        date_patterns = []
        amount_patterns = []
        
        import re
        
        for line in lines:
            # Look for date patterns (DD/MM/YYYY or DD-MM-YYYY)
            if re.search(r'\b\d{2}[/-]\d{2}[/-]\d{4}\b', line):
                date_patterns.append(line.strip())
            
            # Look for amount patterns (numbers with decimal)
            if re.search(r'\b\d+\.\d{2}\b', line) and len(line.strip()) > 10:
                amount_patterns.append(line.strip())
        
        print(f"Lines with date patterns: {len(date_patterns)}")
        print("Sample date lines:")
        for line in date_patterns[:5]:
            print(f"  {line[:100]}...")
            
        print(f"\nLines with amount patterns: {len(amount_patterns)}")
        print("Sample amount lines:")
        for line in amount_patterns[:5]:
            print(f"  {line[:100]}...")

if __name__ == "__main__":
    analyze_with_pdfplumber()
    analyze_with_pymupdf()
    find_transaction_patterns()