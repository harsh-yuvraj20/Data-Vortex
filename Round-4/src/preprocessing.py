"""
Preprocessing and validation functions for DATA VORTEX 2026 — Round 4.
"""

from typing import Dict, Any, List
import pandas as pd

class ValidationError(Exception):
    """Raised when data or model integrity validation fails."""
    pass

def validate_dataframe(
    df: pd.DataFrame,
    required_columns: List[str],
    min_rows: int = 1,
    name: str = "DataFrame",
    allow_empty: bool = False,
) -> Dict[str, Any]:
    """
    Validates that a dataframe meets schema and volume expectations.
    """
    if df is None:
        raise ValidationError(f"[{name}] is None.")
    
    if df.empty and not allow_empty:
        raise ValidationError(f"[{name}] is unexpectedly empty.")
    
    missing_cols = [c for c in required_columns if c not in df.columns]
    if missing_cols:
        raise ValidationError(f"[{name}] missing required columns: {missing_cols}")
    
    if len(df) < min_rows and not allow_empty:
        raise ValidationError(f"[{name}] has {len(df)} rows, expected at least {min_rows}.")
    
    null_counts = {c: int(df[c].isna().sum()) for c in required_columns if df[c].isna().sum() > 0}
    
    return {
        "status": "VALID",
        "rows": len(df),
        "columns": list(df.columns),
        "null_counts": null_counts,
    }

def clean_social_text(text: str) -> str:
    """Standardizes input text for analysis or classification."""
    if not isinstance(text, str):
        return ""
    return " ".join(text.strip().split())
