"""
Command Line Interface for Debrokly
"""

import click
from pathlib import Path
from typing import Optional

from .core.pdf_parser import PDFParser
from .core.extractor import TransactionExtractor
from .core.exporter import DataExporter


@click.command()
@click.argument('pdf_path', type=click.Path(exists=True, path_type=Path))
@click.option('--password', '-p', help='PDF password')
@click.option('--output', '-o', type=click.Path(path_type=Path), 
              help='Output file path (CSV or Excel)')
@click.option('--format', '-f', type=click.Choice(['csv', 'excel']), 
              default='csv', help='Output format')
@click.version_option()
def main(pdf_path: Path, password: Optional[str], output: Optional[Path], format: str):
    """
    Extract transaction data from credit card statement PDF.
    
    PDF_PATH: Path to the credit card statement PDF file
    """
    try:
        click.echo(f"Processing PDF: {pdf_path}")
        
        # Initialize components
        parser = PDFParser()
        extractor = TransactionExtractor()
        exporter = DataExporter()
        
        # Parse PDF
        if password:
            click.echo("Using provided password...")
        parsed_data = parser.parse(pdf_path, password)
        
        # Extract transactions
        click.echo("Extracting transaction data...")
        transactions = extractor.extract(parsed_data)
        
        # Export data
        if not output:
            output = pdf_path.with_suffix(f'.{format}' if format == 'csv' else '.xlsx')
        
        click.echo(f"Exporting to {output} in {format} format...")
        exporter.export(transactions, output, format)
        
        click.echo(f"✅ Successfully extracted {len(transactions)} transactions")
        click.echo(f"📄 Output saved to: {output}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    main()