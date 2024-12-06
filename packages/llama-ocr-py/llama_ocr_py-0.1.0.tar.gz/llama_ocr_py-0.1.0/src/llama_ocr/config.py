"""Configuration management for llama_ocr."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class OCRConfig:
    """Configuration class for OCR settings."""
    
    model_name: str = "llama3.2-vision:latest"
    preprocess_images: bool = True
    optimize_for_ocr: bool = False
    log_level: str = "INFO"
    max_retries: int = 3
    timeout: int = 30
    base_url: Optional[str] = None
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> "OCRConfig":
        """Create config from dictionary."""
        return cls(**{
            k: v for k, v in config_dict.items() 
            if k in cls.__dataclass_fields__
        })
