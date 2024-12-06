import ollama
from typing import List, Dict, Optional
import logging
from pathlib import Path

class OllamaVisionClient:
    """Client for interacting with Ollama Vision model."""
    
    def __init__(self, model_name: str = "llava"):
        """
        Initialize the Ollama Vision client.
        
        Args:
            model_name (str): Name of the Ollama model to use. Defaults to "llava".
        """
        self.model_name = model_name
        self._setup_logging()

    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def process_image(self, image_path: str, prompt: str = None) -> str:
        """
        Process a single image using Ollama Vision model.
        
        Args:
            image_path (str): Path to the image file.
            prompt (str, optional): Custom prompt for the model. 
                                  If None, uses default prompt.
        
        Returns:
            str: Extracted text or description from the image.
        """
        if not prompt:
            prompt = "Extract and describe all text and information from this document:"
        
        try:
            image_path = str(Path(image_path).resolve())
            response = ollama.chat(
                model=self.model_name,
                messages=[{
                    'role': 'user',
                    'content': prompt,
                    'images': [image_path]
                }]
            )
            return response['message']['content']
        except Exception as e:
            self.logger.error(f"Error processing image {image_path}: {str(e)}")
            raise

    def process_multiple_images(self, image_paths: List[str], prompt: str = None) -> List[Dict[str, str]]:
        """
        Process multiple images using Ollama Vision model.
        
        Args:
            image_paths (List[str]): List of paths to image files.
            prompt (str, optional): Custom prompt for the model.
        
        Returns:
            List[Dict[str, str]]: List of dictionaries containing image paths and their extracted content.
        """
        results = []
        for image_path in image_paths:
            try:
                content = self.process_image(image_path, prompt)
                results.append({
                    'image_path': image_path,
                    'content': content
                })
            except Exception as e:
                self.logger.error(f"Error processing image {image_path}: {str(e)}")
                results.append({
                    'image_path': image_path,
                    'error': str(e)
                })
        return results
