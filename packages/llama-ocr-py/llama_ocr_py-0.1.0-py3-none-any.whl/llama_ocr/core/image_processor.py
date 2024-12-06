"""Image processing utilities."""

from pathlib import Path
import cv2
import numpy as np
import logging
from typing import Tuple

from .base import ImagePreprocessor

class ImageProcessor(ImagePreprocessor):
    """Handles image preprocessing for better OCR results."""
    
    def __init__(self):
        """Initialize the image processor."""
        self.logger = logging.getLogger(__name__)
    
    def _resize_if_needed(
        self,
        image: np.ndarray,
        min_width: int = 1024
    ) -> np.ndarray:
        """Resize image if it's too small."""
        height, width = image.shape[:2]
        if width < min_width:
            scale = min_width / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            return cv2.resize(image, (new_width, new_height))
        return image
    
    def _denoise(self, image: np.ndarray) -> np.ndarray:
        """Apply denoising to image."""
        return cv2.fastNlMeansDenoisingColored(image)
    
    def _optimize_for_ocr(self, image: np.ndarray) -> np.ndarray:
        """Apply OCR-specific optimizations."""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Remove small noise
        kernel = np.ones((2,2), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        return binary
    
    def preprocess(
        self,
        image_path: Path,
        optimize_for_ocr: bool = False
    ) -> Path:
        """
        Preprocess an image for better OCR results.
        
        Args:
            image_path: Path to input image
            optimize_for_ocr: Whether to apply OCR-specific optimizations
            
        Returns:
            Path to processed image
        """
        try:
            # Read image
            image = cv2.imread(str(image_path))
            if image is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            # Basic preprocessing
            image = self._resize_if_needed(image)
            image = self._denoise(image)
            
            # OCR-specific processing if requested
            if optimize_for_ocr:
                image = self._optimize_for_ocr(image)
            
            # Save processed image
            output_path = image_path.parent / f"processed_{image_path.name}"
            cv2.imwrite(str(output_path), image)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error preprocessing image: {str(e)}")
            raise
