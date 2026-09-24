"""
Validation utilities for ensuring data integrity, schema consistency, and model readiness.
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
    allow_empty: bool = False
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
        raise ValidationError(
            f"[{name}] has {len(df)} rows, expected at least {min_rows}."
        )
    
    null_counts = {c: int(df[c].isna().sum()) for c in required_columns if df[c].isna().sum() > 0}
    
    return {
        "status": "VALID",
        "rows": len(df),
        "columns": list(df.columns),
        "null_counts": null_counts,
    }

def validate_model_pipeline(pipeline: Any, required_classes: List[str], name: str = "Model") -> Dict[str, Any]:
    """
    Validates a trained scikit-learn pipeline for inference readiness.
    """
    if pipeline is None:
        raise ValidationError(f"[{name}] pipeline is None.")
    
    if not hasattr(pipeline, "predict"):
        raise ValidationError(f"[{name}] pipeline does not implement 'predict'.")
    
    classes = getattr(pipeline, "classes_", None)
    if classes is not None:
        classes_list = list(classes)
        for req_cls in required_classes:
            if req_cls not in classes_list:
                raise ValidationError(f"[{name}] missing expected class '{req_cls}'. Found: {classes_list}")
    
    return {
        "status": "VALID",
        "has_predict_proba": hasattr(pipeline, "predict_proba"),
        "has_decision_function": hasattr(pipeline, "decision_function"),
        "classes": list(classes) if classes is not None else [],
    }
