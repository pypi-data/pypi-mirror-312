"""Document extraction functionality."""

from typing import Dict, Any, Optional
from pathlib import Path
import logging

from ..config import OCRConfig
from .base import VisionClient, ImagePreprocessor
from .vision_client import OllamaVisionClient
from .image_processor import ImageProcessor

class DocumentExtractor:
    """Main class for document information extraction using Ollama Vision."""
    
    def __init__(
        self,
        config: Optional[OCRConfig] = None,
        vision_client: Optional[VisionClient] = None,
        image_processor: Optional[ImagePreprocessor] = None
    ):
        """
        Initialize the document extractor.
        
        Args:
            config: Configuration object
            vision_client: Custom vision client implementation
            image_processor: Custom image processor implementation
        """
        self.config = config or OCRConfig()
        self.vision_client = vision_client or OllamaVisionClient(self.config.model_name)
        self.image_processor = image_processor or ImageProcessor()
        self._setup_logging()

    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(level=getattr(logging, self.config.log_level))
        self.logger = logging.getLogger(__name__)

    def extract_from_image(
        self,
        image_path: str,
        prompt: Optional[str] = None,
        save_processed: bool = False
    ) -> Dict[str, Any]:
        """
        Extract information from a single image.
        
        Args:
            image_path: Path to the image file
            prompt: Custom prompt for the model
            save_processed: Whether to save processed images
        
        Returns:
            Dictionary containing extraction results and metadata
        """
        try:
            image_path = Path(image_path)
            if not image_path.exists():
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            # Preprocess image if enabled
            if self.config.preprocess_images:
                processed_path = self.image_processor.preprocess(
                    image_path,
                    self.config.optimize_for_ocr
                )
            else:
                processed_path = image_path
            
            # Extract text using vision client
            result = self.vision_client.process_image(processed_path, prompt)
            
            # Clean up if needed
            if not save_processed and processed_path != image_path:
                processed_path.unlink()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error extracting from image: {str(e)}")
            raise
