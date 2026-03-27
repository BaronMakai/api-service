# utils.py

import os
import json
import logging
from typing import List, Dict

# Define the logger
logger = logging.getLogger(__name__)

def load_config() -> Dict[str, str]:
    """Load configuration from a JSON file."""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Configuration file not found")
        raise

def validate_config(config: Dict[str, str]) -> bool:
    """Validate the configuration."""
    required_keys = ['API_HOST', 'API_PORT', 'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD']
    for key in required_keys:
        if key not in config:
            logger.error(f"Missing required configuration key: {key}")
            return False
    return True

def ensure_dir(path: str) -> None:
    """Ensure the directory exists."""
    if not os.path.exists(path):
        os.makedirs(path)

def get_local_ip() -> str:
    """Get the local IP address."""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        logger.error(f"Failed to get local IP: {e}")
        return None

def extract_url_params(url: str, params: List[str]) -> Dict[str, str]:
    """Extract URL parameters."""
    url_params = {}
    for param in params:
        url_params[param] = url.split(f'/{param}')[1]
    return url_params