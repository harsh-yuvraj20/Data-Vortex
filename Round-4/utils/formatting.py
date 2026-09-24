"""
Formatting utilities for figures, metrics, and tables.
"""

from typing import Union, Optional
import pandas as pd

def format_number(val: Union[int, float, None], precision: int = 0) -> str:
    """Formats an integer or float with comma separators."""
    if val is None or pd.isna(val):
        return "N/A"
    if precision == 0:
        return f"{int(round(val)):,}"
    return f"{val:,.{precision}f}"

def format_percent(val: Union[int, float, None], precision: int = 1) -> str:
    """Formats a decimal float as a percentage string."""
    if val is None or pd.isna(val):
        return "N/A"
    return f"{val * 100:.{precision}f}%"

def format_delta(val: Union[int, float, None], precision: int = 4) -> str:
    """Formats a delta with explicit + or - sign."""
    if val is None or pd.isna(val):
        return "N/A"
    sign = "+" if val > 0 else ""
    return f"{sign}{val:.{precision}f}"

def format_date(val: Union[str, pd.Timestamp], fmt: str = "%b %d, %Y") -> str:
    """Formats a date or timestamp string."""
    if val is None or pd.isna(val):
        return "N/A"
    try:
        ts = pd.to_datetime(val)
        return ts.strftime(fmt)
    except Exception:
        return str(val)

def truncate_text(text: str, max_chars: int = 80) -> str:
    """Truncates text with ellipsis if exceeding max length."""
    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    return text[:max_chars - 3] + "..."
