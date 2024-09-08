"""
Quart LibreTranslate
"""
from .core import LibreTranslate
from .error import ApiError
from .wrappers import detect, languages, translate

__all__ = [
    "LibreTranslate",
    "ApiError",
    "detect",
    "languages",
    "translate"
]