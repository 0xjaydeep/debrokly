"""
Helper utility functions
"""

import re
from typing import Optional, Union
from datetime import datetime, date


def format_currency(amount: Union[str, float, int]) -> str:
    """
    Format amount as currency string
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted currency string
    """
    try:
        float_amount = float(amount)
        return f"${float_amount:.2f}"
    except (ValueError, TypeError):
        return "$0.00"


def parse_date(date_str: str) -> Optional[date]:
    """
    Parse date string into date object
    
    Args:
        date_str: Date string in various formats
        
    Returns:
        Date object or None if parsing fails
    """
    if not date_str or not isinstance(date_str, str):
        return None
    
    # Common date formats to try
    date_formats = [
        '%m/%d/%Y',    # MM/DD/YYYY
        '%m/%d/%y',    # MM/DD/YY
        '%d/%m/%Y',    # DD/MM/YYYY
        '%d/%m/%y',    # DD/MM/YY
        '%Y-%m-%d',    # YYYY-MM-DD
        '%d %b %Y',    # DD MMM YYYY
        '%b %d %Y',    # MMM DD YYYY
        '%d-%m-%Y',    # DD-MM-YYYY
        '%m-%d-%Y',    # MM-DD-YYYY
    ]
    
    date_str = date_str.strip()
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    return None


def clean_text(text: str) -> str:
    """
    Clean and normalize text string
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text string
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove common PDF artifacts
    text = text.replace('\x00', '')  # Null characters
    text = text.replace('\ufffd', '')  # Replacement characters
    
    # Remove multiple consecutive periods
    text = re.sub(r'\.{3,}', '...', text)
    
    return text


def extract_amount(text: str) -> Optional[float]:
    """
    Extract monetary amount from text
    
    Args:
        text: Text containing amount
        
    Returns:
        Extracted amount as float or None
    """
    if not text:
        return None
    
    # Pattern to match currency amounts
    patterns = [
        r'\$?\s*-?\d{1,3}(?:,\d{3})*\.\d{2}',  # $1,234.56 or -1,234.56
        r'\$?\s*-?\d+\.\d{2}',                  # $123.45 or -123.45
        r'\$?\s*-?\d+',                         # $123 or -123
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            # Take the last match (usually the most relevant)
            amount_str = matches[-1]
            
            # Clean up the string
            amount_str = re.sub(r'[\$\s,]', '', amount_str)
            
            try:
                return float(amount_str)
            except ValueError:
                continue
    
    return None


def is_likely_transaction(text: str) -> bool:
    """
    Determine if text line likely contains a transaction
    
    Args:
        text: Text line to analyze
        
    Returns:
        True if likely a transaction line
    """
    if not text or len(text.strip()) < 10:
        return False
    
    # Look for date patterns
    date_patterns = [
        r'\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b',
        r'\b\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{2,4}\b',
    ]
    
    has_date = any(re.search(pattern, text) for pattern in date_patterns)
    
    # Look for amount patterns
    has_amount = extract_amount(text) is not None
    
    # Must have both date and amount to be likely transaction
    return has_date and has_amount