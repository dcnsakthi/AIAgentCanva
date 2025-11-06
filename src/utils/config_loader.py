"""
Configuration loader utility
"""
import yaml
from pathlib import Path
from typing import Dict, Any
import os
from dotenv import load_dotenv

class ConfigLoader:
    """Load and manage application configuration"""
    
    _config = None
    
    @classmethod
    def load_config(cls) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if cls._config is None:
            # Load environment variables
            load_dotenv()
            
            config_path = Path(__file__).parent.parent.parent / "config.yaml"
            with open(config_path, 'r', encoding='utf-8') as f:
                cls._config = yaml.safe_load(f)
        
        return cls._config
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        config = cls.load_config()
        keys = key.split('.')
        value = config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    @classmethod
    def get_env(cls, key: str, default: str = "") -> str:
        """Get environment variable"""
        return os.getenv(key, default)
