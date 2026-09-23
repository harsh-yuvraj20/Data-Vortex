"""Text normalization utilities.

The classifier receives original text. Normalization here is used only to form
duplicate groups, so that duplicate detection cannot alter model features.
"""
import re
import unicodedata


def normalize_for_duplicate_detection(text: object) -> str:
    value = unicodedata.normalize("NFKC", str(text or "")).lower().strip()
    return re.sub(r"\s+", " ", value)


def has_suspicious_text(text: object) -> bool:
    value = str(text or "")
    return len(value.strip()) < 2 or "\x00" in value
