"""KyakX version information."""

__version__ = "1.2.0"
__author__ = "kyakei"
__email__ = "codtool911@gmail.com"
__description__ = "A powerful web exploitation toolkit"

def get_version_info():
    """Return formatted version information."""
    return f"""
KyakX v{__version__}
Created by: {__author__} <{__email__}>
{__description__}
"""