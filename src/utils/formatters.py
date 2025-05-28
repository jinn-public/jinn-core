"""
Formatting Utilities

Functions for formatting economic data and simulation results for display.
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format a decimal value as a percentage.
    
    Args:
        value: Decimal value (e.g., 0.025 for 2.5%)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimals}f}%"


def format_currency(value: float, currency: str = "USD", decimals: int = 2) -> str:
    """
    Format a value as currency.
    
    Args:
        value: Numeric value
        currency: Currency code
        decimals: Number of decimal places
        
    Returns:
        Formatted currency string
    """
    if currency == "USD":
        symbol = "$"
    elif currency == "EUR":
        symbol = "€"
    elif currency == "GBP":
        symbol = "£"
    else:
        symbol = currency + " "
    
    # Handle large numbers
    if abs(value) >= 1_000_000_000:
        return f"{symbol}{value/1_000_000_000:.{decimals}f}B"
    elif abs(value) >= 1_000_000:
        return f"{symbol}{value/1_000_000:.{decimals}f}M"
    elif abs(value) >= 1_000:
        return f"{symbol}{value/1_000:.{decimals}f}K"
    else:
        return f"{symbol}{value:.{decimals}f}"


def format_number(value: float, decimals: int = 2, thousands_sep: str = ",") -> str:
    """
    Format a number with thousands separator.
    
    Args:
        value: Numeric value
        decimals: Number of decimal places
        thousands_sep: Thousands separator character
        
    Returns:
        Formatted number string
    """
    formatted = f"{value:,.{decimals}f}"
    if thousands_sep != ",":
        formatted = formatted.replace(",", thousands_sep)
    return formatted


def format_basis_points(value: float) -> str:
    """
    Format a decimal value as basis points.
    
    Args:
        value: Decimal value (e.g., 0.0025 for 25 basis points)
        
    Returns:
        Formatted basis points string
    """
    bp = value * 10000
    return f"{bp:.0f} bp"


def format_simulation_summary(results: Dict[str, Any]) -> str:
    """
    Format simulation results into a readable summary.
    
    Args:
        results: Simulation results dictionary
        
    Returns:
        Formatted summary string
    """
    lines = []
    lines.append("=" * 60)
    lines.append("SIMULATION SUMMARY")
    lines.append("=" * 60)
    
    # Basic info
    if 'model' in results:
        lines.append(f"Model: {results['model']}")
    
    if 'metadata' in results:
        metadata = results['metadata']
        if 'execution_time_seconds' in metadata:
            lines.append(f"Execution Time: {metadata['execution_time_seconds']:.2f} seconds")
        if 'start_time' in metadata:
            lines.append(f"Run Time: {metadata['start_time']}")
    
    lines.append("")
    
    # Results summary
    if 'results' in results and 'summary' in results['results']:
        summary = results['results']['summary']
        lines.append("KEY METRICS:")
        lines.append("-" * 30)
        
        for key, value in summary.items():
            if isinstance(value, float):
                if 'gdp' in key.lower() or 'inflation' in key.lower():
                    formatted_value = format_percentage(value)
                elif 'change' in key.lower():
                    formatted_value = format_currency(value)
                else:
                    formatted_value = format_number(value)
                
                # Clean up key name
                clean_key = key.replace('_', ' ').title()
                lines.append(f"  {clean_key}: {formatted_value}")
    
    lines.append("=" * 60)
    return "\n".join(lines)


def format_time_series(data: Dict[str, List], title: str = "Time Series Data") -> str:
    """
    Format time series data for tabular display.
    
    Args:
        data: Dictionary with time series data
        title: Table title
        
    Returns:
        Formatted table string
    """
    if not data:
        return "No data to display"
    
    lines = []
    lines.append(f"\n{title}")
    lines.append("=" * len(title))
    
    # Get periods (assuming it's the first key or 'periods')
    periods_key = 'periods' if 'periods' in data else list(data.keys())[0]
    periods = data[periods_key]
    
    if not periods:
        return "No data to display"
    
    # Prepare headers
    headers = ['Period']
    data_keys = [key for key in data.keys() if key != periods_key]
    headers.extend(data_keys)
    
    # Calculate column widths
    col_widths = [max(len(str(header)), 8) for header in headers]
    for i, period in enumerate(periods):
        col_widths[0] = max(col_widths[0], len(str(period)))
        for j, key in enumerate(data_keys, 1):
            if i < len(data[key]):
                value_str = f"{data[key][i]:.4f}" if isinstance(data[key][i], float) else str(data[key][i])
                col_widths[j] = max(col_widths[j], len(value_str))
    
    # Create header row
    header_row = " | ".join(header.ljust(col_widths[i]) for i, header in enumerate(headers))
    lines.append(header_row)
    lines.append("-" * len(header_row))
    
    # Create data rows
    for i, period in enumerate(periods):
        row_data = [str(period).ljust(col_widths[0])]
        for j, key in enumerate(data_keys, 1):
            if i < len(data[key]):
                value = data[key][i]
                if isinstance(value, float):
                    value_str = f"{value:.4f}"
                else:
                    value_str = str(value)
                row_data.append(value_str.ljust(col_widths[j]))
            else:
                row_data.append("N/A".ljust(col_widths[j]))
        
        lines.append(" | ".join(row_data))
    
    return "\n".join(lines)


def export_results_json(results: Dict[str, Any], filename: str, pretty: bool = True) -> None:
    """
    Export simulation results to JSON file.
    
    Args:
        results: Results dictionary
        filename: Output filename
        pretty: Whether to format JSON for readability
    """
    with open(filename, 'w') as f:
        if pretty:
            json.dump(results, f, indent=2, default=str)
        else:
            json.dump(results, f, default=str)


def create_csv_export(data: Dict[str, List], filename: str) -> None:
    """
    Export time series data to CSV file.
    
    Args:
        data: Dictionary with time series data
        filename: Output filename
    """
    if not data:
        return
    
    # Get periods and data keys
    periods_key = 'periods' if 'periods' in data else list(data.keys())[0]
    periods = data[periods_key]
    data_keys = [key for key in data.keys() if key != periods_key]
    
    with open(filename, 'w') as f:
        # Write header
        headers = ['period'] + data_keys
        f.write(','.join(headers) + '\n')
        
        # Write data rows
        for i, period in enumerate(periods):
            row = [str(period)]
            for key in data_keys:
                if i < len(data[key]):
                    value = data[key][i]
                    row.append(str(value))
                else:
                    row.append('')
            f.write(','.join(row) + '\n') 