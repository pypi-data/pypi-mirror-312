"""Tests for llama_ocr package."""

import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from llama_ocr import DocumentExtractor, OCRConfig
from llama_ocr.core.base import VisionClient, ImagePreprocessor

class TestDocumentExtractor(unittest.TestCase):
    """Test cases for DocumentExtractor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = OCRConfig(
            model_name="test-model",
            preprocess_images=True
        )
        self.extractor = DocumentExtractor(config=self.config)
    
    @patch('llama_ocr.core.vision_client.OllamaVisionClient')
    def test_extract_from_image(self, mock_client):
        """Test basic image extraction."""
        # Setup mock
        mock_client.process_image.return_value = {
            "text": "Sample extracted text",
            "confidence": 0.95
        }
        
        # Test extraction
        result = self.extractor.extract_from_image(
            "test_image.jpg",
            prompt="Extract text"
        )
        
        self.assertIn("text", result)
        self.assertEqual(result["text"], "Sample extracted text")

if __name__ == '__main__':
    unittest.main()
