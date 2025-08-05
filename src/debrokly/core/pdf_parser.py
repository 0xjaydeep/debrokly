"""
PDF parsing functionality for credit card statements
"""

from pathlib import Path
from typing import Optional, Dict, Any
import PyPDF2


class PDFParser:
    """
    Handles parsing of password-protected PDF files
    """
    
    def __init__(self):
        pass
    
    def parse(self, pdf_path: Path, password: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse PDF file and extract text content
        
        Args:
            pdf_path: Path to PDF file
            password: Optional password for encrypted PDFs
            
        Returns:
            Dict containing parsed PDF data
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If password is incorrect or PDF is corrupted
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Handle encrypted PDFs
                if pdf_reader.is_encrypted:
                    if not password:
                        raise ValueError("PDF is password protected but no password provided")
                    
                    if not pdf_reader.decrypt(password):
                        raise ValueError("Incorrect password for encrypted PDF")
                
                # Extract text from all pages
                pages_text = []
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        text = page.extract_text()
                        pages_text.append({
                            'page_number': page_num + 1,
                            'text': text
                        })
                    except Exception as e:
                        # Log warning but continue with other pages
                        print(f"Warning: Could not extract text from page {page_num + 1}: {e}")
                
                return {
                    'file_path': str(pdf_path),
                    'total_pages': len(pdf_reader.pages),
                    'pages': pages_text,
                    'metadata': pdf_reader.metadata
                }
                
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {e}")
    
    def validate_pdf(self, pdf_path: Path) -> bool:
        """
        Validate if file is a valid PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            True if valid PDF, False otherwise
        """
        try:
            with open(pdf_path, 'rb') as file:
                PyPDF2.PdfReader(file)
            return True
        except:
            return False