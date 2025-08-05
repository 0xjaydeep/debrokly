"""
Transaction data extraction from parsed PDF content
"""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from ..utils.helpers import parse_date, extract_amount, clean_text, is_likely_transaction


class TransactionExtractor:
    """
    Extracts transaction data from parsed PDF content using bank-specific patterns
    """
    
    def __init__(self):
        # Bank detection patterns
        self.bank_patterns = {
            'aubank': ['AU BANK', 'AU SMALL FINANCE BANK', 'AUSFB'],
            'hdfc': ['HDFC BANK', 'HDFC', 'Millennia Credit Card'],
            'icici': ['ICICI BANK', 'ICICI'],
            'sbi': ['STATE BANK OF INDIA', 'SBI'],
            'axis': ['AXIS BANK', 'AXIS'],
        }
    
    def extract(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract transaction data from parsed PDF
        
        Args:
            parsed_data: Parsed PDF data from PDFParser
            
        Returns:
            List of transaction dictionaries
        """
        # Detect bank type
        bank_type = self._detect_bank_type(parsed_data)
        print(f"Detected bank type: {bank_type}")
        
        # Extract transactions based on bank type
        if bank_type == 'aubank':
            transactions = self._extract_aubank_transactions(parsed_data)
        elif bank_type == 'hdfc':
            transactions = self._extract_hdfc_transactions(parsed_data)
        else:
            # Generic extraction fallback
            transactions = self._extract_generic_transactions(parsed_data)
        
        return self._clean_and_validate_transactions(transactions)
    
    def _detect_bank_type(self, parsed_data: Dict[str, Any]) -> str:
        """
        Detect bank type from PDF content
        
        Args:
            parsed_data: Parsed PDF data
            
        Returns:
            Bank type identifier
        """
        # Combine all text from all pages
        all_text = ""
        for page in parsed_data.get('pages', []):
            all_text += page.get('text', '') + " "
            # Also check OCR text if available
            all_text += page.get('ocr_text', '') + " "
        
        all_text = all_text.upper()
        
        # Check for bank patterns
        for bank, patterns in self.bank_patterns.items():
            for pattern in patterns:
                if pattern in all_text:
                    return bank
        
        return 'generic'
    
    def _extract_aubank_transactions(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract transactions from AU Bank statement format
        
        Args:
            parsed_data: Parsed PDF data
            
        Returns:
            List of transaction dictionaries
        """
        transactions = []
        
        for page in parsed_data.get('pages', []):
            # Method 1: Extract from tables
            for table in page.get('tables', []):
                rows = table.get('rows', [])
                
                # Check if this is a transaction table
                if self._is_aubank_transaction_table(rows):
                    transactions.extend(self._parse_aubank_table(rows))
            
            # Method 2: Extract from compressed transaction summary
            transactions.extend(self._parse_aubank_summary(page.get('text', '')))
        
        return transactions
    
    def _extract_hdfc_transactions(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract transactions from HDFC Bank statement format
        
        Args:
            parsed_data: Parsed PDF data
            
        Returns:
            List of transaction dictionaries
        """
        transactions = []
        
        for page in parsed_data.get('pages', []):
            text = page.get('text', '')
            
            # Find domestic transactions section
            lines = text.split('\n')
            transaction_section = False
            
            for line in lines:
                line = line.strip()
                
                if 'Domestic Transactions' in line:
                    transaction_section = True
                    continue
                elif any(end_marker in line for end_marker in ['Cash points', 'International Transactions', 'Page']):
                    transaction_section = False
                
                if transaction_section and line:
                    transaction = self._parse_hdfc_transaction_line(line)
                    if transaction:
                        transactions.append(transaction)
        
        return transactions
    
    def _extract_generic_transactions(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generic transaction extraction for unknown bank formats
        
        Args:
            parsed_data: Parsed PDF data
            
        Returns:
            List of transaction dictionaries
        """
        transactions = []
        
        for page in parsed_data.get('pages', []):
            # Try table extraction first
            for table in page.get('tables', []):
                rows = table.get('rows', [])
                if len(rows) > 1:  # Skip single-row tables
                    table_transactions = self._parse_generic_table(rows)
                    transactions.extend(table_transactions)
            
            # Try text-based extraction
            text = page.get('text', '')
            text_transactions = self._parse_generic_text(text)
            transactions.extend(text_transactions)
        
        return transactions
    
    def _is_aubank_transaction_table(self, rows: List[List]) -> bool:
        """
        Check if table contains AU Bank transactions
        
        Args:
            rows: Table rows
            
        Returns:
            True if transaction table
        """
        if not rows or len(rows) < 2:
            return False
        
        # Check for transaction table headers
        header_text = ' '.join(str(cell) for row in rows[:2] for cell in row if cell)
        transaction_indicators = ['Date', 'Transaction', 'Amount', 'Balance', 'Description']
        
        return sum(1 for indicator in transaction_indicators if indicator in header_text) >= 3
    
    def _parse_aubank_table(self, rows: List[List]) -> List[Dict[str, Any]]:
        """
        Parse AU Bank transaction table
        
        Args:
            rows: Table rows
            
        Returns:
            List of transactions
        """
        transactions = []
        
        # Skip header rows and parse data
        for row in rows[2:]:  # Skip headers
            if not row or not any(row):
                continue
            
            # Extract fields based on AU Bank format
            date = row[0] if len(row) > 0 else None
            description = row[1] if len(row) > 1 else None
            amount = row[2] if len(row) > 2 else None
            balance = row[3] if len(row) > 3 else None
            txn_type = row[4] if len(row) > 4 else None
            
            if date and description and amount:
                transaction = {
                    'date': clean_text(str(date)),
                    'description': clean_text(str(description)),
                    'amount': self._parse_amount_with_type(str(amount)),
                    'balance': self._parse_amount_with_type(str(balance)) if balance else None,
                    'type': clean_text(str(txn_type)) if txn_type else None,
                    'bank': 'aubank'
                }
                transactions.append(transaction)
        
        return transactions
    
    def _parse_aubank_summary(self, text: str) -> List[Dict[str, Any]]:
        """
        Parse AU Bank compressed transaction summary
        
        Args:
            text: Page text containing transaction summary
            
        Returns:
            List of transactions
        """
        transactions = []
        
        # Look for transaction summary pattern
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if 'Transaction Summary' in line:
                # Look for transaction data in subsequent lines
                for j in range(i+1, min(i+10, len(lines))):
                    summary_line = lines[j]
                    if summary_line and any(char.isdigit() for char in summary_line):
                        parsed_transactions = self._parse_summary_line(summary_line)
                        transactions.extend(parsed_transactions)
        
        return transactions
    
    def _parse_summary_line(self, line: str) -> List[Dict[str, Any]]:
        """
        Parse compressed transaction summary line
        
        Args:
            line: Line containing multiple transactions
            
        Returns:
            List of transactions
        """
        transactions = []
        
        # Split by date patterns to separate transactions
        date_pattern = r'\b\d{1,2}\s*/\s*\d{1,2}\s*/\s*\d{2,4}\b'
        parts = re.split(date_pattern, line)
        dates = re.findall(date_pattern, line)
        
        # Match dates with descriptions/amounts
        if len(dates) == len(parts) - 1:
            for i, date in enumerate(dates):
                if i + 1 < len(parts):
                    desc_amount = parts[i + 1].strip()
                    
                    # Extract amount from description
                    amount_match = re.search(r'(\d+\.\d+)(Dr\.|Cr\.)?', desc_amount)
                    if amount_match:
                        amount_str = amount_match.group(1)
                        amount_type = amount_match.group(2) or ''
                        
                        # Clean description
                        description = re.sub(r'\d+\.\d+(Dr\.|Cr\.)?', '', desc_amount).strip()
                        
                        transaction = {
                            'date': date.strip(),
                            'description': description,
                            'amount': float(amount_str) * (-1 if 'Dr' in amount_type else 1),
                            'type': 'debit' if 'Dr' in amount_type else 'credit',
                            'bank': 'aubank'
                        }
                        transactions.append(transaction)
        
        return transactions
    
    def _parse_hdfc_transaction_line(self, line: str) -> Optional[Dict[str, Any]]:
        """
        Parse single HDFC transaction line
        
        Args:
            line: Transaction line text
            
        Returns:
            Transaction dictionary or None
        """
        # HDFC format: DD/MM/YYYY Description Amount [Cr]
        date_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'
        date_match = re.search(date_pattern, line)
        
        if not date_match:
            return None
        
        date_str = date_match.group()
        remaining = line[date_match.end():].strip()
        
        # Extract amount (last number in the line)
        amount_pattern = r'([\d,]+\.\d{2})\s*(Cr)?\s*$'
        amount_match = re.search(amount_pattern, remaining)
        
        if not amount_match:
            return None
        
        amount_str = amount_match.group(1).replace(',', '')
        is_credit = amount_match.group(2) == 'Cr'
        
        # Description is everything between date and amount
        description = remaining[:amount_match.start()].strip()
        
        return {
            'date': date_str,
            'description': description,
            'amount': float(amount_str) * (1 if is_credit else -1),
            'type': 'credit' if is_credit else 'debit',
            'bank': 'hdfc'
        }
    
    def _parse_generic_table(self, rows: List[List]) -> List[Dict[str, Any]]:
        """
        Generic table parsing for unknown formats
        
        Args:
            rows: Table rows
            
        Returns:
            List of transactions
        """
        transactions = []
        
        # Simple heuristic: look for rows with date, description, and amount
        for row in rows[1:]:  # Skip header
            if len(row) >= 3:
                # Try to find date, description, amount in any order
                date_col = None
                desc_col = None
                amount_col = None
                
                for i, cell in enumerate(row):
                    if cell and parse_date(str(cell)):
                        date_col = i
                    elif cell and extract_amount(str(cell)):
                        amount_col = i
                    elif cell and len(str(cell).strip()) > 5:  # Likely description
                        desc_col = i
                
                if date_col is not None and amount_col is not None:
                    transaction = {
                        'date': str(row[date_col]),
                        'description': str(row[desc_col]) if desc_col is not None else 'Unknown',
                        'amount': extract_amount(str(row[amount_col])),
                        'bank': 'generic'
                    }
                    transactions.append(transaction)
        
        return transactions
    
    def _parse_generic_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Generic text parsing for transaction-like lines
        
        Args:
            text: Page text
            
        Returns:
            List of transactions
        """
        transactions = []
        
        lines = text.split('\n')
        for line in lines:
            if is_likely_transaction(line):
                # Extract date, description, amount using patterns
                date_match = re.search(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', line)
                amount = extract_amount(line)
                
                if date_match and amount:
                    date_str = date_match.group()
                    description = line.replace(date_str, '').strip()
                    
                    # Remove amount from description
                    amount_pattern = r'[\d,]+\.\d{2}'
                    description = re.sub(amount_pattern, '', description).strip()
                    
                    transaction = {
                        'date': date_str,
                        'description': description,
                        'amount': amount,
                        'bank': 'generic'
                    }
                    transactions.append(transaction)
        
        return transactions
    
    def _parse_amount_with_type(self, amount_str: str) -> Optional[float]:
        """
        Parse amount string with Dr./Cr. indicators
        
        Args:
            amount_str: Amount string
            
        Returns:
            Float amount (negative for debits)
        """
        if not amount_str:
            return None
        
        # Extract numeric amount
        amount_match = re.search(r'([\d,]+\.?\d*)', str(amount_str))
        if not amount_match:
            return None
        
        amount = float(amount_match.group(1).replace(',', ''))
        
        # Check for Dr./Cr. indicators
        if 'Dr' in amount_str:
            return -amount
        elif 'Cr' in amount_str:
            return amount
        else:
            return amount  # Default to positive
    
    def _clean_and_validate_transactions(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Clean and validate extracted transactions
        
        Args:
            transactions: Raw transactions
            
        Returns:
            Cleaned and validated transactions
        """
        cleaned = []
        
        for txn in transactions:
            # Skip invalid transactions
            if not txn.get('date') or not txn.get('amount'):
                continue
            
            # Parse and validate date
            parsed_date = parse_date(txn['date'])
            if not parsed_date:
                continue
            
            # Clean description
            description = clean_text(txn.get('description', 'Unknown'))
            
            # Ensure amount is numeric
            try:
                amount = float(txn['amount'])
            except (ValueError, TypeError):
                continue
            
            cleaned_txn = {
                'date': parsed_date.strftime('%Y-%m-%d'),
                'description': description,
                'amount': amount,
                'type': txn.get('type', 'debit' if amount < 0 else 'credit'),
                'balance': txn.get('balance'),
                'bank': txn.get('bank', 'unknown'),
                'raw_data': txn  # Keep original for debugging
            }
            
            cleaned.append(cleaned_txn)
        
        # Remove duplicates based on date, description, and amount
        seen = set()
        unique_transactions = []
        
        for txn in cleaned:
            key = (txn['date'], txn['description'][:50], txn['amount'])
            if key not in seen:
                seen.add(key)
                unique_transactions.append(txn)
        
        return unique_transactions