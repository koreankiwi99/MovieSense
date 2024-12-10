from unicodedata import normalize
import regex as re
from typing import List

def clean(text: str) -> str:
    """
    Strips, normalizes, and removes non-printable characters from the text.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    return re.sub(r'[^\x20-\x7E\u00A0-\u024F]', '', normalize('NFC', text.strip()))

def filter_texts(texts: List[str]) -> List[str]:
    """
    Filters texts containing only Unicode letters.
    """
    return [t for t in map(clean, texts) if not re.search(r'[^\p{L}]', t)]
