"""Base classes and interfaces for llama_ocr."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path

class VisionClient(ABC):
    """Abstract base class for vision clients."""
    
    @abstractmethod
    def process_image(
        self,
        image_path: Path,
        prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process an image and return results."""
        pass

class ImagePreprocessor(ABC):
    """Abstract base class for image preprocessors."""
    
    @abstractmethod
    def preprocess(
        self,
        image_path: Path,
        optimize_for_ocr: bool = False
    ) -> Path:
        """Preprocess an image and return the processed image path."""
        pass
