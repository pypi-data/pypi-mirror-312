import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional
import logging
from pathlib import Path

class ImageProcessor:
    """Handle image preprocessing operations."""
    
    def __init__(self):
        """Initialize the image processor."""
        self._setup_logging()

    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def preprocess_image(
        self, 
        image_path: str,
        output_path: Optional[str] = None,
        resize: Optional[Tuple[int, int]] = None,
        denoise: bool = True,
        enhance_contrast: bool = True
    ) -> str:
        """
        Preprocess image for better text extraction.
        
        Args:
            image_path (str): Path to input image.
            output_path (str, optional): Path to save processed image.
            resize (Tuple[int, int], optional): Target size (width, height).
            denoise (bool): Apply denoising.
            enhance_contrast (bool): Apply contrast enhancement.
        
        Returns:
            str: Path to processed image.
        """
        try:
            # Read image
            image = cv2.imread(str(Path(image_path).resolve()))
            if image is None:
                raise ValueError(f"Could not read image at {image_path}")

            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply preprocessing steps
            processed = self._apply_preprocessing(
                gray,
                denoise=denoise,
                enhance_contrast=enhance_contrast
            )

            # Resize if specified
            if resize:
                processed = cv2.resize(processed, resize)

            # Determine output path
            if output_path is None:
                path = Path(image_path)
                output_path = str(path.parent / f"{path.stem}_processed{path.suffix}")

            # Save processed image
            cv2.imwrite(output_path, processed)
            self.logger.info(f"Processed image saved to: {output_path}")
            
            return output_path

        except Exception as e:
            self.logger.error(f"Error preprocessing image: {str(e)}")
            raise

    def _apply_preprocessing(
        self,
        image: np.ndarray,
        denoise: bool = True,
        enhance_contrast: bool = True
    ) -> np.ndarray:
        """
        Apply preprocessing steps to the image.
        
        Args:
            image (np.ndarray): Input image array.
            denoise (bool): Apply denoising.
            enhance_contrast (bool): Apply contrast enhancement.
        
        Returns:
            np.ndarray: Processed image array.
        """
        processed = image.copy()

        if denoise:
            processed = cv2.fastNlMeansDenoising(processed)

        if enhance_contrast:
            # Apply adaptive histogram equalization
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            processed = clahe.apply(processed)

        return processed

    def optimize_for_ocr(self, image_path: str, output_path: Optional[str] = None) -> str:
        """
        Apply optimizations specifically for OCR processing.
        
        Args:
            image_path (str): Path to input image.
            output_path (str, optional): Path to save processed image.
        
        Returns:
            str: Path to processed image.
        """
        try:
            # Read image
            image = cv2.imread(str(Path(image_path).resolve()))
            if image is None:
                raise ValueError(f"Could not read image at {image_path}")

            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply Otsu's thresholding
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Determine output path
            if output_path is None:
                path = Path(image_path)
                output_path = str(path.parent / f"{path.stem}_ocr{path.suffix}")

            # Save processed image
            cv2.imwrite(output_path, binary)
            self.logger.info(f"OCR-optimized image saved to: {output_path}")
            
            return output_path

        except Exception as e:
            self.logger.error(f"Error optimizing image for OCR: {str(e)}")
            raise
