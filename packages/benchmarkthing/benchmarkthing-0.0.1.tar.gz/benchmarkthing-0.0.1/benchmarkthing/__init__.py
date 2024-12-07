"""
Benchmarkthing - Evals as an API
The easiest way to evaluate and benchmark AI models and systems
Coming soon at https://benchmarkthing.com
"""

__version__ = "0.0.1"
__author__ = "Benchmarkthing Inc."
__email__ = "hello@benchmarkthing.com"
__license__ = "MIT"

import warnings

def version():
    """Return the package version."""
    return __version__

def info():
    """Return basic package information."""
    return {
        "website": "https://benchmarkthing.com",
        "description": "Evals as an API - The easiest way to evaluate and benchmark AI models and systems",
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "license": __license__
    }

# Show warning about placeholder status
warnings.warn("This is a placeholder package. The full version is coming soon!", UserWarning)

# Make commonly used items available at package level
__all__ = ['version', 'info'] 