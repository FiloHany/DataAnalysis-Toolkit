"""
Data Analysis Package

A professional data analysis toolkit following SOLID principles and design patterns.
Provides modules for web scraping, data processing, cleaning, EDA, API interactions, and visualization.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "Modular data analysis package with SOLID principles"

from .scrapers import *
from .processors import *
from .cleaners import *
from .eda import *
from .api import *
from .visualization import *

__all__ = [
    'scrapers',
    'processors',
    'cleaners',
    'eda',
    'api',
    'visualization'
]
