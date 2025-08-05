"""
Data export functionality for transaction data
"""

from pathlib import Path
from typing import List, Dict, Any, Union
import pandas as pd
import csv
from datetime import datetime


class DataExporter:
    """
    Handles exporting transaction data to various formats
    """
    
    def __init__(self):
        self.base_output_dir = Path("outputs")
    
    def export(self, transactions: List[Dict[str, Any]], output_path: Path, format: str = 'csv') -> None:
        """
        Export transaction data to specified format
        
        Args:
            transactions: List of transaction dictionaries
            output_path: Path for output file
            format: Export format ('csv' or 'excel')
            
        Raises:
            ValueError: If format is not supported
            IOError: If file cannot be written
        """
        if not transactions:
            raise ValueError("No transactions to export")
        
        format = format.lower()
        
        if format == 'csv':
            self._export_csv(transactions, output_path)
        elif format in ['excel', 'xlsx']:
            self._export_excel(transactions, output_path)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def export_organized(self, transactions: List[Dict[str, Any]], format: str = 'csv', base_filename: str = None) -> Path:
        """
        Export transactions with organized folder structure: outputs/bank/YYYY-MM/
        
        Args:
            transactions: List of transaction dictionaries
            format: Export format ('csv' or 'excel')
            base_filename: Optional base filename (default: transactions)
            
        Returns:
            Path to created file
            
        Raises:
            ValueError: If no transactions or unsupported format
        """
        if not transactions:
            raise ValueError("No transactions to export")
        
        # Detect bank and date range from transactions
        bank = transactions[0].get('bank', 'unknown')
        
        # Find the most common month from transactions
        dates = []
        for txn in transactions:
            try:
                date_str = txn.get('date', '')
                if date_str:
                    # Parse date string (assumes YYYY-MM-DD format)
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    dates.append(date_obj)
            except:
                continue
        
        if dates:
            # TODO: FIX - Using latest transaction date causes incorrect folder placement
            # for same-month statements. Should use statement date instead.
            # Issue: Different HDFC PDFs from same month go to different folders
            latest_date = max(dates)
            year_month = latest_date.strftime('%Y-%m')
        else:
            # Fallback to current date
            year_month = datetime.now().strftime('%Y-%m')
        
        # Create organized directory structure
        output_dir = self.base_output_dir / bank / year_month
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        if not base_filename:
            base_filename = f"{bank}_transactions_{year_month}"
        
        # Add extension based on format
        if format.lower() == 'csv':
            filename = f"{base_filename}.csv"
        elif format.lower() in ['excel', 'xlsx']:
            filename = f"{base_filename}.xlsx"
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        output_path = output_dir / filename
        
        # Export using existing methods
        self.export(transactions, output_path, format)
        
        return output_path
    
    def _export_csv(self, transactions: List[Dict[str, Any]], output_path: Path) -> None:
        """
        Export transactions to CSV format
        
        Args:
            transactions: List of transaction dictionaries
            output_path: Path for CSV output
        """
        try:
            # Convert to DataFrame for easier handling
            df = pd.DataFrame(transactions)
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Export to CSV
            df.to_csv(output_path, index=False, encoding='utf-8')
            
        except Exception as e:
            raise IOError(f"Failed to export CSV: {e}")
    
    def _export_excel(self, transactions: List[Dict[str, Any]], output_path: Path) -> None:
        """
        Export transactions to Excel format
        
        Args:
            transactions: List of transaction dictionaries
            output_path: Path for Excel output
        """
        try:
            # Convert to DataFrame
            df = pd.DataFrame(transactions)
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Export to Excel with formatting
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Transactions', index=False)
                
                # Get the workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['Transactions']
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    for cell in column:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    
                    # Set column width with some padding
                    adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
        except Exception as e:
            raise IOError(f"Failed to export Excel: {e}")
    
    def export_summary(self, transactions: List[Dict[str, Any]], output_path: Path) -> None:
        """
        Export a summary report of transactions
        
        Args:
            transactions: List of transaction dictionaries
            output_path: Path for summary output
        """
        try:
            df = pd.DataFrame(transactions)
            
            # Generate summary statistics
            summary = {
                'total_transactions': len(df),
                'total_amount': df['amount'].sum() if 'amount' in df.columns else 0,
                'average_amount': df['amount'].mean() if 'amount' in df.columns else 0,
                'date_range': {
                    'earliest': df['date'].min() if 'date' in df.columns else None,
                    'latest': df['date'].max() if 'date' in df.columns else None
                }
            }
            
            # Write summary to text file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("Credit Card Statement Summary\n")
                f.write("=" * 40 + "\n\n")
                f.write(f"Total Transactions: {summary['total_transactions']}\n")
                f.write(f"Total Amount: ${summary['total_amount']:.2f}\n")
                f.write(f"Average Amount: ${summary['average_amount']:.2f}\n")
                
                if summary['date_range']['earliest']:
                    f.write(f"Date Range: {summary['date_range']['earliest']} to {summary['date_range']['latest']}\n")
                
                f.write("\n" + "=" * 40 + "\n")
        
        except Exception as e:
            raise IOError(f"Failed to export summary: {e}")
    
    def validate_transactions(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate transaction data before export
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            Validation report dictionary
        """
        if not transactions:
            return {'valid': False, 'errors': ['No transactions provided']}
        
        errors = []
        warnings = []
        
        # Check required fields
        required_fields = ['date', 'description', 'amount']
        
        for i, transaction in enumerate(transactions):
            for field in required_fields:
                if field not in transaction or transaction[field] is None:
                    errors.append(f"Transaction {i+1}: Missing required field '{field}'")
            
            # Validate amount is numeric
            if 'amount' in transaction:
                try:
                    float(transaction['amount'])
                except (ValueError, TypeError):
                    errors.append(f"Transaction {i+1}: Amount is not numeric")
            
            # Check for empty descriptions
            if 'description' in transaction and not str(transaction['description']).strip():
                warnings.append(f"Transaction {i+1}: Empty description")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'transaction_count': len(transactions)
        }