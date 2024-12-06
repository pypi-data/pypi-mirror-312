"""Vision client implementation using Ollama."""

from typing import Dict, Any, Optional
from pathlib import Path
import base64
import logging
import ollama

from .base import VisionClient

class OllamaVisionClient(VisionClient):
    """Client for interacting with Ollama Vision models."""
    
    def __init__(self, model_name: str = "llava"):
        """Initialize the vision client."""
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)
        
    def _encode_image(self, image_path: Path) -> str:
        """Encode image to base64."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
            
    def process_image(
        self,
        image_path: Path,
        prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process an image using Ollama Vision model.
        
        Args:
            image_path: Path to the image
            prompt: Optional prompt to guide the model
            
        Returns:
            Dictionary containing model response
        """
        try:
            base64_image = self._encode_image(image_path)
            
            # Default prompt if none provided
            if not prompt:
                prompt = "Please extract and describe the text content from this image."
            
            # Call Ollama API
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                images=[base64_image]
            )
            
            return {
                "text": response.response,
                "model": self.model_name,
                "prompt": prompt
            }
            
        except Exception as e:
            self.logger.error(f"Error processing image with Ollama: {str(e)}")
            raise
