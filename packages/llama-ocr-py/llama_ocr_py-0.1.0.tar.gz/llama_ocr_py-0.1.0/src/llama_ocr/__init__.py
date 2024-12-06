"""
llama_ocr - A package for document extraction using Ollama Vision model.
"""

from .core.extractor import DocumentExtractor
from .core.vision_client import OllamaVisionClient
from .core.image_processor import ImageProcessor
from .config import OCRConfig

__version__ = "0.1.0"
__all__ = ["DocumentExtractor", "OllamaVisionClient", "ImageProcessor", "OCRConfig"]
