"""
Argilla Dataset Manager - A tool for managing and uploading datasets to Argilla.
"""

from .datasets.settings_manager import SettingsManager
from .utils.argilla_client import get_argilla_client
from .utils.dataset_manager import DatasetManager

__version__ = "0.1.0"
__all__ = ["DatasetManager", "get_argilla_client", "SettingsManager"]
