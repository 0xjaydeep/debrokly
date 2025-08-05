"""
PDF parsing functionality for credit card statements using PDFPlumber
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
import pdfplumber
import pdf2image
import pytesseract
from PIL import Image
import io


class PDFParser:
    """
    Handles parsing of password-protected PDF files using PDFPlumber and OCR
    """
    
    def __init__(self):
        self.ocr_enabled = True
        try:
            # Test if tesseract is available
            pytesseract.get_tesseract_version()
        except Exception:
            self.ocr_enabled = False
            print("Warning: Tesseract not found. OCR functionality disabled.")
    
    def parse(self, pdf_path: Path, password: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse PDF file and extract text and table content
        
        Args:
            pdf_path: Path to PDF file
            password: Optional password for encrypted PDFs
            
        Returns:
            Dict containing parsed PDF data with text, tables, and metadata
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If password is incorrect or PDF is corrupted
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            with pdfplumber.open(pdf_path, password=password) as pdf:
                pages_data = []
                
                for page_num, page in enumerate(pdf.pages):
                    page_data = self._extract_page_data(page, page_num + 1)
                    
                    # If text extraction fails, try OCR
                    if not page_data['text'].strip() and self.ocr_enabled:
                        page_data.update(self._extract_with_ocr(pdf_path, page_num, password))
                    
                    pages_data.append(page_data)
                
                return {
                    'file_path': str(pdf_path),
                    'total_pages': len(pdf.pages),
                    'pages': pages_data,
                    'metadata': pdf.metadata
                }
                
        except Exception as e:
            if "incorrect password" in str(e).lower():
                raise ValueError("Incorrect password for encrypted PDF")
            raise ValueError(f"Failed to parse PDF: {e}")
    
    def _extract_page_data(self, page, page_num: int) -> Dict[str, Any]:
        """
        Extract text and table data from a single page
        
        Args:
            page: PDFPlumber page object
            page_num: Page number
            
        Returns:
            Dict containing page text, tables, and layout info
        """
        try:
            # Extract text
            text = page.extract_text() or ""
            
            # Extract tables
            tables = []
            extracted_tables = page.extract_tables()
            
            for table_idx, table in enumerate(extracted_tables):
                if table:  # Skip empty tables
                    tables.append({
                        'table_id': table_idx,
                        'rows': table,
                        'row_count': len(table),
                        'col_count': len(table[0]) if table else 0
                    })
            
            # Get page dimensions and layout
            layout_info = {
                'width': page.width,
                'height': page.height,
                'bbox': page.bbox
            }
            
            return {
                'page_number': page_num,
                'text': text,
                'tables': tables,
                'layout': layout_info,
                'extraction_method': 'pdfplumber'
            }
            
        except Exception as e:
            print(f"Warning: Could not extract data from page {page_num}: {e}")
            return {
                'page_number': page_num,
                'text': "",
                'tables': [],
                'layout': {},
                'extraction_method': 'failed',
                'error': str(e)
            }
    
    def _extract_with_ocr(self, pdf_path: Path, page_num: int, password: Optional[str] = None) -> Dict[str, Any]:
        """
        Extract text using OCR when regular extraction fails
        
        Args:
            pdf_path: Path to PDF file
            page_num: Page number (0-indexed)
            password: Optional password
            
        Returns:
            Dict with OCR-extracted text and metadata
        """
        if not self.ocr_enabled:
            return {'ocr_text': '', 'extraction_method': 'ocr_disabled'}
        
        try:
            # Convert PDF page to image
            images = pdf2image.convert_from_path(
                pdf_path,
                first_page=page_num + 1,
                last_page=page_num + 1,
                dpi=300
            )
            
            if not images:
                return {'ocr_text': '', 'extraction_method': 'ocr_failed'}
            
            # Extract text using OCR
            ocr_text = pytesseract.image_to_string(images[0], lang='eng')
            
            return {
                'ocr_text': ocr_text,
                'extraction_method': 'ocr',
                'ocr_confidence': 'not_calculated'  # Could add confidence calculation
            }
            
        except Exception as e:
            print(f"Warning: OCR failed for page {page_num + 1}: {e}")
            return {
                'ocr_text': '',
                'extraction_method': 'ocr_failed',
                'error': str(e)
            }
    
    def validate_pdf(self, pdf_path: Path) -> bool:
        """
        Validate if file is a valid PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            True if valid PDF, False otherwise
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Try to access first page
                if pdf.pages:
                    return True
            return False
        except:
            return False
    
    def get_pdf_info(self, pdf_path: Path, password: Optional[str] = None) -> Dict[str, Any]:
        """
        Get basic PDF information without full parsing
        
        Args:
            pdf_path: Path to PDF file
            password: Optional password
            
        Returns:
            Dict with PDF metadata and basic info
        """
        try:
            with pdfplumber.open(pdf_path, password=password) as pdf:
                return {
                    'page_count': len(pdf.pages),
                    'is_encrypted': pdf.is_encrypted if hasattr(pdf, 'is_encrypted') else False,
                    'metadata': pdf.metadata,
                    'file_size': pdf_path.stat().st_size
                }
        except Exception as e:
            return {
                'error': str(e),
                'file_exists': pdf_path.exists(),
                'file_size': pdf_path.stat().st_size if pdf_path.exists() else 0
            }