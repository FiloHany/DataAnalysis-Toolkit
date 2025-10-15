"""
Configuration settings for the data analysis package.
"""

import logging
import os
from typing import Dict, Any

# Logging configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# API configurations
CRYPTO_API_KEY = os.getenv('CMC_API_KEY', 'your-api-key-here')
CRYPTO_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

# Default settings
DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3

# Data paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Visualization settings
PLOT_STYLE = 'bmh'
FIGURE_SIZE = (12, 8)

def get_logger(name: str) -> logging.Logger:
    """Get configured logger instance."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(LOG_LEVEL)
    return logger

# Global logger
logger = get_logger(__name__)
