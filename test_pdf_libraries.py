#!/usr/bin/env python3
"""
Test script to evaluate different PDF extraction libraries with sample files.
This helps determine the best library for credit card statement parsing.
"""

import os
import sys
import time
from typing import Dict, Any

def test_pypdf():
    """Test pypdf (modern PyPDF2 replacement)"""
    try:
        import pypdf
        
        pdf_path = "samples/pdfs/HDFC-Statement.pdf"
        
        start_time = time.time()
        with open(pdf_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            
            info = {
                'library': 'pypdf',
                'pages': len(reader.pages),
                'metadata': reader.metadata,
                'encrypted': reader.is_encrypted,
                'text_sample': ''
            }
            
            # Extract text from first page
            if reader.pages:
                text = reader.pages[0].extract_text()
                info['text_sample'] = text[:200] if text else "No text extracted"
        
        info['extraction_time'] = time.time() - start_time
        return info
        
    except ImportError:
        return {'library': 'pypdf', 'error': 'Library not installed'}
    except Exception as e:
        return {'library': 'pypdf', 'error': str(e)}

def test_pdfplumber():
    """Test pdfplumber"""
    try:
        import pdfplumber
        
        pdf_path = "samples/pdfs/HDFC-Statement.pdf"
        
        start_time = time.time()
        with pdfplumber.open(pdf_path) as pdf:
            
            info = {
                'library': 'pdfplumber',
                'pages': len(pdf.pages),
                'metadata': pdf.metadata,
                'text_sample': '',
                'tables_found': 0
            }
            
            # Extract text from first page
            if pdf.pages:
                page = pdf.pages[0]
                text = page.extract_text()
                info['text_sample'] = text[:200] if text else "No text extracted"
                
                # Check for tables
                tables = page.extract_tables()
                info['tables_found'] = len(tables) if tables else 0
                
                # Get page layout info
                info['page_width'] = page.width
                info['page_height'] = page.height
        
        info['extraction_time'] = time.time() - start_time
        return info
        
    except ImportError:
        return {'library': 'pdfplumber', 'error': 'Library not installed'}
    except Exception as e:
        return {'library': 'pdfplumber', 'error': str(e)}

def test_pymupdf():
    """Test PyMuPDF (fitz)"""
    try:
        import fitz  # PyMuPDF
        
        pdf_path = "samples/pdfs/HDFC-Statement.pdf"
        
        start_time = time.time()
        doc = fitz.open(pdf_path)
        
        info = {
            'library': 'PyMuPDF',
            'pages': doc.page_count,
            'metadata': doc.metadata,
            'encrypted': doc.is_encrypted,
            'text_sample': '',
            'has_images': False
        }
        
        # Extract text from first page
        if doc.page_count > 0:
            page = doc[0]
            text = page.get_text()
            info['text_sample'] = text[:200] if text else "No text extracted"
            
            # Check for images
            image_list = page.get_images()
            info['has_images'] = len(image_list) > 0
            info['image_count'] = len(image_list)
        
        doc.close()
        info['extraction_time'] = time.time() - start_time
        return info
        
    except ImportError:
        return {'library': 'PyMuPDF', 'error': 'Library not installed'}
    except Exception as e:
        return {'library': 'PyMuPDF', 'error': str(e)}

def test_pdfminer():
    """Test pdfminer.six"""
    try:
        from pdfminer.high_level import extract_text
        from pdfminer.pdfpage import PDFPage
        from pdfminer.pdfinterp import PDFResourceManager
        
        pdf_path = "samples/pdfs/HDFC-Statement.pdf"
        
        start_time = time.time()
        
        # Count pages
        with open(pdf_path, 'rb') as file:
            pages = list(PDFPage.get_pages(file))
            page_count = len(pages)
        
        # Extract text
        text = extract_text(pdf_path)
        
        info = {
            'library': 'pdfminer.six',
            'pages': page_count,
            'text_sample': text[:200] if text else "No text extracted",
            'extraction_time': time.time() - start_time
        }
        
        return info
        
    except ImportError:
        return {'library': 'pdfminer.six', 'error': 'Library not installed'}
    except Exception as e:
        return {'library': 'pdfminer.six', 'error': str(e)}

def main():
    """Run tests on all available PDF libraries"""
    print("Testing PDF extraction libraries with sample files...")
    print("=" * 60)
    
    # Test all libraries
    libraries = [
        test_pypdf,
        test_pdfplumber, 
        test_pymupdf,
        test_pdfminer
    ]
    
    results = []
    for test_func in libraries:
        result = test_func()
        results.append(result)
        
        print(f"\n{result['library']}:")
        print("-" * 30)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Successfully extracted content")
            print(f"   Pages: {result.get('pages', 'Unknown')}")
            print(f"   Extraction time: {result.get('extraction_time', 0):.3f}s")
            
            if result.get('tables_found'):
                print(f"   Tables found: {result['tables_found']}")
            
            if result.get('has_images'):
                print(f"   Images found: {result.get('image_count', 0)}")
            
            if result.get('text_sample'):
                print(f"   Text sample: {result['text_sample'][:100]}...")
    
    print("\n" + "=" * 60)
    print("Summary and Recommendations:")
    
    working_libs = [r for r in results if 'error' not in r]
    if working_libs:
        fastest = min(working_libs, key=lambda x: x.get('extraction_time', float('inf')))
        print(f"Fastest extraction: {fastest['library']} ({fastest.get('extraction_time'):.3f}s)")
        
        table_libs = [r for r in working_libs if r.get('tables_found', 0) > 0]
        if table_libs:
            print(f"Table detection: {', '.join(r['library'] for r in table_libs)}")
    
    return results

if __name__ == "__main__":
    main()