from typing import List, Dict, Optional, Union
from pathlib import Path
import logging

from .vision_client import OllamaVisionClient
from .image_processor import ImageProcessor

class DocumentExtractor:
    """Main class for document information extraction using Ollama Vision."""
    
    def __init__(
        self,
        model_name: str = "llava",
        preprocess_images: bool = True,
        optimize_for_ocr: bool = False
    ):
        """
        Initialize the document extractor.
        
        Args:
            model_name (str): Name of the Ollama model to use.
            preprocess_images (bool): Whether to apply basic preprocessing.
            optimize_for_ocr (bool): Whether to apply OCR-specific optimizations.
        """
        self.vision_client = OllamaVisionClient(model_name)
        self.image_processor = ImageProcessor()
        self.preprocess_images = preprocess_images
        self.optimize_for_ocr = optimize_for_ocr
        self._setup_logging()

    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def extract_from_image(
        self,
        image_path: str,
        prompt: Optional[str] = None,
        save_processed: bool = False
    ) -> Dict[str, str]:
        """
        Extract information from a single image.
        
        Args:
            image_path (str): Path to the image file.
            prompt (str, optional): Custom prompt for the model.
            save_processed (bool): Whether to save processed images.
        
        Returns:
            Dict[str, str]: Dictionary containing extraction results and metadata.
        """
        try:
            processed_path = image_path
            
            # Apply image processing if enabled
            if self.preprocess_images or self.optimize_for_ocr:
                if self.optimize_for_ocr:
                    processed_path = self.image_processor.optimize_for_ocr(
                        image_path,
                        output_path=str(Path(image_path).parent / f"processed_{Path(image_path).name}") if save_processed else None
                    )
                else:
                    processed_path = self.image_processor.preprocess_image(
                        image_path,
                        output_path=str(Path(image_path).parent / f"processed_{Path(image_path).name}") if save_processed else None
                    )

            # Extract information using vision model
            content = self.vision_client.process_image(processed_path, prompt)

            return {
                'original_image': image_path,
                'processed_image': processed_path if save_processed else None,
                'content': content
            }

        except Exception as e:
            self.logger.error(f"Error extracting from image {image_path}: {str(e)}")
            return {
                'original_image': image_path,
                'error': str(e)
            }

    def extract_from_images(
        self,
        image_paths: List[str],
        prompt: Optional[str] = None,
        save_processed: bool = False
    ) -> List[Dict[str, str]]:
        """
        Extract information from multiple images.
        
        Args:
            image_paths (List[str]): List of paths to image files.
            prompt (str, optional): Custom prompt for the model.
            save_processed (bool): Whether to save processed images.
        
        Returns:
            List[Dict[str, str]]: List of dictionaries containing extraction results.
        """
        results = []
        for image_path in image_paths:
            result = self.extract_from_image(image_path, prompt, save_processed)
            results.append(result)
        return results

    def extract_with_custom_prompt(
        self,
        image_paths: Union[str, List[str]],
        prompt: str,
        save_processed: bool = False
    ) -> Union[Dict[str, str], List[Dict[str, str]]]:
        """
        Extract information using a custom prompt.
        
        Args:
            image_paths: Single image path or list of image paths.
            prompt (str): Custom prompt for the model.
            save_processed (bool): Whether to save processed images.
        
        Returns:
            Extraction results for single or multiple images.
        """
        if isinstance(image_paths, str):
            return self.extract_from_image(image_paths, prompt, save_processed)
        else:
            return self.extract_from_images(image_paths, prompt, save_processed)
