"""Utils package initialization."""
try:
    from utils.logging_config import logger, setup_logger
    from utils.formatting import format_number, format_percent, format_delta, format_date, truncate_text
    from utils.validation import validate_dataframe, validate_model_pipeline, ValidationError
except ImportError:
    from .logging_config import logger, setup_logger
    from .formatting import format_number, format_percent, format_delta, format_date, truncate_text
    from .validation import validate_dataframe, validate_model_pipeline, ValidationError
